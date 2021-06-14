import json
from datetime import datetime, timedelta, timezone

import dateutil
from py42.response import Py42Response
from tests.conftest import (
    create_fake_connector,
    attach_client,
    assert_successful_message,
    assert_success,
    assert_fail_message,
    assert_fail,
    assert_successful_params,
    assert_successful_summary,
    MOCK_SECURITY_EVENT_RESPONSE,
)

TEST_MD5 = "b6312dbe4aa4212da94523ccb28c5c16"
TEST_SHA256 = "41966f10cc59ab466444add08974fde4cd37f88d79321d42da8e4c79b51c2149"
TEST_FILENAME = "test-filename"


def _create_mock_py42_with_file_events(mocker, mock_py42_client):
    mock_stream_response = mocker.MagicMock(spec=Py42Response)
    mock_stream_response.iter_content.return_value = [
        b"f",
        b"i",
        b"l",
        b"e",
        b"c",
        b"o",
        b"n",
        b"t",
        b"e",
        b"n",
        b"t",
    ]
    mock_search_response = mocker.MagicMock(spec=Py42Response)
    mock_search_response.data = MOCK_SECURITY_EVENT_RESPONSE
    mock_py42_client.securitydata.stream_file_by_md5.return_value = mock_stream_response
    mock_py42_client.securitydata.stream_file_by_sha256.return_value = (
        mock_stream_response
    )
    mock_py42_client.securitydata.search_file_events.return_value = mock_search_response


def _create_hunt_file_connector(mocker, mock_py42_client):
    client = _create_mock_py42_with_file_events(mocker, mock_py42_client)
    connector = create_fake_connector("hunt_file")
    return attach_client(connector, client)


def _create_run_query_connector(mocker, mock_py42_client):
    client = _create_mock_py42_with_file_events(mocker, mock_py42_client)
    connector = create_fake_connector("run_query")
    return attach_client(connector, client)


def _create_run_advanced_query_connector(mocker, mock_py42_client):
    client = _create_mock_py42_with_file_events(mocker, mock_py42_client)
    connector = create_fake_connector("run_advanced_query")
    return attach_client(connector, client)


