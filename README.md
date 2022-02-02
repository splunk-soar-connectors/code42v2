[comment]: # "Auto-generated SOAR connector documentation"
# Code42 v2

Publisher: Code42  
Connector Version: 1\.0\.1  
Product Vendor: Code42  
Product Name: Code42 v2  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

Code42 provides simple, fast detection and response to everyday data loss from insider threats by focusing on customer data on endpoints and the cloud

[comment]: # " File: README.md"
[comment]: # ""
[comment]: # "  Copyright (c) 2022 Splunk Inc., Code42"
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


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Code42 v2 asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**cloud\_instance** |  required  | string | Cloud instance to connect to
**username** |  required  | string | Username to connect with
**password** |  required  | password | Password to connect with
**initial\_poll\_start\_date** |  optional  | string | The start date to use in the initial poll in yyyy\-MM\-dd HH\:MM\:SS format \(defaults to 30 days back\)
**initial\_poll\_end\_date** |  optional  | string | The end date to use in the initial poll in yyyy\-MM\-dd HH\:MM\:SS format \(defaults to the current time\)
**severity\_to\_poll\_for** |  optional  | string | A comma\-separated list of alert severities to poll for, such as HIGH, LOW, MODERATE or CRITICAL \(defaults to getting all alerts\)

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[on poll](#action-on-poll) - Callback action for the on\_poll ingest functionality  
[add departing employee](#action-add-departing-employee) - Add a departing employee to the departing employees detection list  
[remove departing employee](#action-remove-departing-employee) - Remove a departing employee from the departing employees detection list  
[list departing employees](#action-list-departing-employees) - Returns a list of users who are on the departing employees list  
[get departing employee](#action-get-departing-employee) - Get a departing employee  
[add highrisk employee](#action-add-highrisk-employee) - Add a high risk employee to the high risk employees detection list  
[remove highrisk employee](#action-remove-highrisk-employee) - Remove a high risk employee from the high risk employees detection list  
[list highrisk employees](#action-list-highrisk-employees) - Returns a list of users who are on the high\-risk employees list  
[get highrisk employee](#action-get-highrisk-employee) - Get a high risk employee  
[add highrisk tag](#action-add-highrisk-tag) - Add a risk tag to a user  
[remove highrisk tag](#action-remove-highrisk-tag) - Remove a risk tag from a user  
[get alert details](#action-get-alert-details) - Get alert details  
[search alerts](#action-search-alerts) - Search Alerts  
[set alert state](#action-set-alert-state) - Set the state of the alert  
[list users](#action-list-users) - List all users  
[create user](#action-create-user) - Create a new Code42 user account  
[block user](#action-block-user) - Blocks a user from accessing their Code42 account  
[deactivate user](#action-deactivate-user) - Deactivates user's Code42 account  
[reactivate user](#action-reactivate-user) - Reactivates a deactivated user's Code42 account  
[unblock user](#action-unblock-user) - Unblocks a user, allowing access to their Code42 account  
[get user profile](#action-get-user-profile) - Get user profile  
[add legalhold custodian](#action-add-legalhold-custodian) - Add a user \(custodian\) to a legal hold matter  
[remove legalhold custodian](#action-remove-legalhold-custodian) - Remove user \(custodian\) from a legal hold matter  
[create case](#action-create-case) - Create a Code42 case  
[update case](#action-update-case) - Update the details of a case  
[close case](#action-close-case) - Change the status of a Code42 case to 'CLOSED'  
[list cases](#action-list-cases) - List Code42 Cases  
[add case event](#action-add-case-event) - Associates a file event with a Code42 case  
[hunt file](#action-hunt-file) - Searches Code42 for a backed\-up file with a matching hash and downloads it  
[run query](#action-run-query) - Search for Code42 file events  
[run advanced query](#action-run-advanced-query) - Run an advanced query using JSON  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'on poll'
Callback action for the on\_poll ingest functionality

Type: **ingest**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container\_id** |  optional  | Alert IDs to limit the ingestion to \(limited to 100\) | string | 
**start\_time** |  optional  | Parameter ignored in this app | string | 
**end\_time** |  optional  | Parameter ignored in this app | string | 
**container\_count** |  optional  | Maximum number of alerts to create \(only used in Poll Now\) | numeric | 
**artifact\_count** |  optional  | Maximum number of artifacts to create \(only used in Poll Now\) | numeric | 

#### Action Output
No Output  

## action: 'add departing employee'
Add a departing employee to the departing employees detection list

Type: **contain**  
Read only: **False**

There is a short delay before you can query the updated results\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username of the employee to add | string |  `email`  `user name` 
**departure\_date** |  optional  | Date of departure for employee in format yyyy\-MM\-dd | string | 
**note** |  optional  | A note to include | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.departure\_date | string | 
action\_result\.parameter\.note | string | 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.departureDate | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove departing employee'
Remove a departing employee from the departing employees detection list

Type: **correct**  
Read only: **False**

There is a short delay before you can query the updated results\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username of the employee to remove | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.data\.\*\.userId | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list departing employees'
Returns a list of users who are on the departing employees list

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filter\_type** |  optional  | Filters the results based on specific filters | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.filter\_type | string | 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.riskFactors\.\*\.tag | string |  `code42 risk tag` 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.numEvents | numeric | 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.totalBytes | numeric | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.data\.\*\.departureDate | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_count | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get departing employee'
Get a departing employee

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | The username of the departing employee to get | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.data\.\*\.departureDate | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.is\_departing\_employee | boolean | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add highrisk employee'
Add a high risk employee to the high risk employees detection list

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username of the employee to add | string |  `email`  `user name` 
**note** |  optional  | A note to include | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.note | string | 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove highrisk employee'
Remove a high risk employee from the high risk employees detection list

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username of the employee to remove | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.data\.\*\.userId | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list highrisk employees'
Returns a list of users who are on the high\-risk employees list

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**filter\_type** |  optional  | Filters the results based on specific filters | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.filter\_type | string | 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.numEvents | numeric | 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.totalBytes | numeric | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.summary\.total\_count | numeric | 
action\_result\.data\.\*\.riskFactors\.\*\.tag | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get highrisk employee'
Get a high risk employee

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | The username of the high risk employee to get | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.riskFactors\.\*\.tag | string |  `code42 risk tag` 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.is\_high\_risk\_employee | boolean | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add highrisk tag'
Add a risk tag to a user

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username of the employee to add a risk tag to | string |  `email`  `user name` 
**risk\_tag** |  required  | A risk tag to add to the user | string |  `code42 risk tag` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.risk\_tag | string |  `code42 risk tag` 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.data\.\*\.riskFactors\.\*\.tag | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove highrisk tag'
Remove a risk tag from a user

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username of the employee to remove a risk tag from | string |  `email`  `user name` 
**risk\_tag** |  required  | A risk tag to remove from the user | string |  `code42 risk tag` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.risk\_tag | string |  `code42 risk tag` 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.riskFactors\.\*\.tag | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get alert details'
Get alert details

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**alert\_id** |  required  | ID of the alert to retrieve | string |  `code42 alert id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.alert\_id | string |  `code42 alert id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.actor | string |  `email`  `user name` 
action\_result\.data\.\*\.actorId | string |  `email` 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.data\.\*\.type | string | 
action\_result\.data\.\*\.severity | string | 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.note\.id | string | 
action\_result\.data\.\*\.note\.type$ | string | 
action\_result\.data\.\*\.note\.message | string | 
action\_result\.data\.\*\.note\.lastModifiedAt | string | 
action\_result\.data\.\*\.note\.lastModifiedBy | string |  `user name`  `email` 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.ruleId | string | 
action\_result\.data\.\*\.target | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.ruleSource | string | 
action\_result\.data\.\*\.observations\.\*\.id | string | 
action\_result\.data\.\*\.observations\.\*\.data\.id | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.name | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.path | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.size | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.eventId | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.category | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.observedAt | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.riskSeverityInfo\.score | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.riskSeverityInfo\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.riskSeverityInfo\.severity | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.riskSeverityInfo\.matchedRiskIndicators\.\*\.name | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.riskSeverityInfo\.matchedRiskIndicators\.\*\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.data\.files\.\*\.riskSeverityInfo\.matchedRiskIndicators\.\*\.weight | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.data\.fileCount | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.totalFileSize | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.appReadDetails\.\*\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.data\.appReadDetails\.\*\.destinationName | string | 
action\_result\.data\.\*\.observations\.\*\.data\.appReadDetails\.\*\.destinationCategory | string | 
action\_result\.data\.\*\.observations\.\*\.data\.fileCategories\.\*\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.data\.fileCategories\.\*\.category | string | 
action\_result\.data\.\*\.observations\.\*\.data\.fileCategories\.\*\.fileCount | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.fileCategories\.\*\.isSignificant | boolean | 
action\_result\.data\.\*\.observations\.\*\.data\.fileCategories\.\*\.totalFileSize | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.lastActivityAt | string | 
action\_result\.data\.\*\.observations\.\*\.data\.firstActivityAt | string | 
action\_result\.data\.\*\.observations\.\*\.data\.isRemoteActivity | boolean | 
action\_result\.data\.\*\.observations\.\*\.data\.riskSeveritySummary\.\*\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.data\.riskSeveritySummary\.\*\.severity | string | 
action\_result\.data\.\*\.observations\.\*\.data\.riskSeveritySummary\.\*\.numEvents | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.riskSeveritySummary\.\*\.summarizedRiskIndicators\.\*\.name | string | 
action\_result\.data\.\*\.observations\.\*\.data\.riskSeveritySummary\.\*\.summarizedRiskIndicators\.\*\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.data\.riskSeveritySummary\.\*\.summarizedRiskIndicators\.\*\.numEvents | numeric | 
action\_result\.data\.\*\.observations\.\*\.data\.destinationIsSignificant | boolean | 
action\_result\.data\.\*\.observations\.\*\.data\.exposureTypeIsSignificant | boolean | 
action\_result\.data\.\*\.observations\.\*\.data\.fileCategoryIsSignificant | boolean | 
action\_result\.data\.\*\.observations\.\*\.data\.riskSeverityIsSignificant | boolean | 
action\_result\.data\.\*\.observations\.\*\.type | string | 
action\_result\.data\.\*\.observations\.\*\.type$ | string | 
action\_result\.data\.\*\.observations\.\*\.observedAt | string | 
action\_result\.data\.\*\.riskSeverity | string | 
action\_result\.data\.\*\.stateLastModifiedAt | string | 
action\_result\.data\.\*\.stateLastModifiedBy | string |  `user name`  `email` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
action\_result\.summary\.username | string |  `email`  `user name` 
action\_result\.summary\.user\_id | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'search alerts'
Search Alerts

Type: **investigate**  
Read only: **True**

All query parameters are optional; at least one search term is required\. All query parameters are in logical AND with each other\. Defaults to last 30 days if no date range is provided\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  optional  | Username of the actor listed on alert | string |  `email`  `user name` 
**alert\_state** |  optional  | Alert state | string |  `code42 alert state` 
**start\_date** |  optional  | Beginning of date range to search\. Time \(in UTC\) may also be supplied but is not required | string | 
**end\_date** |  optional  | End of date range to search\. Time \(in UTC\) may also be supplied but is not required | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.alert\_state | string |  `code42 alert state` 
action\_result\.parameter\.start\_date | string | 
action\_result\.parameter\.end\_date | string | 
action\_result\.data\.\*\.actor | string |  `email`  `user name` 
action\_result\.data\.\*\.state | string | 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.severity | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.type | string | 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.ruleId | string | 
action\_result\.data\.\*\.target | string | 
action\_result\.data\.\*\.actorId | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.ruleSource | string | 
action\_result\.data\.\*\.riskSeverity | string | 
action\_result\.data\.\*\.stateLastModifiedAt | string | 
action\_result\.data\.\*\.stateLastModifiedBy | string |  `user name`  `email` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_count | numeric | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'set alert state'
Set the state of the alert

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**alert\_id** |  required  | Alert ID | string |  `code42 alert id` 
**alert\_state** |  required  | Alert State | string | 
**note** |  optional  | A note to include | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.alert\_id | string |  `code42 alert id` 
action\_result\.parameter\.alert\_state | string | 
action\_result\.parameter\.note | string | 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.alert\_id | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list users'
List all users

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**org\_uid** |  optional  | Organization UID | string | 
**role\_id** |  optional  | User role ID | numeric | 
**email** |  optional  | User's email | string |  `email` 
**user\_status** |  optional  | User's status \(Default\: All\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.org\_uid | string | 
action\_result\.parameter\.role\_id | numeric | 
action\_result\.parameter\.email | string |  `email` 
action\_result\.parameter\.user\_status | string | 
action\_result\.data\.\*\.email | string |  `email` 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.orgId | numeric | 
action\_result\.data\.\*\.active | boolean | 
action\_result\.data\.\*\.orgUid | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.userId | numeric | 
action\_result\.data\.\*\.blocked | boolean | 
action\_result\.data\.\*\.invited | boolean | 
action\_result\.data\.\*\.orgName | string | 
action\_result\.data\.\*\.orgType | string | 
action\_result\.data\.\*\.userUId | string | 
action\_result\.data\.\*\.lastName | string | 
action\_result\.data\.\*\.licenses | string | 
action\_result\.data\.\*\.username | string |  `user name`  `email` 
action\_result\.data\.\*\.firstName | string | 
action\_result\.data\.\*\.emailPromo | boolean | 
action\_result\.data\.\*\.userExtRef | string | 
action\_result\.data\.\*\.creationDate | string | 
action\_result\.data\.\*\.quotaInBytes | numeric | 
action\_result\.data\.\*\.passwordReset | boolean | 
action\_result\.data\.\*\.modificationDate | string | 
action\_result\.data\.\*\.usernameIsAnEmail | boolean | 
action\_result\.data\.\*\.localAuthenticationOnly | boolean | 
action\_result\.data\.\*\.userUid | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_users | numeric | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create user'
Create a new Code42 user account

Type: **generic**  
Read only: **False**

There is a short delay before you will be able to add the new user to the departing employee or high risk employee lists\. For security reasons, we strongly recommend you to reset your password after first time login\. <b>Note\:</b> If the provided username already exists for a user, it will be updated in the database instead\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**org\_uid** |  required  | Org UID to create user in | string | 
**username** |  required  | Username to create | string |  `email`  `user name` 
**password** |  required  | Password for newly created user | string | 
**first\_name** |  optional  | User's first name | string | 
**last\_name** |  optional  | User's last name | string | 
**notes** |  optional  | Notes about user | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.org\_uid | string | 
action\_result\.parameter\.first\_name | string | 
action\_result\.parameter\.last\_name | string | 
action\_result\.parameter\.notes | string | 
action\_result\.parameter\.password | password | 
action\_result\.data\.\*\.email | string |  `user name`  `email` 
action\_result\.data\.\*\.notes | string | 
action\_result\.data\.\*\.orgId | numeric | 
action\_result\.data\.\*\.active | boolean | 
action\_result\.data\.\*\.orgUid | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.userId | numeric | 
action\_result\.data\.\*\.blocked | boolean | 
action\_result\.data\.\*\.invited | boolean | 
action\_result\.data\.\*\.orgName | string | 
action\_result\.data\.\*\.orgType | string | 
action\_result\.data\.\*\.userUid | string | 
action\_result\.data\.\*\.lastName | string | 
action\_result\.data\.\*\.username | string |  `user name`  `email` 
action\_result\.data\.\*\.firstName | string | 
action\_result\.data\.\*\.emailPromo | boolean | 
action\_result\.data\.\*\.userExtRef | string | 
action\_result\.data\.\*\.creationDate | string | 
action\_result\.data\.\*\.quotaInBytes | numeric | 
action\_result\.data\.\*\.passwordReset | boolean | 
action\_result\.data\.\*\.modificationDate | string | 
action\_result\.data\.\*\.usernameIsAnEmail | string | 
action\_result\.data\.\*\.localAuthenticationOnly | boolean | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.user\_id | string | 
action\_result\.summary\.username | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'block user'
Blocks a user from accessing their Code42 account

Type: **contain**  
Read only: **False**

Blocks a user from accessing their Code42 account \(endpoint backup/security processes continue while blocked\)\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username to block | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'deactivate user'
Deactivates user's Code42 account

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username to deactivate | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.status | string | 
action\_result\.data | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'reactivate user'
Reactivates a deactivated user's Code42 account

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username to reactivate | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.status | string | 
action\_result\.data | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'unblock user'
Unblocks a user, allowing access to their Code42 account

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username to unblock | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.status | string | 
action\_result\.data | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get user profile'
Get user profile

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | The username associated with the user profile to get | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.data\.\*\.city | string | 
action\_result\.data\.\*\.cloudUsernames\.\*\.username | string |  `email`  `user name` 
action\_result\.data\.\*\.country | string | 
action\_result\.data\.\*\.department | string | 
action\_result\.data\.\*\.displayName | string | 
action\_result\.data\.\*\.managerDisplayName | string | 
action\_result\.data\.\*\.managerUsername | string |  `email`  `user name` 
action\_result\.data\.\*\.riskFactors\.\*\.tag | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.data\.\*\.title | string | 
action\_result\.data\.\*\.userId | string | 
action\_result\.data\.\*\.userName | string |  `email`  `user name` 
action\_result\.data\.\*\.type$ | string | 
action\_result\.data\.\*\.tenantId | string | 
action\_result\.data\.\*\.notes | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
action\_result\.summary\.user\_id | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add legalhold custodian'
Add a user \(custodian\) to a legal hold matter

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username to be added to legal hold matter | string |  `email`  `user name` 
**matter\_id** |  required  | The identifier of the legal hold matter | string |  `code42 matter id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.matter\_id | string |  `code42 matter id` 
action\_result\.data\.\*\.user\.email | string |  `user name`  `email` 
action\_result\.data\.\*\.user\.userUid | string | 
action\_result\.data\.\*\.user\.username | string |  `user name`  `email` 
action\_result\.data\.\*\.user\.userExtRef | string | 
action\_result\.data\.\*\.active | boolean | 
action\_result\.data\.\*\.legalHold\.name | string | 
action\_result\.data\.\*\.legalHold\.legalHoldUid | string | 
action\_result\.data\.\*\.creationDate | string | 
action\_result\.data\.\*\.legalHoldMembershipUid | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove legalhold custodian'
Remove user \(custodian\) from a legal hold matter

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**username** |  required  | Username of user to be removed from legal hold matter | string |  `email`  `user name` 
**matter\_id** |  required  | ID of the legal hold matter to remove the user from | string |  `code42 matter id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.matter\_id | string |  `code42 matter id` 
action\_result\.data | string | 
action\_result\.data\.\*\.userId | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create case'
Create a Code42 case

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case\_name** |  required  | Case name | string | 
**subject** |  optional  | Subject of case \(username\) | string |  `email`  `user name` 
**description** |  optional  | Description | string | 
**assignee** |  optional  | Assignee \(username\) | string |  `email`  `user name` 
**findings** |  optional  | Findings \(markdown text\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.case\_name | string | 
action\_result\.parameter\.description | string | 
action\_result\.parameter\.subject | string |  `email`  `user name` 
action\_result\.parameter\.assignee | string |  `email`  `user name` 
action\_result\.parameter\.findings | string | 
action\_result\.data\.\*\.number | string |  `code42 case number` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.assignee | string | 
action\_result\.data\.\*\.findings | string | 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.updatedAt | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.subjectUsername | string | 
action\_result\.data\.\*\.assigneeUsername | string | 
action\_result\.data\.\*\.createdByUserUid | string | 
action\_result\.data\.\*\.createdByUsername | string |  `user name`  `email` 
action\_result\.data\.\*\.lastModifiedByUserUid | string | 
action\_result\.data\.\*\.lastModifiedByUsername | string |  `user name`  `email` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.case\_number | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'update case'
Update the details of a case

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case\_number** |  required  | Case number | numeric |  `code42 case number` 
**case\_name** |  optional  | Case name | string | 
**description** |  optional  | Description | string | 
**subject** |  optional  | Subject | string |  `email`  `user name` 
**assignee** |  optional  | Assignee | string |  `email`  `user name` 
**findings** |  optional  | Findings \(markdown\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.case\_number | numeric |  `code42 case number` 
action\_result\.parameter\.case\_name | string | 
action\_result\.parameter\.description | string | 
action\_result\.parameter\.subject | string |  `email`  `user name` 
action\_result\.parameter\.assignee | string |  `email`  `user name` 
action\_result\.parameter\.findings | string | 
action\_result\.data\.\*\.number | numeric |  `code42 case number` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.subjectUsername | string |  `email`  `user name` 
action\_result\.data\.\*\.assigneeUsername | string |  `email`  `user name` 
action\_result\.data\.\*\.findings | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.assignee | string | 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.updatedAt | string | 
action\_result\.data\.\*\.createdByUserUid | string | 
action\_result\.data\.\*\.createdByUsername | string |  `user name`  `email` 
action\_result\.data\.\*\.lastModifiedByUserUid | string | 
action\_result\.data\.\*\.lastModifiedByUsername | string |  `user name`  `email` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.case\_number | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'close case'
Change the status of a Code42 case to 'CLOSED'

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case\_number** |  required  | Case number | numeric |  `code42 case number` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.case\_number | numeric |  `code42 case number` 
action\_result\.data | string | 
action\_result\.data\.\*\.number | numeric |  `code42 case number` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.subjectUsername | string |  `email`  `user name` 
action\_result\.data\.\*\.assigneeUsername | string |  `email`  `user name` 
action\_result\.data\.\*\.findings | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.assignee | string | 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.updatedAt | string | 
action\_result\.data\.\*\.createdByUserUid | string | 
action\_result\.data\.\*\.createdByUsername | string |  `user name`  `email` 
action\_result\.data\.\*\.lastModifiedByUserUid | string | 
action\_result\.data\.\*\.lastModifiedByUsername | string |  `user name`  `email` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.case\_number | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list cases'
List Code42 Cases

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**status** |  required  | Filter cases by status | string | 
**assignee** |  optional  | Filter cases by assignee username | string |  `email`  `user name` 
**subject** |  optional  | Filter cases by subject username | string |  `email`  `user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.status | string | 
action\_result\.parameter\.assignee | string |  `email`  `user name` 
action\_result\.parameter\.subject | string |  `email`  `user name` 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.number | numeric |  `code42 case number` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.subjectUsername | string |  `email`  `user name` 
action\_result\.data\.\*\.assigneeUsername | string |  `email`  `user name` 
action\_result\.data\.\*\.createdAt | string | 
action\_result\.data\.\*\.createdByUsername | string |  `email`  `user name` 
action\_result\.data\.\*\.subject | string | 
action\_result\.data\.\*\.assignee | string | 
action\_result\.data\.\*\.updatedAt | string | 
action\_result\.data\.\*\.createdByUserUid | string | 
action\_result\.data\.\*\.lastModifiedByUserUid | string | 
action\_result\.data\.\*\.lastModifiedByUsername | string |  `user name`  `email` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_count | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add case event'
Associates a file event with a Code42 case

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case\_number** |  required  | Case number | numeric |  `code42 case number` 
**event\_id** |  required  | Event ID | string |  `code42 file event` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.case\_number | string |  `code42 case number` 
action\_result\.parameter\.event\_id | string |  `code42 file event` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.case\_number | numeric | 
action\_result\.summary\.event\_id | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'hunt file'
Searches Code42 for a backed\-up file with a matching hash and downloads it

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hash** |  required  | The MD5 or SHA256 hash of the file to download | string |  `md5`  `sha256` 
**file\_name** |  optional  | The name to give to the file after it is downloaded\. If not supplied, the hash will be used | string |  `file name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.hash | string |  `md5`  `sha256` 
action\_result\.parameter\.file\_name | string |  `file name` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'run query'
Search for Code42 file events

Type: **investigate**  
Read only: **True**

You can use wildcards \(\*,?\) with most string\-based fields\. All query parameters are optional; at least one search term is required\. All query parameters are in logical AND with each other\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start\_date** |  optional  | Beginning of date range to search\. Time \(in UTC\) may also be supplied but is not required | string | 
**end\_date** |  optional  | End of date range to search\. Time \(in UTC\) may also be supplied but is not required | string | 
**file\_hash** |  optional  | MD5 or SHA256 hash of a file | string |  `md5`  `sha256` 
**file\_name** |  optional  | Name of the file observed | string |  `file name` 
**file\_path** |  optional  | Path of the file observed | string |  `file path` 
**file\_category** |  optional  | Category of the file observed | string |  `code42 file category` 
**username** |  optional  | Name of the user associated with the event | string |  `email`  `user name` 
**hostname** |  optional  | Hostname | string |  `host name` 
**private\_ip** |  optional  | Private IPv4 or IPv6 address | string |  `ip`  `ipv6` 
**public\_ip** |  optional  | Public IPv4 or IPv6 address | string |  `ip`  `ipv6` 
**exposure\_type** |  optional  | Type of exposure that occurred | string |  `code42 exposure type` 
**process\_name** |  optional  | Process name involved in the exposure | string |  `code42 process name` 
**url** |  optional  | Urls of all the browser tabs open during exposure | string |  `url` 
**window\_title** |  optional  | Names of all the open browser tabs or windows during exposure | string |  `code42 window title` 
**untrusted\_only** |  optional  | Return only events representing untrusted activity | boolean | 
**max\_results** |  optional  | Maximum number of results to fetch \(default\: 1000\) | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.start\_date | string | 
action\_result\.parameter\.end\_date | string | 
action\_result\.parameter\.file\_name | string |  `file name` 
action\_result\.parameter\.file\_hash | string |  `md5`  `sha256` 
action\_result\.parameter\.file\_path | string |  `file path` 
action\_result\.parameter\.untrusted\_only | boolean | 
action\_result\.parameter\.file\_category | string |  `code42 file category` 
action\_result\.parameter\.username | string |  `email`  `user name` 
action\_result\.parameter\.hostname | string |  `host name` 
action\_result\.parameter\.private\_ip | string |  `ip`  `ipv6` 
action\_result\.parameter\.public\_ip | string |  `ip`  `ipv6` 
action\_result\.parameter\.exposure\_type | string |  `code42 exposure type` 
action\_result\.parameter\.process\_name | string |  `code42 process name` 
action\_result\.parameter\.url | string |  `url` 
action\_result\.parameter\.window\_title | string |  `code42 window title` 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.data\.\*\.eventTimestamp | string | 
action\_result\.data\.\*\.eventType | string | 
action\_result\.data\.\*\.fileName | string |  `file name` 
action\_result\.data\.\*\.filePath | string |  `file path` 
action\_result\.data\.\*\.createTimestamp | string | 
action\_result\.data\.\*\.modifyTimestamp | string | 
action\_result\.data\.\*\.md5Checksum | string |  `md5` 
action\_result\.data\.\*\.sha256Checksum | string |  `sha256` 
action\_result\.data\.\*\.url | string |  `url` 
action\_result\.data\.\*\.actor | string |  `email`  `user name` 
action\_result\.data\.\*\.fileId | string | 
action\_result\.data\.\*\.shared | string | 
action\_result\.data\.\*\.source | string | 
action\_result\.data\.\*\.tabUrl | string |  `url` 
action\_result\.data\.\*\.windowTitle\.\*\.windowTitle | string |  `code42 window title` 
action\_result\.data\.\*\.eventId | string |  `code42 file event` 
action\_result\.data\.\*\.trusted | boolean | 
action\_result\.data\.\*\.userUid | string | 
action\_result\.data\.\*\.fileSize | numeric | 
action\_result\.data\.\*\.fileType | string | 
action\_result\.data\.\*\.deviceUid | string | 
action\_result\.data\.\*\.emailFrom | string |  `email`  `user name` 
action\_result\.data\.\*\.fileOwner | string | 
action\_result\.data\.\*\.riskScore | string | 
action\_result\.data\.\*\.domainName | string |  `domain` 
action\_result\.data\.\*\.osHostName | string |  `host name` 
action\_result\.data\.\*\.emailSender | string |  `email`  `user name` 
action\_result\.data\.\*\.printerName | string | 
action\_result\.data\.\*\.processName | string | 
action\_result\.data\.\*\.cloudDriveId | string | 
action\_result\.data\.\*\.emailSubject | string | 
action\_result\.data\.\*\.fileCategory | string | 
action\_result\.data\.\*\.printJobName | string | 
action\_result\.data\.\*\.processOwner | string | 
action\_result\.data\.\*\.riskSeverity | string | 
action\_result\.data\.\*\.deviceUserName | string |  `email`  `user name` 
action\_result\.data\.\*\.remoteActivity | string | 
action\_result\.data\.\*\.destinationName | string | 
action\_result\.data\.\*\.emailRecipients | string | 
action\_result\.data\.\*\.mimeTypeByBytes | string | 
action\_result\.data\.\*\.publicIpAddress | string |  `ip` 
action\_result\.data\.\*\.syncDestination | string | 
action\_result\.data\.\*\.mimeTypeMismatch | boolean | 
action\_result\.data\.\*\.insertionTimestamp | string | 
action\_result\.data\.\*\.outsideActiveHours | boolean | 
action\_result\.data\.\*\.privateIpAddresses | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.removableMediaName | string | 
action\_result\.data\.\*\.destinationCategory | string | 
action\_result\.data\.\*\.emailDlpPolicyNames | string | 
action\_result\.data\.\*\.fileCategoryByBytes | string | 
action\_result\.data\.\*\.mimeTypeByExtension | string | 
action\_result\.data\.\*\.operatingSystemUser | string | 
action\_result\.data\.\*\.detectionSourceAlias | string | 
action\_result\.data\.\*\.removableMediaVendor | string | 
action\_result\.data\.\*\.removableMediaBusType | string | 
action\_result\.data\.\*\.printedFilesBackupPath | string | 
action\_result\.data\.\*\.removableMediaCapacity | string | 
action\_result\.data\.\*\.fileCategoryByExtension | string | 
action\_result\.data\.\*\.removableMediaMediaName | string | 
action\_result\.data\.\*\.removableMediaSerialNumber | string | 
action\_result\.data\.\*\.tabs\.\*\.url | string | 
action\_result\.data\.\*\.tabs\.\*\.title | string | 
action\_result\.data\.\*\.tabs\.\*\.urlError | string | 
action\_result\.data\.\*\.tabs\.\*\.titleError | string | 
action\_result\.data\.\*\.reportId | string | 
action\_result\.data\.\*\.reportName | string | 
action\_result\.data\.\*\.reportType | string | 
action\_result\.data\.\*\.sourceName | string | 
action\_result\.data\.\*\.trustReason | string | 
action\_result\.data\.\*\.riskIndicators\.\*\.name | string | 
action\_result\.data\.\*\.riskIndicators\.\*\.weight | numeric | 
action\_result\.data\.\*\.sourceCategory | string | 
action\_result\.data\.\*\.reportDescription | string | 
action\_result\.data\.\*\.reportRecordCount | string | 
action\_result\.data\.\*\.reportColumnHeaders | string | 
action\_result\.data\.\*\.sourceTabs\.\*\.url | string |  `url` 
action\_result\.data\.\*\.sourceTabs\.\*\.title | string | 
action\_result\.data\.\*\.sourceTabs\.\*\.urlError | string | 
action\_result\.data\.\*\.sourceTabs\.\*\.titleError | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_count | numeric | 
action\_result\.summary\.results\_returned\_count | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'run advanced query'
Run an advanced query using JSON

Type: **investigate**  
Read only: **True**

If page\-related keys \(pgNum, pgSize, pgToken\) are available in the query, they will be ignored\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**json\_query** |  required  | The raw JSON of the query to execute | string | 
**max\_results** |  optional  | Maximum number of results to fetch \(default\: 1000\) | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.json\_query | string | 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.data\.\*\.eventTimestamp | string | 
action\_result\.data\.\*\.eventType | string | 
action\_result\.data\.\*\.fileName | string |  `file name` 
action\_result\.data\.\*\.filePath | string |  `file path` 
action\_result\.data\.\*\.createTimestamp | string | 
action\_result\.data\.\*\.modifyTimestamp | string | 
action\_result\.data\.\*\.md5Checksum | string |  `md5` 
action\_result\.data\.\*\.sha256Checksum | string |  `sha256` 
action\_result\.data\.\*\.url | string |  `url` 
action\_result\.data\.\*\.actor | string | 
action\_result\.data\.\*\.fileId | string | 
action\_result\.data\.\*\.shared | string | 
action\_result\.data\.\*\.source | string | 
action\_result\.data\.\*\.tabUrl | string |  `url` 
action\_result\.data\.\*\.eventId | string |  `code42 file event` 
action\_result\.data\.\*\.trusted | boolean | 
action\_result\.data\.\*\.userUid | string | 
action\_result\.data\.\*\.fileSize | numeric | 
action\_result\.data\.\*\.fileType | string | 
action\_result\.data\.\*\.deviceUid | string | 
action\_result\.data\.\*\.emailFrom | string |  `email`  `user name` 
action\_result\.data\.\*\.fileOwner | string | 
action\_result\.data\.\*\.riskScore | numeric | 
action\_result\.data\.\*\.domainName | string |  `domain` 
action\_result\.data\.\*\.osHostName | string |  `host name` 
action\_result\.data\.\*\.emailSender | string |  `email`  `user name` 
action\_result\.data\.\*\.printerName | string | 
action\_result\.data\.\*\.processName | string | 
action\_result\.data\.\*\.cloudDriveId | string | 
action\_result\.data\.\*\.emailSubject | string | 
action\_result\.data\.\*\.fileCategory | string | 
action\_result\.data\.\*\.printJobName | string | 
action\_result\.data\.\*\.processOwner | string | 
action\_result\.data\.\*\.riskSeverity | string | 
action\_result\.data\.\*\.deviceUserName | string |  `email`  `user name` 
action\_result\.data\.\*\.remoteActivity | string | 
action\_result\.data\.\*\.destinationName | string | 
action\_result\.data\.\*\.emailRecipients | string | 
action\_result\.data\.\*\.mimeTypeByBytes | string | 
action\_result\.data\.\*\.publicIpAddress | string |  `ip` 
action\_result\.data\.\*\.syncDestination | string | 
action\_result\.data\.\*\.mimeTypeMismatch | boolean | 
action\_result\.data\.\*\.insertionTimestamp | string | 
action\_result\.data\.\*\.outsideActiveHours | boolean | 
action\_result\.data\.\*\.privateIpAddresses | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.removableMediaName | string | 
action\_result\.data\.\*\.destinationCategory | string | 
action\_result\.data\.\*\.emailDlpPolicyNames | string | 
action\_result\.data\.\*\.fileCategoryByBytes | string | 
action\_result\.data\.\*\.mimeTypeByExtension | string | 
action\_result\.data\.\*\.operatingSystemUser | string | 
action\_result\.data\.\*\.detectionSourceAlias | string | 
action\_result\.data\.\*\.removableMediaVendor | string | 
action\_result\.data\.\*\.removableMediaBusType | string | 
action\_result\.data\.\*\.printedFilesBackupPath | string | 
action\_result\.data\.\*\.removableMediaCapacity | string | 
action\_result\.data\.\*\.fileCategoryByExtension | string | 
action\_result\.data\.\*\.removableMediaMediaName | string | 
action\_result\.data\.\*\.removableMediaSerialNumber | string | 
action\_result\.data\.\*\.tabs\.\*\.url | string |  `url` 
action\_result\.data\.\*\.tabs\.\*\.title | string | 
action\_result\.data\.\*\.tabs\.\*\.urlError | string | 
action\_result\.data\.\*\.tabs\.\*\.titleError | string | 
action\_result\.data\.\*\.reportId | string | 
action\_result\.data\.\*\.reportName | string | 
action\_result\.data\.\*\.reportType | string | 
action\_result\.data\.\*\.sourceName | string | 
action\_result\.data\.\*\.trustReason | string | 
action\_result\.data\.\*\.windowTitle\.\*\.windowTitle | string | 
action\_result\.data\.\*\.riskIndicators\.\*\.name | string | 
action\_result\.data\.\*\.riskIndicators\.\*\.weight | numeric | 
action\_result\.data\.\*\.sourceCategory | string | 
action\_result\.data\.\*\.reportDescription | string | 
action\_result\.data\.\*\.reportRecordCount | string | 
action\_result\.data\.\*\.reportColumnHeaders | string | 
action\_result\.data\.\*\.sourceTabs\.\*\.url | string | 
action\_result\.data\.\*\.sourceTabs\.\*\.title | string | 
action\_result\.data\.\*\.sourceTabs\.\*\.urlError | string | 
action\_result\.data\.\*\.sourceTabs\.\*\.titleError | string | 
action\_result\.summary\.results\_returned\_count | numeric | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_count | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 