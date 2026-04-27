---
title: "(BL) ME03-US114b. Change logic for satellite data on Collar's list"
sidebar_label: "(BL) ME03-US114b. Change logic for satellite data on Collar's list"
sidebar_position: 478
last_modified: "Jan 30, 2025"
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-17038 - MOB+BE: updates to texts, Advanced settings screen, change logic for ok satellite data on Collar's list Closed |
| Click here to expand...As of: 14 Jul 2023 Ekaterina Dupanova created initial draft of the story30 Jan 2025 baselined to ME03-F11 by Galina Lonskaya |# Contents

Acceptance criteria

# Acceptance criteria

| AC | Description | Links, design | Text updates | As is | To be | As is | To be |
|---|---|---|---|---|---|---|---|
| ME03-US114-AC02 | Collar's list screen, GPS tilePrecondition: GloExp/GpsEXP is not up to date. SGEE data on the collar is outdatedAs is To beNo satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and leave it powered on while charging.No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and leave it turned on while charging. | No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and leave it powered on while charging. | No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and leave it turned on while charging. | Zeplin: iOS | Android |
| No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and leave it powered on while charging. | No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and leave it turned on while charging. |
| ME03-US114-AC03 | Collar's list screen, GPS tilePrecondition: the collar's FW doesn't support SGEE feature.As is To beFor the greatest location accuracy, please upgrade the firmware of your collar. If your firmware status indicates ‘up-to-date’, please notify Customer Support.Firmware update is required. Satellite position data is not supported by this version. | For the greatest location accuracy, please upgrade the firmware of your collar. If your firmware status indicates ‘up-to-date’, please notify Customer Support. | Firmware update is required. Satellite position data is not supported by this version. | Zeplin: iOS |
| For the greatest location accuracy, please upgrade the firmware of your collar. If your firmware status indicates ‘up-to-date’, please notify Customer Support. | Firmware update is required. Satellite position data is not supported by this version. |
| Logic of Satellite position data on Collar's list |
| ME03-US114-AC09 | Precondition: Collar does not require initializationSatellite position data is up-to-datePet is assigned to the collarThe app should display'Satellite data is up-to-date'GPS signal icon (states of the icon are listed in ME07-F03-AC12)Whether satellite position data is up-to-date should based on the real time status. | Zeplin: iOS | Android |
| ME03-US114-AC12 | Precondition: Collar does not require initializationSatellite position data is up-to-datePet is not assigned to the collarThe app should display'Satellite data is up-to-date'No GPS signal icon |  |
| ME03-US114-AC10 | Collar's list screen, GPS tilePreconditionTelemetry not outdatedSGEE data on the collar is outdatedThe app should show: 'No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and leave it turned on while charging.' |  |