class TestCode42FileEventsConnector(object):
    def test_handle_action_when_hunt_file_given_md5_and_filename_outputs_expected_params(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_MD5, "file_name": TEST_FILENAME}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_params(connector, param)

    def test_handle_action_when_hunt_file_given_md5_and_no_filename_outputs_expected_params(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_MD5}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_params(connector, param)

    def test_handle_action_when_hunt_file_given_md5_calls_stream_file_by_md5(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_MD5, "file_name": TEST_FILENAME}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_py42_client.securitydata.stream_file_by_md5.assert_called_once_with(
            TEST_MD5
        )
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_md5_and_filename_calls_create_attachment_with_expected_args(
        self, mocker, mock_py42_client, mock_create_attachment
    ):
        param = {"hash": TEST_MD5, "file_name": TEST_FILENAME}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_create_attachment.assert_called_once_with(
            b"filecontent", 42, file_name=TEST_FILENAME
        )
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_md5_and_no_filename_calls_create_attachment_with_expected_args(
        self, mocker, mock_py42_client, mock_create_attachment
    ):
        param = {"hash": TEST_MD5}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_create_attachment.assert_called_once_with(
            b"filecontent", 42, file_name=TEST_MD5
        )
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_md5_and_filename_sets_success_message(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_MD5, "file_name": TEST_FILENAME}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = (
            f"{TEST_FILENAME} was successfully downloaded and attached to container 42"
        )
        assert_successful_message(connector, message)

    def test_handle_action_when_hunt_file_given_md5_and_no_filename_sets_success_message(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_MD5}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = f"{TEST_MD5} was successfully downloaded and attached to container 42"
        assert_successful_message(connector, message)

    def test_handle_action_when_hunt_file_given_sha256_and_filename_outputs_expected_params(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_SHA256, "file_name": TEST_FILENAME}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_params(connector, param)

    def test_handle_action_when_hunt_file_given_shas256_and_no_filename_outputs_expected_params(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_SHA256}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_params(connector, param)

    def test_handle_action_when_hunt_file_given_sha256_calls_stream_file_by_sha256(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_SHA256, "file_name": TEST_FILENAME}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_py42_client.securitydata.stream_file_by_sha256.assert_called_once_with(
            TEST_SHA256
        )
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_sha256_and_filename_calls_create_attachment_with_expected_args(
        self, mocker, mock_py42_client, mock_create_attachment
    ):
        param = {"hash": TEST_SHA256, "file_name": TEST_FILENAME}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_create_attachment.assert_called_once_with(
            b"filecontent", 42, file_name=TEST_FILENAME
        )
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_sha256_and_no_filename_calls_create_attachment_with_expected_args(
        self, mocker, mock_py42_client, mock_create_attachment
    ):
        param = {"hash": TEST_SHA256}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_create_attachment.assert_called_once_with(
            b"filecontent", 42, file_name=TEST_SHA256
        )
        assert_success(connector)

    def test_handle_action_when_hunt_file_given_sha256_and_filename_sets_success_message(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_SHA256, "file_name": TEST_FILENAME}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = (
            f"{TEST_FILENAME} was successfully downloaded and attached to container 42"
        )
        assert_successful_message(connector, message)

    def test_handle_action_when_hunt_file_given_sha256_and_no_filename_sets_success_message(
        self, mocker, mock_py42_client
    ):
        param = {"hash": TEST_SHA256}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = (
            f"{TEST_SHA256} was successfully downloaded and attached to container 42"
        )
        assert_successful_message(connector, message)

    def test_handle_action_when_hunt_file_given_unsupported_hash_sets_error_message(
        self, mocker, mock_py42_client
    ):
        param = {"hash": "not-a-valid-hash"}
        connector = _create_hunt_file_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = (
            "Code42: Failed execution of action hunt_file: "
            "Unsupported hash format. Hash must be either md5 or sha256"
        )
        assert_fail_message(connector, message)

    def test_handle_action_when_run_query_calls_search_file_events_with_expected_query(
        self, mocker, mock_py42_client
    ):
        eq_param = {
            "username": "test@example.com",
            "file_hash": "6849f4e9b2ee9d45052145d8e25d7b99",
            "file_name": "filename.txt",
            "file_path": "/some/path/to/a/file",
            "file_category": "Spreadsheet",
            "hostname": "MSEDGEWIN10",
            "private_ip": "65.29.153.33",
            "public_ip": "127.0.0.1",
            "exposure_type": "ApplicationRead",
            "process_name": "/Device/HarddiskVolume1/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
            "url": "https://drive.google.com/drive/my-drive",
            "window_title": "My Drive - Google Drive and 1 more page - Profile 1 - Microsoft​ Edge",
        }

        date_param = {
            "start_date": "2031-01-01",
            "end_date": "2031-06-01",
        }

        param = {}
        param.update(eq_param)
        param.update(date_param)

        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)

        actual_query = mock_py42_client.securitydata.search_file_events.call_args[0][0]
        query_json = json.loads(str(actual_query))

        for key in eq_param:
            check_filter(query_json, "IS", eq_param[key])

        check_filter(query_json, "ON_OR_AFTER", "2031-01-01T00:00:00.000Z")
        check_filter(query_json, "ON_OR_BEFORE", "2031-06-01T00:00:00.000Z")

        assert_success(connector)

    def test_handle_action_when_run_query_and_all_params_missing_or_default_sets_error_message(
        self, mocker, mock_py42_client
    ):
        param = {"context": {"debugging_info": "blah"}, "untrusted_only": "false"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        expected_message = (
            "Code42: Must supply a search term when calling action 'run_query'."
        )
        assert_fail_message(connector, expected_message)

    def test_handle_action_when_run_query_and_only_start_date_set_calls_search(
        self, mocker, mock_py42_client
    ):
        param = {"start_date": "2031-01-01"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_success(connector)

    def test_handle_action_when_run_query_and_only_end_date_set_calls_search(
        self, mocker, mock_py42_client
    ):
        param = {"end_date": "2031-01-01"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_success(connector)

    def test_handle_action_when_run_query_and_date_format_invalid_sets_error_status(
        self, mocker, mock_py42_client
    ):
        param = {
            "start_date": "2031-31-12",
            "end_date": "2032-31-01",
        }
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)

        # Fails with error message from date util for an improper month.
        assert_fail(connector)

    def test_handle_action_when_run_query_and_start_date_after_end_date_sets_error_message(
        self, mocker, mock_py42_client
    ):
        param = {
            "start_date": "2031-06-01",
            "end_date": "2031-05-01",
        }
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        expected_message = "Code42: Failed execution of action run_query: Start date cannot be after end date."
        assert_fail_message(connector, expected_message)

    def test_handle_action_when_run_query_adds_response_items_to_data(
        self, mocker, mock_py42_client
    ):
        param = {"username": "barney.frankenberry@chocula.com"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        action_result_data = connector.get_action_results()[0].get_data()
        assert action_result_data[0] == MOCK_SECURITY_EVENT_RESPONSE["fileEvents"][0]
        assert action_result_data[1] == MOCK_SECURITY_EVENT_RESPONSE["fileEvents"][1]
        assert action_result_data[2] == MOCK_SECURITY_EVENT_RESPONSE["fileEvents"][2]

        assert_success(connector)

    def test_handle_action_when_run_query_adds_summary(self, mocker, mock_py42_client):
        param = {"username": "barney.frankenberry@chocula.com"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_summary(
            connector,
            {
                "total_count": MOCK_SECURITY_EVENT_RESPONSE["totalCount"],
                "results_returned_count": len(
                    MOCK_SECURITY_EVENT_RESPONSE["fileEvents"]
                ),
            },
        )

    def test_handle_action_when_run_query_and_no_date_range_provided_defaults_to_last_30_days(
        self, mocker, mock_py42_client
    ):
        param = {"username": "barney.frankenberry@chocula.com"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        actual_query = mock_py42_client.securitydata.search_file_events.call_args[0][0]
        query_json = json.loads(str(actual_query))
        actual_date = dateutil.parser.parse(
            query_json["groups"][1]["filters"][0]["value"]
        )
        expected_date = datetime.now(timezone.utc) - timedelta(days=30)
        assert abs((actual_date - expected_date)).seconds < 1
        assert_success(connector)

    def test_handle_action_when_run_query_given_all_exposure_uses_expected_query(
        self, mocker, mock_py42_client
    ):
        param = {"exposure_type": "All"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        actual_query = mock_py42_client.securitydata.search_file_events.call_args[0][0]
        query_json = json.loads(str(actual_query))
        assert query_json["groups"][0]["filters"][0]["term"] == "exposure"
        assert query_json["groups"][0]["filters"][0]["operator"] == "EXISTS"
        assert query_json["groups"][0]["filters"][0]["value"] is None
        assert_success(connector)

    def test_handle_action_when_run_query_and_only_untrusted_only_set_calls_search(
        self, mocker, mock_py42_client
    ):
        param = {"context": {"debugging_info": "blah"}, "untrusted_only": "true"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        actual_query = mock_py42_client.securitydata.search_file_events.call_args[0][0]
        query_json = json.loads(str(actual_query))
        assert query_json["groups"][0]["filters"][0]["term"] == "trusted"
        assert query_json["groups"][0]["filters"][0]["operator"] == "IS"
        assert query_json["groups"][0]["filters"][0]["value"] == "FALSE"
        assert_success(connector)

    def test_handle_action_when_run_query_given_unsupported_hash_sets_error_message(
        self, mocker, mock_py42_client
    ):
        param = {"file_hash": "not-a-valid-hash"}
        connector = _create_run_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        message = (
            "Code42: Failed execution of action run_query: "
            "Unsupported hash format. Hash must be either md5 or sha256"
        )
        assert_fail_message(connector, message)

    def test_handle_action_when_run_advanced_query_adds_response_items_to_data(
        self, mocker, mock_py42_client
    ):
        param = {"json_query": "arbitrary JSON"}
        connector = _create_run_advanced_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        action_result_data = connector.get_action_results()[0].get_data()
        assert action_result_data[0] == MOCK_SECURITY_EVENT_RESPONSE["fileEvents"][0]
        assert action_result_data[1] == MOCK_SECURITY_EVENT_RESPONSE["fileEvents"][1]
        assert action_result_data[2] == MOCK_SECURITY_EVENT_RESPONSE["fileEvents"][2]

        assert_success(connector)

    def test_handle_action_when_run_advanced_query_calls_search_file_events_with_expected_params(
        self, mocker, mock_py42_client
    ):
        param = {"json_query": "arbitrary JSON"}
        connector = _create_run_advanced_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        mock_py42_client.securitydata.search_file_events.assert_called_once_with(
            "arbitrary JSON"
        )

        assert_success(connector)

    def test_handle_action_when_run_advanced_query_adds_summary(
        self, mocker, mock_py42_client
    ):
        param = {"json_query": "arbitrary JSON"}
        connector = _create_run_advanced_query_connector(mocker, mock_py42_client)
        connector.handle_action(param)
        assert_successful_summary(
            connector,
            {
                "total_count": MOCK_SECURITY_EVENT_RESPONSE["totalCount"],
                "results_returned_count": len(
                    MOCK_SECURITY_EVENT_RESPONSE["fileEvents"]
                ),
            },
        )


def check_filter(query_dict, operator, value):
    groups = query_dict["groups"]
    found = False
    for group in groups:
        if found == True:
            break
        for filter in group["filters"]:
            if filter["operator"] == operator and filter["value"] == value:
                found = True
                break
    assert found
