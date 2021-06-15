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


def get_alert_details_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
                        filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_alert_details_1() called')

    source_data_identifier_value = container.get('source_data_identifier', None)

    # collect data for 'get_alert_details_1' call

    parameters = []

    # build parameters list for 'get_alert_details_1' call
    parameters.append({
        'alert_id': source_data_identifier_value,
    })

    phantom.act(action="get alert details", parameters=parameters, assets=['partner'],
                callback=prompt_further_investigation, name="get_alert_details_1")

    return


def prompt_further_investigation(action=None, success=None, container=None, results=None, handle=None,
                                 filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_further_investigation() called')

    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """Further Investigation Needed for alert {0}?"""

    # parameter list for template variable replacement
    parameters = [
        "get_alert_details_1:action_result.data.*.name",
    ]

    # responses:
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

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30,
                    name="prompt_further_investigation", parameters=parameters, response_types=response_types,
                    callback=create_case_1)

    return


def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
             filtered_results=None, custom_function=None, **kwargs):
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
        get_alert_details_1(action=action, success=success, container=container, results=results, handle=handle,
                            custom_function=custom_function, filtered_artifacts=matched_artifacts_1,
                            filtered_results=matched_results_1)

    return


def create_case_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
                  filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('create_case_1() called')

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'create_case_1' call
    results_data_1 = phantom.collect2(container=container,
                                      datapath=['prompt_further_investigation:action_result.summary.responses.1',
                                                'prompt_further_investigation:action_result.parameter.context.artifact_id'],
                                      action_results=results)
    results_data_2 = phantom.collect2(container=container,
                                      datapath=['get_alert_details_1:action_result.data.*.username',
                                                'get_alert_details_1:action_result.parameter.context.artifact_id'],
                                      action_results=results)

    parameters = []

    # build parameters list for 'create_case_1' call
    for results_item_1 in results_data_1:
        for results_item_2 in results_data_2:
            if results_item_1[0]:
                parameters.append({
                    'case_name': results_item_1[0],
                    'subject': results_item_2[0],
                    'description': "",
                    'assignee': "",
                    'findings': "",
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': results_item_1[1]},
                })

    phantom.act(action="create case", parameters=parameters, assets=['partner'], callback=add_case_event_1,
                name="create_case_1")

    return


def add_case_event_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
                     filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_case_event_1() called')

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'add_case_event_1' call
    container_data = phantom.collect2(container=container,
                                      datapath=['artifact:*.source_data_identifier', 'artifact:*.id'])
    results_data_1 = phantom.collect2(container=container, datapath=['create_case_1:action_result.data.*.number',
                                                                     'create_case_1:action_result.parameter.context.artifact_id'],
                                      action_results=results)

    parameters = []

    # build parameters list for 'add_case_event_1' call
    for container_item in container_data:
        for results_item_1 in results_data_1:
            if results_item_1[0] and container_item[0]:
                parameters.append({
                    'case_number': results_item_1[0],
                    'event_id': container_item[0],
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': results_item_1[1]},
                })

    phantom.act(action="add case event", parameters=parameters, assets=['partner'], callback=prompt_2,
                name="add_case_event_1", parent_action=action)

    return


def prompt_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
             filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_2() called')

    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """Added case event: {0}"""

    # parameter list for template variable replacement
    parameters = [
        "add_case_event_1:action_result.message",
    ]

    # responses:
    response_types = [
        {
            "prompt": "",
            "options": {
                "type": "message",
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_2",
                    parameters=parameters, response_types=response_types, callback=hunt_file_1)

    return


def hunt_file_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
                filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('hunt_file_1() called')

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'hunt_file_1' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=[
        'filtered-data:filter_1:condition_1:artifact:*.cef.fileHashMd5',
        'filtered-data:filter_1:condition_1:artifact:*.id'])

    parameters = []

    # build parameters list for 'hunt_file_1' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            parameters.append({
                'hash': filtered_artifacts_item_1[0],
                'file_name': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_item_1[1]},
            })

    phantom.act(action="hunt file", parameters=parameters, assets=['partner'], callback=prompt_3, name="hunt_file_1")

    return


def prompt_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
             filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_3() called')

    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """What response should be taken for user {0}?"""

    # parameter list for template variable replacement
    parameters = [
        "get_alert_details_1:action_result.data.*.username",
    ]

    # responses:
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

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_3",
                    parameters=parameters, response_types=response_types, callback=decision_2)

    return


