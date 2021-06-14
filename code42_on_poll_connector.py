import dateutil.parser
import phantom.app as phantom
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import (
    ExposureType,
    DeviceUsername,
    Actor,
    EventTimestamp,
    EventType,
    FileCategory,
)

from code42_util import get_thirty_days_ago, build_alerts_query

"""The contents of this module that related to mapping alert observations to file events borrows heavily from the
Code42 Cortex XSOAR integration.
"""


def get_file_category_value(key):
    # Meant to handle all possible cases
    key = key.lower().replace("-", "").replace("_", "")
    category_map = {
        "sourcecode": FileCategory.SOURCE_CODE,
        "audio": FileCategory.AUDIO,
        "executable": FileCategory.EXECUTABLE,
        "document": FileCategory.DOCUMENT,
        "image": FileCategory.IMAGE,
        "pdf": FileCategory.PDF,
        "presentation": FileCategory.PRESENTATION,
        "script": FileCategory.SCRIPT,
        "spreadsheet": FileCategory.SPREADSHEET,
        "video": FileCategory.VIDEO,
        "virtualdiskimage": FileCategory.VIRTUAL_DISK_IMAGE,
        "archive": FileCategory.ZIP,
    }
    return category_map.get(key, "UNCATEGORIZED")


class Code42OnPollConnector:
    def __init__(self, connector, client, state):
        self._connector = connector
        self._client = client
        self._state = state or {}

    def handle_on_poll(self, param, action_result):
        last_time = self._state.get("last_time")
        param = _adjust_date_parameters(last_time, param)
        query = build_alerts_query(param["start_date"], param.get("end_date"))
        response = self._client.alerts.search(query)

        for alert in response["alerts"]:
            details = self._get_alert_details(alert["id"])
            container_id = self._init_container(details)
            observations = details.get("observations", [])
            for observation in observations:
                file_events = self._get_file_events(observation, details)
                self._save_artifacts_from_file_events(
                    container_id, details, file_events
                )

        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_alert_details(self, alert_id):
        return self._client.alerts.get_details(alert_id).data["alerts"][0]

    def _init_container(self, alert_details):
        container_label = self._get_container_label()
        container_json = _create_container(alert_details, container_label)
        _, _, container_id = self._connector.save_container(container_json)
        return container_id

    def _get_container_label(self):
        return self._connector.get_config().get("ingest", {}).get("container_label")

    def _get_file_events(self, observation, alert_details):
        query = _get_file_event_query(observation, alert_details)
        response = self._client.securitydata.search_file_events(query)
        file_events = response.data.get("fileEvents", [])
        return file_events

    def _save_artifacts_from_file_events(self, container_id, details, file_events):
        artifacts = [
            _create_artifact_json(container_id, details, event) for event in file_events
        ]
        self._connector.save_artifacts(artifacts)


def _adjust_date_parameters(last_time, param):
    """Only use start_date and end_date if never check-pointed."""
    if not last_time:
        default_start_date = get_thirty_days_ago().strftime("%Y-%m-%dT%H:%M:%S.%f")
        param["start_date"] = param.get("start_date", default_start_date)
    else:
        param["start_date"] = last_time
        param["end_date"] = None

    return param


def _create_container(alert, container_label):
    return {
        "name": alert["name"],
        "data": alert,
        "severity": alert["severity"],
        "description": alert["description"],
        "source_data_identifier": alert["id"],
        "label": container_label,
    }


def _get_file_event_query(observation, alert):
    mapper = ObservationToSecurityQueryMapper(observation, alert.get("actor"))
    return mapper.map()


