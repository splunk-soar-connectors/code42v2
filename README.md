# Code42 Phantom App V2

Code42 provides simple, fast detection and response to everyday data loss from insider threats by focusing on customer
data on endpoints and the cloud.

## py42

This app is built using <a href="https://github.com/code42/py42">py42</a>, the official Code42 python SDK.

## Objective

This app implements various investigative actions on the Code42 Incydr platform. Additionally, this app
ingests alerts from Code42 to facilitate a timely response.

## How to Configure the App

Access the Asset Settings tab on the Asset Configuration page. Input the cloud instance, username, and password
to use to connect to Code42.

If using the polling feature, you may set the Start Date and End Date for the initial ingest. Otherwise,
it ingests up to 30 days back. Ongoing queries will only get new alerts. Configure the polling interval in the
Ingest Settings tab. Additionally, you can configure which alert severities to poll for, such as HIGH, MEDIUM,
or LOW.

## On Poll

The 'on poll' functionality first ingests the past 30 days of Code42 alerts (or uses the configured state and
end dates). Note that if you use the "poll now" feature, you are limited to the number of containers and
artifacts listed in the parameter fields. Adjust the polling interval in the ingest settings to determine how
frequent polling occurs. The app ingests individual alerts only once unless deleted and re-polled.

## Automatically Run the Playbook

To automatically run the `code42_alert_response` playbook, do the following:

1. Add a custom event label.

Go to Administration -> Event Settings -> Label Settings.
Create a new label named something like “code42 alerts”.

2. Specify the ingest label on the Code42 App.
Go to Apps -> Code42 -> <your asset> -> Ingest Settings -> Edit
The part that is titled “Label to apply to objects from this source”, select your newly created “code42 alerts” label.

3. Delete events, reset your timestamp, and re-poll (either let it happen or use Poll Now).
Notice the new events have a label “code42 alerts” now (in the rows, right after NAME).