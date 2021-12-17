# File: code42v2_connector.py
#
# Copyright (c) Code42, 2021
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.


# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

import json

import phantom.app as phantom
import phantom.utils as utils
import py42.sdk
import requests
# Phantom App imports
from code42v2_consts import *
from code42v2_on_poll_connector import Code42OnPollConnector
from code42v2_util import build_alerts_query, build_date_range_filter
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from phantom.vault import Vault
from py42.exceptions import Py42BadRequestError, Py42NotFoundError, Py42UpdateClosedCaseError
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import (MD5, SHA256, DeviceUsername, EventTimestamp, FileCategory, OSHostname, PrivateIPAddress,
                                                 ProcessName, PublicIPAddress, TabURL, TrustedActivity, WindowTitle)
from py42.sdk.queries.fileevents.filters.exposure_filter import ExposureType
from py42.sdk.queries.fileevents.filters.file_filter import FileName, FilePath
from py42.services.detectionlists.departing_employee import DepartingEmployeeFilters
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeFilters


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class Code42UnsupportedHashError(Exception):
    def __init__(self):
        super().__init__("Unsupported hash format. Hash must be either md5 or sha256")


ACTION_MAP = {}


def action_handler_for(key):
    def wrapper(f):
        ACTION_MAP[key] = f
        return f

    return wrapper


def _convert_to_obj_list(scalar_list, sub_object_key="item"):
    return [{sub_object_key: item} for item in scalar_list]


def add_eq_filter(filters, value, filter_class):
    return filters.append(filter_class.eq(value))