class ObservationToSecurityQueryMapper(object):
    """Class to simplify the process of mapping observation data to query objects."""

    # Exfiltration consts
    _ENDPOINT_TYPE = "FedEndpointExfiltration"
    _CLOUD_TYPE = "FedCloudSharePermissions"

    # Query consts
    _PUBLIC_SEARCHABLE = "PublicSearchableShare"
    _PUBLIC_LINK = "PublicLinkShare"
    _OUTSIDE_TRUSTED_DOMAINS = "SharedOutsideTrustedDomain"

    exposure_type_map = {
        "PublicSearchableShare": ExposureType.IS_PUBLIC,
        "PublicLinkShare": ExposureType.SHARED_VIA_LINK,
        "SharedOutsideTrustedDomain": ExposureType.OUTSIDE_TRUSTED_DOMAINS,
    }

    def __init__(self, observation, actor):
        self._obs = observation
        self._actor = actor

    @property
    def _observation_data(self):
        return self._obs.get("data")

    @property
    def _exfiltration_type(self):
        return self._obs.get("type")

    @property
    def _is_endpoint_exfiltration(self):
        return self._exfiltration_type == self._ENDPOINT_TYPE

    @property
    def _is_cloud_exfiltration(self):
        return self._exfiltration_type == self._CLOUD_TYPE

    def _create_user_filter(self):
        return (
            DeviceUsername.eq(self._actor)
            if self._is_endpoint_exfiltration
            else Actor.eq(self._actor)
        )

    def map(self):
        search_args = self._create_search_args()
        query = search_args.to_all_query()
        return query

    def _create_search_args(self):
        filters = FileEventQueryFilters()
        exposure_types = self._observation_data.get("exposureTypes")
        first_activity = self._observation_data.get("firstActivityAt")
        last_activity = self._observation_data.get("lastActivityAt")
        filters.append(self._create_user_filter())
        if first_activity:
            begin_time = dateutil.parser.parse(first_activity)
            if begin_time:
                filters.append(EventTimestamp.on_or_after(begin_time))
        if last_activity:
            end_time = dateutil.parser.parse(last_activity)
            if end_time:
                filters.append(EventTimestamp.on_or_before(end_time))
        filters.extend(self._create_exposure_filters(exposure_types))
        filters.append(self._create_file_category_filters())
        return filters

    def _create_exposure_filters(self, exposure_types):
        """Determine exposure types based on alert type"""
        exp_types = []
        if self._is_cloud_exfiltration:
            for t in exposure_types:
                exp_type = self.exposure_type_map.get(t)
                if exp_type:
                    exp_types.append(exp_type)
            if exp_types:
                return [ExposureType.is_in(exp_types)]
            else:
                # If not given a support exposure type, search for all unsupported exposure types
                supported_exp_types = list(self.exposure_type_map.values())
                return [ExposureType.not_in(supported_exp_types)]
        elif self._is_endpoint_exfiltration:
            return [
                EventType.is_in(
                    [EventType.CREATED, EventType.MODIFIED, EventType.READ_BY_APP]
                ),
                ExposureType.is_in(exposure_types),
            ]
        return []

    def _create_file_category_filters(self):
        """Determine if file categorization is significant"""
        observed_file_categories = self._observation_data.get("fileCategories")
        if observed_file_categories:
            categories = [
                get_file_category_value(cat.get("category"))
                for cat in observed_file_categories
                if cat.get("isSignificant") and cat.get("category")
            ]
            if categories:
                return FileCategory.is_in(categories)


class Code42SearchFilters(object):
    def __init__(self):
        self._filters = []

    @property
    def filters(self):
        return self._filters

    def to_all_query(self):
        """Override"""

    def append(self, _filter):
        if _filter:
            self._filters.append(_filter)

    def extend(self, _filters):
        if _filters:
            self._filters.extend(_filters)

    def append_result(self, value, create_filter):
        """Safely creates and appends the filter to the working list."""
        if not value:
            return
        _filter = create_filter(value)
        self.append(_filter)


class FileEventQueryFilters(Code42SearchFilters):
    """Class for simplifying building up a file event search query"""

    def __init__(self, pg_size=None):
        self._pg_size = pg_size
        super(FileEventQueryFilters, self).__init__()

    def to_all_query(self):
        """Convert list of search criteria to *args"""
        query = FileEventQuery.all(*self._filters)
        if self._pg_size:
            query.page_size = self._pg_size
        return query


def _create_artifact_json(container_id, alert_details, file_event):
    normalized_event = {
        key: val for key, val in file_event.items() if val not in [[], None, ""]
    }
    file_name = normalized_event.get("fileName", "Unknown file")
    event_type = normalized_event.get("eventType", "Code42 file event")
    artifact_name = f"{file_name} - {event_type}"
    return {
        "name": artifact_name,
        "container_id": container_id,
        "source_data_identifier": normalized_event["eventId"],
        "label": alert_details.get("ruleSource"),
        "cef": normalized_event,
        "start_time": normalized_event["eventTimestamp"],
    }
