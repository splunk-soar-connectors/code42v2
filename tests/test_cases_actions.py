import json
from requests import Response
from pytest import fixture

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CaseNameExistsError
from py42.exceptions import Py42UpdateClosedCaseError

from py42.response import Py42Response
from .conftest import (
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
_TEST_USER_UID = "1234"

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
def mock_py42_with_case(mocker, mock_py42_client):
    mock_cases_response = mocker.MagicMock(spec=Response)
    mock_cases_response.text = json.dumps(_TEST_CASE_RESPONSE)
    mock_py42_client.cases.create.return_value = Py42Response(mock_cases_response)
    mock_py42_client.cases.get.return_value = Py42Response(mock_cases_response)
    mock_py42_client.cases.update.return_value = Py42Response(mock_cases_response)
    return mock_py42_client


class TestCode42CasesConnector(object):
    def test_handle_action_when_creating_case_calls_with_expected_args_and_sets_success_status(
        self, mocker, mock_py42_with_case
    ):
        mock_user_response = mocker.MagicMock(spec=Response)
        mock_user_response.text = f'{{"users": [{{"userUid": "{_TEST_USER_UID}"}}]}}'
        mock_py42_with_case.users.get_by_username.return_value = Py42Response(
            mock_user_response
        )
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
            "name": _TEST_NAME,
            "subject": _TEST_SUBJECT,
            "description": _TEST_DESCRIPTION,
            "assignee": _TEST_ASSIGNEE,
            "findings": _TEST_FINDINGS,
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
        expected_summary = {
            "case_number": 1,
            "name": _TEST_NAME,
            "subject": _TEST_SUBJECT,
            "description": _TEST_DESCRIPTION,
            "assignee": _TEST_ASSIGNEE,
            "findings": _TEST_FINDINGS,
        }
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
