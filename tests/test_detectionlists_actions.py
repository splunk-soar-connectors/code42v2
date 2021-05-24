from pytest import fixture

from phantom.action_result import ActionResult
from .conftest import create_fake_connector, create_mock_response

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


def _attach_client(connector, client):
    connector._client = client
    return connector


class TestCode42DetectionListsConnector(object):

    def test_handle_action_when_add_departing_employee_calls_add_with_expected_args(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.add.assert_called_once_with(
            "TEST_USER_UID", departure_date="2030-01-01"
        )

    def test_handle_action_when_add_departing_employee_adds_info_to_summary(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        summary = action_results[0].get_summary()
        assert summary == {"user_id": _TEST_USER_UID, "username": "test@example.com"}

    def test_handle_action_when_add_departing_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user
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

        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        data = action_results[0].get_data()
        assert data[0] == response_data

    def test_handle_action_when_add_departing_employee_and_is_successful_sets_success_status(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        msg = action_results[0].get_message()
        assert msg == f"test@example.com was added to the departing employee list"

    def test_handle_action_when_add_departing_employee_and_including_note_adds_note(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "note": "Test Note"}
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
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        summary = action_results[0].get_summary()
        assert summary == {"user_id": _TEST_USER_UID, "username": "test@example.com"}

    def test_handle_action_when_remove_departing_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user,
    ):
        param = {"username": "test@example.com"}

        # This API call does not have response data.
        mock_py42_with_user.detectionlists.departing_employee.remove.return_value = create_mock_response(
            mocker, {}
        )
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        data = action_results[0].get_data()
        assert data[0] == {"userId": _TEST_USER_UID}

    def test_handle_action_when_remove_departing_employee_and_is_successful_sets_success_status(
        self, mocker, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        msg = action_results[0].get_message()
        assert msg == f"test@example.com was removed from the departing employee list"
