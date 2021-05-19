# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

import requests
import json

import py42.sdk


class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class Code42Connector(BaseConnector):

    def __init__(self):
        super(Code42Connector, self).__init__()

        self._state = None
        self._cloud_instance = None
        self._username = None
        self._password = None
        self._client = None

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        self._cloud_instance = config["cloud_instance"]
        self._username = config["username"]
        self._password = config["password"]
        self._client = py42.sdk.from_local_account(self._cloud_instance, self._username, self._password)

        return phantom.APP_SUCCESS

    def handle_action(self, param):
        action_id = self.get_action_identifier()
        self.debug_print("action_id", action_id)

        if action_id == "test_connectivity":
            return self._handle_test_connectivity(param)
        elif action_id == "add_departing_employee":
            return self._handle_add_departing_employee(param)
        elif action_id == "remove_departing_employee":
            return self._handle_remove_departing_employee(param)
        return phantom.APP_SUCCESS

    def _handle_test_connectivity(self, param_dict):
        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param_dict)))
        self.save_progress("Connecting to endpoint")

        try:
            self._client.users.get_current()
        except Exception as e:
            exception_message = e.args[0].strip()
            return action_result.set_status(phantom.APP_ERROR, "Unable to connect to Code42.", exception_message),

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_add_departing_employee(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))
        # username = param["username"]
        # departure_date = param.get("departure_date")
        # self._client.detectionlists.departing_employee.add(username, departure_date=departure_date)
        # action_result.update_summary({})
        # status_message = "{} was added to the departing employee list".format(username)

        status_message = "TEST"
        return action_result.set_status(phantom.APP_SUCCESS, status_message=status_message)

    def _handle_remove_departing_employee(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))
        username = param["username"]
        self._client.detectionlists.departing_employee.remove(username)
        action_result.update_summary({})
        status_message = "{} was removed from the departing employee list".format(username)
        return action_result.set_status(phantom.APP_SUCCESS, status_message=status_message)

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


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

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == "__main__":
    main()
