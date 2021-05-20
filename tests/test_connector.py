import json
from logging import getLogger
from unittest import mock

from py42.exceptions import Py42UnauthorizedError
from py42.response import Py42Response
from pytest import fixture
from requests import Response

from code42_connector import Code42Connector
from phantom.action_result import ActionResult
import phantom.app as phantom
import py42.sdk
from py42.services.users import UserService

logger = getLogger(name=__name__)

NULL_VALUE = object()


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


@fixture
def test_connectivity_connector(mock_py42_client):
    connector = create_fake_connector("test_connectivity")
    connector._client = mock_py42_client
    return connector


class TestCode42Connector(object):
    def test_handle_test_connectivity(self, mocker, connector, mock_result_adder):
        param = {}
        mock_result_adder.return_value = ActionResult(dict(param))
        set_status = mocker.patch("phantom.action_result.ActionResult.set_status")

        connector._handle_test_connectivity(param)

        set_status.assert_called_with(phantom.APP_SUCCESS)

    def test_handle_test_connectivity_calls_users_get_current(self, connector, mock_result_adder):
        param = {}
        mock_result_adder.return_value = ActionResult(dict(param))
        connector._handle_test_connectivity(param)
        connector._client.users.get_current.assert_called_with()

    def test_handle_connectivity_sets_error_status_if_sdk_throws_exception(
        self, mocker, mock_py42_client, connector, mock_result_adder
    ):
        param = {}
        mock_result_adder.return_value = ActionResult(dict(param))
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

    def test_handle_action_when_add_departing_employee_calls_add_with_expected_args(
        self, mocker, mock_py42_client, mock_result_adder
    ):
        param = {"username": "test@example.com", "departure_date": "2030-01-01"}
        result = ActionResult(dict(param))
        result.update_summary = mocker.MagicMock()
        mock_result_adder.return_value = result
        http_response = mocker.MagicMock(spec=Response)
        http_response.text = json.dumps({"users": [{"userUid": "TEST_USER_UID"}]})
        mock_py42_client.users.get_by_username.return_value = Py42Response(http_response)
        connector = create_fake_connector("add_departing_employee")
        connector._client = mock_py42_client
        connector.handle_action(param)
        mock_py42_client.detectionlists.departing_employee.add.assert_called_once_with(
            "TEST_USER_UID", departure_date="2030-01-01"
        )

    def test_handle_action_when_remove_departing_employee_calls_remove_with_expected_args(
        self, mocker, mock_py42_client, mock_result_adder
    ):
        param = {"username": "test@example.com"}
        result = ActionResult(dict(param))
        result.update_summary = mocker.MagicMock()
        mock_result_adder.return_value = result
        http_response = mocker.MagicMock(spec=Response)
        http_response.text = json.dumps({"users": [{"userUid": "TEST_USER_UID"}]})
        mock_py42_client.users.get_by_username.return_value = Py42Response(http_response)
        connector = create_fake_connector("remove_departing_employee")
        connector._client = mock_py42_client
        connector.handle_action(param)
        mock_py42_client.detectionlists.departing_employee.remove.assert_called_once_with(
            "TEST_USER_UID"
        )
