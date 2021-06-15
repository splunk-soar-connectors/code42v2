import json
from datetime import datetime, timedelta, timezone

import py42.sdk
import dateutil.parser
from pytest import fixture
from tests.conftest import (
    assert_artifacts_added,
    assert_container_added,
    assert_state_saved,
    assert_success,
    attach_client,
    create_fake_connector,
    create_mock_response,
    MOCK_ALERT_DETAIL_RESPONSE,
    MOCK_SEARCH_ALERTS_LIST_RESPONSE,
    MOCK_SECURITY_EVENT_RESPONSE,
)

EXPECTED_ARTIFACTS = expected = [
    {
        "cef": {
            "deviceExternalId": "935873453596901068",
            "dvchost": "host.docker.internal",
            "end": "1590669999838",
            "eventName": "READ_BY_APP",
            "externalId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "fileCreateTime": "1590669814902",
            "fileHash": "9cea266b4e07974df1982ae3b9de92ce",
            "fileModificationTime": "1590669815105",
            "filePath": "C:/Users/QA/Downloads/",
            "fileType": "IMAGE",
            "fname": "company_secrets.txt",
            "fsize": 265122,
            "reason": "ApplicationRead",
            "request": "example.com",
            "requestClientApplication": "Jira",
            "rt": "1590670310040",
            "shost": "HOSTNAME",
            "signatureId": "C42203",
            "sourceServiceName": "Endpoint",
            "spriv": "QA",
            "sproc": "chrome.exe",
            "src": "255.255.255.255",
            "suid": "912098363086307495",
            "suser": "test@example.com",
        },
        "container_id": "CONTAINER_ID",
        "data": {
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "deviceUid": "935873453596901068",
            "deviceUserName": "test@example.com",
            "domainName": "host.docker.internal",
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "eventType": "READ_BY_APP",
            "exposure": ["ApplicationRead"],
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileName": "company_secrets.txt",
            "fileOwner": "Test",
            "filePath": "C:/Users/QA/Downloads/",
            "fileSize": 265122,
            "fileType": "FILE",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "operatingSystemUser": "IEUser",
            "osHostName": "HOSTNAME",
            "outsideActiveHours": False,
            "privateIpAddresses": ["255.255.255.255", "127.0.0.1"],
            "processName": "chrome.exe",
            "processOwner": "QA",
            "publicIpAddress": "255.255.255.255",
            "remoteActivity": "UNKNOWN",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "source": "Endpoint",
            "tabUrl": "example.com",
            "trusted": False,
            "userUid": "912098363086307495",
            "windowTitle": ["Jira"],
        },
        "label": "Alerting",
        "name": "Code42 File Event Artifact",
        "source_data_identifier": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "start_time": "2020-05-28T12:46:39.838Z",
    },
    {
        "cef": {
            "deviceExternalId": "935873453596901068",
            "dvchost": "host.docker.internal",
            "end": "1590669999838",
            "eventName": "READ_BY_APP",
            "externalId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "fileCreateTime": "1590669814902",
            "fileHash": "9cea266b4e07974df1982ae3b9de92ce",
            "fileModificationTime": "1590669815105",
            "filePath": "C:/Users/QA/Downloads/",
            "fileType": "IMAGE",
            "fname": "company_secrets.txt",
            "fsize": 265122,
            "reason": "ApplicationRead",
            "request": "example.com",
            "requestClientApplication": "Jira",
            "rt": "1590670310040",
            "shost": "HOSTNAME",
            "signatureId": "C42203",
            "sourceServiceName": "Endpoint",
            "spriv": "QA",
            "sproc": "chrome.exe",
            "src": "255.255.255.255",
            "suid": "912098363086307495",
            "suser": "test@example.com",
        },
        "container_id": "CONTAINER_ID",
        "data": {
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "deviceUid": "935873453596901068",
            "deviceUserName": "test@example.com",
            "domainName": "host.docker.internal",
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "eventType": "READ_BY_APP",
            "exposure": ["ApplicationRead"],
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileName": "company_secrets.txt",
            "fileOwner": "Test",
            "filePath": "C:/Users/QA/Downloads/",
            "fileSize": 265122,
            "fileType": "FILE",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "operatingSystemUser": "IEUser",
            "osHostName": "HOSTNAME",
            "outsideActiveHours": False,
            "privateIpAddresses": ["255.255.255.255", "127.0.0.1"],
            "processName": "chrome.exe",
            "processOwner": "QA",
            "publicIpAddress": "255.255.255.255",
            "remoteActivity": "UNKNOWN",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "source": "Endpoint",
            "tabUrl": "example.com",
            "trusted": False,
            "userUid": "912098363086307495",
            "windowTitle": ["Jira"],
        },
        "label": "Alerting",
        "name": "Code42 File Event Artifact",
        "source_data_identifier": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "start_time": "2020-05-28T12:46:39.838Z",
    },
    {
        "cef": {
            "deviceExternalId": "935873453596901068",
            "dvchost": "host.docker.internal",
            "end": "1590669999838",
            "eventName": "READ_BY_APP",
            "externalId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "fileCreateTime": "1590669814902",
            "fileHash": "9cea266b4e07974df1982ae3b9de92ce",
            "fileModificationTime": "1590669815105",
            "filePath": "C:/Users/QA/Downloads/",
            "fileType": "IMAGE",
            "fname": "company_secrets.txt",
            "fsize": 265122,
            "reason": "ApplicationRead",
            "request": "example.com",
            "requestClientApplication": "Jira",
            "rt": "1590670310040",
            "shost": "HOSTNAME",
            "signatureId": "C42203",
            "sourceServiceName": "Endpoint",
            "spriv": "QA",
            "sproc": "chrome.exe",
            "src": "255.255.255.255",
            "suid": "912098363086307495",
            "suser": "test@example.com",
        },
        "container_id": "CONTAINER_ID",
        "data": {
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "deviceUid": "935873453596901068",
            "deviceUserName": "test@example.com",
            "domainName": "host.docker.internal",
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "eventType": "READ_BY_APP",
            "exposure": ["ApplicationRead"],
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileName": "company_secrets.txt",
            "fileOwner": "Test",
            "filePath": "C:/Users/QA/Downloads/",
            "fileSize": 265122,
            "fileType": "FILE",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "operatingSystemUser": "IEUser",
            "osHostName": "HOSTNAME",
            "outsideActiveHours": False,
            "privateIpAddresses": ["255.255.255.255", "127.0.0.1"],
            "processName": "chrome.exe",
            "processOwner": "QA",
            "publicIpAddress": "255.255.255.255",
            "remoteActivity": "UNKNOWN",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "source": "Endpoint",
            "tabUrl": "example.com",
            "trusted": False,
            "userUid": "912098363086307495",
            "windowTitle": ["Jira"],
        },
        "label": "Alerting",
        "name": "Code42 File Event Artifact",
        "source_data_identifier": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "start_time": "2020-05-28T12:46:39.838Z",
    },
    {
        "cef": {
            "deviceExternalId": "935873453596901068",
            "dvchost": "host.docker.internal",
            "end": "1590669999838",
            "eventName": "READ_BY_APP",
            "externalId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "fileCreateTime": "1590669814902",
            "fileHash": "9cea266b4e07974df1982ae3b9de92ce",
            "fileModificationTime": "1590669815105",
            "filePath": "C:/Users/QA/Downloads/",
            "fileType": "IMAGE",
            "fname": "company_secrets.txt",
            "fsize": 265122,
            "reason": "ApplicationRead",
            "request": "example.com",
            "requestClientApplication": "Jira",
            "rt": "1590670310040",
            "shost": "HOSTNAME",
            "signatureId": "C42203",
            "sourceServiceName": "Endpoint",
            "spriv": "QA",
            "sproc": "chrome.exe",
            "src": "255.255.255.255",
            "suid": "912098363086307495",
            "suser": "test@example.com",
        },
        "container_id": "CONTAINER_ID",
        "data": {
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "deviceUid": "935873453596901068",
            "deviceUserName": "test@example.com",
            "domainName": "host.docker.internal",
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "eventType": "READ_BY_APP",
            "exposure": ["ApplicationRead"],
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileName": "company_secrets.txt",
            "fileOwner": "Test",
            "filePath": "C:/Users/QA/Downloads/",
            "fileSize": 265122,
            "fileType": "FILE",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "operatingSystemUser": "IEUser",
            "osHostName": "HOSTNAME",
            "outsideActiveHours": False,
            "privateIpAddresses": ["255.255.255.255", "127.0.0.1"],
            "processName": "chrome.exe",
            "processOwner": "QA",
            "publicIpAddress": "255.255.255.255",
            "remoteActivity": "UNKNOWN",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "source": "Endpoint",
            "tabUrl": "example.com",
            "trusted": False,
            "userUid": "912098363086307495",
            "windowTitle": ["Jira"],
        },
        "label": "Alerting",
        "name": "Code42 File Event Artifact",
        "source_data_identifier": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "start_time": "2020-05-28T12:46:39.838Z",
    },
    {
        "cef": {
            "deviceExternalId": "935873453596901068",
            "dvchost": "host.docker.internal",
            "end": "1590669999838",
            "eventName": "READ_BY_APP",
            "externalId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "fileCreateTime": "1590669814902",
            "fileHash": "9cea266b4e07974df1982ae3b9de92ce",
            "fileModificationTime": "1590669815105",
            "filePath": "C:/Users/QA/Downloads/",
            "fileType": "IMAGE",
            "fname": "company_secrets.txt",
            "fsize": 265122,
            "reason": "ApplicationRead",
            "request": "example.com",
            "requestClientApplication": "Jira",
            "rt": "1590670310040",
            "shost": "HOSTNAME",
            "signatureId": "C42203",
            "sourceServiceName": "Endpoint",
            "spriv": "QA",
            "sproc": "chrome.exe",
            "src": "255.255.255.255",
            "suid": "912098363086307495",
            "suser": "test@example.com",
        },
        "container_id": "CONTAINER_ID",
        "data": {
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "deviceUid": "935873453596901068",
            "deviceUserName": "test@example.com",
            "domainName": "host.docker.internal",
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "eventType": "READ_BY_APP",
            "exposure": ["ApplicationRead"],
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileName": "company_secrets.txt",
            "fileOwner": "Test",
            "filePath": "C:/Users/QA/Downloads/",
            "fileSize": 265122,
            "fileType": "FILE",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "operatingSystemUser": "IEUser",
            "osHostName": "HOSTNAME",
            "outsideActiveHours": False,
            "privateIpAddresses": ["255.255.255.255", "127.0.0.1"],
            "processName": "chrome.exe",
            "processOwner": "QA",
            "publicIpAddress": "255.255.255.255",
            "remoteActivity": "UNKNOWN",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "source": "Endpoint",
            "tabUrl": "example.com",
            "trusted": False,
            "userUid": "912098363086307495",
            "windowTitle": ["Jira"],
        },
        "label": "Alerting",
        "name": "Code42 File Event Artifact",
        "source_data_identifier": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "start_time": "2020-05-28T12:46:39.838Z",
    },
    {
        "cef": {
            "deviceExternalId": "935873453596901068",
            "dvchost": "host.docker.internal",
            "end": "1590669999838",
            "eventName": "READ_BY_APP",
            "externalId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "fileCreateTime": "1590669814902",
            "fileHash": "9cea266b4e07974df1982ae3b9de92ce",
            "fileModificationTime": "1590669815105",
            "filePath": "C:/Users/QA/Downloads/",
            "fileType": "IMAGE",
            "fname": "company_secrets.txt",
            "fsize": 265122,
            "reason": "ApplicationRead",
            "request": "example.com",
            "requestClientApplication": "Jira",
            "rt": "1590670310040",
            "shost": "HOSTNAME",
            "signatureId": "C42203",
            "sourceServiceName": "Endpoint",
            "spriv": "QA",
            "sproc": "chrome.exe",
            "src": "255.255.255.255",
            "suid": "912098363086307495",
            "suser": "test@example.com",
        },
        "container_id": "CONTAINER_ID",
        "data": {
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "deviceUid": "935873453596901068",
            "deviceUserName": "test@example.com",
            "domainName": "host.docker.internal",
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "eventType": "READ_BY_APP",
            "exposure": ["ApplicationRead"],
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileName": "company_secrets.txt",
            "fileOwner": "Test",
            "filePath": "C:/Users/QA/Downloads/",
            "fileSize": 265122,
            "fileType": "FILE",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "operatingSystemUser": "IEUser",
            "osHostName": "HOSTNAME",
            "outsideActiveHours": False,
            "privateIpAddresses": ["255.255.255.255", "127.0.0.1"],
            "processName": "chrome.exe",
            "processOwner": "QA",
            "publicIpAddress": "255.255.255.255",
            "remoteActivity": "UNKNOWN",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "source": "Endpoint",
            "tabUrl": "example.com",
            "trusted": False,
            "userUid": "912098363086307495",
            "windowTitle": ["Jira"],
        },
        "label": "Alerting",
        "name": "Code42 File Event Artifact",
        "source_data_identifier": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "start_time": "2020-05-28T12:46:39.838Z",
    },
]


