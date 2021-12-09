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

## Playbook

### Installation

The playbook lives in the directory `playbooks/` and is an example of how to respond to a Code42 Alert.

Install the playbook by first creating a tar of the `.py` and `.json` files.

```bash
make playbook
```

Then, upload it to Splunk SOAR.

### Running

To run the playbook from security events out-of-the-box, create a custom label named `code42 alerts`.

Next, make sure you have a Code42 asset that has permissions to retrieve Code42 Alerts and File Events.

In Ingest settings, set the label to the newly created `code42 alerts` label.

Additionally, ensure the playbook named `code42_alert_response_playbook` is active.
