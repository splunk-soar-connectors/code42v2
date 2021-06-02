from pytest import fixture

from tests.conftest import (
    assert_success,
    create_fake_connector,
    attach_client,
    create_mock_response,
    assert_successful_single_data,
    assert_successful_message,
    TEST_USER_UID,
    assert_fail_message,
)

_TEST_MATTER_ID = "123456780000"
_TEST_MEMBERSHIP_ID = "0000414491315181992"

_MOCK_LIST_LEGAL_HOLD_MEMBERSHIPS = {
    "legalHoldMemberships": [
        {
            "legalHoldMembershipUid": _TEST_MEMBERSHIP_ID,
            "active": True,
            "creationDate": "2021-03-29T18:05:03.961Z",
            "legalHold": {"legalHoldUid": _TEST_MATTER_ID, "name": "Matter B"},
            "user": {
                "userUid": TEST_USER_UID,
                "username": "test@example.com",
                "email": "test@example.com",
                "userExtRef": "",
            },
        },
        {
            "legalHoldMembershipUid": "000072752321386991",
            "active": True,
            "creationDate": "2020-11-02T12:33:56.258Z",
            "legalHold": {"legalHoldUid": _TEST_MATTER_ID, "name": "Matter B"},
            "user": {
                "userUid": "000042029369432200",
                "username": "test-1603288842@test.com",
                "email": "test-1603288842@test.com",
                "userExtRef": "",
            },
        },
    ]
}


@fixture
def mock_py42_with_legal_hold_memberships(mocker, mock_py42_with_user):
    def gen(*args, **kwargs):
        yield create_mock_response(mocker, _MOCK_LIST_LEGAL_HOLD_MEMBERSHIPS)

    mock_py42_with_user.legalhold.get_all_matter_custodians.side_effect = gen
    return mock_py42_with_user


def _create_add_legalhold_user_connector(client):
    connector = create_fake_connector("add_legalhold_user")
    return attach_client(connector, client)


def _create_remove_legalhold_user_connector(client):
    connector = create_fake_connector("remove_legalhold_user")
    return attach_client(connector, client)


class TestCode42LegalHoldConnector(object):
    def test_handle_action_when_add_legal_hold_user_calls_add_with_expected_args(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "matter_id": _TEST_MATTER_ID}
        connector = _create_add_legalhold_user_connector(mock_py42_with_user)
        connector.handle_action(param)
        mock_py42_with_user.legalhold.add_to_matter.assert_called_once_with(
            "TEST_USER_UID", _TEST_MATTER_ID
        )
        assert_success(connector)

    def test_handle_action_when_add_legal_hold_user_adds_response_to_data(
        self, mocker, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "matter_id": _TEST_MATTER_ID}
        response_data = {
            "legalHoldMembershipUid": "1009118679333039731",
            "active": True,
            "creationDate": "2021-05-28T19:13:24.312Z",
            "legalHold": {
                "legalHoldUid": "1002360211054033697",
                "name": "test-matter-752367781",
            },
            "user": {
                "userUid": "990572034162882387",
                "username": "test2@example.com",
                "email": "test2@example.com",
                "userExtRef": None,
            },
        }
        mock_py42_with_user.legalhold.add_to_matter.return_value = create_mock_response(
            mocker, response_data
        )
        connector = _create_add_legalhold_user_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_single_data(connector, response_data)

    def test_handle_action_when_add_legal_hold_user_and_is_successful_sets_success_message(
        self, mock_py42_with_user
    ):
        param = {"username": "test@example.com", "matter_id": _TEST_MATTER_ID}
        connector = _create_add_legalhold_user_connector(mock_py42_with_user)
        connector.handle_action(param)
        assert_successful_message(
            connector,
            f"test@example.com was added to legal hold matter {_TEST_MATTER_ID}.",
        )

    def test_handle_action_when_remove_legal_hold_user_calls_remove_with_expected_args(
        self, mock_py42_with_legal_hold_memberships
    ):
        param = {"username": "test@example.com", "matter_id": _TEST_MATTER_ID}
        connector = _create_remove_legalhold_user_connector(
            mock_py42_with_legal_hold_memberships
        )
        connector.handle_action(param)
        mock_py42_with_legal_hold_memberships.legalhold.remove_from_matter.assert_called_once_with(
            _TEST_MEMBERSHIP_ID
        )
        assert_success(connector)

    def test_handle_action_when_remove_legal_hold_user_adds_removed_user_id_to_data(
        self, mocker, mock_py42_with_legal_hold_memberships
    ):
        param = {"username": "test@example.com", "matter_id": _TEST_MATTER_ID}
        # This API call does not have response data
        mock_py42_with_legal_hold_memberships.legalhold.remove_from_matter.return_value = create_mock_response(
            mocker, {}
        )
        connector = _create_remove_legalhold_user_connector(
            mock_py42_with_legal_hold_memberships
        )
        connector.handle_action(param)
        assert_successful_single_data(connector, {"userId": TEST_USER_UID})

    def test_handle_action_when_remove_legal_hold_user_and_is_successful_sets_success_message(
        self, mock_py42_with_legal_hold_memberships
    ):
        param = {"username": "test@example.com", "matter_id": _TEST_MATTER_ID}
        connector = _create_remove_legalhold_user_connector(
            mock_py42_with_legal_hold_memberships
        )
        connector.handle_action(param)
        assert_successful_message(
            connector,
            f"test@example.com was removed from legal hold matter {_TEST_MATTER_ID}.",
        )

    def test_handle_action_when_remove_legal_hold_user_and_user_not_member_raises_error(
        self, mocker, mock_py42_with_legal_hold_memberships
    ):
        param = {"username": "nonmember@example.com", "matter_id": _TEST_MATTER_ID}
        mock_py42_with_legal_hold_memberships.users.get_by_username.return_value = create_mock_response(
            mocker, {"users": [{"userUid": "bogus-user-id-not-a-member"}]}
        )
        connector = _create_remove_legalhold_user_connector(
            mock_py42_with_legal_hold_memberships
        )
        connector.handle_action(param)
        assert_fail_message(
            connector,
            f"Code42: User is not an active member of legal hold matter {_TEST_MATTER_ID} for action 'remove_legalhold_user'."
        )
