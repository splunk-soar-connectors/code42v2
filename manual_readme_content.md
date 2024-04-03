[comment]: # " File: README.md"
[comment]: # ""
[comment]: # "  Copyright (c) 2024 Splunk Inc., Code42"
[comment]: # ""
[comment]: # "  Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "  you may not use this file except in compliance with the License."
[comment]: # "  You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "      http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "  Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "  the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "  either express or implied. See the License for the specific language governing permissions"
[comment]: # "  and limitations under the License."
[comment]: # ""
## Note

This app will be the one supported moving forward, and the [other
version](https://github.com/splunk-soar-connectors/code42) will be deprecated

## py42

This app is built using [py42](https://github.com/code42/py42) , the official Code42 python SDK.

## Objective

This app implements various investigative actions on the Code42 Incydr platform. Additionally, this
app ingests alerts from Code42 to facilitate a timely response.

## How to Configure the App

Access the Asset Settings tab on the Asset Configuration page. Input the cloud instance, username,
and password to use to connect to Code42.

If using the polling feature, you may set the Start Date and End Date for the initial ingest.
Otherwise, it ingests up to 30 days back. Ongoing queries will only get new alerts. Configure the
polling interval in the Ingest Settings tab. Additionally, you can configure which alert severities
to poll for, such as HIGH, LOW, MODERATE or CRITICAL.

## On Poll

The 'on poll' functionality first ingests the past 30 days of Code42 alerts (or uses the configured
start and end dates). Note that if you use the "poll now" feature, you are limited to the number of
containers and artifacts listed in the parameter fields. Adjust the polling interval in the ingest
settings to determine how frequent polling occurs. The app ingests individual alerts only once
unless deleted and re-polled.

## Port Information

The app uses HTTP/ HTTPS protocol for communicating with the Code42 v2 server. Below are the default
ports used by the Splunk SOAR Connector.

| SERVICE NAME | TRANSPORT PROTOCOL | PORT |
|--------------|--------------------|------|
| http         | tcp                | 80   |
| https        | tcp                | 443  |
