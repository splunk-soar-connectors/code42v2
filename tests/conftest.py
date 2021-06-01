import json

import phantom.app
import py42.sdk
from py42.response import Py42Response
from py42.services.users import UserService
from pytest import fixture
from requests import Response

from code42_connector import Code42Connector


TEST_USER_UID = "TEST_USER_UID"


@fixture(autouse=True)
def mock_py42_client(mocker):
    client = mocker.MagicMock(spec=py42.sdk.SDKClient)
    client.users = mocker.MagicMock(spec=UserService)
    mocker.patch("py42.sdk.from_local_account", return_value=client)
    return client


@fixture
def mock_py42_with_user(mocker, mock_py42_client):
    response_data = {"users": [{"userUid": TEST_USER_UID}]}
    mock_py42_client.users.get_by_username.return_value = create_mock_response(
        mocker, response_data
    )
    return mock_py42_client


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


def attach_client(connector, client):
    connector._client = client
    return connector


def create_mock_response(mocker, response_data):
    response = mocker.MagicMock(spec=Response)
    response.text = json.dumps(response_data)
    return Py42Response(response)


def assert_success(connector):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    status = action_results[0].get_status()
    assert status == phantom.app.APP_SUCCESS


def assert_fail(connector):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    status = action_results[0].get_status()
    assert status == phantom.app.APP_ERROR


def assert_fail_message(connector, expected_message):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    msg = action_results[0].get_message()
    status = action_results[0].get_status()
    assert msg == expected_message
    assert status == phantom.app.APP_ERROR


def assert_successful_single_data(connector, expected_data):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    data = action_results[0].get_data()
    status = action_results[0].get_status()
    assert data[0] == expected_data
    assert status == phantom.app.APP_SUCCESS


def assert_successful_summary(connector, expected_summary):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    summary = action_results[0].get_summary()
    status = action_results[0].get_status()
    assert summary == expected_summary
    assert status == phantom.app.APP_SUCCESS


def assert_successful_message(connector, expected_message):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    msg = action_results[0].get_message()
    status = action_results[0].get_status()
    assert msg == expected_message
    assert status == phantom.app.APP_SUCCESS


def attach_client(connector, client):
    connector._client = client
    return connector