def _create_on_poll_connector(client):
    connector = create_fake_connector("on_poll")
    connector._config["ingest"] = {"container_label": "TEST_C_LABEL"}
    return attach_client(connector, client)


def _create_expected_container(expected_alert):
    return {
        "data": expected_alert,
        "description": expected_alert["description"],
        "label": "TEST_C_LABEL",
        "name": expected_alert["name"],
        "severity": expected_alert["severity"],
        "source_data_identifier": expected_alert["id"],
    }


@fixture
def mock_py42_for_alert_polling(mocker, mock_py42_client):
    mock_py42_client.alerts.search.return_value = create_mock_response(
        mocker, MOCK_SEARCH_ALERTS_LIST_RESPONSE
    )
    mock_py42_client.alerts.get_details.return_value = create_mock_response(
        mocker, MOCK_ALERT_DETAIL_RESPONSE
    )
    smaller_file_event_response = dict(MOCK_SECURITY_EVENT_RESPONSE)
    smaller_file_event_response["totalCount"] = 1
    smaller_file_event_response["fileEvents"] = [
        MOCK_SECURITY_EVENT_RESPONSE["fileEvents"][0]
    ]
    mock_py42_client.securitydata.search_file_events.return_value = create_mock_response(
        mocker, smaller_file_event_response
    )
    return mock_py42_client


