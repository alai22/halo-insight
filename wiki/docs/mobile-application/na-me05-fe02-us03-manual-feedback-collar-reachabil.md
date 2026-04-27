---
title: "(NA) ME05-FE02-US03. Manual Feedback: Collar Reachability Status"
sidebar_label: "(NA) ME05-FE02-US03. Manual Feedback: Collar Reachability Status"
sidebar_position: 549
author: "Galina Lonskaya"
---

Page info| Story owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| HALO-23076 - [iOS] Manual Feedback: Collar Reachability Status Open HALO-23077 - [Android] Manual Feedback: Collar Reachability Status Open |
| History of changes17 Apr 2025 draft user story is created |Contents*User story Acceptance criteria*Technical solutionSee the link:[S3] Detect if a Collar is reachable over BLE/internet# User story

\> As Halo app account owner I want to see if my collar is reachable on the instant feedback card so that I understand if I can send Instant feedback or not at the moment.

# Acceptance criteria

| AC | Description | UI/UX design, links | Collar reachability displaying on the MF card | MF buttons behavior |
|---|---|---|---|---|
| AC01 | The collar reachability status should be displayed in the bottom right corner of the pet pin on MF sheet. |  |
| AC02 | There are the following collar reachability states:Reachable states (=MF should sent to the collars in these states):'Bluetooth connected' icon'Wi-Fi connected' icon'LTE connected' iconNot reachable states (=MF should NOT sent to the collars in these states):'Search' state: animated icon'Not available' state: static icon See UI in Table ME05-FE02-US03-1 Collar reachability determination logic |
| AC03 | MF buttons can have 2 states:enableddisabled | - |
| AC04 | If at least one pet is reachable and selected, then:all MF buttons should be enabled. | Figma |
| AC05 | If no selected pets are reachable, then:all MF buttons should be shown as temporarily unavailable. | Figma |
| AC06 | If I tap on any of disabled MF buttons, then the specific toast message should be shown. | Figma |
| AC07 | If the feedback settings of the collar are updating at the moment, then the following animation should be shown on pets. | Figma |Table ME05-FE02-US03-1 Collar reachability determination logic

| AC | Internet statuses | BLE statuses | Collar is reachable over BLE | Collar is NOT reachable over BLE (priority 2) | AC08 | Collar is reachable over Internet | AC09 | Collar is NOT reachable over Internet (collar issue) (priority 4) | AC10 | Collar battery discharged (priority 3) | AC11 | BE is not available (BE issue, error 500) (priority 2) | AC12 | LTE/Wi-Fi is not available on the smartphone (priority 1) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Figma | FigmaLTE/Wi-Fi icon should reflect the strength of LTE/Wi-Fi signal. Note: The same logic as implemented on the pet card |
| Search Animation FigmaSearching.json |
| Not Available iconFigma |Implementation details

The current Reachability status for each pet should be detected by Reachability System, see more details in Replicating Reachability System.