def is_default_dict(_dict):
    for key in _dict:
        # All action param dictionaries contain the key "context"; we don't care about that key.
        if key != "context" and _dict.get(key):
            return False
    return True


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

    def _validate_integer(self, action_result, parameter, key, allow_zero=False):
        try:
            if not float(parameter).is_integer():
                return action_result.set_status(phantom.APP_ERROR, CODE42V2_VALID_INT_MSG.format(param=key)), None

            parameter = int(parameter)
        except:
            return action_result.set_status(phantom.APP_ERROR, CODE42V2_VALID_INT_MSG.format(param=key)), None

        if parameter < 0:
            return action_result.set_status(phantom.APP_ERROR, CODE42V2_NON_NEG_INT_MSG.format(param=key)), None
        if not allow_zero and parameter == 0:
            return action_result.set_status(phantom.APP_ERROR, CODE42V2_NON_NEG_NON_ZERO_INT_MSG.format(param=key)), None

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

    @action_handler_for("on_poll")
    def _handle_on_poll(self, param, action_result):
        connector = Code42OnPollConnector(self, self._client, self._state)
        return connector.handle_on_poll(param, action_result)

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
        if filter_type not in CODE42V2_FILTER_TYPE_DEPARTING_LIST:
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('filter_type', CODE42V2_FILTER_TYPE_DEPARTING_LIST)
            return action_result.set_status(phantom.APP_SUCCESS, msg)
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

    @action_handler_for("get_departing_employee")
    def _handle_get_departing_employee(self, param, action_result):
        username = param["username"]
        user_id = self._get_user_id(username)

        try:
            response = self._client.detectionlists.departing_employee.get(user_id)
            action_result.add_data(response.data)
            action_result.update_summary({"is_departing_employee": True})
        except Py42NotFoundError:
            action_result.update_summary({"is_departing_employee": False})

        return action_result.set_status(phantom.APP_SUCCESS)

    """ HIGH RISK EMPLOYEE ACTIONS """

    @action_handler_for("add_highrisk_employee")
    def _handle_add_high_risk_employee(self, param, action_result):
        username = param["username"]
        user_id = self._get_user_id(username)
        response = self._client.detectionlists.high_risk_employee.add(user_id)

        note = param.get("note")
        if note:
            self._client.detectionlists.update_user_notes(user_id, note)
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
        if filter_type not in CODE42V2_FILTER_TYPE_HIGH_RISK_LIST:
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('filter_type', CODE42V2_FILTER_TYPE_HIGH_RISK_LIST)
            return action_result.set_status(phantom.APP_SUCCESS, msg)
        results_generator = self._client.detectionlists.high_risk_employee.get_all(
            filter_type=filter_type
        )

        page = None
        for page in results_generator:
            employees = page.data.get("items", [])
            for employee in employees:
                all_tags = employee.get("riskFactors", [])
                if all_tags:
                    employee["riskFactors"] = _convert_to_obj_list(all_tags, "tag")
                action_result.add_data(employee)

        total_count = page.data.get("totalCount", 0) if page else None
        action_result.update_summary({"total_count": total_count})
        return action_result.set_status(phantom.APP_SUCCESS)

    @action_handler_for("get_highrisk_employee")
    def _handle_get_high_risk_employee(self, param, action_result):
        username = param["username"]
        user_id = self._get_user_id(username)

        try:
            response = self._client.detectionlists.high_risk_employee.get(user_id)
            all_tags = response.data.get("riskFactors", [])
            response["riskFactors"] = _convert_to_obj_list(all_tags, "tag")
            action_result.add_data(response.data)
            action_result.update_summary({"is_high_risk_employee": True})
        except Py42NotFoundError:
            action_result.update_summary({"is_high_risk_employee": False})

        return action_result.set_status(phantom.APP_SUCCESS)

    @action_handler_for("add_highrisk_tag")
    def _handle_add_high_risk_tag(self, param, action_result):
        username = param["username"]

        risk_tag = param["risk_tag"]
        if risk_tag not in CODE42V2_RISK_TAG_LIST:
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('risk_tag', CODE42V2_RISK_TAG_LIST)
            return action_result.set_status(phantom.APP_SUCCESS, msg)

        user_id = self._get_user_id(username)
        response = self._client.detectionlists.add_user_risk_tags(user_id, risk_tag)
        all_tags = response.data.get("riskFactors", [])
        response["riskFactors"] = _convert_to_obj_list(all_tags, "tag")
        action_result.add_data(response.data)
        message = f"All risk tags for user: {','.join(all_tags)}"
        return action_result.set_status(phantom.APP_SUCCESS, message)

    @action_handler_for("remove_highrisk_tag")
    def _handle_remove_high_risk_tag(self, param, action_result):
        username = param["username"]

        risk_tag = param["risk_tag"]
        if risk_tag not in CODE42V2_RISK_TAG_LIST:
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('risk_tag', CODE42V2_RISK_TAG_LIST)
            return action_result.set_status(phantom.APP_SUCCESS, msg)

        user_id = self._get_user_id(username)
        response = self._client.detectionlists.remove_user_risk_tags(user_id, risk_tag)
        all_tags = response.data.get("riskFactors", [])
        response["riskFactors"] = _convert_to_obj_list(all_tags, "tag")
        action_result.add_data(response.data)
        message = (
            f"All risk tags for user: {','.join(all_tags)}"
            if all_tags
            else "User has no risk tags"
        )
        return action_result.set_status(phantom.APP_SUCCESS, message)

    """ USER ACTIONS """

    @action_handler_for("create_user")
    def _handle_create_user(self, param, action_result):
        username = param["username"]
        response = self._client.users.create_user(
            org_uid=param["org_uid"],
            username=username,
            email=username,
            password=param.get("password"),
            first_name=param.get("first_name"),
            last_name=param.get("last_name"),
            notes=param.get("notes"),
        )
        user_id = response["userUid"]
        action_result.add_data(response.data)
        return action_result.set_status(
            phantom.APP_SUCCESS, f"{username} was created with user_id: {user_id}"
        )

    @action_handler_for("block_user")
    def _handle_block_user(self, param, action_result):
        username = param["username"]
        user = self._get_user(username)
        response = self._client.users.block(user["userId"])
        action_result.add_data(response.data)
        return action_result.set_status(phantom.APP_SUCCESS, f"{username} was blocked")

    @action_handler_for("unblock_user")
    def _handle_unblock_user(self, param, action_result):
        username = param["username"]
        user = self._get_user(username)
        response = self._client.users.unblock(user["userId"])
        action_result.add_data(response.data)
        return action_result.set_status(
            phantom.APP_SUCCESS, f"{username} was unblocked"
        )

    @action_handler_for("deactivate_user")
    def _handle_deactivate_user(self, param, action_result):
        username = param["username"]
        user = self._get_user(username)
        response = self._client.users.deactivate(user["userId"])
        action_result.add_data(response.data)
        return action_result.set_status(
            phantom.APP_SUCCESS, f"{username} was deactivated"
        )

    @action_handler_for("reactivate_user")
    def _handle_reactivate_user(self, param, action_result):
        username = param["username"]
        user = self._get_user(username)
        response = self._client.users.reactivate(user["userId"])
        action_result.add_data(response.data)
        return action_result.set_status(
            phantom.APP_SUCCESS, f"{username} was reactivated"
        )

    @action_handler_for("get_user_profile")
    def _handle_get_user_profile(self, param, action_result):
        username = param["username"]
        user_id = self._get_user_id(username)
        response = self._client.detectionlists.get_user_by_id(user_id)
        all_tags = response.data.get("riskFactors", [])
        all_cloud_usernames = response.data.get("cloudUsernames", [])
        response["riskFactors"] = _convert_to_obj_list(all_tags, "tag")
        response["cloudUsernames"] = _convert_to_obj_list(
            all_cloud_usernames, "username"
        )
        action_result.add_data(response.data)
        return action_result.set_status(phantom.APP_SUCCESS)

    """ALERTS ACTIONS"""

    @action_handler_for("get_alert_details")
    def _handle_get_alert_details(self, param, action_result):
        alert_id = param["alert_id"]
        response = self._client.alerts.get_details([alert_id])
        alert = response["alerts"][0]
        action_result.add_data(alert)
        action_result.update_summary(
            {"username": alert["actor"], "user_id": alert["actorId"]}
        )
        return action_result.set_status(phantom.APP_SUCCESS)

    @action_handler_for("search_alerts")
    def _handle_search_alerts(self, param, action_result):

        if is_default_dict(param):
            return action_result.set_status(
                phantom.APP_ERROR,
                "Code42: Must supply a search term when calling action 'search_alerts'",
            )

        username = param.get("username")
        start_date = param.get("start_date")
        end_date = param.get("end_date")
        alert_state = param.get("alert_state")

        if alert_state not in CODE42V2_ALERT_STATE:
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('alert_state', CODE42V2_ALERT_STATE)
            return action_result.set_status(phantom.APP_SUCCESS, msg)

        query = build_alerts_query(
            start_date, end_date, username=username, alert_state=alert_state
        )

        response = self._client.alerts.search(query)
        for alert in response["alerts"]:
            action_result.add_data(alert)
        action_result.update_summary({"total_count": response["totalCount"]})
        return action_result.set_status(phantom.APP_SUCCESS)

    @action_handler_for("set_alert_state")
    def _handle_set_alert_state(self, param, action_result):
        alert_id = param["alert_id"]
        alert_state = param["alert_state"]
        note = param.get("note")

        if alert_state not in CODE42V2_ALERT_STATE:
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('alert_state', CODE42V2_ALERT_STATE)
            return action_result.set_status(phantom.APP_SUCCESS, msg)
        response = self._client.alerts.update_state(alert_state, [alert_id], note=note)
        action_result.add_data(response.data)
        action_result.update_summary({"alert_id": alert_id})
        status_message = f"State of alert {alert_id} was updated to {alert_state}"
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("add_legalhold_custodian")
    def _handle_add_legal_hold_custodian(self, param, action_result):
        username = param["username"]
        matter_id = param["matter_id"]
        user_id = self._get_user_id(username)
        self._check_matter_is_accessible(matter_id)
        response = self._client.legalhold.add_to_matter(user_id, matter_id)
        action_result.add_data(response.data)
        status_message = f"{username} was added to legal hold matter {matter_id}."
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("remove_legalhold_custodian")
    def _handle_remove_legal_hold_custodian(self, param, action_result):
        username = param["username"]
        matter_id = param["matter_id"]
        user_id = self._get_user_id(username)
        self._check_matter_is_accessible(matter_id)
        legal_hold_membership_id = self._get_legal_hold_membership_id(
            user_id, matter_id
        )
        if legal_hold_membership_id is None:
            return action_result.set_status(
                phantom.APP_ERROR,
                f"Code42: User is not an active member of "
                f"legal hold matter {matter_id} for action 'remove_legalhold_custodian'.",
            )
        self._client.legalhold.remove_from_matter(legal_hold_membership_id)
        action_result.add_data({"userId": user_id})
        status_message = f"{username} was removed from legal hold matter {matter_id}."
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    """ CASES ACTIONS """

    @action_handler_for("create_case")
    def _handle_create_case(self, param, action_result):
        name = param["case_name"]
        description = param.get("description")
        subject = param.get("subject")
        if subject:
            subject = self._get_user_id(subject)
        assignee = param.get("assignee")
        if assignee:
            assignee = self._get_user_id(assignee)
        findings = param.get("findings")
        response = self._client.cases.create(
            name,
            description=description,
            subject=subject,
            assignee=assignee,
            findings=findings,
        )
        case_number = response["number"]
        action_result.add_data(response.data)
        status_message = f"Case successfully created with case_id: {case_number}"
        action_result.update_summary({"case_number": case_number})
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("update_case")
    def _handle_update_case(self, param, action_result):
        ret_val, case_number = self._validate_integer(action_result, param["case_number"], CODE42V2_CASE_NUM_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        name = param.get("case_name")
        subject = param.get("subject")
        if subject:
            subject = self._get_user_id(subject)
        assignee = param.get("assignee")
        if assignee:
            assignee = self._get_user_id(assignee)
        description = param.get("description")
        findings = param.get("findings")
        try:
            response = self._client.cases.update(
                case_number,
                name=name,
                subject=subject,
                assignee=assignee,
                description=description,
                findings=findings,
            )
        except Py42NotFoundError as err:
            self._handle_case_not_found(err, case_number)
        status_message = f"Case number {case_number} successfully updated"
        action_result.add_data(response.data)
        action_result.update_summary({"case_number": case_number})
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("close_case")
    def _handle_close_case(self, param, action_result):
        ret_val, case_number = self._validate_integer(action_result, param["case_number"], CODE42V2_CASE_NUM_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        try:
            response = self._client.cases.update(case_number, status="CLOSED")
            status_message = f"Case number {case_number} successfully closed"
        except Py42NotFoundError as err:
            self._handle_case_not_found(err, case_number)
        except Py42UpdateClosedCaseError:
            response = self._client.cases.get(case_number)
            status_message = f"Case number {case_number} already closed!"
        action_result.add_data(response.data)
        action_result.update_summary({"case_number": case_number})
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("list_cases")
    def _handle_list_cases(self, param, action_result):
        status = param["status"]
        if status not in CODE42V2_CASE_STATUS_LIST:
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('status', CODE42V2_CASE_STATUS_LIST)
            return action_result.set_status(phantom.APP_SUCCESS, msg)

        if status == "ALL":
            status = None
        assignee = param.get("assignee")
        if assignee:
            assignee = self._get_user_id(assignee)
        subject = param.get("subject")
        if subject:
            subject = self._get_user_id(subject)
        results_generator = self._client.cases.get_all(
            status=status, assignee=assignee, subject=subject
        )
        page = None
        for page in results_generator:
            cases = page.data.get("cases", [])
            for case in cases:
                action_result.add_data(case)

        total_count = page.data.get("totalCount", 0) if page else None
        action_result.update_summary({"total_count": total_count})
        return action_result.set_status(phantom.APP_SUCCESS)

    @action_handler_for("add_case_event")
    def _handle_add_case_event(self, param, action_result):
        ret_val, case_number = self._validate_integer(action_result, param["case_number"], CODE42V2_CASE_NUM_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        event_id = param["event_id"]
        try:
            self._client.cases.file_events.add(
                case_number=case_number, event_id=event_id
            )
        except Py42BadRequestError as err:
            if "NO_SUCH_CASE" in err.response.text:
                self._handle_case_not_found(err, case_number)
            elif "NO_SUCH_EVENT" in err.response.text:
                message = f"Event ID {event_id} not found."
                err.args = (message,)
                raise err
            else:
                raise
        status_message = f"Event {event_id} added to case number {case_number}"
        action_result.update_summary({"case_number": case_number, "event_id": event_id})
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @staticmethod
    def _handle_case_not_found(exception, case_number):
        """Returns a better error message when cases service returns 404."""
        message = f"Case number {case_number} not found."
        exception.args = (message,)
        raise exception

    """ FILE EVENT ACTIONS """

    @action_handler_for("hunt_file")
    def _handle_hunt_file(self, param, action_result):
        file_hash = param["hash"]
        file_name = param.get("file_name")
        if not file_name:
            param["file_name"] = file_hash
            action_result.update_param(param)
            file_name = file_hash

        file_content = self._get_file_content(file_hash)
        container_id = self.get_container_id()
        Vault.create_attachment(file_content, container_id, file_name=file_name)
        status_message = f"{file_name} was successfully downloaded and attached to container {container_id}"
        return action_result.set_status(phantom.APP_SUCCESS, status_message)

    @action_handler_for("run_query")
    def _handle_run_query(self, param, action_result):
        # Boolean action parameters are passed as lowercase string representations, fix that here.
        if "untrusted_only" in param:
            param["untrusted_only"] = str(param["untrusted_only"]).lower() == "true"

        if is_default_dict(param):
            return action_result.set_status(
                phantom.APP_ERROR,
                "Code42: Must supply a search term when calling action 'run_query'.",
            )

        file_category = param.get("file_category")
        if file_category and (file_category not in CODE42V2_FILE_CATEGORY_LIST):
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('file_category', CODE42V2_FILE_CATEGORY_LIST)
            return action_result.set_status(phantom.APP_SUCCESS, msg)

        exposure_type = param.get("exposure_type")
        if exposure_type and exposure_type not in CODE42V2_EXPOSURE_TYPE_LIST:
            msg = CODE42V2_VALUE_LIST_ERR_MSG.format('exposure_type', CODE42V2_EXPOSURE_TYPE_LIST)
            return action_result.set_status(phantom.APP_SUCCESS, msg)

        query = self._build_file_events_query(
            param.get("start_date"),
            param.get("end_date"),
            param.get("file_hash"),
            param.get("file_name"),
            param.get("file_path"),
            param.get("file_category"),
            param.get("username"),
            param.get("hostname"),
            param.get("private_ip"),
            param.get("public_ip"),
            param.get("exposure_type"),
            param.get("process_name"),
            param.get("url"),
            param.get("window_title"),
            param.get("untrusted_only"),
        )
        self._add_file_event_results(query, action_result)
        return action_result.set_status(phantom.APP_SUCCESS)

    @action_handler_for("run_advanced_query")
    def _handle_run_json_query(self, param, action_result):
        query = param["json_query"]
        self._add_file_event_results(query, action_result)
        return action_result.set_status(phantom.APP_SUCCESS)

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _build_file_events_query(
        self,
        start_date,
        end_date,
        file_hash,
        file_name,
        file_path,
        file_category,
        username,
        hostname,
        private_ip,
        public_ip,
        exposure_type,
        process_name,
        url,
        window_title,
        untrusted_only,
    ):
        filters = []
        if file_hash:
            if utils.is_md5(file_hash):
                filters.append(MD5.eq(file_hash))
            elif utils.is_sha256(file_hash):
                filters.append(SHA256.eq(file_hash))
            else:
                raise Code42UnsupportedHashError()

        if file_name:
            add_eq_filter(filters, file_name, FileName)
        if file_path:
            add_eq_filter(filters, file_path, FilePath)
        if file_category:
            add_eq_filter(filters, file_category, FileCategory)
        if hostname:
            add_eq_filter(filters, hostname, OSHostname)
        if username:
            add_eq_filter(filters, username, DeviceUsername)
        if private_ip:
            add_eq_filter(filters, private_ip, PrivateIPAddress)
        if public_ip:
            add_eq_filter(filters, public_ip, PublicIPAddress)
        if exposure_type:
            if exposure_type.lower() == "all":
                filters.append(ExposureType.exists())
            else:
                add_eq_filter(filters, exposure_type, ExposureType)
        if process_name:
            add_eq_filter(filters, process_name, ProcessName)
        if url:
            add_eq_filter(filters, url, TabURL)
        if window_title:
            add_eq_filter(filters, window_title, WindowTitle)
        if untrusted_only:
            filters.append(TrustedActivity.is_false())

        filters.append(build_date_range_filter(EventTimestamp, start_date, end_date))
        query = FileEventQuery.all(*filters)
        return query

    def _get_user(self, username):
        users = self._client.users.get_by_username(username)["users"]
        if not users:
            raise Exception(
                f"User '{username}' not found. Do you have the correct permissions?"
            )
        return users[0]

    def _get_user_id(self, username):
        return self._get_user(username)["userUid"]

    def _get_file_content(self, file_hash):
        if utils.is_md5(file_hash):
            response = self._client.securitydata.stream_file_by_md5(file_hash)
        elif utils.is_sha256(file_hash):
            response = self._client.securitydata.stream_file_by_sha256(file_hash)
        else:
            raise Code42UnsupportedHashError()

        chunks = [chunk for chunk in response.iter_content(chunk_size=128) if chunk]
        return b"".join(chunks)

    def _add_file_event_results(self, query, action_result):
        results = self._client.securitydata.search_file_events(query)
        for result in results.data.get("fileEvents", []):
            result = dict(result)
            all_window_titles = result.get("windowTitle", [])
            if all_window_titles:
                result["windowTitle"] = _convert_to_obj_list(
                    all_window_titles, "windowTitle"
                )
            action_result.add_data(result)

        action_result.update_summary(
            {
                "total_count": results.data["totalCount"],
                "results_returned_count": len(results.data["fileEvents"]),
            }
        )

    # Following three helper functions are copy+pasted from cmds/legal_hold.py in `code42cli`
    def _get_legal_hold_membership_id(self, user_id, matter_id):
        memberships = self._get_legal_hold_memberships_for_matter(matter_id)
        for member in memberships:
            if member["user"]["userUid"] == user_id:
                return member["legalHoldMembershipUid"]
        return None

    def _get_legal_hold_memberships_for_matter(self, matter_id):
        memberships_generator = self._client.legalhold.get_all_matter_custodians(
            legal_hold_uid=matter_id, active=True
        )
        memberships = [
            member
            for page in memberships_generator
            for member in page["legalHoldMemberships"]
        ]
        return memberships

    # Fails when a legal hold matter is inaccessible from the user's account or the matter ID is not valid
    def _check_matter_is_accessible(self, matter_id):
        return self._client.legalhold.get_matter_by_uid(matter_id)


def main():
    import argparse

    import pudb

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
