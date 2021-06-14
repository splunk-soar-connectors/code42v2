from requests import Response
from requests.exceptions import HTTPError
from pytest import fixture

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42CaseNameExistsError
from py42.exceptions import Py42UpdateClosedCaseError

from py42.response import Py42Response
from .conftest import (
    TEST_USER_UID as _TEST_USER_UID,
    assert_success,
    assert_fail,
    assert_fail_message,
    create_fake_connector,
    create_mock_response,
    assert_successful_single_data,
    assert_successful_message,
    assert_successful_summary,
)

_TEST_NAME = "test_case"
_TEST_DESCRIPTION = "test_description"
_TEST_SUBJECT = "test@example.com"
_TEST_ASSIGNEE = "admin@example.com"
_TEST_FINDINGS = "some findings: ```code here```"
_TEST_EVENT_ID = "0_12345_abcdef"

_TEST_CASE_RESPONSE = {
    "number": 2,
    "name": _TEST_NAME,
    "createdAt": "2021-01-01T12:00:00.000000Z",
    "updatedAt": "2021-01-01T12:00:00.000000Z",
    "description": _TEST_DESCRIPTION,
    "findings": _TEST_FINDINGS,
    "subject": _TEST_USER_UID,
    "subjectUsername": _TEST_SUBJECT,
    "status": "OPEN",
    "assignee": _TEST_USER_UID,
    "assigneeUsername": _TEST_ASSIGNEE,
    "createdByUserUid": "987654321098765433",
    "createdByUsername": "admin@example.com",
    "lastModifiedByUserUid": "987654321098765433",
    "lastModifiedByUsername": "admin@example.com",
}


@fixture
def mock_py42_with_case(mocker, mock_py42_with_user):
    mock_cases_response = create_mock_response(mocker, _TEST_CASE_RESPONSE)
    mock_py42_with_user.cases.create.return_value = Py42Response(mock_cases_response)
    mock_py42_with_user.cases.get.return_value = Py42Response(mock_cases_response)
    mock_py42_with_user.cases.update.return_value = Py42Response(mock_cases_response)
    return mock_py42_with_user


@fixture
def mock_py42_with_cases(mocker, mock_py42_client):
    response = {"cases": [_TEST_CASE_RESPONSE], "totalCount": 2}

    def gen(*args, **kwargs):
        yield create_mock_response(mocker, response)

    mock_py42_client.cases.get_all.side_effect = gen
    return mock_py42_client


