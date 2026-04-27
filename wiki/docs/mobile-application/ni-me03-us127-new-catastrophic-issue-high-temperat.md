---
title: "(NI) ME03-US127 New catastrophic issue: High temperature"
sidebar_label: "(NI) ME03-US127 New catastrophic issue: High temperature"
sidebar_position: 397
last_modified: "Jun 07, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages |
|---|---|---|---|
| DRAFT |
| Kiryl Trafimau |
| HALO-19478 - BE: Add a cat.issue: high temperature Open |
| Appendix 14 - List of catastrophic and non-catastrophic issuesMQTT Communication implemented on the back-end |User Story Acceptance criteria Implementation notes

# User Story

\> As a USER I want to get notified when the there is a catastrophic issue with the collar so that I can replace it

## Acceptance criteria

| ID | Acceptance criteria |
|---|---|
| ME03-US127-AC01 | IF Based on Daily Diagnostic catastrophic issue happened according to the rule in the tableTHEN I should see the error text on the Collar diagnostic issue according to the rule in the tableAND I should see grey text on the Collar diagnostic issue according to the rule in the table |Rules

| Section name | Error name | Error validations | Error text to be displayed on the Diagnostics screen in red | Grey text in the diagnostics screen |
|---|---|---|---|---|
| Other | High temperature | Notes after discussion with AntonIt can indicate 'smoking' collar OR collar is under a sunlight for a too long timeWe don't know which temperature is critical.We can potentially measure:-power of discharge (have it in telemetry, need to detect when it's high permanently for a long duration e.g. hour) - need FW implementation to be able to measure it on long duration, now we cannot. -battery % - if discharged very fast (e.g. 10% in 15 min, need to define critical level)-this telling about too hot collar-catastrophic issue - need to compare 2 telemetry's-requires implementation change.-and high temperature (telemetry, but need some extra conditions, e.g. in Texas temperature is high and it's ok, we have 3 chip-indicators inside collar which potentially can be used) - need FW investigate first.Discussed during the BA call with Michael that the FW will be updated to be able to detect this issue | 'High temperature'TBR, should be reviewed by Michael | 'Too high temperature of the collar was detected. Tap here to review our warranty and Protection Plans or contact support for further instructions.'tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103contact support = Dog ParkTBR, should be reviewed by Michael |Note for BA: Add proper row to Appendix 14 when requirements approved

## Implementation notes

| ID | Implementation note |
|---|---|
| ME03-US127-IN01 |  |
