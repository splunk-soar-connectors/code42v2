from logging import getLogger
from unittest import mock

from pytest import fixture, fail

# from code42_connector import Code42Connector
import code42_connector
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
import phantom.app as phantom
import py42.sdk


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
    state = {}
    yield connector


def test_handle_connectivity(mocker, connector):
    param = {}
    mocker.patch('phantom.base_connector.BaseConnector.add_action_result', return_value=ActionResult(dict(param)))
    set_status = mocker.patch('phantom.action_result.ActionResult.set_status')
    mocker.patch('code42_connector.Code42Connector._create_client')

    connector._handle_test_connectivity(param)

    set_status.assert_called_with(phantom.APP_SUCCESS)
