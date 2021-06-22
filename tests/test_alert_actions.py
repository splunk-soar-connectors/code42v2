from datetime import datetime, timedelta, timezone
from unittest import mock

import dateutil
from py42.exceptions import Py42NotFoundError
from pytest import fixture

from tests.conftest import (
    create_fake_connector,
    create_mock_response,
    attach_client,
    assert_successful_single_data,
    assert_successful_summary,
    assert_fail,
    assert_successful_message,
    assert_success,
    assert_fail_message,
    MOCK_SEARCH_ALERTS_LIST_RESPONSE,
    MOCK_ALERT_DETAIL_RESPONSE,
)


def _create_get_alert_details_connector(client):
    connector = create_fake_connector("get_alert_details")
    return attach_client(connector, client)


def _create_search_alerts_connector(client):
    connector = create_fake_connector("search_alerts")
    return attach_client(connector, client)


def _create_set_alert_state_connector(client):
    connector = create_fake_connector("set_alert_state")
    return attach_client(connector, client)


@fixture
def mock_py42_with_search_alerts(mocker, mock_py42_client):
    mock_py42_client.alerts.search.return_value = create_mock_response(
        mocker, MOCK_SEARCH_ALERTS_LIST_RESPONSE
    )
    return mock_py42_client


@fixture
def mock_py42_with_alert_details(mocker, mock_py42_client):
    mock_py42_client.alerts.get_details.return_value = create_mock_response(
        mocker, MOCK_ALERT_DETAIL_RESPONSE
    )


