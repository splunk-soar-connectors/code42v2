from pytest import fixture

from tests.conftest import (
    assert_artifacts_added,
    assert_container_added,
    attach_client,
    create_fake_connector,
    create_mock_response,
    MOCK_ALERT_DETAIL_RESPONSE,
    MOCK_SEARCH_ALERTS_LIST_RESPONSE,
    MOCK_SECURITY_EVENT_RESPONSE,
)


def _create_on_poll_connector(client):
    connector = create_fake_connector("on_poll")
    return attach_client(connector, client)


@fixture
def mock_py42_for_alert_polling(mocker, mock_py42_client):
    mock_py42_client.alerts.search.return_value = create_mock_response(
        mocker, MOCK_SEARCH_ALERTS_LIST_RESPONSE
    )
    mock_py42_client.alerts.get_details.return_value = create_mock_response(
        mocker, MOCK_ALERT_DETAIL_RESPONSE
    )
    mock_py42_client.securitydata.search_file_events.return_value = (
        create_mock_response(mocker, MOCK_SECURITY_EVENT_RESPONSE)
    )
    return mock_py42_client


class TestCode42OnPollConnector(object):
    def test_on_poll_adds_container_per_alert(self, mock_py42_for_alert_polling):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._config["ingest"] = {"container_label": "TEST_C_LABEL"}
        connector.handle_action({})
        expected_alert = MOCK_ALERT_DETAIL_RESPONSE["alerts"][0]
        expected_container = {
            "data": expected_alert,
            "description": expected_alert["description"],
            "label": "TEST_C_LABEL",
            "name": expected_alert["name"],
            "severity": expected_alert["severity"],
            "source_data_identifier": expected_alert["id"],
        }
        assert_container_added(connector, [expected_container, expected_container])

    def test_on_poll_adds_artifacts_per_file_event(self, mock_py42_for_alert_polling):
        connector = _create_on_poll_connector(mock_py42_for_alert_polling)
        connector._config["ingest"] = {"container_label": "TEST_C_LABEL"}
        connector.handle_action({})
        expected = [
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=company_secrets.txt fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=HOSTNAME dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=data.jpg fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=TEST'S MAC dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com/test",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=confidential.pdf fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=Test's Windows "
                "dvchost=host.docker.internal src=255.255.255.255 "
                "deviceExternalId=935873453596901068 suid=912098363086307495 "
                "sourceServiceName=Endpoint reason=ApplicationRead spriv=QA "
                "sproc=chrome.exe requestClientApplication=Jira "
                "request=example.com/foo",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=company_secrets.txt fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=HOSTNAME dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=data.jpg fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=TEST'S MAC dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com/test",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=confidential.pdf fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=Test's Windows "
                "dvchost=host.docker.internal src=255.255.255.255 "
                "deviceExternalId=935873453596901068 suid=912098363086307495 "
                "sourceServiceName=Endpoint reason=ApplicationRead spriv=QA "
                "sproc=chrome.exe requestClientApplication=Jira "
                "request=example.com/foo",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=company_secrets.txt fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=HOSTNAME dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=data.jpg fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=TEST'S MAC dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com/test",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=confidential.pdf fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=Test's Windows "
                "dvchost=host.docker.internal src=255.255.255.255 "
                "deviceExternalId=935873453596901068 suid=912098363086307495 "
                "sourceServiceName=Endpoint reason=ApplicationRead spriv=QA "
                "sproc=chrome.exe requestClientApplication=Jira "
                "request=example.com/foo",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=company_secrets.txt fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=HOSTNAME dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=data.jpg fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=TEST'S MAC dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com/test",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=confidential.pdf fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=Test's Windows "
                "dvchost=host.docker.internal src=255.255.255.255 "
                "deviceExternalId=935873453596901068 suid=912098363086307495 "
                "sourceServiceName=Endpoint reason=ApplicationRead spriv=QA "
                "sproc=chrome.exe requestClientApplication=Jira "
                "request=example.com/foo",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=company_secrets.txt fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=HOSTNAME dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=data.jpg fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=TEST'S MAC dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com/test",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=confidential.pdf fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=Test's Windows "
                "dvchost=host.docker.internal src=255.255.255.255 "
                "deviceExternalId=935873453596901068 suid=912098363086307495 "
                "sourceServiceName=Endpoint reason=ApplicationRead spriv=QA "
                "sproc=chrome.exe requestClientApplication=Jira "
                "request=example.com/foo",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=company_secrets.txt fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=HOSTNAME dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=data.jpg fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=TEST'S MAC dvchost=host.docker.internal "
                "src=255.255.255.255 deviceExternalId=935873453596901068 "
                "suid=912098363086307495 sourceServiceName=Endpoint "
                "reason=ApplicationRead spriv=QA sproc=chrome.exe "
                "requestClientApplication=Jira request=example.com/test",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
            {
                "cef": "CEF:0|Code42|Advanced Exfiltration "
                "Detection|1|C42203|READ_BY_APP|5|externalId=0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5 "
                "end=1590669999838 rt=1590670310040 filePath=C:/Users/QA/Downloads/ "
                "fname=confidential.pdf fileType=IMAGE fsize=265122 "
                "fileHash=9cea266b4e07974df1982ae3b9de92ce "
                "fileCreateTime=1590669814902 fileModificationTime=1590669815105 "
                "suser=test@example.com shost=Test's Windows "
                "dvchost=host.docker.internal src=255.255.255.255 "
                "deviceExternalId=935873453596901068 suid=912098363086307495 "
                "sourceServiceName=Endpoint reason=ApplicationRead spriv=QA "
                "sproc=chrome.exe requestClientApplication=Jira "
                "request=example.com/foo",
                "container_id": "CONTAINER_ID",
                "label": "Alerting",
                "source_data_identifier": "11111111-9724-4005-b848-76af488cf5e2",
            },
        ]
        assert_artifacts_added(connector, expected)
