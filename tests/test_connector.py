from logging import getLogger
from unittest import mock

from pytest import fixture, fail

import code42_connector
from phantom.action_result import ActionResult
import phantom.app as phantom
import py42.sdk
from requests import HTTPError


logger = getLogger(name=__name__)


NULL_VALUE = object()


@fixture
def py42_sdk(mocker):
    return mocker.MagicMock(spec=py42.sdk)


@fixture
def py42_client(mocker):
    client = mocker.MagicMock(spec=py42.sdk.SDKClient)
    client.users = mocker.MagicMock(spec=py42.services.users.UserService)
    return client


@fixture
def connector(request, py42_client):
    connector = code42_connector.Code42Connector()
    connector._client = py42_client
    return connector


@fixture
def clean_connector():
    connector = code42_connector.Code42Connector()
    connector._client = py42.sdk.from_local_account('https://console.us.code42.com', 'peter.briggs+partner@code42.com', 'admin')
    return connector


class TestCode42Connector(object):
    def test_handle_connectivity(self, mocker, connector):
        param = {}
        mocker.patch('phantom.base_connector.BaseConnector.add_action_result', return_value=ActionResult(dict(param)))
        set_status = mocker.patch('phantom.action_result.ActionResult.set_status')

        connector._handle_test_connectivity(param)

        set_status.assert_called_with(phantom.APP_SUCCESS)

    def test_handle_test_connectivity_calls_users_get_current(self, mocker, connector):
        param = {}
        mocker.patch('phantom.base_connector.BaseConnector.add_action_result', return_value=ActionResult(dict(param)))
        
        connector._handle_test_connectivity(param)

        connector._client.users.get_current.assert_called_with()

    def test_handle_connectivity_sets_error_status_if_sdk_throws_exception(self, mocker, connector, py42_client):
        param = {}
        mocker.patch('phantom.base_connector.BaseConnector.add_action_result', return_value=ActionResult(dict(param)))
        py42_client.users.get_current.side_effect = HTTPError(mock.Mock(status=401))
        set_status = mocker.patch('phantom.action_result.ActionResult.set_status')

        connector._handle_test_connectivity(param)

        set_status.assert_called_with(phantom.APP_ERROR, mocker.ANY)

    def test_handle_action_calls_handle_connectivity(self, mocker, connector):
        param = {}
        handle_test_connectivity = mocker.patch('code42_connector.Code42Connector._handle_test_connectivity',
                                                return_value=phantom.APP_SUCCESS)
        mocker.patch('phantom.base_connector.BaseConnector.get_action_identifier', return_value='test_connectivity')

        ret = connector.handle_action(param)

        handle_test_connectivity.assert_called_with(param)
        assert ret == phantom.APP_SUCCESS

    def test_initialize_reads_creds_from_config_and_creates_py42_client_from_local_account(self, mocker, py42_client):
        connector = code42_connector.Code42Connector()
        config = {'cloud_instance': 'http://cloud.code42.com', 'username': 'user.name', 'password': 'password123!'}
        mocker.patch('phantom.base_connector.BaseConnector.get_config', return_value=config)
        from_local_account = mocker.patch('py42.sdk.from_local_account')

        connector.initialize()

        from_local_account.assert_called_with(config['cloud_instance'], config['username'], config['password'])
