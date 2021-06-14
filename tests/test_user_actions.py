from unittest import mock

from py42.exceptions import Py42UserAlreadyExistsError
from pytest import fixture

from .conftest import (
    assert_success,
    assert_fail,
    create_fake_connector,
    create_mock_response,
    assert_successful_single_data,
    assert_successful_message,
)

_TEST_ORG_UID = "TEST_ORG_UID"
_TEST_USER_UID = "TEST_USER_UID"
_TEST_USER_LEGACY_ID = "TEST_USER_LEGACY_ID"
_TEST_USERNAME = "test@example.com"
_TEST_PASSWORD = "test_pass"
_TEST_FIRSTNAME = "test_first"
_TEST_LASTNAME = "test_last"
_TEST_NOTE = "noting a test"


@fixture
def mock_py42_with_create_user(mocker, mock_py42_client):
    response_data = {"userUid": _TEST_USER_UID, "userId": _TEST_USER_LEGACY_ID}
    mock_py42_client.users.create_user.return_value = create_mock_response(
        mocker, response_data
    )
    return mock_py42_client


@fixture
def mock_py42_with_legacy_id_user(mocker, mock_py42_client):
    response_data = {
        "users": [{"userUid": _TEST_USER_UID, "userId": _TEST_USER_LEGACY_ID}]
    }
    mock_py42_client.users.get_by_username.return_value = create_mock_response(
        mocker, response_data
    )
    return mock_py42_client


@fixture
def mock_py42_with_user_not_found(mocker, mock_py42_client):
    mock_py42_client.users.get_by_username.return_value = create_mock_response(
        mocker, {"totalCount": 0, "users": []}
    )
    return mock_py42_client


