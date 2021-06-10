from datetime import datetime, timedelta

import dateutil.parser
from phantom.base_connector import BaseConnector
from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters import Actor, AlertState, DateObserved


def get_thirty_days_ago():
    return datetime.utcnow() - timedelta(days=30)


class Code42BaseConnector(BaseConnector):
    def _build_alerts_query(
        self, start_date, end_date, username=None, alert_state=None
    ):
        filters = []
        if username:
            filters.append(Actor.eq(username))
        if alert_state:
            filters.append(AlertState.eq(alert_state))
        filters.append(self._build_date_range_filter(start_date, end_date))
        query = AlertQuery.all(*filters)
        return query

    def _build_date_range_filter(self, start_date, end_date):
        if start_date and not end_date:
            return DateObserved.on_or_after(dateutil.parser.parse(start_date))
        elif end_date and not start_date:
            return DateObserved.on_or_before(dateutil.parser.parse(end_date))
        elif end_date and start_date:
            return DateObserved.in_range(
                dateutil.parser.parse(start_date), dateutil.parser.parse(end_date)
            )
        else:
            return DateObserved.on_or_after(get_thirty_days_ago())
