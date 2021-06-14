import json

import phantom.app
import py42.sdk
from py42.response import Py42Response
from py42.services.users import UserService
from pytest import fixture
from requests import Response

from code42_connector import Code42Connector

TEST_USER_UID = "TEST_USER_UID"
MOCK_ALERT_DETAIL_RESPONSE = {
    "alerts": [
        {
            "type$": "ALERT_SUMMARY",
            "tenantId": "11111111-abcd-4231-99ab-df6434da4663",
            "type": "FED_COMPOSITE",
            "name": "Test Alert",
            "description": "it's a test",
            "actor": "cool.guy@code42.com",
            "actorId": "987210998131391466",
            "target": "N/A",
            "severity": "LOW",
            "ruleId": "cab2d5ee-a512-45b1-8848-809327033048",
            "ruleSource": "Alerting",
            "id": "11111111-9724-4005-b848-76af488cf5e2",
            "createdAt": "2021-05-13T16:51:35.4259080Z",
            "state": "OPEN",
            "observations": [
                {
                    "type$": "OBSERVATION",
                    "id": "240526fc-3a32-4755-85ab-c6ee6e7f31ce",
                    "observedAt": "2020-05-28T12:50:00.0000000Z",
                    "type": "FedEndpointExfiltration",
                    "data": {
                        "type$": "OBSERVED_ENDPOINT_ACTIVITY",
                        "id": "240526fc-3a32-4755-85ab-c6ee6e7f31ce",
                        "sources": ["Endpoint"],
                        "exposureTypes": ["ApplicationRead"],
                        "firstActivityAt": "2020-05-28T12:50:00.0000000Z",
                        "lastActivityAt": "2020-05-28T12:50:00.0000000Z",
                        "fileCount": 3,
                        "totalFileSize": 533846,
                        "fileCategories": [
                            {
                                "type$": "OBSERVED_FILE_CATEGORY",
                                "category": "SourceCode",
                                "fileCount": 3,
                                "totalFileSize": 533846,
                                "isSignificant": True,
                            },
                            {
                                "type$": "OBSERVED_FILE_CATEGORY",
                                "category": "Pdf",
                                "fileCount": 3,
                                "totalFileSize": 533846,
                                "isSignificant": True,
                            },
                        ],
                        "files": [
                            {
                                "type$": "OBSERVED_FILE",
                                "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
                                "path": "C:/Users/QA/Downloads/",
                                "name": "Customers.jpg",
                                "category": "Image",
                                "size": 265122,
                            },
                            {
                                "type$": "OBSERVED_FILE",
                                "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_6",
                                "path": "C:/Users/QA/Downloads/",
                                "name": "data.png",
                                "category": "Image",
                                "size": 129129,
                            },
                            {
                                "type$": "OBSERVED_FILE",
                                "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_7",
                                "path": "C:/Users/QA/Downloads/",
                                "name": "company_secrets.ps",
                                "category": "Image",
                                "size": 139595,
                            },
                        ],
                        "syncToServices": [],
                        "sendingIpAddresses": ["127.0.0.1"],
                    },
                },
                {
                    "type$": "OBSERVATION",
                    "id": "7f4d125d-c7ca-4264-83fe-fa442bf270b6",
                    "observedAt": "2020-06-11T20:20:00.0000000Z",
                    "type": "FedCloudSharePermissions",
                    "data": {
                        "type$": "OBSERVED_CLOUD_SHARE_ACTIVITY",
                        "id": "7f4d125d-c7ca-4264-83fe-fa442bf270b6",
                        "sources": ["GoogleDrive"],
                        "exposureTypes": ["SharedOutsideTrustedDomain"],
                        "firstActivityAt": "2020-06-11T20:20:00.0000000Z",
                        "lastActivityAt": "2020-06-11T20:25:00.0000000Z",
                        "fileCount": 1,
                        "totalFileSize": 182554405,
                        "fileCategories": [
                            {
                                "type$": "OBSERVED_FILE_CATEGORY",
                                "category": "Archive",
                                "fileCount": 1,
                                "totalFileSize": 182554405,
                                "isSignificant": False,
                            }
                        ],
                        "files": [
                            {
                                "type$": "OBSERVED_FILE",
                                "eventId": "14FnN9-YOhVUO_Tv8Mu-hEgevc2K4l07l_5_9e633ffd-9329-4cf4-8645-27a23b83ebc0",
                                "name": "Code42CrashPlan_8.0.0_1525200006800_778_Mac.dmg",
                                "category": "Archive",
                                "size": 182554405,
                            }
                        ],
                        "outsideTrustedDomainsEmails": ["user1@example.com"],
                        "outsideTrustedDomainsEmailsCount": 1,
                        "outsideTrustedDomainsCounts": [
                            {
                                "type$": "OBSERVED_DOMAIN_INFO",
                                "domain": "gmail.com",
                                "count": 1,
                            }
                        ],
                        "outsideTrustedDomainsTotalDomainCount": 1,
                        "outsideTrustedDomainsTotalDomainCountTruncated": False,
                    },
                },
                {
                    "type$": "OBSERVATION",
                    "id": "7f4d125d-c7ca-4264-83fe-fa442bf270b6",
                    "observedAt": "2020-06-11T20:20:00.0000000Z",
                    "type": "FedCloudSharePermissions",
                    "data": {
                        "type$": "OBSERVED_CLOUD_SHARE_ACTIVITY",
                        "id": "7f4d125d-c7ca-4264-83fe-fa442bf270b6",
                        "sources": ["GoogleDrive"],
                        "exposureTypes": ["UnknownExposureTypeThatWeDontSupportYet"],
                        "firstActivityAt": "2020-06-11T20:20:00.0000000Z",
                        "lastActivityAt": "2020-06-11T20:25:00.0000000Z",
                        "fileCount": 1,
                        "totalFileSize": 182554405,
                        "fileCategories": [
                            {
                                "type$": "OBSERVED_FILE_CATEGORY",
                                "category": "Archive",
                                "fileCount": 1,
                                "totalFileSize": 182554405,
                                "isSignificant": False,
                            }
                        ],
                        "files": [
                            {
                                "type$": "OBSERVED_FILE",
                                "eventId": "14FnN9-YOhVUO_Tv8Mu-hEgevc2K4l07l_5_9e633ffd-9329-4cf4-8645-27a23b83ebc0",
                                "name": "Code42CrashPlan_8.0.0_1525200006800_778_Mac.dmg",
                                "category": "Archive",
                                "size": 182554405,
                            }
                        ],
                        "outsideTrustedDomainsEmails": ["user1@example.com"],
                        "outsideTrustedDomainsEmailsCount": 1,
                        "outsideTrustedDomainsCounts": [
                            {
                                "type$": "OBSERVED_DOMAIN_INFO",
                                "domain": "gmail.com",
                                "count": 1,
                            }
                        ],
                        "outsideTrustedDomainsTotalDomainCount": 1,
                        "outsideTrustedDomainsTotalDomainCountTruncated": False,
                    },
                },
            ],
        }
    ]
}
MOCK_SEARCH_ALERTS_LIST_RESPONSE = {
    "type$": "ALERT_QUERY_RESPONSE",
    "alerts": [
        {
            "type$": "ALERT_SUMMARY",
            "tenantId": "11111111-af5b-4231-9d8e-df6434da4663",
            "type": "FED_COMPOSITE",
            "name": "Alert 1",
            "description": "Its a test :)",
            "actor": "barney.frankenberry@chocula.com",
            "actorId": "987210998131391466",
            "target": "N/A",
            "severity": "LOW",
            "ruleId": "cab2d5ee-a512-45b1-8848-809327033048",
            "ruleSource": "Alerting",
            "id": "11111111-9724-4005-b848-76af488cf5e2",
            "createdAt": "2021-05-13T16:51:35.4259080Z",
            "state": "OPEN",
        },
        {
            "type$": "ALERT_SUMMARY",
            "tenantId": "11111111-af5b-4231-9d8e-df6434da4663",
            "type": "FED_COMPOSITE",
            "name": "File Upload Alert",
            "description": "Alert on any file upload events",
            "actor": "barney.frankenberry@chocula.com",
            "actorId": "987210998131391466",
            "target": "N/A",
            "severity": "MEDIUM",
            "ruleId": "962a6a1c-54f6-4477-90bd-a08cc74cbf71",
            "ruleSource": "Alerting",
            "id": "1111111-555f-4880-8909-f5679448e67c",
            "createdAt": "2021-05-13T16:51:35.3465540Z",
            "state": "OPEN",
        },
    ],
    "totalCount": 2,
    "problems": [],
}
MOCK_SECURITY_EVENT_RESPONSE = {
    "totalCount": 3,
    "fileEvents": [
        {
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventType": "READ_BY_APP",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "fieldErrors": [],
            "filePath": "C:/Users/QA/Downloads/",
            "fileName": "company_secrets.txt",
            "fileType": "FILE",
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileSize": 265122,
            "fileOwner": "Test",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "deviceUserName": "test@example.com",
            "osHostName": "HOSTNAME",
            "domainName": "host.docker.internal",
            "publicIpAddress": "255.255.255.255",
            "privateIpAddresses": ["255.255.255.255", "127.0.0.1"],
            "deviceUid": "935873453596901068",
            "userUid": "912098363086307495",
            "actor": None,
            "directoryId": [],
            "source": "Endpoint",
            "url": None,
            "shared": None,
            "sharedWith": [],
            "sharingTypeAdded": [],
            "cloudDriveId": None,
            "detectionSourceAlias": None,
            "fileId": None,
            "exposure": ["ApplicationRead"],
            "processOwner": "QA",
            "processName": "chrome.exe",
            "windowTitle": ["Jira"],
            "tabUrl": "example.com",
            "removableMediaVendor": None,
            "removableMediaName": None,
            "removableMediaSerialNumber": None,
            "removableMediaCapacity": None,
            "removableMediaBusType": None,
            "removableMediaMediaName": None,
            "removableMediaVolumeName": [],
            "removableMediaPartitionId": [],
            "syncDestination": None,
            "emailDlpPolicyNames": None,
            "emailSubject": None,
            "emailSender": None,
            "emailFrom": None,
            "emailRecipients": None,
            "outsideActiveHours": False,
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "printJobName": None,
            "printerName": None,
            "printedFilesBackupPath": None,
            "remoteActivity": "UNKNOWN",
            "trusted": False,
            "operatingSystemUser": "IEUser",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
        },
        {
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventType": "READ_BY_APP",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "fieldErrors": [],
            "filePath": "C:/Users/QA/Downloads/",
            "fileName": "data.jpg",
            "fileType": "FILE",
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileSize": 265122,
            "fileOwner": "QA",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "deviceUserName": "test@example.com",
            "osHostName": "TEST'S MAC",
            "domainName": "host.docker.internal",
            "publicIpAddress": "255.255.255.255",
            "privateIpAddresses": ["127.0.0.1"],
            "deviceUid": "935873453596901068",
            "userUid": "912098363086307495",
            "actor": None,
            "directoryId": [],
            "source": "Endpoint",
            "url": None,
            "shared": None,
            "sharedWith": [],
            "sharingTypeAdded": [],
            "cloudDriveId": None,
            "detectionSourceAlias": None,
            "fileId": None,
            "exposure": ["ApplicationRead"],
            "processOwner": "QA",
            "processName": "chrome.exe",
            "windowTitle": ["Jira"],
            "tabUrl": "example.com/test",
            "removableMediaVendor": None,
            "removableMediaName": None,
            "removableMediaSerialNumber": None,
            "removableMediaCapacity": None,
            "removableMediaBusType": None,
            "removableMediaMediaName": None,
            "removableMediaVolumeName": [],
            "removableMediaPartitionId": [],
            "syncDestination": None,
            "emailDlpPolicyNames": None,
            "emailSubject": None,
            "emailSender": None,
            "emailFrom": None,
            "emailRecipients": None,
            "outsideActiveHours": False,
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "printJobName": None,
            "printerName": None,
            "printedFilesBackupPath": None,
            "remoteActivity": "UNKNOWN",
            "trusted": False,
            "operatingSystemUser": "IEUser",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
        },
        {
            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventType": "READ_BY_APP",
            "eventTimestamp": "2020-05-28T12:46:39.838Z",
            "insertionTimestamp": "2020-05-28T12:51:50.040Z",
            "fieldErrors": [],
            "filePath": "C:/Users/QA/Downloads/",
            "fileName": "confidential.pdf",
            "fileType": "FILE",
            "fileCategory": "IMAGE",
            "fileCategoryByBytes": "Image",
            "fileCategoryByExtension": "Image",
            "fileSize": 265122,
            "fileOwner": "Mock",
            "md5Checksum": "9cea266b4e07974df1982ae3b9de92ce",
            "sha256Checksum": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "createTimestamp": "2020-05-28T12:43:34.902Z",
            "modifyTimestamp": "2020-05-28T12:43:35.105Z",
            "deviceUserName": "test@example.com",
            "osHostName": "Test's Windows",
            "domainName": "host.docker.internal",
            "publicIpAddress": "255.255.255.255",
            "privateIpAddresses": ["0:0:0:0:0:0:0:1", "127.0.0.1"],
            "deviceUid": "935873453596901068",
            "userUid": "912098363086307495",
            "actor": None,
            "directoryId": [],
            "source": "Endpoint",
            "url": None,
            "shared": None,
            "sharedWith": [],
            "sharingTypeAdded": [],
            "cloudDriveId": None,
            "detectionSourceAlias": None,
            "fileId": None,
            "exposure": ["ApplicationRead"],
            "processOwner": "QA",
            "processName": "chrome.exe",
            "windowTitle": ["Jira"],
            "tabUrl": "example.com/foo",
            "removableMediaVendor": None,
            "removableMediaName": None,
            "removableMediaSerialNumber": None,
            "removableMediaCapacity": None,
            "removableMediaBusType": None,
            "removableMediaMediaName": None,
            "removableMediaVolumeName": [],
            "removableMediaPartitionId": [],
            "syncDestination": None,
            "emailDlpPolicyNames": None,
            "emailSubject": None,
            "emailSender": None,
            "emailFrom": None,
            "emailRecipients": None,
            "outsideActiveHours": False,
            "mimeTypeByBytes": "image/png",
            "mimeTypeByExtension": "image/png",
            "mimeTypeMismatch": False,
            "printJobName": None,
            "printerName": None,
            "printedFilesBackupPath": None,
            "remoteActivity": "UNKNOWN",
            "trusted": False,
            "operatingSystemUser": "IEUser",
            "destinationCategory": "Cloud Storage",
            "destinationName": "Google Drive",
            "riskScore": 5,
            "riskSeverity": "HIGH",
            "riskIndicators": [
                {"name": "Google Drive upload", "weight": 5},
                {"name": "Spreadsheet", "weight": 0},
            ],
        },
    ],
}


