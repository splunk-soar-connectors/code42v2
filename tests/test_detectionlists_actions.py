from pytest import fixture

from phantom.action_result import ActionResult
from tests.conftest import create_fake_connector
from tests.conftest import create_mock_response

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
_MOCK_ADD_RISK_TAGS_RESPONSE = {
    "type$": "USER_V2",
    "tenantId": "11114444-2222-3333-4444-666634888863",
    "userId": _TEST_USER_UID,
    "userName": "test@example.com",
    "displayName": "Test Testerson",
    "cloudUsernames": [
        "test@example.com"
    ],
    "riskFactors": [
        "FLIGHT_RISK",
        "HIGH_IMPACT_EMPLOYEE",
    ]
}
_MOCK_REMOVE_RISK_TAGS_RESPONSE = {
    "type$": "USER_V2",
    "tenantId": "11114444-2222-3333-4444-666634888863",
    "userId": _TEST_USER_UID,
    "userName": "test@example.com",
    "displayName": "Test Testerson",
    "cloudUsernames": [
        "test@example.com"
    ],
    "riskFactors": [
        "ELEVATED_ACCESS_PRIVILEGES"
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


@fixture
def mock_py42_for_risk_tags(mocker, mock_py42_with_user):
    add_response = create_mock_response(mocker, _MOCK_ADD_RISK_TAGS_RESPONSE)
    remove_response = create_mock_response(mocker, _MOCK_REMOVE_RISK_TAGS_RESPONSE)
    mock_py42_with_user.detectionlists.add_user_risk_tags.return_value = add_response
    mock_py42_with_user.detectionlists.remove_user_risk_tags.return_value = remove_response
    return mock_py42_with_user


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


def _create_add_risk_tags_connector(client):
    connector = create_fake_connector("add_highrisk_tags")
    return _attach_client(connector, client)


def _create_remove_risk_tags_connector(client):
    connector = create_fake_connector("remove_highrisk_tags")
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
        expected_message = "test@example.com was added to the departing employees list"
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
        expected_message = "test@example.com was removed from the departing employees list"
        set_status_mock.assert_called_once_with(1, expected_message)

    def test_handle_action_when_list_departing_employees_and_given_filter_type_calls_get_all_with_given_filter(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {"filter_type": "EXFILTRATION_30_DAYS"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_list_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.get_all.assert_called_once_with(
            filter_type="EXFILTRATION_30_DAYS"
        )

    def test_handle_action_when_list_departing_employees_and_not_given_filter_type_calls_remove_with_expected_args(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_list_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.get_all.assert_called_once_with(
            filter_type="OPEN"
        )

    def test_handle_action_when_list_departing_employee_updates_summary(
        self, mocker, mock_py42_with_departing_employees, mock_result_adder
    ):
        result = ActionResult(dict({}))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = _create_list_de_connector(mock_py42_with_departing_employees)
        connector.handle_action({})
        update_summary_mock.assert_called_once_with({"total_count": 2})

    def test_handle_action_when_list_departing_employees_adds_response_items_to_data(
        self, mocker, mock_py42_with_departing_employees, mock_result_adder
    ):
        result = ActionResult(dict({}))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = _create_list_de_connector(mock_py42_with_departing_employees)
        connector.handle_action({})
        call_args = add_data_mock.call_args_list
        assert add_data_mock.call_count == 2
        assert call_args[0][0][0] == _MOCK_LIST_DEPARTING_EMPLOYEES_RESPONSE["items"][0]
        assert call_args[1][0][0] == _MOCK_LIST_DEPARTING_EMPLOYEES_RESPONSE["items"][1]

    def test_handle_action_when_list_departing_employee_and_is_successful_sets_success_status(
        self, mocker, mock_py42_with_departing_employees, mock_result_adder
    ):
        result = ActionResult(dict({}))
        set_status_mock = mocker.MagicMock()
        result.set_status = set_status_mock
        mock_result_adder.return_value = result
        connector = _create_list_de_connector(mock_py42_with_departing_employees)
        connector.handle_action({})
        set_status_mock.assert_called_once_with(1)

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
        expected_message = "test@example.com was added to the high risk employees list"
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
        expected_message = "test@example.com was removed from the high risk employees list"
        set_status_mock.assert_called_once_with(1, expected_message)

    def test_handle_action_when_list_high_risk_employees_and_given_filter_type_calls_get_all_with_given_filter(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {"filter_type": "EXFILTRATION_30_DAYS"}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_list_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.high_risk_employee.get_all.assert_called_once_with(
            filter_type="EXFILTRATION_30_DAYS"
        )

    def test_handle_action_when_list_high_risk_employees_and_not_given_filter_type_calls_remove_with_expected_args(
        self, mock_py42_with_user, mock_result_adder
    ):
        param = {}
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_list_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.high_risk_employee.get_all.assert_called_once_with(
            filter_type="OPEN"
        )

    def test_handle_action_when_list_high_risk_employee_updates_summary(
        self, mocker, mock_py42_with_high_risk_employees, mock_result_adder
    ):
        result = ActionResult(dict({}))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = _create_list_hr_connector(mock_py42_with_high_risk_employees)
        connector.handle_action({})
        update_summary_mock.assert_called_once_with({"total_count": 2})

    def test_handle_action_when_list_high_risk_employees_adds_response_items_to_data(
        self, mocker, mock_py42_with_high_risk_employees, mock_result_adder
    ):
        result = ActionResult(dict({}))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = _create_list_hr_connector(mock_py42_with_high_risk_employees)
        connector.handle_action({})
        call_args = add_data_mock.call_args_list
        assert add_data_mock.call_count == 2
        assert call_args[0][0][0] == _MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE["items"][0]
        assert call_args[1][0][0] == _MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE["items"][1]

    def test_handle_action_when_list_high_risk_employee_and_is_successful_sets_success_status(
        self, mocker, mock_py42_with_high_risk_employees, mock_result_adder
    ):
        result = ActionResult(dict({}))
        set_status_mock = mocker.MagicMock()
        result.set_status = set_status_mock
        mock_result_adder.return_value = result
        connector = _create_list_hr_connector(mock_py42_with_high_risk_employees)
        connector.handle_action({})
        set_status_mock.assert_called_once_with(1)

    def test_handle_action_when_add_high_risk_tags_calls_add_with_expected_args(
        self, mock_py42_for_risk_tags, mock_result_adder
    ):
        param = {
            "username": "test@example.com",
            "risk_tags": "FLIGHT_RISK,HIGH_IMPACT_EMPLOYEE"
        }
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_add_risk_tags_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)
        mock_py42_for_risk_tags.detectionlists.add_user_risk_tags.assert_called_once_with(
            "TEST_USER_UID", ["FLIGHT_RISK", "HIGH_IMPACT_EMPLOYEE"]
        )

    def test_handle_action_when_add_high_risk_tags_adds_response_items_to_data(
        self, mocker, mock_py42_for_risk_tags, mock_result_adder
    ):
        param = {
            "username": "test@example.com",
            "risk_tags": "FLIGHT_RISK,HIGH_IMPACT_EMPLOYEE,ELEVATED_ACCESS_PRIVILEGES"
        }
        result = ActionResult(dict(param))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = _create_add_risk_tags_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)
        add_data_mock.assert_called_once_with(_MOCK_ADD_RISK_TAGS_RESPONSE)

    def test_handle_action_when_add_high_risk_tags_updates_summary(
        self, mocker, mock_py42_for_risk_tags, mock_result_adder
    ):
        param = {
            "username": "test@example.com",
            "risk_tags": "FLIGHT_RISK,HIGH_IMPACT_EMPLOYEE"
        }
        result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = _create_add_risk_tags_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)

        # Found in _MOCK_ADD_RISK_TAGS_RESPONSE
        risk_tags_from_add_response = [
            "FLIGHT_RISK",
            "HIGH_IMPACT_EMPLOYEE",
        ]

        update_summary_mock.assert_called_once_with(
            {"all_user_risk_tags": risk_tags_from_add_response}
        )

    def test_handle_action_when_remove_high_risk_tags_calls_remove_with_expected_args(
        self, mock_py42_for_risk_tags, mock_result_adder
    ):
        param = {
            "username": "test@example.com",
            "risk_tags": "FLIGHT_RISK,HIGH_IMPACT_EMPLOYEE"
        }
        result = ActionResult(dict(param))
        mock_result_adder.return_value = result
        connector = _create_remove_risk_tags_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)
        mock_py42_for_risk_tags.detectionlists.remove_user_risk_tags.assert_called_once_with(
            "TEST_USER_UID", ["FLIGHT_RISK", "HIGH_IMPACT_EMPLOYEE"]
        )

    def test_handle_action_when_remove_high_risk_tags_adds_response_items_to_data(
        self, mocker, mock_py42_for_risk_tags, mock_result_adder
    ):
        param = {
            "username": "test@example.com",
            "risk_tags": "FLIGHT_RISK,HIGH_IMPACT_EMPLOYEE,ELEVATED_ACCESS_PRIVILEGES"
        }
        result = ActionResult(dict(param))
        add_data_mock = mocker.MagicMock()
        result.add_data = add_data_mock
        mock_result_adder.return_value = result
        connector = _create_remove_risk_tags_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)
        add_data_mock.assert_called_once_with(_MOCK_REMOVE_RISK_TAGS_RESPONSE)

    def test_handle_action_when_remove_high_risk_tags_updates_summary(
        self, mocker, mock_py42_for_risk_tags, mock_result_adder
    ):
        param = {
            "username": "test@example.com",
            "risk_tags": "FLIGHT_RISK,HIGH_IMPACT_EMPLOYEE"
        }
        result = ActionResult(dict(param))
        update_summary_mock = mocker.MagicMock()
        result.update_summary = update_summary_mock
        mock_result_adder.return_value = result
        connector = _create_remove_risk_tags_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)

        # Found in _MOCK_REMOVE_RISK_TAGS_RESPONSE
        risk_tags_from_remove_response = ["ELEVATED_ACCESS_PRIVILEGES"]

        update_summary_mock.assert_called_once_with(
            {"all_user_risk_tags": risk_tags_from_remove_response}
        )
