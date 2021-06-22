from py42.sdk.queries.alerts.filters import DateObserved

from code42_util import build_alerts_query
from code42_util import build_date_range_filter


def test_build_date_range_filter_when_given_float_timestamp_returns_expected_filter():
    test_timestamp = "2021-05-25T15:26:52.373Z"
    filter_object = dict(build_date_range_filter(DateObserved, test_timestamp, None))
    assert filter_object["filterClause"] == "AND"
    assert len(filter_object["filters"]) == 1
    assert filter_object["filters"][0]["operator"] == "ON_OR_AFTER"
    assert filter_object["filters"][0]["term"] == "createdAt"
    assert filter_object["filters"][0]["value"] == test_timestamp


def test_build_alerts_query_returns_expected_query():
    start_date = "2021-05-13T16:51:35.425Z"
    end_date = "2021-06-13T16:51:35.425Z"
    actual = dict(build_alerts_query(start_date, end_date))
    assert actual["groupClause"] == "AND"
    assert len(actual["groups"]) == 1
    assert actual["groups"][0]["filterClause"] == "AND"
    assert len(actual["groups"][0]["filters"]) == 2
    _assert_on_or_after(actual["groups"][0]["filters"][0], start_date)
    _assert_on_or_before(actual["groups"][0]["filters"][1], end_date)


def test_build_alerts_query_when_given_username_returns_expected_query():
    start_date = "2021-05-13T16:51:35.425Z"
    end_date = "2021-06-13T16:51:35.425Z"
    username = "test@example.com"
    actual = dict(build_alerts_query(start_date, end_date, username=username))
    assert actual["groupClause"] == "AND"
    assert len(actual["groups"]) == 2
    assert actual["groups"][0]["filterClause"] == "AND"
    assert len(actual["groups"][0]["filters"]) == 1
    _assert_on_or_after(actual["groups"][1]["filters"][0], start_date)
    _assert_on_or_before(actual["groups"][1]["filters"][1], end_date)


def test_build_alerts_query_returns_query_with_sort_direction_ascending():
    actual = build_alerts_query("2021-05-13T16:51:35.425Z", "2021-06-13T16:51:35.425Z")
    assert actual.sort_direction == "asc"


def _assert_on_or_after(actual_filter, expected):
    assert actual_filter == {
        "operator": "ON_OR_AFTER",
        "term": "createdAt",
        "value": expected,
    }


def _assert_on_or_before(actual_filter, expected):
    assert actual_filter == {
        "operator": "ON_OR_BEFORE",
        "term": "createdAt",
        "value": expected,
    }
