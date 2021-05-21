from pytest import fixture

from phantom.action_result import ActionResult
from tests.conftest import create_fake_connector, create_mock_response

_TEST_USER_UID = "TEST_USER_UID"


@fixture
def mock_py42_with_user(mocker, mock_py42_client):
    response_data = {"users": [{"userUid": _TEST_USER_UID}]}
    mock_py42_client.users.get_by_username.return_value = create_mock_response(mocker, response_data)
    return mock_py42_client


def _create_add_de_connector(client):
    connector = create_fake_connector("add_departing_employee")
    return _attach_client(connector, client)


def _create_remove_de_connector(client):
    connector = create_fake_connector("remove_departing_employee")
    return _attach_client(connector, client)


def _create_add_hr_connector(client):
    connector = create_fake_connector("add_high_risk_employee")
    return _attach_client(connector, client)


def _create_remove_hr_connector(client):
    connector = create_fake_connector("remove_high_risk_employee")
    return _attach_client(connector, client)


def _attach_client(connector, client):
    connector._client = client
    return connector


class TestCode42DetectionListsConnector(object):

    def test_handle_action_when_add_departing_employee_calls_add_with_expected_args(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.add.assert_called_once_with(
            "TEST_USER_UID", departure_date="2030-01-01"
        )

    def test_handle_action_when_add_departing_employee_adds_info_to_summary(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        update_summary_mock.assert_called_once_with({"user_id": _TEST_USER_UID, "username": "test@example.com"})

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
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        add_data_mock.assert_called_once_with(response_data)

    def test_handle_action_when_add_departing_employee_and_is_successful_sets_success_status(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        result = ActionResult(dict(param))
        set_status_mock = mocker.MagicMock()
        result.set_status = set_status_mock
        mock_result_adder.return_value = result
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        expected_message = f"test@example.com was added to the departing employees list"
        set_status_mock.assert_called_once_with(1, expected_message)

    def test_handle_action_when_add_departing_employee_and_including_note_adds_note(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com", "note": "Test Note"}
        result = ActionResult(dict(param))
        set_status_mock = mocker.MagicMock()
        result.set_status = set_status_mock
        mock_result_adder.return_value = result
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.update_user_notes.assert_called_once_with(
            _TEST_USER_UID, "Test Note"
        )

    def test_handle_action_when_remove_departing_employee_calls_remove_with_expected_args(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.remove.assert_called_once_with(
            "TEST_USER_UID"
        )

    def test_handle_action_when_remove_departing_employee_adds_info_to_summary(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        update_summary_mock.assert_called_once_with({"user_id": _TEST_USER_UID, "username": "test@example.com"})

    def test_handle_action_when_remove_departing_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}

        # This API call does not have response data.
        mock_py42_with_user.detectionlists.departing_employee.remove.return_value = create_mock_response(
            mocker, {}
        )
        result = ActionResult(dict(param))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        add_data_mock.assert_called_once_with({"userId": _TEST_USER_UID})

    def test_handle_action_when_remove_departing_employee_and_is_successful_sets_success_status(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        set_status_mock = mocker.MagicMock()
        result.set_status = set_status_mock
        mock_result_adder.return_value = result
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        expected_message = f"test@example.com was removed from the departing employees list"
        set_status_mock.assert_called_once_with(1, expected_message)

    def test_handle_action_when_add_high_risk_employee_calls_add_with_expected_args(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_add_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.high_risk_employee.add.assert_called_once_with(
            "TEST_USER_UID"
        )

    def test_handle_action_when_add_high_risk_employee_adds_user_info_to_summary(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = _create_add_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        update_summary_mock.assert_called_once_with({"user_id": _TEST_USER_UID, "username": "test@example.com"})

    def test_handle_action_when_add_high_risk_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        response_data = {
            "type$": "HIGH_RISK_EMPLOYEE_V2",
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
        mock_py42_with_user.detectionlists.high_risk_employee.add.return_value = create_mock_response(
            mocker, response_data
        )
        result = ActionResult(dict(param))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = _create_add_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        add_data_mock.assert_called_once_with(response_data)

    def test_handle_action_when_add_high_risk_employee_and_is_successful_sets_success_status(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        set_status_mock = mocker.MagicMock()
        result.set_status = set_status_mock
        mock_result_adder.return_value = result
        connector = _create_add_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        expected_message = f"test@example.com was added to the high risk employees list"
        set_status_mock.assert_called_once_with(1, expected_message)

    def test_handle_action_when_remove_high_risk_employee_calls_remove_with_expected_args(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_remove_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.high_risk_employee.remove.assert_called_once_with(
            "TEST_USER_UID"
        )

    def test_handle_action_when_remove_high_risk_employee_adds_user_info_to_summary(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = _create_remove_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        update_summary_mock.assert_called_once_with({"user_id": _TEST_USER_UID, "username": "test@example.com"})

    def test_handle_action_when_remove_high_risk_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}

        # This API call does not have response data.
        mock_py42_with_user.detectionlists.high_risk_employee.remove.return_value = create_mock_response(
            mocker, {}
        )
        result = ActionResult(dict(param))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = _create_remove_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        add_data_mock.assert_called_once_with({"userId": _TEST_USER_UID})

    def test_handle_action_when_remove_high_risk_employee_and_is_successful_sets_success_status(
        self, mocker, mock_py42_with_user, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        set_status_mock = mocker.MagicMock()
        result.set_status = set_status_mock
        mock_result_adder.return_value = result
        connector = _create_remove_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        expected_message = f"test@example.com was removed from the high risk employees list"
        set_status_mock.assert_called_once_with(1, expected_message)
