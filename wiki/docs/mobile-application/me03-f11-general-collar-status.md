---
title: "ME03-F11. General collar status"
sidebar_label: "ME03-F11. General collar status"
sidebar_position: 633
author: "Galina Lonskaya"
---

| Document owners | Linear/Jira ticket | History of changes |
|---|---|---|
| Mariya Kolyada Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-150/[ios]-collar-status-states |
| 12 Feb 2025 draft user story is created |## User story

\> As Halo app account owner, I want to view General Collar Status so it catches my attention if there are any issues to be fixed.

## Acceptance Criteria

| AC | Description | AC | Priority | Issue Type | Issue Reason | UI design |
|---|---|---|---|---|---|---|
| AC01 | If no issues are detected, then the status field should display 'No Issue' state, see Figma. |
| AC02 | If one issue is detected from the table 1 below, then the status field should display the corresponding issue. |
| AC03 | If multiple issues are detected, then the status field should display only the highest-priority issue according to the following priority order shown in the table 1. |
| Table 1 List of the collar issues ACPriorityIssue TypeIssue Reason UI designAC041 (the highest priority)Catastrophic Issue in Collar Diagnosticself-explanatoryFigma AC052Collar Unassignedself-explanatoryAC063Battery Fully Dischargedself-explanatoryAC074Low Batteryself-explanatoryAC085Bring OutsideGPS initialization requiredAC096Collar Updating(1) applying new settings to the collar (feedback settings update, etc.)(2) no telemetry data available yetAC107SGEE Update (the user should plug in the collar and internet should be used as a connection channel)Satellite data is outdatedAC118 (the lowest priority)Low GPS/No GPS/No GPS dataself-explanatory | AC04 | 1 (the highest priority) | Catastrophic Issue in Collar Diagnostic | self-explanatory | Figma | AC05 | 2 | Collar Unassigned | self-explanatory | AC06 | 3 | Battery Fully Discharged | self-explanatory | AC07 | 4 | Low Battery | self-explanatory | AC08 | 5 | Bring Outside | GPS initialization required | AC09 | 6 | Collar Updating | (1) applying new settings to the collar (feedback settings update, etc.)(2) no telemetry data available yet | AC10 | 7 | SGEE Update (the user should plug in the collar and internet should be used as a connection channel) | Satellite data is outdated | AC11 | 8 (the lowest priority) | Low GPS/No GPS/No GPS data | self-explanatory |
| AC04 | 1 (the highest priority) | Catastrophic Issue in Collar Diagnostic | self-explanatory | Figma |
| AC05 | 2 | Collar Unassigned | self-explanatory |
| AC06 | 3 | Battery Fully Discharged | self-explanatory |
| AC07 | 4 | Low Battery | self-explanatory |
| AC08 | 5 | Bring Outside | GPS initialization required |
| AC09 | 6 | Collar Updating | (1) applying new settings to the collar (feedback settings update, etc.)(2) no telemetry data available yet |
| AC10 | 7 | SGEE Update (the user should plug in the collar and internet should be used as a connection channel) | Satellite data is outdated |
| AC11 | 8 (the lowest priority) | Low GPS/No GPS/No GPS data | self-explanatory |
| AC12 | Only one issue should be displayed in the status field at any given time. |
| AC13 | If the highest-priority issue is resolved, then the next highest-priority issue should be displayed (if exists). |
| AC14 | If all issues are resolved, then the status should return to 'No Issues' state, see Figma. |
| AC15 | The status must update dynamically as issues appear or disappear. |Implementation note

Some of the data for the definition can only be obtained via the Backend APISome of it can be obtained via Backend API and telemetry.It is assumed that this screen will receive data from all sources and compile a final model for further use (see Replicating Real Time Telemetry Updates system).Collar Diagnostic, can only be retrieved from GET /collar/my or GET /collar/\{id\}Collar Unassigned, can only be retrieved from GET /collar/my or GET /collar/\{id\}. In this case PetInfo will be nullCollar Updating can only be retrieved from GET /collar/my or GET /collar/\{id\} - ConfigurationSyncStatus field, or when we don't have any telemetry yet (Backend API also doesn't return telemetry to us)All other data can be obtained either from telemetry or from Backend API.The processing of this data will be the same as in the specific section with which the status is associated (details in separate stories, related to sections:

- Battery in Battery Section,
- GPS, Satellite in Tracking Section