class TestCode42AlertsConnector(object):
    def test_handle_action_when_alert_detail_calls_get_with_expected_args(
        self, mock_py42_client
    ):
        param = {"alert_id": "123-456-7890"}
        connector = _create_get_alert_details_connector(mock_py42_client)
        connector.handle_action(param)
        mock_py42_client.alerts.get_details.assert_called_once_with([param["alert_id"]])
        assert_success(connector)

    def test_handle_action_when_alert_detail_adds_response_to_data(
        self, mock_py42_with_alert_details
    ):
        param = {"alert_id": "123-456-7890"}
        connector = _create_get_alert_details_connector(mock_py42_with_alert_details)
        connector.handle_action(param)
        assert_successful_single_data(
            connector, MOCK_ALERT_DETAIL_RESPONSE["alerts"][0]
        )

    def test_handle_action_when_alert_detail_adds_info_to_summary(
        self, mock_py42_with_alert_details
    ):
        param = {"alert_id": "123-456-7890"}
        connector = _create_get_alert_details_connector(mock_py42_with_alert_details)
        connector.handle_action(param)
        expected_summary = {
            "username": MOCK_ALERT_DETAIL_RESPONSE["alerts"][0]["actor"],
            "user_id": MOCK_ALERT_DETAIL_RESPONSE["alerts"][0]["actorId"],
        }
        assert_successful_summary(connector, expected_summary)

    def test_handle_action_when_search_alerts_calls_search(self, mock_py42_client):
        param = {
            "username": "gilbert.lequiche@finance.biz",
            "start_date": "2031-01-01",
            "end_date": "2031-06-01",
            "alert_state": "OPEN",
        }
        connector = _create_search_alerts_connector(mock_py42_client)
        connector.handle_action(param)
        mock_py42_client.alerts.search.assert_called_once()
        assert_success(connector)

    def test_handle_action_when_search_alerts_and_all_params_missing_sets_error_message(
        self, mock_py42_client
    ):
        param = {}
        connector = _create_search_alerts_connector(mock_py42_client)
        connector.handle_action(param)
        expected_message = (
            "Code42: Must supply a search term when calling action 'search_alerts`."
        )
        assert_fail_message(connector, expected_message)

    def test_handle_action_when_search_alerts_and_date_range_incomplete_calls_search(
        self, mock_py42_client
    ):
        param = {"start_date": "2031-01-01"}
        connector = _create_search_alerts_connector(mock_py42_client)
        connector.handle_action(param)
        assert_success(connector)

    def test_handle_action_when_search_alerts_and_date_format_invalid_sets_error_status(
        self, mock_py42_client
    ):
        param = {
            "start_date": "2031-31-12",
            "end_date": "2032-31-01",
        }
        connector = _create_search_alerts_connector(mock_py42_client)
        connector.handle_action(param)
        assert_fail(connector)

    def test_handle_action_when_search_alerts_adds_response_items_to_data(
        self, mock_py42_with_search_alerts
    ):
        param = {"username": "barney.frankenberry@chocula.com"}
        connector = _create_search_alerts_connector(mock_py42_with_search_alerts)
        connector.handle_action(param)
        action_results = connector.get_action_results()
        assert len(action_results) == 1
        data = action_results[0].get_data()
        assert data[0] == MOCK_SEARCH_ALERTS_LIST_RESPONSE["alerts"][0]
        assert data[1] == MOCK_SEARCH_ALERTS_LIST_RESPONSE["alerts"][1]

    def test_handle_action_when_search_alerts_adds_summary(
        self, mock_py42_with_search_alerts
    ):
        param = {"username": "barney.frankenberry@chocula.com"}
        connector = _create_search_alerts_connector(mock_py42_with_search_alerts)
        connector.handle_action(param)
        assert_successful_summary(
            connector, {"total_count": MOCK_SEARCH_ALERTS_LIST_RESPONSE["totalCount"]}
        )

    def test_handle_action_when_search_alerts_and_no_date_range_provided_defaults_to_last_30_days(
        self, mock_py42_client
    ):
        param = {"username": "barney.frankenberry@chocula.com"}
        connector = _create_search_alerts_connector(mock_py42_client)
        connector.handle_action(param)
        actual_query = mock_py42_client.alerts.search.call_args[0][0]
        query_json = dict(actual_query)
        actual_date = dateutil.parser.parse(
            query_json["groups"][1]["filters"][0]["value"]
        )
        expected_date = datetime.now(timezone.utc) - timedelta(days=30)
        assert abs((actual_date - expected_date)).seconds < 1
        assert_success(connector)

    def test_handle_action_when_search_alerts_and_start_date_after_end_date_sets_error_message(
        self, mock_py42_with_search_alerts
    ):
        param = {
            "username": "gilbert.lequiche@finance.biz",
            "start_date": "2031-06-01",
            "end_date": "2031-01-01",
        }
        connector = _create_search_alerts_connector(mock_py42_with_search_alerts)
        connector.handle_action(param)
        expected_message = "Code42: Failed execution of action search_alerts: Start date cannot be after end date."
        assert_fail_message(connector, expected_message)

    def test_handle_action_when_set_alert_state_calls_update_state(
        self, mock_py42_client
    ):
        param = {"alert_id": "1234-5678-0000", "alert_state": "RESOLVED"}
        connector = _create_set_alert_state_connector(mock_py42_client)
        connector.handle_action(param)
        mock_py42_client.alerts.update_state.assert_called_once_with(
            param["alert_state"], [param["alert_id"]], note=None
        )
        assert_success(connector)

    def test_handle_action_when_set_alert_state_sets_message(self, mock_py42_client):
        param = {"alert_id": "1234-5678-0000", "alert_state": "RESOLVED"}
        connector = _create_set_alert_state_connector(mock_py42_client)
        connector.handle_action(param)
        expected_message = (
            f"State of alert {param['alert_id']} was updated to {param['alert_state']}"
        )
        assert_successful_message(connector, expected_message)

    def test_handle_action_when_set_alert_state_updates_summary(self, mock_py42_client):
        param = {"alert_id": "1234-5678-0000", "alert_state": "RESOLVED"}
        connector = _create_set_alert_state_connector(mock_py42_client)
        connector.handle_action(param)
        assert_successful_summary(connector, {"alert_id": param["alert_id"]})

    def test_handle_action_when_set_alert_state_and_alert_doesnt_exist_sets_error_status(
        self, mock_py42_client
    ):
        param = {"alert_id": "1234-doesnt-exist-5678", "alert_state": "OPEN"}
        connector = _create_set_alert_state_connector(mock_py42_client)
        mock_py42_client.alerts.update_state.side_effect = Py42NotFoundError(
            mock.Mock(status=404)
        )
        connector.handle_action(param)
        assert_fail(connector)
