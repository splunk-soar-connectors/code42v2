from datetime import datetime, timedelta

import dateutil.parser
from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters import Actor, AlertState, DateObserved, Severity


def get_thirty_days_ago():
    return datetime.utcnow() - timedelta(days=30)


def parse_datetime(date_str):
    return dateutil.parser.parse(date_str)


def build_date_range_filter(date_filter_cls, start_date_str, end_date_str):
    if start_date_str and not end_date_str:
        return date_filter_cls.on_or_after(parse_datetime(start_date_str))
    elif end_date_str and not start_date_str:
        return date_filter_cls.on_or_before(parse_datetime(end_date_str))
    elif end_date_str and start_date_str:
        start_datetime = parse_datetime(start_date_str)
        end_datetime = parse_datetime(end_date_str)
        if start_datetime >= end_datetime:
            raise Exception("Start date cannot be after end date.")
        return date_filter_cls.in_range(start_datetime, end_datetime)
    else:
        return date_filter_cls.on_or_after(get_thirty_days_ago())


def build_alerts_query(
    start_date, end_date, username=None, alert_state=None, severities=None
):
    filters = []
    if username is not None:
        filters.append(Actor.eq(username))
    if alert_state is not None:
        filters.append(AlertState.eq(alert_state))
    if severities:
        filters.append(Severity.is_in(severities))
    filters.append(build_date_range_filter(DateObserved, start_date, end_date))
    query = AlertQuery.all(*filters)
    query.sort_direction = "asc"
    return query
