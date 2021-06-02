from requests import Response

from tests.conftest import (
    create_fake_connector,
    attach_client,
    assert_successful_message,
    assert_success,
    assert_fail_message,
    assert_successful_params
)

TEST_MD5 = "b6312dbe4aa4212da94523ccb28c5c16"
TEST_SHA256 = "41966f10cc59ab466444add08974fde4cd37f88d79321d42da8e4c79b51c2149"
TEST_FILENAME = "test-filename"

def _create_mock_py42_with_file_events(mocker, mock_py42_client):
    mock_stream_response = mocker.MagicMock(spec=Response)
    mock_stream_response.iter_content.return_value = [b"f", b"i", b"l", b"e", b"c", b"o", b"n", b"t", b"e", b"n", b"t" ]
    mock_py42_client.securitydata.stream_file_by_md5.return_value = mock_stream_response
    mock_py42_client.securitydata.stream_file_by_sha256.return_value = mock_stream_response

def _create_hunt_file_connector(mocker, mock_py42_client):
    client = _create_mock_py42_with_file_events(mocker, mock_py42_client)
    connector = create_fake_connector("hunt_file")
    return attach_client(connector, client)


class TestCode42FileEventsConnector(object):
    def test_handle_action_when_hunt_file_given_md5_and_filename_outputs_expected_params(self, mocker, mock_py42_client):
        param = {"hash": TEST_MD5, "filename": TEST_FILENAME }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_params(connector, param)

    def test_handle_action_when_hunt_file_given_md5_and_no_filename_outputs_expected_params(self, mocker, mock_py42_client):
        param = {"hash": TEST_MD5 }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_params(connector, param)

    def test_handle_action_when_hunt_file_given_md5_calls_stream_file_by_md5(self, mocker, mock_py42_client):
        param = {"hash": TEST_MD5, "filename": TEST_FILENAME }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_py42_client.securitydata.stream_file_by_md5.assert_called_once_with(TEST_MD5)
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_md5_and_filename_calls_create_attachment_with_expected_args(self, mocker, mock_py42_client, mock_create_attachment):
        param = {"hash": TEST_MD5, "filename": TEST_FILENAME }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_create_attachment.assert_called_once_with(b"filecontent", 42, file_name=TEST_FILENAME)
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_md5_and_no_filename_calls_create_attachment_with_expected_args(self, mocker, mock_py42_client, mock_create_attachment):
        param = {"hash": TEST_MD5 }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_create_attachment.assert_called_once_with(b"filecontent", 42, file_name=TEST_MD5)
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_md5_and_filename_sets_success_message(self, mocker, mock_py42_client):
        param = {"hash": TEST_MD5, "filename": TEST_FILENAME }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = f"{TEST_FILENAME} was successfully downloaded and attached to container 42"
        assert_successful_message(connector, message)

    def test_handle_action_when_hunt_file_given_md5_and_no_filename_sets_success_message(self, mocker, mock_py42_client):
        param = {"hash": TEST_MD5 }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = f"{TEST_MD5} was successfully downloaded and attached to container 42"
        assert_successful_message(connector, message)

    def test_handle_action_when_hunt_file_given_sha256_and_filename_outputs_expected_params(self, mocker, mock_py42_client):
        param = {"hash": TEST_SHA256, "filename": TEST_FILENAME }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_params(connector, param)

    def test_handle_action_when_hunt_file_given_shas256_and_no_filename_outputs_expected_params(self, mocker, mock_py42_client):
        param = {"hash": TEST_SHA256 }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_params(connector, param)

    def test_handle_action_when_hunt_file_given_sha256_calls_stream_file_by_sha256(self, mocker, mock_py42_client):
        param = {"hash": TEST_SHA256, "filename": TEST_FILENAME }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_py42_client.securitydata.stream_file_by_sha256.assert_called_once_with(TEST_SHA256)
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_sha256_and_filename_calls_create_attachment_with_expected_args(self, mocker, mock_py42_client, mock_create_attachment):
        param = {"hash": TEST_SHA256, "filename": TEST_FILENAME }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_create_attachment.assert_called_once_with(b"filecontent", 42, file_name=TEST_FILENAME)
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_sha256_and_no_filename_calls_create_attachment_with_expected_args(self, mocker, mock_py42_client, mock_create_attachment):
        param = {"hash": TEST_SHA256 }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_create_attachment.assert_called_once_with(b"filecontent", 42, file_name=TEST_SHA256)
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_sha256_and_filename_sets_success_message(self, mocker, mock_py42_client):
        param = {"hash": TEST_SHA256, "filename": TEST_FILENAME }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = f"{TEST_FILENAME} was successfully downloaded and attached to container 42"
        assert_successful_message(connector, message)

    def test_handle_action_when_hunt_file_given_sha256_and_no_filename_sets_success_message(self, mocker, mock_py42_client):
        param = {"hash": TEST_SHA256 }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = f"{TEST_SHA256} was successfully downloaded and attached to container 42"
        assert_successful_message(connector, message)

    def test_handle_action_when_hunt_file_given_unsupported_hash_sets_error_message(self, mocker, mock_py42_client):
        param = {"hash": "not-a-valid-hash" }
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = "Code42: Failed execution of action hunt_file: Unsupported hash format. Hash must be either md5 or sha256"
        assert_fail_message(connector, message)