def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
               filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('decision_2() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_3:action_result.summary.responses.0", "==", "No response necessary"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        join_update_case_1(action=action, success=success, container=container, results=results, handle=handle,
                           custom_function=custom_function)
        return

    # check for 'elif' condition 2
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_3:action_result.summary.responses.0", "==", "Add user to High Risk"],
        ])

    # call connected blocks if condition 2 matched
    if matched:
        add_highrisk_employee_1(action=action, success=success, container=container, results=results, handle=handle,
                                custom_function=custom_function)
        return

    # check for 'elif' condition 3
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_3:action_result.summary.responses.0", "==", "Add user to Legal Hold"],
        ])

    # call connected blocks if condition 3 matched
    if matched:
        block_user_1(action=action, success=success, container=container, results=results, handle=handle,
                     custom_function=custom_function)
        return

    # check for 'elif' condition 4
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_3:action_result.summary.responses.0", "==", "Block User"],
        ])

    # call connected blocks if condition 4 matched
    if matched:
        prompt_4(action=action, success=success, container=container, results=results, handle=handle,
                 custom_function=custom_function)
        return

    return


def prompt_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
             filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_4() called')

    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """Legal hold matter ID?"""

    # responses:
    response_types = [
        {
            "prompt": "",
            "options": {
                "type": "message",
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_4",
                    response_types=response_types, callback=add_legalhold_custodian_1)

    return


def add_highrisk_employee_1(action=None, success=None, container=None, results=None, handle=None,
                            filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_highrisk_employee_1() called')

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'add_highrisk_employee_1' call
    results_data_1 = phantom.collect2(container=container,
                                      datapath=['get_alert_details_1:action_result.data.*.username',
                                                'get_alert_details_1:action_result.parameter.context.artifact_id'],
                                      action_results=results)

    parameters = []

    # build parameters list for 'add_highrisk_employee_1' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'username': results_item_1[0],
                'note': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act(action="add highrisk employee", parameters=parameters, assets=['partner'], callback=join_update_case_1,
                name="add_highrisk_employee_1")

    return


def block_user_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
                 filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('block_user_1() called')

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'block_user_1' call
    results_data_1 = phantom.collect2(container=container,
                                      datapath=['get_alert_details_1:action_result.data.*.username',
                                                'get_alert_details_1:action_result.parameter.context.artifact_id'],
                                      action_results=results)

    parameters = []

    # build parameters list for 'block_user_1' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'username': results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act(action="block user", parameters=parameters, assets=['partner'], callback=join_update_case_1,
                name="block_user_1")

    return


def add_legalhold_custodian_1(action=None, success=None, container=None, results=None, handle=None,
                              filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_legalhold_custodian_1() called')

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'add_legalhold_custodian_1' call
    results_data_1 = phantom.collect2(container=container,
                                      datapath=['get_alert_details_1:action_result.data.*.username',
                                                'get_alert_details_1:action_result.parameter.context.artifact_id'],
                                      action_results=results)
    results_data_2 = phantom.collect2(container=container, datapath=['prompt_4:action_result.summary.responses.0',
                                                                     'prompt_4:action_result.parameter.context.artifact_id'],
                                      action_results=results)

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

    phantom.act(action="add legalhold custodian", parameters=parameters, assets=['partner'],
                callback=join_update_case_1, name="add_legalhold_custodian_1")

    return


def close_case_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
                 filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('close_case_1() called')

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'close_case_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['create_case_1:action_result.data.*.number',
                                                                     'create_case_1:action_result.parameter.context.artifact_id'],
                                      action_results=results)

    parameters = []

    # build parameters list for 'close_case_1' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'case_number': results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act(action="close case", parameters=parameters, assets=['partner'], name="close_case_1",
                parent_action=action)

    return


def update_case_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
                  filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_case_1() called')

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    # collect data for 'update_case_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['create_case_1:action_result.data.*.number',
                                                                     'create_case_1:action_result.parameter.context.artifact_id'],
                                      action_results=results)
    results_data_2 = phantom.collect2(container=container, datapath=['prompt_3:action_result.summary.responses.0',
                                                                     'prompt_3:action_result.parameter.context.artifact_id'],
                                      action_results=results)

    parameters = []

    # build parameters list for 'update_case_1' call
    for results_item_1 in results_data_1:
        for results_item_2 in results_data_2:
            if results_item_1[0]:
                parameters.append({
                    'case_number': results_item_1[0],
                    'case_name': "",
                    'description': "",
                    'subject': "",
                    'assignee': "",
                    'findings': results_item_2[0],
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': results_item_1[1]},
                })

    phantom.act(action="update case", parameters=parameters, assets=['partner'], callback=close_case_1,
                name="update_case_1")

    return


def join_update_case_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None,
                       filtered_results=None, custom_function=None):
    phantom.debug('join_update_case_1() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(
            action_names=['prompt_3', 'block_user_1', 'add_legalhold_custodian_1', 'add_highrisk_employee_1']):
        # call connected block "update_case_1"
        update_case_1(container=container, handle=handle)

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