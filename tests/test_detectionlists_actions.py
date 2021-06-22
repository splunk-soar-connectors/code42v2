from unittest import mock

from py42.exceptions import Py42NotFoundError
from pytest import fixture

from tests.conftest import (
    assert_success,
    create_fake_connector,
    create_mock_response,
    assert_successful_single_data,
    assert_successful_message,
    assert_successful_summary,
    assert_fail_message,
    attach_client,
    TEST_USER_UID,
)

_MOCK_GET_DEPARTING_EMPLOYEE_RESPONSE = {
    "type$": "DEPARTING_EMPLOYEE_V2",
    "tenantId": "11114444-2222-3333-4444-666634888863",
    "userId": TEST_USER_UID,
    "userName": "test@example.com",
    "displayName": "Test Testerson",
    "notes": "Test test test",
    "createdAt": "2021-05-24T17:19:06.2830000Z",
    "status": "OPEN",
    "cloudUsernames": ["alias1"],
    "departureDate": "2021-02-02",
}
_MOCK_LIST_DEPARTING_EMPLOYEES_RESPONSE = {
    "totalCount": 2,
    "items": [
        {
            "type$": "DEPARTING_EMPLOYEE_V2",
            "tenantId": "11114444-2222-3333-4444-666634888863",
            "userId": TEST_USER_UID,
            "userName": "test@example.com",
            "displayName": "Test Testerson",
            "notes": "Test test test",
            "createdAt": "2021-04-22T00:00:00.0000000Z",
            "status": "OPEN",
            "cloudUsernames": ["alias1",],
            "totalBytes": 0,
            "numEvents": 3,
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
            "cloudUsernames": ["alias2",],
            "totalBytes": 0,
            "numEvents": 6,
        },
    ],
}
_MOCK_GET_HIGH_RISK_EMPLOYEE_RESPONSE = {
    "type$": "HIGH_RISK_EMPLOYEE_V2",
    "tenantId": "11114444-2222-3333-4444-666634888863",
    "userId": TEST_USER_UID,
    "userName": "test@example.com",
    "displayName": "Test Testerson",
    "notes": "Test test test",
    "createdAt": "2021-05-25T18:43:29.6890000Z",
    "status": "OPEN",
    "cloudUsernames": ["alias1"],
    "riskFactors": ["FLIGHT_RISK", "CONTRACT_EMPLOYEE"],
}
_MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE = {
    "totalCount": 2,
    "items": [
        {
            "type$": "HIGH_RISK_EMPLOYEE_V2",
            "tenantId": "11114444-2222-3333-4444-666634888863",
            "userId": TEST_USER_UID,
            "userName": "test@example.com",
            "displayName": "Test Testerson",
            "notes": "Test test test",
            "createdAt": "2021-04-22T00:00:00.0000000Z",
            "status": "OPEN",
            "cloudUsernames": ["alias1",],
            "totalBytes": 0,
            "numEvents": 3,
            "riskFactors": ["FLIGHT_RISK", "CONTRACT_EMPLOYEE"],
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
            "cloudUsernames": ["alias2",],
            "totalBytes": 0,
            "numEvents": 6,
        },
    ],
}
_MOCK_ADD_RISK_TAGS_RESPONSE = {
    "type$": "USER_V2",
    "tenantId": "11114444-2222-3333-4444-666634888863",
    "userId": TEST_USER_UID,
    "userName": "test@example.com",
    "displayName": "Test Testerson",
    "cloudUsernames": ["test@example.com"],
    "riskFactors": ["FLIGHT_RISK", "HIGH_IMPACT_EMPLOYEE",],
}
_MOCK_REMOVE_RISK_TAGS_RESPONSE = {
    "type$": "USER_V2",
    "tenantId": "11114444-2222-3333-4444-666634888863",
    "userId": TEST_USER_UID,
    "userName": "test@example.com",
    "displayName": "Test Testerson",
    "cloudUsernames": ["test@example.com"],
    "riskFactors": ["ELEVATED_ACCESS_PRIVILEGES"],
}


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
    mock_py42_with_user.detectionlists.remove_user_risk_tags.return_value = (
        remove_response
    )
    return mock_py42_with_user