@fixture(autouse=True)
def mock_py42_client(mocker):
    client = mocker.MagicMock(spec=py42.sdk.SDKClient)
    client.users = mocker.MagicMock(spec=UserService)
    mocker.patch("py42.sdk.from_local_account", return_value=client)
    return client


@fixture(autouse=True)
def mock_create_attachment(mocker):
    mock_vault = mocker.patch("phantom.vault.Vault.create_attachment")
    return mock_vault


@fixture
def mock_py42_with_user(mocker, mock_py42_client):
    response_data = {"users": [{"userUid": TEST_USER_UID}]}
    return _set_py42_users(mocker, mock_py42_client, response_data)


@fixture
def mock_py42_without_user(mocker, mock_py42_client):
    return _set_py42_users(mocker, mock_py42_client, {"users": []})


def _set_py42_users(mocker, mock_py42_client, response_data):
    mock_py42_client.users.get_by_username.return_value = create_mock_response(
        mocker, response_data
    )
    return mock_py42_client


@fixture
def connector():
    connector = Code42Connector()
    return connector


def create_fake_connector(action_identifier, client=None):
    def fake_get_action_identifier():
        return action_identifier

    def fake_get_container_id():
        return 42

    connector = Code42Connector()
    connector.get_action_identifier = fake_get_action_identifier
    connector.get_container_id = fake_get_container_id
    connector._client = client
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


def assert_successful_params(connector, expected_params):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    params = action_results[0].get_param()
    status = action_results[0].get_status()
    assert params == expected_params
    assert status == phantom.app.APP_SUCCESS


def assert_container_added(connector, expected_containers):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    assert connector._containers == expected_containers
    status = action_results[0].get_status()
    assert status == phantom.app.APP_SUCCESS


def assert_artifacts_added(connector, expected_artifacts):
    action_results = connector.get_action_results()
    assert len(action_results) == 1
    assert connector._artifacts == expected_artifacts
    status = action_results[0].get_status()
    assert status == phantom.app.APP_SUCCESS
