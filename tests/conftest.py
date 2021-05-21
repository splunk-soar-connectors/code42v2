import json

import py42.sdk
from py42.response import Py42Response
from py42.services.users import UserService
from pytest import fixture
from requests import Response

from code42_connector import Code42Connector


@fixture(autouse=True)
def mock_py42_client(mocker):
    client = mocker.MagicMock(spec=py42.sdk.SDKClient)
    client.users = mocker.MagicMock(spec=UserService)
    mocker.patch("py42.sdk.from_local_account", return_value=client)
    return client


@fixture
def mock_result_adder(mocker):
    return mocker.patch("phantom.base_connector.BaseConnector.add_action_result")


@fixture
def connector():
    connector = Code42Connector()
    return connector


def create_fake_connector(action_identifier):
    def fake_get_action_identifier():
        return action_identifier

    connector = Code42Connector()
    connector.get_action_identifier = fake_get_action_identifier
    return connector


def create_mock_response(mocker, response_data):
    response = mocker.MagicMock(spec=Response)
    response.text = json.dumps(response_data)
    return Py42Response(response)