def _create_add_de_connector(client):
    connector = create_fake_connector("add_departing_employee")
    return attach_client(connector, client)


def _create_remove_de_connector(client):
    connector = create_fake_connector("remove_departing_employee")
    return attach_client(connector, client)


def _create_list_de_connector(client):
    connector = create_fake_connector("list_departing_employees")
    return attach_client(connector, client)


def _create_get_de_connector(client):
    connector = create_fake_connector("get_departing_employee")
    return attach_client(connector, client)


def _create_add_hr_connector(client):
    connector = create_fake_connector("add_highrisk_employee")
    return attach_client(connector, client)


def _create_remove_hr_connector(client):
    connector = create_fake_connector("remove_highrisk_employee")
    return attach_client(connector, client)


def _create_list_hr_connector(client):
    connector = create_fake_connector("list_highrisk_employees")
    return attach_client(connector, client)


def _create_get_hr_connector(client):
    connector = create_fake_connector("get_highrisk_employee")
    return _attach_client(connector, client)


def _create_add_risk_tag_connector(client):
    connector = create_fake_connector("add_highrisk_tag")
    return _attach_client(connector, client)


def _create_remove_risk_tag_connector(client):
    connector = create_fake_connector("remove_highrisk_tag")
    return _attach_client(connector, client)


def _attach_client(connector, client):
    connector._client = client
    return connector


