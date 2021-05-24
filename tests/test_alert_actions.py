from pytest import fixture

from phantom.action_result import ActionResult
from tests.conftest import create_fake_connector, create_mock_response, attach_client


# @fixture
# def mock_py42_with_alert(mocker, mock_py42_client):
#     response_data = {"alerts": [{}]}
#     mock_py42_client.alerts.get_details.return_value = create_mock_response(mocker, response_data)
#     return mock_py42_client


def _create_get_alert_details_connector(client):
    connector = create_fake_connector("get_alert_details")
    return attach_client(connector, client)

def _get_alert_detail_response_data():
    return {
        "alerts": [{
            "type$": "ALERT_SUMMARY",
            "tenantId": "11111111-abcd-4231-99ab-df6434da4663",
            "type": "FED_COMPOSITE",
            "name": "Test Alert",
            "description": "it's a test",
            "actor": "cool.guy@code42.com",
            "actorId": "987210998131391466",
            "target": "N/A",
            "severity": "LOW",
            "ruleId": "cab2d5ee-a512-45b1-8848-809327033048",
            "ruleSource": "Alerting",
            "id": "11111111-9724-4005-b848-76af488cf5e2",
            "createdAt": "2021-05-13T16:51:35.4259080Z",
            "state": "OPEN"}]
    }


class TestCode42AlertsConnector(object):

    def test_handle_action_when_alert_detail_calls_get_with_expected_args(
            self, mock_py42_client, mock_result_adder
    ):
        param = {"alert_id": "123-456-7890"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_get_alert_details_connector(mock_py42_client)

        connector.handle_action(param)

        mock_py42_client.alerts.get_details.assert_called_once_with([param["alert_id"]])

    def test_handle_action_when_alert_detail_adds_response_to_data(
            self, mocker, mock_py42_client, mock_result_adder
    ):
        param = {"alert_id": "123-456-7890"}
        response_data = _get_alert_detail_response_data()
        mock_py42_client.alerts.get_details.return_value = create_mock_response(mocker, response_data)
        connector = _create_get_alert_details_connector(mock_py42_client)
        action_result = ActionResult(dict(param))
        add_data_mock = mocker.MagicMock()
        action_result.add_data = add_data_mock
        mock_result_adder.return_value = action_result

        connector.handle_action(param)

        add_data_mock.assert_called_once_with(response_data["alerts"][0])

    def test_handle_action_when_alert_detail_adds_info_to_summary(self, mocker, mock_py42_client, mock_result_adder):
        param = {"alert_id": "123-456-7890"}
        response_data = _get_alert_detail_response_data()
        mock_py42_client.alerts.get_details.return_value = create_mock_response(mocker, response_data)
        connector = _create_get_alert_details_connector(mock_py42_client)
        action_result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        action_result.update_summary = update_summary_mock
        mock_result_adder.return_value = action_result

        connector.handle_action(param)

        expected_summary = {"username": response_data["alerts"][0]["actor"], "user_id": response_data["alerts"][0]["actorId"]}
        update_summary_mock.assert_called_once_with(expected_summary)





