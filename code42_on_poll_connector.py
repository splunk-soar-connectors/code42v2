import phantom.app as phantom

from code42_base_connector import Code42BaseConnector
from code42_base_connector import get_thirty_days_ago


class Code42OnPollConnector(Code42BaseConnector):
    def __init__(self, client, state):
        super(Code42OnPollConnector, self).__init__()
        self._client = client
        self._state = state

    def handle_on_poll(self, param, action_result):
        last_time = self._state.get("last_time")

        # Only use start_date and end_date if never checkpointed.
        if not last_time:
            default_start_date = get_thirty_days_ago().strftime("%Y-%m-%dT%H:%M:%S.%f")
            param["start_date"] = param.get("start_date", default_start_date)
        else:
            param["start_date"] = last_time
            param["end_date"] = None

        query = self._build_alerts_query(param["start_date"], param.get("end_date"))
        response = self._client.alerts.search(query)

        for alert in response["alerts"]:
            alert_id = alert["id"]

            # Include `observations` in the container data.
            details = self._client.alerts.get_details(alert_id).data["alerts"][0]

            container_json = {
                "name": alert["name"],
                "data": details,
                "severity": alert["severity"],
                "description": alert["description"],
                "source_data_identifier": alert_id,
                "label": self.get_config().get("ingest", {}).get("container_label"),
            }
            ret_val, _, container_id = self.save_container(container_json)

            observations = details.get("observations")
            if observations:
                artifact_json = {
                    "container_id": container_id,
                    "source_data_identifier": alert_id,
                    "label": alert["ruleSource"],
                }

        return action_result.set_status(phantom.APP_SUCCESS)
