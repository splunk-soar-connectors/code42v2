from pytest import fixture

from tests.conftest import assert_success, create_fake_connector, create_mock_response, assert_successful_single_data, assert_successful_message, assert_succesful_summary

_TEST_USER_UID = "TEST_USER_UID"
_MOCK_LIST_DEPARTING_EMPLOYEES_RESPONSE = {
    "totalCount": 2,
    "items":
    [
        {
            "type$": "DEPARTING_EMPLOYEE_V2",
            "tenantId": "11114444-2222-3333-4444-666634888863",
            "userId": _TEST_USER_UID,
            "userName": "test@example.com",
            "displayName": "Test Testerson",
            "notes": "Test test test",
            "createdAt": "2021-04-22T00:00:00.0000000Z",
            "status": "OPEN",
            "cloudUsernames": [
                "alias1",
            ],
            "totalBytes": 0,
            "numEvents": 3
        },
        {
            "type$": "DEPARTING_EMPLOYEE_V2",
            "tenantId": "11114444-2222-3333-4444-666634888863",
            "userId": "id2",
            "userName": "test2@example.com",
            "displayName": "Test2 Testerson",
            "notes": "Test test test2",
            "createdAt": "2021-04-22T00:00:00.0000000Z",
            "status": "OPEN",
            "cloudUsernames": [
                "alias2",
            ],
            "totalBytes": 0,
            "numEvents": 6
        }
    ]
}
_MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE = {
    "totalCount": 2,
    "items":
    [
        {
            "type$": "HIGH_RISK_EMPLOYEE_V2",
            "tenantId": "11114444-2222-3333-4444-666634888863",
            "userId": _TEST_USER_UID,
            "userName": "test@example.com",
            "displayName": "Test Testerson",
            "notes": "Test test test",
            "createdAt": "2021-04-22T00:00:00.0000000Z",
            "status": "OPEN",
            "cloudUsernames": [
                "alias1",
            ],
            "totalBytes": 0,
            "numEvents": 3
        },
        {
            "type$": "HIGH_RISK_EMPLOYEE_V2",
            "tenantId": "11114444-2222-3333-4444-666634888863",
            "userId": "id2",
            "userName": "test2@example.com",
            "displayName": "Test2 Testerson",
            "notes": "Test test test2",
            "createdAt": "2021-04-22T00:00:00.0000000Z",
            "status": "OPEN",
            "cloudUsernames": [
                "alias2",
            ],
            "totalBytes": 0,
            "numEvents": 6
        }
    ]
}


@fixture
def mock_py42_with_user(mocker, mock_py42_client):
    response_data = {"users": [{"userUid": _TEST_USER_UID}]}
    mock_py42_client.users.get_by_username.return_value = create_mock_response(mocker, response_data)
    return mock_py42_client


@fixture
def mock_py42_with_departing_employees(mocker, mock_py42_client):
    def gen(*args, **kwargs):
        yield create_mock_response(mocker, _MOCK_LIST_DEPARTING_EMPLOYEES_RESPONSE)

    mock_py42_client.detectionlists.departing_employee.get_all.side_effect = gen
    return mock_py42_client


@fixture
def mock_py42_with_high_risk_employees(mocker, mock_py42_client):
    def gen(*args, **kwargs):
        yield create_mock_response(mocker, _MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE)

    mock_py42_client.detectionlists.high_risk_employee.get_all.side_effect = gen
    return mock_py42_client


def _create_add_de_connector(client):
    connector = create_fake_connector("add_departing_employee")
    return _attach_client(connector, client)


def _create_remove_de_connector(client):
    connector = create_fake_connector("remove_departing_employee")
    return _attach_client(connector, client)


def _create_list_de_connector(client):
    connector = create_fake_connector("list_departing_employees")
    return _attach_client(connector, client)


def _create_add_hr_connector(client):
    connector = create_fake_connector("add_highrisk_employee")
    return _attach_client(connector, client)


def _create_remove_hr_connector(client):
    connector = create_fake_connector("remove_highrisk_employee")
    return _attach_client(connector, client)


