"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')

    # call 'filter_1' block
    filter_1(container=container)

    return

def get_alert_details_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_alert_details_1() called')

    source_data_identifier_value = container.get('source_data_identifier', None)

    # collect data for 'get_alert_details_1' call

    parameters = []

    # build parameters list for 'get_alert_details_1' call
    parameters.append({
        'alert_id': source_data_identifier_value,
    })

    phantom.act(action="get alert details", parameters=parameters, assets=['partner'], callback=prompt_further_investigation, name="get_alert_details_1")

    return

def prompt_further_investigation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_further_investigation() called')

    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """Further Investigation Needed for alert {0}?"""

    # parameter list for template variable replacement
    parameters = [
        "get_alert_details_1:action_result.data.*.name",
    ]

    #responses:
    response_types = [
        {
            "prompt": "Further investigate?",
            "options": {
                "type": "list",
                "choices": [
                    "Yes",
                    "No",
                ]
            },
        },
        {
            "prompt": "Case name",
            "options": {
                "type": "message",
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_further_investigation", parameters=parameters, response_types=response_types, callback=create_case_1)

    return

def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_1() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.name", "==", "Code42 File Event Artifact"],
        ],
        name="filter_1:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        get_alert_details_1(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def create_case_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_case_1() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'create_case_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['get_alert_details_1:action_result.data.*.username', 'get_alert_details_1:action_result.parameter.context.artifact_id'], action_results=results)
    results_data_2 = phantom.collect2(container=container, datapath=['prompt_further_investigation:action_result.summary.responses.1', 'prompt_further_investigation:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []

    # build parameters list for 'create_case_1' call
    for results_item_1 in results_data_1:
        for results_item_2 in results_data_2:
            if results_item_2[0]:
                parameters.append({
                    'subject': results_item_1[0],
                    'assignee': "",
                    'findings': "",
                    'case_name': results_item_2[0],
                    'description': "",
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': results_item_1[1]},
                })

    phantom.act(action="create case", parameters=parameters, assets=['partner'], callback=add_case_event_1, name="create_case_1")

    return

def add_case_event_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_case_event_1() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'add_case_event_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.source_data_identifier', 'artifact:*.id'])
    results_data_1 = phantom.collect2(container=container, datapath=['create_case_1:action_result.data.*.number', 'create_case_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []

    # build parameters list for 'add_case_event_1' call
    for container_item in container_data:
        for results_item_1 in results_data_1:
            if container_item[0] and results_item_1[0]:
                parameters.append({
                    'event_id': container_item[0],
                    'case_number': results_item_1[0],
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': container_item[1]},
                })

    phantom.act(action="add case event", parameters=parameters, assets=['partner'], callback=hunt_file_1, name="add_case_event_1", parent_action=action)

    return

def prompt_response_type(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_response_type() called')

    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """What response should be taken for user {0}?"""

    # parameter list for template variable replacement
    parameters = [
        "get_alert_details_1:action_result.data.*.username",
    ]

    #responses:
    response_types = [
        {
            "prompt": "",
            "options": {
                "type": "list",
                "choices": [
                    "Add user to Legal Hold",
                    "Add user to High Risk",
                    "Block User",
                    "No response necessary",
                ]
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_response_type", parameters=parameters, response_types=response_types, callback=decision_2)

    return

def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('decision_2() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_response_type:action_result.summary.responses.0", "==", "No response necessary"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        join_update_case_2(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # check for 'elif' condition 2
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_response_type:action_result.summary.responses.0", "==", "Add user to High Risk"],
        ])

    # call connected blocks if condition 2 matched
    if matched:
        add_highrisk_employee_1(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # check for 'elif' condition 3
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_response_type:action_result.summary.responses.0", "==", "Add user to Legal Hold"],
        ])

    # call connected blocks if condition 3 matched
    if matched:
        prompt_matter_id(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # check for 'elif' condition 4
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_response_type:action_result.summary.responses.0", "==", "Block User"],
        ])

    # call connected blocks if condition 4 matched
    if matched:
        block_user_1(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    return

def prompt_matter_id(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_matter_id() called')

    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """Legal hold matter ID?"""

    #responses:
    response_types = [
        {
            "prompt": "",
            "options": {
                "type": "message",
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_matter_id", response_types=response_types, callback=add_legalhold_custodian_1)

    return

def add_highrisk_employee_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_highrisk_employee_1() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'add_highrisk_employee_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['get_alert_details_1:action_result.summary.username', 'get_alert_details_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []

    # build parameters list for 'add_highrisk_employee_1' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'note': "",
                'username': results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act(action="add highrisk employee", parameters=parameters, assets=['partner'], callback=join_update_case_2, name="add_highrisk_employee_1")

    return

def block_user_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('block_user_1() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'block_user_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['get_alert_details_1:action_result.data.*.username', 'get_alert_details_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []

    # build parameters list for 'block_user_1' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'username': results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act(action="block user", parameters=parameters, assets=['partner'], callback=join_update_case_2, name="block_user_1")

    return

def add_legalhold_custodian_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_legalhold_custodian_1() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'add_legalhold_custodian_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['get_alert_details_1:action_result.data.*.username', 'get_alert_details_1:action_result.parameter.context.artifact_id'], action_results=results)
    results_data_2 = phantom.collect2(container=container, datapath=['prompt_matter_id:action_result.summary.responses.0', 'prompt_matter_id:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []

    # build parameters list for 'add_legalhold_custodian_1' call
    for results_item_1 in results_data_1:
        for results_item_2 in results_data_2:
            if results_item_1[0] and results_item_2[0]:
                parameters.append({
                    'username': results_item_1[0],
                    'matter_id': results_item_2[0],
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': results_item_1[1]},
                })

    phantom.act(action="add legalhold custodian", parameters=parameters, assets=['partner'], callback=join_update_case_2, name="add_legalhold_custodian_1")

    return

def update_case_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_case_2() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'update_case_2' call
    results_data_1 = phantom.collect2(container=container, datapath=['prompt_response_type:action_result.summary.responses.0', 'prompt_response_type:action_result.parameter.context.artifact_id'], action_results=results)
    results_data_2 = phantom.collect2(container=container, datapath=['create_case_1:action_result.data.*.number', 'create_case_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []

    # build parameters list for 'update_case_2' call
    for results_item_1 in results_data_1:
        for results_item_2 in results_data_2:
            if results_item_2[0]:
                parameters.append({
                    'subject': "",
                    'assignee': "",
                    'findings': results_item_1[0],
                    'case_name': "",
                    'case_number': results_item_2[0],
                    'description': "",
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': results_item_1[1]},
                })

    phantom.act(action="update case", parameters=parameters, assets=['partner'], callback=close_case_2, name="update_case_2", parent_action=action)

    return

def join_update_case_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_update_case_2() called')

    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key='join_update_case_2_called'):
        return

    # no callbacks to check, call connected block "update_case_2"
    phantom.save_run_data(key='join_update_case_2_called', value='update_case_2', auto=True)

    update_case_2(container=container, handle=handle)

    return

def close_case_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('close_case_2() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'close_case_2' call
    results_data_1 = phantom.collect2(container=container, datapath=['create_case_1:action_result.data.*.number', 'create_case_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []

    # build parameters list for 'close_case_2' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'case_number': results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act(action="close case", parameters=parameters, assets=['partner'], name="close_case_2", parent_action=action)

    return

def hunt_file_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('hunt_file_1() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'hunt_file_1' call
    inputs_data_1 = phantom.collect2(container=container, datapath=['add_case_event_1:artifact:*.cef.fileHashMd5', 'add_case_event_1:artifact:*.cef.fname', 'add_case_event_1:artifact:*.id'], action_results=results)

    parameters = []

    # build parameters list for 'hunt_file_1' call
    for inputs_item_1 in inputs_data_1:
        if inputs_item_1[0]:
            parameters.append({
                'hash': inputs_item_1[0],
                'file_name': inputs_item_1[1],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': inputs_item_1[2]},
            })

    phantom.act(action="hunt file", parameters=parameters, assets=['partner'], callback=format_1, name="hunt_file_1", parent_action=action)

    return

def send_email_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('send_email_1() called')

    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'send_email_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['get_alert_details_1:action_result.data.*.name', 'get_alert_details_1:action_result.parameter.context.artifact_id'], action_results=results)
    formatted_data_1 = phantom.get_format_data(name='format_1')

    parameters = []

    # build parameters list for 'send_email_1' call
    for results_item_1 in results_data_1:
        parameters.append({
            'from': "Code42 Alert Response",
            'to': "peter.briggs@code42.com",
            'cc': "",
            'bcc': "",
            'subject': results_item_1[0],
            'body': formatted_data_1,
            'attachments': "",
            'headers': "",
            # context (artifact id) is added to associate results with the artifact
            'context': {'artifact_id': results_item_1[1]},
        })

    phantom.act(action="send email", parameters=parameters, assets=['gmail dev'], callback=prompt_response_type, name="send_email_1", parent_action=action)

    return

def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_1() called')

    template = """Data exfiltration activity has been detected by Code42 for user {0}. File exfiltration details:

Files:
{1}

Paths:
{2}

Exposures:
{3}"""

    # parameter list for template variable replacement
    parameters = [
        "get_alert_details_1:action_result.data.*.username",
        "artifact:*.cef.fname",
        "artifact:*.cef.filePath",
        "artifact:*.cef.message",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    send_email_1(container=container)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return