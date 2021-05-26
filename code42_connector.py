# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

import json

import py42.sdk
from py42.services.detectionlists.departing_employee import DepartingEmployeeFilters
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeFilters
import requests
from datetime import datetime, timedelta

from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters import Actor, AlertState, DateObserved

# Phantom App imports
import phantom.app as phantom
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


ACTION_MAP = {}


def action_handler_for(key):
    def wrapper(f):
        ACTION_MAP[key] = f
        return f

    return wrapper


class Code42Connector(BaseConnector):
    def __init__(self):
        super(Code42Connector, self).__init__()

        self._state = None
        self._cloud_instance = None
        self._username = None
        self._password = None
        self._client = None

    def initialize(self):
        # use this to store data that needs to be accessed across actions
        self._state = self.load_state()

        config = self.get_config()
        self._cloud_instance = config["cloud_instance"]
        self._username = config["username"]
        self._password = config["password"]

        return phantom.APP_SUCCESS

    def handle_action(self, param):
        action_id = self.get_action_identifier()
        self.debug_print("action_id", action_id)

        action_handler = ACTION_MAP.get(action_id)
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not action_handler:
            return action_result.set_status(
                phantom.APP_ERROR, f"Code42: Action {action_id} does not exist."
            )

        try:
            if not self._client:
                self._client = py42.sdk.from_local_account(
                    self._cloud_instance, self._username, self._password
                )
            self.save_progress(f"Code42: handling action {action_id}...")
            return action_handler(self, param, action_result)
        except Exception as ex:
            msg = f"Code42: Failed execution of action {action_id}: {ex}"
            return action_result.set_status(phantom.APP_ERROR, msg)

    @action_handler_for("test_connectivity")
    def _handle_test_connectivity(self, param, action_result):
        self._client.users.get_current()
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    """ DEPARTING EMPLOYEE ACTIONS """

    @action_handler_for("add_departing_employee")
    def _handle_add_departing_employee(self, param, action_result):
        username = param["username"]
        departure_date = param.get("departure_date")
        user_id = self._get_user_id(username)
        response = self._client.detectionlists.departing_employee.add(
            user_id, departure_date=departure_date
        )

        note = param.get("note")
        if note:
            self._client.detectionlists.update_user_notes(user_id, note)

        action_result.add_data(response.data)
        status_message = f"{username} was added to the departing employees list"
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("remove_departing_employee")
    def _handle_remove_departing_employee(self, param, action_result):
        username = param["username"]
        user_id = self._get_user_id(username)
        self._client.detectionlists.departing_employee.remove(user_id)
        action_result.add_data({"userId": user_id})
        status_message = f"{username} was removed from the departing employees list"
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("list_departing_employees")
    def _handle_list_departing_employees(self, param, action_result):
        filter_type = param.get("filter_type", DepartingEmployeeFilters.OPEN)
        results_generator = self._client.detectionlists.departing_employee.get_all(
            filter_type=filter_type
        )

        page = None
        for page in results_generator:
            employees = page.data.get("items", [])
            for employee in employees:
                action_result.add_data(employee)

        total_count = page.data.get("totalCount", 0) if page else None
        action_result.update_summary({"total_count": total_count})
        return action_result.set_status(phantom.APP_SUCCESS)

    """ HIGH RISK EMPLOYEE ACTIONS """

    @action_handler_for("add_highrisk_employee")
    def _handle_add_high_risk_employee(self, param, action_result):
        username = param["username"]
        user_id = self._get_user_id(username)
        response = self._client.detectionlists.high_risk_employee.add(user_id)
        action_result.add_data(response.data)
        status_message = f"{username} was added to the high risk employees list"
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("remove_highrisk_employee")
    def _handle_remove_high_risk_employee(self, param, action_result):
        username = param["username"]
        user_id = self._get_user_id(username)
        self._client.detectionlists.high_risk_employee.remove(user_id)
        action_result.add_data({"userId": user_id})
        status_message = f"{username} was removed from the high risk employees list"
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("list_highrisk_employees")
    def _handle_list_high_risk_employees(self, param, action_result):
        filter_type = param.get("filter_type", HighRiskEmployeeFilters.OPEN)
        results_generator = self._client.detectionlists.high_risk_employee.get_all(
            filter_type=filter_type
        )

        page = None
        for page in results_generator:
            employees = page.data.get("items", [])
            for employee in employees:
                action_result.add_data(employee)

        total_count = page.data.get("totalCount", 0) if page else None
        action_result.update_summary({"total_count": total_count})
        return action_result.set_status(phantom.APP_SUCCESS)

    """ALERTS ACTIONS"""

    @action_handler_for("get_alert_details")
    def _handle_get_alert_details(self, param, action_result):
        alert_id = param["alert_id"]
        response = self._client.alerts.get_details([alert_id])
        alert = response.data["alerts"][0]
        action_result.add_data(alert)
        action_result.update_summary(
            {"username": alert["actor"], "user_id": alert["actorId"]}
        )
        return action_result.set_status(phantom.APP_SUCCESS)

    @action_handler_for("search_alerts")
    def _handle_search_alerts(self, param, action_result):
        username = param.get("username")
        start_date = param.get("start_date")
        end_date = param.get("end_date")
        alert_state = param.get("alert_state")

        if not username and not start_date and not end_date and not alert_state:
            return action_result.set_status(
                phantom.APP_ERROR, "Code42: Must supply a search term when calling action 'search_alerts`."
            )

        if not self._validate_date_range(start_date, end_date):
            return action_result.set_status(
                phantom.APP_ERROR,
                "Code42: Start Date and End Date are both required to search by date range for action 'search_alerts'.",
            )
        try:
            query = self._build_alerts_query(
                username, start_date, end_date, alert_state
            )
        except ValueError as exception:
            return action_result.set_status(
                phantom.APP_ERROR,
                f"Code42: Start Date and End Date must be in format YYYY-mm-dd: {exception} for action 'search_alerts'",
            )

        response = self._client.alerts.search(query)
        action_result.add_data(response.data)
        action_result.update_summary({"total_count": response["totalCount"]})
        return action_result.set_status(phantom.APP_SUCCESS)

    @action_handler_for("set_alert_state")
    def _handle_set_alert_state(self, param, action_result):
        alert_id = param["alert_id"]
        alert_state = param["alert_state"]
        note = param.get("note")
        response = self._client.alerts.update_state(alert_state, [alert_id], note=note)
        action_result.add_data(response.data)
        status_message = f"State of alert {alert_id} was updated to {alert_state}"
        action_result.update_summary({"alert_id": alert_id})
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _validate_date_range(self, start_date, end_date):
        return (not start_date and not end_date) or (
            start_date is not None and end_date is not None
        )

    def _build_alerts_query(self, username, start_date, end_date, alert_state):
        filters = []
        if username is not None:
            filters.append(Actor.eq(username))
        if start_date is not None and end_date is not None:
            # This will raise a ValueError if dates not in Y-m-d H:M:S format
            filters.append(
                DateObserved.in_range(f"{start_date} 00:00:00", f"{end_date} 00:00:00")
            )
        else:
            # If a date range is not provided, default to returning alerts from last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            filters.append(DateObserved.on_or_after(thirty_days_ago))
        if alert_state is not None:
            filters.append(AlertState.eq(alert_state))
        query = AlertQuery.all(*filters)
        return query

    def _get_user_id(self, username):
        users = self._client.users.get_by_username(username)["users"]
        if not users:
            raise Exception(f"User '{username}' does not exist")
        return users[0]["userUid"]


def main():
    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    csrftoken = None
    headers = None
    if username and password:
        try:
            login_url = Code42Connector._get_phantom_base_url() + "/login"

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = Code42Connector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            if csrftoken and headers:
                connector._set_csrf_info(csrftoken, headers["Referer"])

        json_string = json.dumps(in_json)
        ret_val = connector._handle_action(json_string, None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == "__main__":
    main()
