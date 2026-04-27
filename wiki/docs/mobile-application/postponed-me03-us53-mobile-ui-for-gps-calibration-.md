---
title: "[Postponed] ME03-US53. Mobile UI for GPS calibration: cancel 'calibration process' via Bluetooth"
sidebar_label: "[Postponed] ME03-US53. Mobile UI for GPS calibration: cancel 'calibration process' via Bluetooth"
sidebar_position: 144
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| HALO-6705 - [RI] ME03-US53. Mobile UI for GPS calibration: cancel 'calibration process' via Bluetooth Closed |
| 20 Oct 2021 Maria Shikareva [X] The story is marked as "Postponed". |# User story

\> As an account owner, I want to cancel calibration process via Bluetooth so that I can cancel calibration process without the direct multi-step interaction with the collar.

# Acceptance criteria

| AC | Description | iOS IU design / implementation status | Android IU design / implementation status |  |
|---|---|---|---|---|
| See the initial story: ME03-US50. Mobile UI for GPS calibration: instruction how to calibrate |
| ME03-US53-AC01 | If I tap on 'Cancel' button on 'Step 1-7' screen, then:'Cancel Calibration' popup should be shown;data update performed 1 sec should be paused, see the details in ME03-US50-AC20. | Pic 1 'Cancel Calibration' popup, see Zeplin | The same screen as for iOS |
| ME03-US53-AC02 | Precondition: 'Cancel Calibration' popup is displayed.If I submit cancelation, then:the smartphone breaks Bluetooth connection with the collar;'Collars' list should be opened with the expanded collar card that was shown before the opening of 'Outdoor/Indoor' settings. | - | - |
| ME03-US53-AC03 | The 'Canceled Calibration' command can be failed due to the following errors:M70. No answer from the collar M124 Security error for provisioning M126 Communication error M125 Connection error M181 Bluetooth is disabled (calibration process) | - | - |
| ME03-US53-AC04 | Precondition: 'Cancel Calibration' popup is displayed.If I decline cancelation, then:'Cancel Calibration' popup should be closed; previously shown screen still should be displayed;data update performed 1 sec should be unpaused, see the details in ME03-US50-AC20. | - | - |
|  | Note: How we can handle the following situation: the 'cancel GPS custom-configuration' command is failed, but the user still wants to close the instruction.Perhaps we can add a separate button for canceling and use 'Close'/'Cancel' button just for the navigation within the app. |  |  |
