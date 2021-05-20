from pytest import fixture

from phantom.action_result import ActionResult
from tests.conftest import create_fake_connector, create_mock_response

_TEST_USER_UID = "TEST_USER_UID"


@fixture
def mock_py42_with_user(mocker, mock_py42_client):
    response_data = {"users": [{"userUid": _TEST_USER_UID}]}
    mock_py42_client.users.get_by_username.return_value = create_mock_response(mocker, response_data)
    return mock_py42_client


class TestCode42DetectionListsConnector(object):

    def test_handle_action_when_add_departing_employee_calls_add_with_expected_args(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = create_fake_connector("add_departing_employee")
        connector._client = mock_py42_with_user
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.add.assert_called_once_with(
            "TEST_USER_UID", departure_date="2030-01-01"
        )

    def test_handle_action_when_add_departing_employee_adds_user_id_to_summary(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = create_fake_connector("add_departing_employee")
        connector._client = mock_py42_with_user
        connector.handle_action(param)
        update_summary_mock.assert_called_once_with({"userId": _TEST_USER_UID})

    def test_handle_action_when_add_departing_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        response_data = {
            "type$": "DEPARTING_EMPLOYEE_V2",
            "tenantId": "11114444-2222-3333-4444-666634888863",
            "userId": _TEST_USER_UID,
            "userName": "test@example.com",
            "displayName": "",
            "createdAt": "2021-05-20T19:40:14.8909434Z",
            "status": "OPEN",
            "cloudUsernames": [
                "test@example.com"
            ]
        }
        mock_py42_with_user.detectionlists.departing_employee.add.return_value = create_mock_response(
            mocker, response_data
        )
        result = ActionResult(dict(param))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = create_fake_connector("add_departing_employee")
        connector._client = mock_py42_with_user
        connector.handle_action(param)
        add_data_mock.assert_called_once_with(response_data)

    def test_handle_action_when_remove_departing_employee_calls_remove_with_expected_args(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = create_fake_connector("remove_departing_employee")
        connector._client = mock_py42_with_user
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.remove.assert_called_once_with(
            "TEST_USER_UID"
        )

    def test_handle_action_when_remove_departing_employee_adds_user_id_to_summary(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = create_fake_connector("remove_departing_employee")
        connector._client = mock_py42_with_user
        connector.handle_action(param)
        update_summary_mock.assert_called_once_with({"userId": _TEST_USER_UID})

    def test_handle_action_when_remove_departing_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        response_data = {}
        mock_py42_with_user.detectionlists.departing_employee.remove.return_value = create_mock_response(
            mocker, response_data
        )
        result = ActionResult(dict(param))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = create_fake_connector("remove_departing_employee")
        connector._client = mock_py42_with_user
        connector.handle_action(param)
        add_data_mock.assert_called_once_with(response_data)