class TestCode42DetectionListsConnector(object):
    def test_handler_action_when_acting_on_user_that_does_not_exists_sets_expected_error_message(
        self, mock_py42_without_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_add_de_connector(mock_py42_without_user)
        connector.handle_action(param)
        expected_message = (
            "Code42: Failed execution of action add_departing_employee: User 'test@example.com' not found. "
            "Do you have the correct permissions?"
        )
        assert_fail_message(connector, expected_message)

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
            "userId": TEST_USER_UID,
            "userName": "test@example.com",
            "displayName": "",
            "createdAt": "2021-05-20T19:40:14.8909434Z",
            "status": "OPEN",
            "cloudUsernames": ["test@example.com"],
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
        assert_successful_message(
            connector, "test@example.com was added to the departing employees list"
        )

    def test_handle_action_when_add_departing_employee_and_including_note_adds_note(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "note": "Test Note"}
        connector = _create_add_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.update_user_notes.assert_called_once_with(
            TEST_USER_UID, "Test Note"
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
        assert_successful_single_data(connector, {"userId": TEST_USER_UID})

    def test_handle_action_when_remove_departing_employee_and_is_successful_sets_success_message(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_remove_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_message(
            connector, "test@example.com was removed from the departing employees list"
        )

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

    def test_handle_action_when_list_departing_employee_updates_summary(
        self, mock_py42_with_departing_employees
    ):
        connector = _create_list_de_connector(mock_py42_with_departing_employees)
        connector.handle_action({})
        assert_successful_summary(connector, {"total_count": 2})

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

    def test_handle_action_when_get_departing_employee_calls_get_with_expected_params(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_get_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.departing_employee.get.assert_called_once_with(
            TEST_USER_UID
        )
        assert_success(connector)

    def test_handle_action_when_get_departing_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        mock_py42_with_user.detectionlists.departing_employee.get.return_value = create_mock_response(
            mocker, _MOCK_GET_DEPARTING_EMPLOYEE_RESPONSE
        )
        connector = _create_get_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_single_data(connector, _MOCK_GET_DEPARTING_EMPLOYEE_RESPONSE)

    def test_handle_action_when_get_departing_employee_updates_summary(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_get_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_summary(connector, {"is_departing_employee": True})

    def test_handle_action_when_get_departing_employee_and_employee_not_found_updates_summary(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        mock_py42_with_user.detectionlists.departing_employee.get.side_effect = Py42NotFoundError(
            mock.Mock(status=404)
        )
        connector = _create_get_de_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_summary(connector, {"is_departing_employee": False})

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
            "userId": TEST_USER_UID,
            "userName": "test@example.com",
            "displayName": "",
            "createdAt": "2021-05-20T19:40:14.8909434Z",
            "status": "OPEN",
            "cloudUsernames": ["test@example.com"],
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
        assert_successful_message(
            connector, "test@example.com was added to the high risk employees list"
        )

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
        assert_successful_single_data(connector, {"userId": TEST_USER_UID})

    def test_handle_action_when_remove_high_risk_employee_and_is_successful_sets_success_message(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_remove_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_message(
            connector, "test@example.com was removed from the high risk employees list"
        )

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

    def test_handle_action_when_list_high_risk_employee_updates_summary(
        self, mock_py42_with_high_risk_employees
    ):
        connector = _create_list_hr_connector(mock_py42_with_high_risk_employees)
        connector.handle_action({})
        assert_successful_summary(connector, {"total_count": 2})

    def test_handle_action_when_list_high_risk_employee_adds_response_items_to_data(
        self, mock_py42_with_high_risk_employees
    ):
        connector = _create_list_hr_connector(mock_py42_with_high_risk_employees)
        connector.handle_action({})
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        data = action_results[0].get_data()
        expected_employee_1 = dict(_MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE["items"][0])
        expected_employee_1["riskFactors"] = [
            {"tag": "FLIGHT_RISK"},
            {"tag": "CONTRACT_EMPLOYEE"},
        ]
        expected_employee_2 = dict(_MOCK_LIST_HIGH_RISK_EMPLOYEES_RESPONSE["items"][1])
        assert data[0] == expected_employee_1
        assert data[1] == expected_employee_2

    def test_handle_action_when_get_high_risk_employee_calls_get_with_expected_params(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_get_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.detectionlists.high_risk_employee.get.assert_called_once_with(
            TEST_USER_UID
        )
        assert_success(connector)

    def test_handle_action_when_get_high_risk_employee_adds_response_to_data(
        self, mocker, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        mock_py42_with_user.detectionlists.high_risk_employee.get.return_value = create_mock_response(
            mocker, _MOCK_GET_HIGH_RISK_EMPLOYEE_RESPONSE
        )
        connector = _create_get_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        expected_response = dict(_MOCK_GET_HIGH_RISK_EMPLOYEE_RESPONSE)
        expected_response["riskFactors"] = [
            {"tag": "FLIGHT_RISK"},
            {"tag": "CONTRACT_EMPLOYEE"},
        ]
        assert_successful_single_data(connector, expected_response)

    def test_handle_action_when_get_high_risk_employee_updates_summary(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        connector = _create_get_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_summary(connector, {"is_high_risk_employee": True})

    def test_handle_action_when_get_high_risk_employee_and_employee_not_found_updates_summary(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com"}
        mock_py42_with_user.detectionlists.high_risk_employee.get.side_effect = Py42NotFoundError(
            mock.Mock(status=404)
        )
        connector = _create_get_hr_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_summary(connector, {"is_high_risk_employee": False})

    def test_handle_action_when_add_high_risk_tag_calls_add_with_expected_args(
        self, mock_py42_for_risk_tags
    ):
        param = {
            "username": "test@example.com",
            "risk_tag": "FLIGHT_RISK",
        }
        connector = _create_add_risk_tag_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)
        mock_py42_for_risk_tags.detectionlists.add_user_risk_tags.assert_called_once_with(
            "TEST_USER_UID", "FLIGHT_RISK"
        )
        assert_success(connector)

    def test_handle_action_when_add_high_risk_tag_adds_response_items_to_data(
        self, mock_py42_for_risk_tags
    ):
        param = {
            "username": "test@example.com",
            "risk_tag": "HIGH_IMPACT_EMPLOYEE",
        }
        connector = _create_add_risk_tag_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)
        expected_response = dict(_MOCK_ADD_RISK_TAGS_RESPONSE)

        # Transforms its scalar list to be a list of objects
        # These tags are found in _MOCK_ADD_RISK_TAGS_RESPONSE.
        expected_response["riskFactors"] = [
            {"tag": "FLIGHT_RISK"},
            {"tag": "HIGH_IMPACT_EMPLOYEE"},
        ]

        assert_successful_single_data(connector, expected_response)

    def test_handle_action_when_add_high_risk_tag_sets_success_message(
        self, mock_py42_for_risk_tags
    ):
        param = {
            "username": "test@example.com",
            "risk_tag": "FLIGHT_RISK",
        }
        connector = _create_add_risk_tag_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)

        # Found in _MOCK_ADD_RISK_TAGS_RESPONSE
        risk_tags_from_add_response = "FLIGHT_RISK,HIGH_IMPACT_EMPLOYEE"

        expected = "All risk tags for user: FLIGHT_RISK,HIGH_IMPACT_EMPLOYEE"
        assert_successful_message(connector, expected)

    def test_handle_action_when_remove_high_risk_tag_calls_remove_with_expected_args(
        self, mock_py42_for_risk_tags
    ):
        param = {
            "username": "test@example.com",
            "risk_tag": "HIGH_IMPACT_EMPLOYEE",
        }
        connector = _create_remove_risk_tag_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)
        mock_py42_for_risk_tags.detectionlists.remove_user_risk_tags.assert_called_once_with(
            "TEST_USER_UID", "HIGH_IMPACT_EMPLOYEE"
        )
        assert_success(connector)

    def test_handle_action_when_remove_high_risk_tag_adds_response_items_to_data(
        self, mock_py42_for_risk_tags
    ):
        param = {
            "username": "test@example.com",
            "risk_tag": "ELEVATED_ACCESS_PRIVILEGES",
        }
        connector = _create_remove_risk_tag_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)

        # Transforms its scalar list to be a list of objects
        # These tags are found in _MOCK_ADD_RISK_TAGS_RESPONSE.
        expected_response = dict(_MOCK_REMOVE_RISK_TAGS_RESPONSE)
        expected_response["riskFactors"] = [{"tag": "ELEVATED_ACCESS_PRIVILEGES"}]

        assert_successful_single_data(connector, expected_response)

    def test_handle_action_when_remove_high_risk_tag_sets_success_message(
        self, mock_py42_for_risk_tags
    ):
        param = {
            "username": "test@example.com",
            "risk_tag": "FLIGHT_RISK",
        }
        connector = _create_remove_risk_tag_connector(mock_py42_for_risk_tags)
        connector.handle_action(param)

        # Found in _MOCK_REMOVE_RISK_TAGS_RESPONSE
        risk_tags_from_remove_response = "ELEVATED_ACCESS_PRIVILEGES"

        expected = "All risk tags for user: ELEVATED_ACCESS_PRIVILEGES"
        assert_successful_message(connector, expected)

    def test_handle_action_when_remove_high_risk_tag_and_user_now_has_no_tags_sets_expected_message(
        self, mocker, mock_py42_with_user
    ):
        param = {
            "username": "test@example.com",
            "risk_tag": "FLIGHT_RISK",
        }

        response_dict = dict(_MOCK_REMOVE_RISK_TAGS_RESPONSE)
        response_dict["riskFactors"] = []
        remove_response = create_mock_response(mocker, response_dict)
        mock_py42_with_user.detectionlists.remove_user_risk_tags.return_value = (
            remove_response
        )

        connector = _create_remove_risk_tag_connector(mock_py42_with_user)
        connector.handle_action(param)
        expected = "User has no risk tags"
        assert_successful_message(connector, expected)