class TestCode42CasesConnector(object):
    def test_handle_action_when_creating_case_calls_with_expected_args_and_sets_success_status(
        self, mock_py42_with_case
    ):
        param = {
            "case_name": _TEST_NAME,
            "description": _TEST_DESCRIPTION,
            "subject": _TEST_SUBJECT,
            "assignee": _TEST_ASSIGNEE,
            "findings": _TEST_FINDINGS,
        }
        connector = create_fake_connector("create_case", mock_py42_with_case)
        connector.handle_action(param)
        mock_py42_with_case.cases.create.assert_called_once_with(
            _TEST_NAME,
            description=_TEST_DESCRIPTION,
            findings=_TEST_FINDINGS,
            assignee=_TEST_USER_UID,
            subject=_TEST_USER_UID,
        )
        assert_success(connector)

    def test_handle_action_when_creating_case_when_case_name_already_exists_sets_error_status(
        self, mock_py42_with_case
    ):
        mock_py42_with_case.cases.create.side_effect = Py42CaseNameExistsError(
            Py42BadRequestError, _TEST_NAME
        )
        param = {"case_name": _TEST_NAME}
        connector = create_fake_connector("create_case", mock_py42_with_case)
        connector.handle_action(param)
        assert_fail_message(
            connector,
            f"Code42: Failed execution of action create_case: Case name '{_TEST_NAME}' already exists, please set another name",
        )

    def test_handle_action_when_creating_case_adds_response_to_data(
        self, mock_py42_with_case
    ):
        param = {"case_name": _TEST_NAME}
        connector = create_fake_connector("create_case", mock_py42_with_case)
        connector.handle_action(param)
        assert_successful_single_data(connector, _TEST_CASE_RESPONSE)

    def test_handle_action_when_creating_case_adds_info_to_summary(
        self, mock_py42_with_case
    ):
        param = {"case_name": _TEST_NAME}
        connector = create_fake_connector("create_case", mock_py42_with_case)
        connector.handle_action(param)
        expected_summary = {
            "case_number": 2,
        }
        assert_successful_summary(connector, expected_summary)

    def test_handle_action_when_updating_case_calls_with_expected_args_and_sets_success_status(
        self, mocker, mock_py42_with_case
    ):
        mock_user_response = mocker.MagicMock(spec=Response)
        mock_user_response.text = f'{{"users": [{{"userUid": "{_TEST_USER_UID}"}}]}}'
        mock_py42_with_case.users.get_by_username.return_value = Py42Response(
            mock_user_response
        )
        param = {
            "case_number": 1,
            "case_name": _TEST_NAME,
            "description": _TEST_DESCRIPTION,
            "subject": _TEST_SUBJECT,
            "assignee": _TEST_ASSIGNEE,
            "findings": _TEST_FINDINGS,
        }
        connector = create_fake_connector("update_case", mock_py42_with_case)
        connector.handle_action(param)
        mock_py42_with_case.cases.update.assert_called_once_with(
            1,
            name=_TEST_NAME,
            description=_TEST_DESCRIPTION,
            findings=_TEST_FINDINGS,
            assignee=_TEST_USER_UID,
            subject=_TEST_USER_UID,
        )
        assert_success(connector)

    def test_handle_action_when_updating_case_adds_response_to_data(
        self, mock_py42_with_case
    ):
        param = {"case_number": 1, "case_name": _TEST_NAME}
        connector = create_fake_connector("update_case", mock_py42_with_case)
        connector.handle_action(param)
        assert_successful_single_data(connector, _TEST_CASE_RESPONSE)

    def test_handle_action_when_updating_case_adds_info_to_summary(
        self, mock_py42_with_case
    ):
        param = {"case_number": 1, "case_name": _TEST_NAME}
        connector = create_fake_connector("update_case", mock_py42_with_case)
        connector.handle_action(param)
        expected_summary = {"case_number": 1}
        assert_successful_summary(connector, expected_summary)

    def test_handle_action_when_updating_case_when_case_closed_sets_error_status(
        self, mock_py42_with_case
    ):
        mock_py42_with_case.cases.update.side_effect = Py42UpdateClosedCaseError(
            Py42BadRequestError
        )
        param = {"case_number": 1, "case_name": _TEST_NAME}
        connector = create_fake_connector("update_case", mock_py42_with_case)
        connector.handle_action(param)
        assert_fail_message(
            connector,
            "Code42: Failed execution of action update_case: Cannot update a closed case.",
        )

    def test_handle_action_when_closing_case_calls_with_expected_args_and_sets_success_status(
        self, mock_py42_with_case
    ):
        param = {"case_number": 1}
        connector = create_fake_connector("close_case", mock_py42_with_case)
        connector.handle_action(param)
        mock_py42_with_case.cases.update.assert_called_once_with(1, status="CLOSED")
        assert_success(connector)

    def test_handle_action_when_closing_case_adds_response_to_data(
        self, mock_py42_with_case
    ):
        param = {"case_number": 1}
        connector = create_fake_connector("close_case", mock_py42_with_case)
        connector.handle_action(param)
        assert_successful_single_data(connector, _TEST_CASE_RESPONSE)

    def test_handle_action_when_closing_case_adds_info_to_summary(
        self, mock_py42_with_case
    ):
        param = {"case_number": 1}
        connector = create_fake_connector("close_case", mock_py42_with_case)
        connector.handle_action(param)
        expected_summary = {"case_number": 1}
        assert_successful_summary(connector, expected_summary)

    def test_handle_action_when_closing_case_when_case_already_closed_calls_get_and_sets_expected_success_message(
        self, mock_py42_with_case
    ):
        mock_py42_with_case.cases.update.side_effect = Py42UpdateClosedCaseError(
            Py42BadRequestError
        )
        param = {"case_number": 1}
        connector = create_fake_connector("close_case", mock_py42_with_case)
        connector.handle_action(param)
        mock_py42_with_case.cases.get.assert_called_once_with(1)
        assert_successful_message(connector, "Case number 1 already closed!")

    def test_handle_action_when_closing_case_when_case_number_not_found_sets_error_status(
        self, mocker, mock_py42_with_case
    ):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.text = ""
        http_error = HTTPError(response=mock_response)
        mock_py42_with_case.cases.update.side_effect = Py42NotFoundError(http_error)
        param = {"case_number": 1}
        connector = create_fake_connector("close_case", mock_py42_with_case)
        connector.handle_action(param)
        assert_fail(connector)

    def test_handle_action_when_list_cases_and_status_all_given_passes_none(
        self, mock_py42_with_case
    ):
        param = {"status": "ALL"}
        connector = create_fake_connector("list_cases", mock_py42_with_case)
        connector.handle_action(param)
        mock_py42_with_case.cases.get_all.assert_called_once_with(
            status=None, subject=None, assignee=None
        )
        assert_success(connector)

    def test_handle_action_when_list_cases_calls_py42_with_correct_filters(
        self, mock_py42_with_case
    ):
        param = {"status": "OPEN", "assignee": _TEST_ASSIGNEE, "subject": _TEST_SUBJECT}
        connector = create_fake_connector("list_cases", mock_py42_with_case)
        connector.handle_action(param)
        mock_py42_with_case.cases.get_all.assert_called_once_with(
            status="OPEN", assignee=_TEST_ASSIGNEE, subject=_TEST_SUBJECT
        )
        assert_success(connector)

    def test_handle_action_when_list_departing_employee_updates_summary(
        self, mock_py42_with_cases
    ):
        param = {"status": "ALL"}
        connector = create_fake_connector("list_cases", mock_py42_with_cases)
        connector.handle_action(param)
        assert_successful_summary(connector, {"total_count": 2})

    def test_handle_action_when_list_cases_adds_response_items_to_data(
        self, mock_py42_with_cases
    ):
        param = {"status": "ALL"}
        connector = create_fake_connector("list_cases", mock_py42_with_cases)
        connector.handle_action(param)
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        data = action_results[0].get_data()
        assert data[0] == _TEST_CASE_RESPONSE

    def test_handle_action_when_adding_event_to_case_calls_with_expected_args(
        self, mock_py42_with_case
    ):
        param = {"case_number": "10", "event_id": _TEST_EVENT_ID}
        connector = create_fake_connector("add_case_event", mock_py42_with_case)
        connector.handle_action(param)
        mock_py42_with_case.cases.file_events.add.assert_called_once_with(
            case_number="10", event_id=_TEST_EVENT_ID
        )
        assert_success(connector)

    def test_handle_action_when_adding_event_to_case_and_is_successful_sets_success_message(
        self, mock_py42_with_case
    ):
        param = {"case_number": "10", "event_id": _TEST_EVENT_ID}
        connector = create_fake_connector("add_case_event", mock_py42_with_case)
        connector.handle_action(param)
        expected_message = f"Event {_TEST_EVENT_ID} added to case number 10"
        assert_successful_message(connector, expected_message)

    def test_handle_action_when_adding_event_to_case_sets_error_status_when_case_or_event_not_found(
        self, mocker, mock_py42_with_case
    ):
        mock_response = create_mock_response(mocker, {"problem": "NO_SUCH_CASE"})
        mock_py42_with_case.cases.file_events.add.side_effect = Py42BadRequestError(
            HTTPError(response=mock_response)
        )
        param = {"case_number": "10", "event_id": _TEST_EVENT_ID}
        connector = create_fake_connector("add_case_event", mock_py42_with_case)
        connector.handle_action(param)
        assert_fail(connector)
