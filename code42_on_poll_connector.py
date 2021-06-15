from datetime import datetime

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
Code42 Cortex XSOAR integration as well as the code42cli python package.
"""


JSON_TO_CEF_MAP = {
    "actor": "suser",
    "cloudDriveId": "aid",
    "createTimestamp": "fileCreateTime",
    "deviceUid": "deviceExternalId",
    "deviceUserName": "suser",
    "domainName": "dvchost",
    "emailRecipients": "duser",
    "emailSender": "suser",
    "eventId": "externalId",
    "eventTimestamp": "end",
    "exposure": "reason",
    "fileCategory": "fileType",
    "fileName": "fname",
    "filePath": "filePath",
    "fileSize": "fsize",
    "insertionTimestamp": "rt",
    "md5Checksum": "fileHashMd5",
    "modifyTimestamp": "fileModificationTime",
    "osHostName": "shost",
    "processName": "sproc",
    "processOwner": "spriv",
    "publicIpAddress": "src",
    "removableMediaBusType": "cs1",
    "removableMediaCapacity": "cn1",
    "removableMediaName": "cs3",
    "removableMediaSerialNumber": "cs4",
    "removableMediaVendor": "cs2",
    "sharedWith": "duser",
    "source": "sourceServiceName",
    "syncDestination": "destinationServiceName",
    "tabUrl": "request",
    "url": "filePath",
    "userUid": "suid",
    "windowTitle": "requestClientApplication",
}
CEF_CUSTOM_FIELD_NAME_MAP = {
    "cn1Label": "Code42AEDRemovableMediaCapacity",
    "cs1Label": "Code42AEDRemovableMediaBusType",
    "cs2Label": "Code42AEDRemovableMediaVendor",
    "cs3Label": "Code42AEDRemovableMediaName",
    "cs4Label": "Code42AEDRemovableMediaSerialNumber",
}
FILE_EVENT_TO_SIGNATURE_ID_MAP = {
    "CREATED": "C42200",
    "MODIFIED": "C42201",
    "DELETED": "C42202",
    "READ_BY_APP": "C42203",
    "EMAILED": "C42204",
}
CEF_TIMESTAMP_FIELDS = ["end", "fileCreateTime", "fileModificationTime", "rt"]
DEFAULT_CONTAINER_COUNT_FOR_POLL_NOW = 1
DEFAULT_ARTIFACT_COUNT_FOR_POLL_NOW = 10


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
        param = self._adjust_date_parameters(param)
        query = build_alerts_query(param["start_date"], param.get("end_date"))
        alerts = self._get_alerts(param, query)
        details = {}
        for alert in alerts:
            details = self._get_alert_details(alert["id"])
            container_id = self._init_container(details)
            observations = details.get("observations", [])
            file_events = self._get_file_events(param, observations, details)
            self._save_artifacts_from_file_events(container_id, details, file_events)

        # Save last time of last alert for future polling
        if not self._connector.is_poll_now() and details.get("createdAt"):
            self._state["last_time"] = details["createdAt"]
            self._connector.save_state(self._state)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_alerts(self, param, query):
        response = self._client.alerts.search(query)
        alerts = response.data.get("alerts", [])
        if self._connector.is_poll_now():
            container_count = param.get(
                "container_count", DEFAULT_CONTAINER_COUNT_FOR_POLL_NOW
            )
            return alerts[:container_count]

        return alerts

    def _get_alert_details(self, alert_id):
        return self._client.alerts.get_details(alert_id).data["alerts"][0]

    def _init_container(self, alert_details):
        container_label = self._get_container_label()
        container_json = _create_container(alert_details, container_label)
        _, _, container_id = self._connector.save_container(container_json)
        return container_id

    def _get_container_label(self):
        return self._connector.get_config().get("ingest", {}).get("container_label")

    def _get_file_events(self, param, observations, alert_details):
        artifact_count = param.get(
            "artifact_count", DEFAULT_ARTIFACT_COUNT_FOR_POLL_NOW
        )
        file_events = []
        for observation in observations:
            events = self._get_file_events_for_observation(
                param, observation, alert_details
            )
            for event in events:
                file_events.append(event)
                if self._connector.is_poll_now() and len(file_events) >= artifact_count:
                    break
            if self._connector.is_poll_now() and len(file_events) >= artifact_count:
                break

        return file_events

    def _get_file_events_for_observation(self, param, observation, alert_details):
        query = _get_file_event_query(observation, alert_details)
        response = self._client.securitydata.search_file_events(query)
        file_events = response.data.get("fileEvents", [])
        return file_events

    def _save_artifacts_from_file_events(self, container_id, details, file_events):
        artifacts = [
            _create_artifact_json(container_id, details, event) for event in file_events
        ]
        self._connector.save_artifacts(artifacts)

    def _adjust_date_parameters(self, param):
        param["end_date"] = None  # Not used

        last_time = (
            None if self._connector.is_poll_now() else self._state.get("last_time", 0)
        )
        if not last_time:
            # If there was never a stored last_time or is_poll_now().
            param["start_date"] = get_thirty_days_ago().strftime("%Y-%m-%dT%H:%M:%S.%f")
        else:
            last_time_as_date_str = datetime.utcfromtimestamp(last_time).strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
            )
            param["start_date"] = last_time_as_date_str

        return param


def _create_container(alert, container_label):
    return {
        "name": alert.get("name"),
        "data": alert,
        "severity": alert.get("severity"),
        "description": alert.get("description"),
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
        user_filter = self._create_user_filter()
        filters.append(user_filter)
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


class FileEventQueryFilters:
    """Class for simplifying building up a file event search query"""

    def __init__(self, pg_size=None):
        self._pg_size = pg_size
        self._filters = []

    @property
    def filters(self):
        return self._filters

    def to_all_query(self):
        """Convert list of search criteria to *args"""
        query = FileEventQuery.all(*self._filters)
        if self._pg_size:
            query.page_size = self._pg_size
        return query

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


def _create_artifact_json(container_id, alert_details, file_event):
    normalized_event = {
        key: val for key, val in file_event.items() if val not in [[], None, ""]
    }
    cef = _map_event_to_cef(normalized_event)
    artifact_dict = {
        "name": "Code42 File Event Artifact",
        "container_id": container_id,
        "source_data_identifier": normalized_event["eventId"],
        "label": alert_details.get("ruleSource"),
        "cef": cef,
        "data": normalized_event,
        "start_time": normalized_event.get("eventTimestamp"),
    }
    return artifact_dict


def _map_event_to_cef(normalized_event):
    cef_dict = {}
    init_cef_dict = _init_cef_dict(normalized_event)
    sub_cef_dict_list = [
        _format_cef_kvp(key, value) for key, value in init_cef_dict.items()
    ]
    for sub_dict in sub_cef_dict_list:
        cef_dict.update(sub_dict)

    event_name = normalized_event.get("eventType", "UNKNOWN")
    cef_dict["signatureId"] = FILE_EVENT_TO_SIGNATURE_ID_MAP.get(event_name, "C42000")
    cef_dict["eventName"] = event_name
    return cef_dict


def _init_cef_dict(normalized_event):
    return {
        cef_key: normalized_event[json_key]
        for json_key, cef_key in JSON_TO_CEF_MAP.items()
        if json_key in normalized_event
    }


def _format_cef_kvp(cef_field_key, cef_field_value):
    if cef_field_key + "Label" in CEF_CUSTOM_FIELD_NAME_MAP:
        return _format_custom_cef_kvp(cef_field_key, cef_field_value)

    cef_field_value = _handle_nested_json_fields(cef_field_key, cef_field_value)
    if isinstance(cef_field_value, list):
        cef_field_value = _convert_list_to_csv(cef_field_value)
    elif cef_field_key in CEF_TIMESTAMP_FIELDS:
        cef_field_value = convert_file_event_timestamp_to_cef_timestamp(cef_field_value)

    return {cef_field_key: cef_field_value}


def _format_custom_cef_kvp(custom_cef_field_key, custom_cef_field_value):
    custom_cef_label_key = f"{custom_cef_field_key}Label"
    custom_cef_label_value = CEF_CUSTOM_FIELD_NAME_MAP[custom_cef_label_key]
    return {
        custom_cef_field_key: custom_cef_field_value,
        custom_cef_label_key: custom_cef_label_value,
    }


def _handle_nested_json_fields(cef_field_key, cef_field_value):
    result = []
    if cef_field_key == "duser":
        result = [
            item["cloudUsername"] for item in cef_field_value if type(item) is dict
        ]

    return result or cef_field_value


def _convert_list_to_csv(_list):
    value = ",".join([val for val in _list])
    return value


def convert_file_event_timestamp_to_cef_timestamp(timestamp_value):
    try:
        _datetime = datetime.strptime(timestamp_value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        _datetime = datetime.strptime(timestamp_value, "%Y-%m-%dT%H:%M:%SZ")
    value = f"{_datetime_to_ms_since_epoch(_datetime):.0f}"
    return value


def _datetime_to_ms_since_epoch(_datetime):
    epoch = datetime.utcfromtimestamp(0)
    total_seconds = (_datetime - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds * 1000