class TestCode42OnPollConnector(object):
    def test_on_poll_adds_container_per_alert(self, mock_py42_for_alert_polling):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector.handle_action({})
        expected_alert = MOCK_ALERT_DETAIL_RESPONSE["alerts"][0]
        expected_container = _create_expected_container(expected_alert)
        assert_container_added(connector, [expected_container, expected_container])

    def test_on_poll_when_is_poll_now_honors_container_count_param(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._is_poll_now = True
        connector.handle_action({"container_count": 1})
        expected_alert = MOCK_ALERT_DETAIL_RESPONSE["alerts"][0]
        expected_container = _create_expected_container(expected_alert)
        assert_container_added(connector, [expected_container])

    def test_on_poll_adds_artifacts_per_file_event_per_alert(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector.handle_action({})
        assert_artifacts_added(connector, EXPECTED_ARTIFACTS)

    def test_on_poll_when_is_poll_now_honors_artifact_count_param(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._is_poll_now = True
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        assert_artifacts_added(connector, [EXPECTED_ARTIFACTS[0]])

    def test_on_poll_when_is_poll_now_uses_start_date_of_30_days_back(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._is_poll_now = True
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        actual_date_str = json.loads(
            str(mock_py42_for_alert_polling.alerts.search.call_args[0][0])
        )["groups"][0]["filters"][0]["value"]
        actual_date = dateutil.parser.parse(actual_date_str)
        expected_date = datetime.now(timezone.utc) - timedelta(days=30)
        assert abs((actual_date - expected_date)).seconds < 1
        assert_success(connector)

    def test_on_poll_when_is_not_poll_now_uses_previously_stored_timestamp(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._is_poll_now = False
        test_timestamp = 1623293946
        connector._state = {"last_time": test_timestamp}
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        actual_date_str = json.loads(
            str(mock_py42_for_alert_polling.alerts.search.call_args[0][0])
        )["groups"][0]["filters"][0]["value"]
        actual_date = dateutil.parser.parse(actual_date_str)
        expected_date = datetime.utcfromtimestamp(0) + timedelta(seconds=test_timestamp)
        expected_date = expected_date.replace(tzinfo=actual_date.tzinfo)
        assert abs((actual_date - expected_date)).seconds < 1
        assert_success(connector)

    def test_on_poll_when_is_not_poll_now_uses_and_no_previously_stored_timestamp_uses_30_days_back(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._is_poll_now = False
        connector._state = {"last_time": None}
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        actual_date_str = json.loads(
            str(mock_py42_for_alert_polling.alerts.search.call_args[0][0])
        )["groups"][0]["filters"][0]["value"]
        actual_date = dateutil.parser.parse(actual_date_str)
        expected_date = datetime.now(timezone.utc) - timedelta(days=30)
        assert abs((actual_date - expected_date)).seconds < 1
        assert_success(connector)

    def test_on_poll_saves_state_with_last_alert_created_at(
        self, mocker, mock_py42_for_alert_polling
    ):
        test_last_timestamp = "TEST TIMESTAMP"

        def get_alert_details(alert_id, *args, **kwargs):
            if alert_id != MOCK_SEARCH_ALERTS_LIST_RESPONSE["alerts"][-1]["id"]:
                return create_mock_response(mocker, MOCK_ALERT_DETAIL_RESPONSE)

            response_dict = {"alerts": [{"id": 0, "createdAt": test_last_timestamp}]}
            return create_mock_response(mocker, response_dict)

        mock_py42_for_alert_polling.alerts.get_details.side_effect = get_alert_details
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._is_poll_now = False
        connector._state = {"last_time": None}
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        expected_state = {"last_time": test_last_timestamp}
        assert_state_saved(connector, expected_state)

    def test_on_poll_when_is_poll_now_does_not_save_state(
        self, mocker, mock_py42_for_alert_polling
    ):
        test_last_timestamp = "TEST TIMESTAMP"

        def get_alert_details(alert_id, *args, **kwargs):
            if alert_id != MOCK_SEARCH_ALERTS_LIST_RESPONSE["alerts"][-1]["id"]:
                return create_mock_response(mocker, MOCK_ALERT_DETAIL_RESPONSE)

            response_dict = {"alerts": [{"id": 0, "createdAt": test_last_timestamp}]}
            return create_mock_response(mocker, response_dict)

        mock_py42_for_alert_polling.alerts.get_details.side_effect = get_alert_details
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._is_poll_now = True
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        assert not connector._state
        assert_success(connector)

    def test_on_poll_makes_file_event_query_with_expected_number_of_filter_groups(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        call_args = (
            mock_py42_for_alert_polling.securitydata.search_file_events.call_args
        )
        actual = json.loads(str(call_args[0][0]))
        assert actual["groupClause"] == "AND"
        assert len(actual["groups"]) == 4
        assert actual["groups"][0]["filterClause"] == "AND"
        assert_success(connector)

    def test_on_poll_when_no_exposure_data_in_alert_searches_all_unsupported_exposures(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        call_args = (
            mock_py42_for_alert_polling.securitydata.search_file_events.call_args_list
        )

        # Corresponds to unsupported exposure type observation
        actual = json.loads(str(call_args[5][0][0]))

        assert len(actual["groups"][3]["filters"]) == 3
        assert actual["groups"][3]["filters"][0]["operator"] == "IS_NOT"
        assert actual["groups"][3]["filters"][0]["term"] == "exposure"
        assert actual["groups"][3]["filters"][0]["value"] == "IsPublic"
        assert actual["groups"][3]["filters"][1]["operator"] == "IS_NOT"
        assert actual["groups"][3]["filters"][1]["term"] == "exposure"
        assert actual["groups"][3]["filters"][1]["value"] == "OutsideTrustedDomains"
        assert actual["groups"][3]["filters"][2]["operator"] == "IS_NOT"
        assert actual["groups"][3]["filters"][2]["term"] == "exposure"
        assert actual["groups"][3]["filters"][2]["value"] == "SharedViaLink"
        assert_success(connector)

    def test_on_poll_when_is_exfiltration_searches_for_event_type(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        call_args = (
            mock_py42_for_alert_polling.securitydata.search_file_events.call_args_list
        )

        # Corresponds to unsupported exposure type observation
        actual = json.loads(str(call_args[0][0][0]))

        assert len(actual["groups"][3]["filters"]) == 3
        assert actual["groups"][3]["filters"][0]["operator"] == "IS"
        assert actual["groups"][3]["filters"][0]["term"] == "eventType"
        assert actual["groups"][3]["filters"][0]["value"] == "CREATED"
        assert_success(connector)

    def test_on_poll_when_is_outside_trusted_domains_searches_for_outside_trusted_domains_exposure(
        self, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        call_args = (
            mock_py42_for_alert_polling.securitydata.search_file_events.call_args_list
        )

        # Corresponds to outside-trusted-domains type observation
        actual = json.loads(str(call_args[4][0][0]))

        assert len(actual["groups"][3]["filters"]) == 1
        assert actual["groups"][3]["filters"][0]["operator"] == "IS"
        assert actual["groups"][3]["filters"][0]["term"] == "exposure"
        assert actual["groups"][3]["filters"][0]["value"] == "OutsideTrustedDomains"
        assert_success(connector)

    def test_on_poll_makes_expected_file_event_actor_query(
        self, mocker, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        call_args = (
            mock_py42_for_alert_polling.securitydata.search_file_events.call_args_list
        )

        # Corresponds to FedCloudSharePermissions observation type
        actual = json.loads(str(call_args[1][0][0]))

        assert actual["groups"][0]["filters"][0]["operator"] == "IS"
        assert actual["groups"][0]["filters"][0]["term"] == "actor"
        assert actual["groups"][0]["filters"][0]["value"] == "cool.guy@code42.com"
        assert_success(connector)

    def test_on_poll_makes_expected_file_event_device_user_name_query(
        self, mocker, mock_py42_for_alert_polling
    ):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        param = {"container_count": 1, "artifact_count": 1}
        connector.handle_action(param)
        call_args = (
            mock_py42_for_alert_polling.securitydata.search_file_events.call_args_list
        )

        # Corresponds to FedEndpointExfiltration observation type
        actual = json.loads(str(call_args[0][0][0]))

        assert len(actual["groups"][0]["filters"]) == 1
        assert actual["groups"][0]["filters"][0]["operator"] == "IS"
        assert actual["groups"][0]["filters"][0]["term"] == "deviceUserName"
        assert actual["groups"][0]["filters"][0]["value"] == "cool.guy@code42.com"
        assert_success(connector)
