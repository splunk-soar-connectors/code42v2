from logging import getLogger
from unittest import mock

from py42.exceptions import Py42UnauthorizedError
from pytest import fixture

import phantom.app as phantom
from code42_connector import Code42Connector
from phantom.action_result import ActionResult
from .conftest import create_fake_connector

@fixture
def test_connectivity_connector(mock_py42_client):
    connector = create_fake_connector("test_connectivity")
    connector._client = mock_py42_client
    return connector


class TestCode42Connector(object):
    def test_handle_test_connectivity(self, mocker, test_connectivity_connector):
        result = test_connectivity_connector.handle_action({})
        status = result.data["status"]
        assert status == phantom.APP_SUCCESS

    def test_handle_test_connectivity_calls_users_get_current(self, connector):
        param = {}
        connector._handle_test_connectivity(param)
        connector._client.users.get_current.assert_called_once_with()

    def test_handle_connectivity_sets_error_status_if_sdk_throws_exception(
        self, mocker, mock_py42_client, connector
    ):
        param = {}
        mock_py42_client.users.get_current.side_effect = Py42UnauthorizedError(mock.Mock(status=401))
        set_status = mocker.patch("phantom.action_result.ActionResult.set_status")

        connector._handle_test_connectivity(param)

        set_status.assert_called_with(phantom.APP_ERROR, mocker.ANY)

    def test_handle_action_calls_handle_connectivity(
        self, mocker, test_connectivity_connector, mock_result_adder
    ):
        def fake_set_status(self, status, message=None):
            return status == phantom.APP_SUCCESS

        mocker.patch("phantom.action_result.ActionResult.set_status", new=fake_set_status)
        param = {}
        mock_result_adder.return_value = ActionResult(dict(param))

        ret = test_connectivity_connector.handle_action(param)

        assert ret == phantom.APP_SUCCESS

    def test_initialize_reads_credentials_from_config(self, mocker):
        connector = Code42Connector()
        config = {
            "cloud_instance": "http://cloud.code42.com",
            "username": "user.name",
            "password": "password123!"
        }
        mocker.patch("phantom.base_connector.BaseConnector.get_config", return_value=config)

        connector.initialize()

        assert connector._cloud_instance == config["cloud_instance"]
        assert connector._username == config["username"]
        assert connector._password == config["password"]
