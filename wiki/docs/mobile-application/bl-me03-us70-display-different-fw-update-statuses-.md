---
title: "[BL] ME03-US70. Display different FW update statuses depending on FW version"
sidebar_label: "[BL] ME03-US70. Display different FW update statuses depending on FW version"
sidebar_position: 195
last_modified: "Mar 18, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Story owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] |
| HALO-10531 - BE+MOB: Display different FW update statuses depending on FW version Closed |
| Click here to expand...18 Mar 2022 Maria Shikareva [X] Marked the story as baselined (see ME03-F01. Collars list). |# Contents

General description User story Acceptance criteria FW update status Tables Table ME03-US70-1 Statuses of the FW update that should be described within the app

# General description

Initially FW update could be downloaded only using Wi-Fi connection. But starting from 01.01.00 FW version (when WGET manager was included) the collar is able to download files using LTE connection (if Wi-Fi is not configured, then the files will be uploaded using LTE immediately if other conditions are met; if Wi-Fi is configured, then there's a 12 hours time-out when the collar waits for Wi-Fi connection and afterwards downloads files using LTE).

Info: 01.02 FW version includes new sapi 2.4 (as of 03 Feb 2022 we don't have such FWs), 01.03.00 FW version includes Airoha.

# User story

\> As a Halo app owner I want to see the relevant instructions about updating collar's FW version so that to clearly understand how my collar can be updated.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ Implementation status | FW update status |
|---|---|---|---|---|
| ME03-US70-AC01 | Precondition: the collar has FW version lower than 01.01.00;the collar doesn't have "Up-to-date" FW.The system should display status tiles as described in the 1st column of Table ME03-US70-1 Statuses of the FW update that should be described within the app (see below).Note: the statuses remain the same as described in ME03-F01-AC49. | - | - |
| ME03-US70-AC02 | Precondition: the collar has FW version 01.01.00 and higher;the collar doesn't have "Up-to-date" FW.The system should display status tiles as described in the 2nd column of Table ME03-US70-1 Statuses of the FW update that should be described within the app(see below).Note: for better experience new texts in the table are highlighted with green background → only these texts should be changed, the other should remain the same. | - | - |# Tables

#### Table ME03-US70-1 Statuses of the FW update that should be described within the app

| Status titles for FW version \< 01.01.00 | Status titles for FW version ≥ 01.01.00 |
|---|---|
| Collar is offline. Charge collar in Wi-Fi range. If needed, connect collar to phone hot-spot. | Collar is offline. Charge collar where Wi-Fi or LTE is available. If needed, connect collar to phone hot-spot. |
| Downloading paused, needs Wi-Fi connection. If needed, connect collar to phone hot-spot. | Downloading paused, collar needs an Internet connection. If needed, connect collar to phone hot-spot. |
| Downloading paused, low battery. Make sure collar is charging. | Downloading paused, low battery. Make sure collar is charging. |
| Downloading paused, not charging. Plug collar into charger. | Downloading paused, not charging. Plug collar into charger. |
| Downloading. Please be patient while firmware file downloads. If possible, avoid using collar. | Downloading. Please be patient while firmware file downloads. If possible, avoid using collar. |
| Downloading failed. Consider moving collar and charger into better Wi-Fi location. | Downloading failed. Consider moving collar and charger into better Internet connection. |
| Verification in progress. This will take a few seconds. | Verification in progress. This will take a few seconds. |
| Verification failed. File will re-download automatically. If possible, avoid using collar. | Verification failed. File will re-download automatically. If possible, avoid using collar. |
| Update paused, not charging. Please plug collar in to complete upgrade. | Update paused, not charging. Please plug collar in to complete upgrade. |
| Firmware update in progress. This may take several minutes. Do not unplug collar while red LED is blinking. | Firmware update in progress. This may take several minutes. Do not unplug collar while red LED is blinking. |
| Firmware update failed. Upgrade will re-start automatically. If possible, avoid using collar. | Firmware update failed. Upgrade will re-start automatically. If possible, avoid using collar. |
