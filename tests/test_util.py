import json

from code42_util import build_alerts_query


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
