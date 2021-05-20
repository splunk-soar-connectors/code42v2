import json

from py42.response import Py42Response
from requests import Response

from phantom.action_result import ActionResult
from tests.conftest import create_fake_connector


class TestCode42DetectionListsConnector(object):

    def test_handle_action_when_add_departing_employee_calls_add_with_expected_args(
        self, mocker, mock_py42_client, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        result = ActionResult(dict(param))
        result.update_summary = mocker.MagicMock()
        mock_result_adder.return_value = result
        http_response = mocker.MagicMock(spec=Response)
        http_response.text = json.dumps({"users": [{"userUid": "TEST_USER_UID"}]})
        mock_py42_client.users.get_by_username.return_value = Py42Response(http_response)
        connector = create_fake_connector("add_departing_employee")
        connector._client = mock_py42_client
        connector.handle_action(param)
        mock_py42_client.detectionlists.departing_employee.add.assert_called_once_with(
            "TEST_USER_UID", departure_date="2030-01-01"
        )

    def test_handle_action_when_remove_departing_employee_calls_remove_with_expected_args(
        self, mocker, mock_py42_client, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        result.update_summary = mocker.MagicMock()
        mock_result_adder.return_value = result
        http_response = mocker.MagicMock(spec=Response)
        http_response.text = json.dumps({"users": [{"userUid": "TEST_USER_UID"}]})
        mock_py42_client.users.get_by_username.return_value = Py42Response(http_response)
        connector = create_fake_connector("remove_departing_employee")
        connector._client = mock_py42_client
        connector.handle_action(param)
        mock_py42_client.detectionlists.departing_employee.remove.assert_called_once_with(
            "TEST_USER_UID"
        )
