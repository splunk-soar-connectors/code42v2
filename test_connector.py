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
    return mocker.MagicMock(spec=py42.sdk.SDKClient)


@fixture
def connector(request, py42_client):
    connector = code42_connector.Code42Connector()
    connector._client = py42_client
    yield connector


def test_handle_connectivity(mocker, connector):
    param = {}
    mocker.patch('phantom.base_connector.BaseConnector.add_action_result', return_value=ActionResult(dict(param)))
    set_status = mocker.patch('phantom.action_result.ActionResult.set_status')

    connector._handle_test_connectivity(param)

    set_status.assert_called_with(phantom.APP_SUCCESS)


def test_handle_connectivity_sets_error_status_if_sdk_throws_exception(mocker, connector, py42_client):
    param = {}
    mocker.patch('phantom.base_connector.BaseConnector.add_action_result', return_value=ActionResult(dict(param)))
    py42_client.users.get_current.side_effect = HTTPError(mock.Mock(status=401))
    set_status = mocker.patch('phantom.action_result.ActionResult.set_status')

    connector._handle_test_connectivity(param)

    set_status.assert_called_with(phantom.APP_ERROR, mocker.ANY, mocker.ANY)


def test_handle_action_calls_handle_connectivity(mocker, connector):
    param = {}
    handle_test_connectivity = mocker.patch('code42_connector.Code42Connector._handle_test_connectivity',
                                            return_value=phantom.APP_SUCCESS)
    mocker.patch('phantom.base_connector.BaseConnector.get_action_identifier', return_value='test_connectivity')

    ret = connector.handle_action(param)

    handle_test_connectivity.assert_called_with(param)
    assert ret == phantom.APP_SUCCESS
