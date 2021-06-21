# File: code42_view.py
# Copyright (c) 2018-2021 Splunk Inc.
#
# Licensed under Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
#


def get_ctx_result(provides, result):
    """Function that parses data."""

    ctx_result = {}

    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result["param"] = param

    if summary:
        ctx_result["summary"] = summary
    ctx_result["action"] = provides
    if not data:
        single_result_actions = [
            "get departing employee",
            "get highrisk employee",
            "get user profile",
        ]
        ctx_result["data"] = {} if provides in single_result_actions else []
        return ctx_result

    ctx_result["data"] = data

    return ctx_result


def display_view(provides, all_app_runs, context):
    """Function that displays view."""

    context["results"] = results = []
    for summary, action_results in all_app_runs:
        for result in action_results:

            ctx_result = get_ctx_result(provides, result)
            if not ctx_result:
                continue
            results.append(ctx_result)

    return f"code42_{provides.replace(' ', '_')}.html"
