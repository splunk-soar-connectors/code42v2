from unittest import mock

from py42.exceptions import Py42UnauthorizedError
from pytest import fixture

from code42_connector import Code42Connector
from .conftest import assert_fail, create_fake_connector, assert_success

@fixture
def test_connectivity_connector(mock_py42_client):
    connector = create_fake_connector("test_connectivity")
    connector._client = mock_py42_client
    return connector


class TestCode42Connector(object):
    def test_handle_test_connectivity_calls_users_get_current(self, test_connectivity_connector):
        test_connectivity_connector.handle_action({})
        test_connectivity_connector._client.users.get_current.assert_called_once_with()
        assert_success(test_connectivity_connector)

    def test_handle_connectivity_sets_error_status_if_sdk_throws_exception(
        self, test_connectivity_connector
    ):
        test_connectivity_connector._client.users.get_current.side_effect = Py42UnauthorizedError(mock.Mock(status=401))
        test_connectivity_connector.handle_action({})
        assert_fail(test_connectivity_connector)

    def test_initialize_reads_credentials_from_config(self, mocker):
        connector = Code42Connector()
        config = {
            "cloud_instance": "http://cloud.code42.com",
            "username": "user.name",
            "password": "password123!"
        }
        connector.get_config = mocker.MagicMock(return_value=config)
        connector.initialize()

        assert connector._cloud_instance == config["cloud_instance"]
        assert connector._username == config["username"]
        assert connector._password == config["password"]