def _create_list_hr_connector(client):
    connector = create_fake_connector("list_highrisk_employees")
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
        assert_success(connector)

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
        assert_successful_single_data(connector, response_data)

    def test_handle_action_when_add_departing_employee_and_is_successful_sets_success_message(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_message(connector, "test@example.com was added to the departing employees list")

    def test_handle_action_when_add_departing_employee_and_including_note_adds_note(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "note": "Test Note"}
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.update_user_notes.assert_called_once_with(
            _TEST_USER_UID, "Test Note"
        )
        assert_success(connector)

    def test_handle_action_when_remove_departing_employee_calls_remove_with_expected_args(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.remove.assert_called_once_with(
            "TEST_USER_UID"
        )
        assert_success(connector)

    def test_handle_action_when_remove_departing_employee_adds_removed_user_id_to_data(
        self, mocker, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}

        # This API call does not have response data.
        mock_py42_with_user.detectionlists.departing_employee.remove.return_value = create_mock_response(
            mocker, {}
        )
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_single_data(connector, {"userId": _TEST_USER_UID})
        
    def test_handle_action_when_remove_departing_employee_and_is_successful_sets_success_message(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_message(connector, "test@example.com was removed from the departing employees list")

    def test_handle_action_when_list_departing_employees_and_given_filter_type_calls_get_all_with_given_filter(
        self, mock_py42_with_user
    ):
        param = {"filter_type": "EXFILTRATION_30_DAYS"}
        connector = _create_list_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.get_all.assert_called_once_with(
            filter_type="EXFILTRATION_30_DAYS"
        )
        assert_success(connector)

    def test_handle_action_when_list_departing_employees_and_not_given_filter_type_calls_remove_with_expected_args(
        self, mock_py42_with_user
    ):
        connector = _create_list_de_connector(mock_py42_with_user)
        connector.handle_action({})
        mock_py42_with_user.detectionlists.departing_employee.get_all.assert_called_once_with(
            filter_type="OPEN"
        )
        assert_success(connector)

    def test_handle_action_when_list_departing_employee_adds_info_to_summary(
        self, mock_py42_with_departing_employees
    ):
        connector = _create_list_de_connector(mock_py42_with_departing_employees)
        connector.handle_action({})
        assert_succesful_summary(connector, {"total_count": 2})

    def test_handle_action_when_list_departing_employees_adds_response_items_to_data(
        self, mock_py42_with_departing_employees
    ):
        connector = _create_list_de_connector(mock_py42_with_departing_employees)
        connector.handle_action({})
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        data = action_results[0].get_data()
        assert data[0] == _MOCK_LIST_DEPARTING_EMPLOYEES_RESPONSE["items"][0]
        assert data[1] == _MOCK_LIST_DEPARTING_EMPLOYEES_RESPONSE["items"][1]

    def test_handle_action_when_add_high_risk_employee_calls_add_with_expected_args(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_add_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.high_risk_employee.add.assert_called_once_with(
            "TEST_USER_UID"
        )
        assert_success(connector)

    def test_handle_action_when_add_high_risk_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user
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

        connector = _create_add_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_single_data(connector, response_data)

    def test_handle_action_when_add_high_risk_employee_and_is_successful_sets_success_message(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_add_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_message(connector, "test@example.com was added to the high risk employees list")

    def test_handle_action_when_remove_high_risk_employee_calls_remove_with_expected_args(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_remove_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.high_risk_employee.remove.assert_called_once_with(
            "TEST_USER_UID"
        )
        assert_success(connector)

    def test_handle_action_when_remove_high_risk_employee_adds_user_id_to_data(
        self, mocker, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}

        # This API call does not have response data.
        mock_py42_with_user.detectionlists.high_risk_employee.remove.return_value = create_mock_response(
            mocker, {}
        )
        connector = _create_remove_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_single_data(connector, {"userId": _TEST_USER_UID})

    def test_handle_action_when_remove_high_risk_employee_and_is_successful_sets_success_message(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_remove_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_message(connector, "test@example.com was removed from the high risk employees list")

    def test_handle_action_when_list_high_risk_employees_and_given_filter_type_calls_get_all_with_given_filter(
        self, mock_py42_with_user
    ):
        param = {"filter_type": "EXFILTRATION_30_DAYS"}
        connector = _create_list_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.high_risk_employee.get_all.assert_called_once_with(
            filter_type="EXFILTRATION_30_DAYS"
        )
        assert_success(connector)

    def test_handle_action_when_list_high_risk_employees_and_not_given_filter_type_calls_remove_with_expected_args(
        self, mock_py42_with_user
    ):
        connector = _create_list_hr_connector(mock_py42_with_user)
        connector.handle_action({})
        mock_py42_with_user.detectionlists.high_risk_employee.get_all.assert_called_once_with(
            filter_type="OPEN"
        )
        assert_success(connector)

    def test_handle_action_when_list_high_risk_employee_adds_info_to_summary(
        self, mock_py42_with_high_risk_employees
    ):
        connector = _create_list_hr_connector(mock_py42_with_high_risk_employees)
        connector.handle_action({})
        assert_succesful_summary(connector, {"total_count": 2})

    def test_handle_action_when_list_high_risk_employee_adds_response_items_to_data(
        self, mock_py42_with_high_risk_employees
    ):
        connector = _create_list_hr_connector(mock_py42_with_high_risk_employees)
        connector.handle_action({})
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        data = action_results[0].get_data()
        assert data[0] == _MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE["items"][0]
        assert data[1] == _MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE["items"][1]