class TestCode42UsersConnector(object):
    def test_handle_action_when_creating_user_calls_with_expected_args_and_sets_success_status(
        self, mock_py42_with_create_user
    ):
        param = {
            "org_uid": _TEST_ORG_UID,
            "username": _TEST_USERNAME,
            "password": _TEST_PASSWORD,
            "first_name": _TEST_FIRSTNAME,
            "last_name": _TEST_LASTNAME,
            "notes": _TEST_NOTE,
        }
        connector = create_fake_connector("create_user", mock_py42_with_create_user)
        connector.handle_action(param)
        mock_py42_with_create_user.users.create_user.assert_called_once_with(
            org_uid=_TEST_ORG_UID,
            username=_TEST_USERNAME,
            email=_TEST_USERNAME,
            password=_TEST_PASSWORD,
            first_name=_TEST_FIRSTNAME,
            last_name=_TEST_LASTNAME,
            notes=_TEST_NOTE,
        )
        assert_success(connector)

    def test_handle_action_when_creating_user_and_is_successful_sets_success_message(
        self, mock_py42_with_create_user
    ):
        param = {"org_uid": _TEST_ORG_UID, "username": _TEST_USERNAME}
        connector = create_fake_connector("create_user", mock_py42_with_create_user)
        connector.handle_action(param)
        expected_message = (
            f"{_TEST_USERNAME} was created with user_id: {_TEST_USER_UID}"
        )
        assert_successful_message(connector, expected_message)

    def test_handle_action_when_creating_user_adds_response_to_data(
        self, mock_py42_with_create_user
    ):
        param = {"org_uid": _TEST_ORG_UID, "username": _TEST_USERNAME}
        connector = create_fake_connector("create_user", mock_py42_with_create_user)
        connector.handle_action(param)
        assert_successful_single_data(
            connector,
            {"userUid": _TEST_USER_UID, "userId": _TEST_USER_LEGACY_ID},
        )

    def test_handle_action_when_creating_user_sets_error_status_when_duplicate_user(
        self, mock_py42_with_create_user
    ):
        mock_py42_with_create_user.users.create_user.side_effect = (
            Py42UserAlreadyExistsError(mock.Mock(status=500))
        )
        param = {"org_uid": _TEST_ORG_UID, "username": _TEST_USERNAME}
        connector = create_fake_connector("create_user", mock_py42_with_create_user)
        connector.handle_action(param)
        assert_fail(connector)

    def test_handle_action_when_blocking_user_calls_with_expected_args(
        self, mock_py42_with_legacy_id_user
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector("block_user", mock_py42_with_legacy_id_user)
        connector.handle_action(param)
        mock_py42_with_legacy_id_user.users.block.assert_called_once_with(
            _TEST_USER_LEGACY_ID
        )
        assert_success(connector)

    def test_handle_action_when_blocking_user_and_is_successful_sets_success_message(
        self, mock_py42_with_legacy_id_user
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector("block_user", mock_py42_with_legacy_id_user)
        connector.handle_action(param)
        expected_message = f"{_TEST_USERNAME} was blocked"
        assert_successful_message(connector, expected_message)

    def test_handle_action_when_blocking_user_sets_error_status_when_user_not_found(
        self, mock_py42_with_user_not_found
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector("block_user", mock_py42_with_user_not_found)
        connector.handle_action(param)
        assert_fail(connector)

    def test_handle_action_when_unblocking_user_calls_with_expected_args(
        self, mock_py42_with_legacy_id_user
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector("unblock_user", mock_py42_with_legacy_id_user)
        connector.handle_action(param)
        mock_py42_with_legacy_id_user.users.unblock.assert_called_once_with(
            _TEST_USER_LEGACY_ID
        )

    def test_handle_action_when_unblocking_user_and_is_successful_sets_success_message(
        self, mock_py42_with_legacy_id_user
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector("unblock_user", mock_py42_with_legacy_id_user)
        connector.handle_action(param)
        expected_message = f"{_TEST_USERNAME} was unblocked"
        assert_successful_message(connector, expected_message)

    def test_handle_action_when_unblocking_user_sets_error_status_when_user_not_found(
        self, mock_py42_with_user_not_found
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector("unblock_user", mock_py42_with_user_not_found)
        connector.handle_action(param)
        assert_fail(connector)

    def test_handle_action_when_deactivating_user_calls_with_expected_args(
        self, mock_py42_with_legacy_id_user
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector(
            "deactivate_user", mock_py42_with_legacy_id_user
        )
        connector.handle_action(param)
        mock_py42_with_legacy_id_user.users.deactivate.assert_called_once_with(
            _TEST_USER_LEGACY_ID
        )
        assert_success(connector)

    def test_handle_action_when_deactivating_user_and_is_successful_sets_success_message(
        self, mock_py42_with_legacy_id_user
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector(
            "deactivate_user", mock_py42_with_legacy_id_user
        )
        connector.handle_action(param)
        expected_message = f"{_TEST_USERNAME} was deactivated"
        assert_successful_message(connector, expected_message)

    def test_handle_action_when_deactivating_user_sets_error_status_when_user_not_found(
        self, mock_py42_with_user_not_found
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector(
            "reactivate_user", mock_py42_with_user_not_found
        )
        connector.handle_action(param)
        assert_fail(connector)

    def test_handle_action_when_reactivating_user_calls_with_expected_args(
        self, mock_py42_with_legacy_id_user
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector(
            "reactivate_user", mock_py42_with_legacy_id_user
        )
        connector.handle_action(param)
        mock_py42_with_legacy_id_user.users.reactivate.assert_called_once_with(
            _TEST_USER_LEGACY_ID
        )
        assert_success(connector)

    def test_handle_action_when_reactivating_user_and_is_successful_sets_success_message(
        self, mock_py42_with_legacy_id_user
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector(
            "reactivate_user", mock_py42_with_legacy_id_user
        )
        connector.handle_action(param)
        expected_message = f"{_TEST_USERNAME} was reactivated"
        assert_successful_message(connector, expected_message)

    def test_handle_action_when_reactivating_user_sets_error_status_when_user_not_found(
        self, mock_py42_with_user_not_found
    ):
        param = {"username": _TEST_USERNAME}
        connector = create_fake_connector(
            "reactivate_user", mock_py42_with_user_not_found
        )
        connector.handle_action(param)
        assert_fail(connector)
