---
title: "ME05-US59. Display collar reachability on IF card"
sidebar_label: "ME05-US59. Display collar reachability on IF card"
sidebar_position: 706
last_modified: "Aug 29, 2023"
author: "Galina Lonskaya"
---

Page info| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Timofey Burak [X] |
| HALO-16232 - MOB+BE: ME05-US59. Display collar reachability on IF card Closed |
| History of changes12 Jul 2023 the story is separated from IF redesign story by Galina Lonskaya , since this dividing will make the development process more effective |Contents*User story Acceptance criteria Implementation notes*Background and goalAt the moment, we know that some users are receiving multiple errors stating that the collar is unavailable when attempting to send instant feedback. This is one of the top 5 errors by the number of repetitions. Thus, users are unable to send instant feedback, and the system does not give them precise understanding of what specific problem is preventing them from doing so. Only a general error is displayed 'Your collar is out of Wi-Fi, cellular and Bluetooth range or powered OFF'.

With this feature the goal is to:

- Decrease number of unsuccessful trying to send IF (IF-Instant Feedback)
- Increase user loyalty (ratings)

Technical solutionSee the link:[S3] Detect if a Collar is reachable over BLE/internet# User story

\> As Halo app account owner I want to see if my collar is reachable on the instant feedback card so that I understand if I can send Instant feedback or not at the moment.

# Acceptance criteria

| AC | Description | UI/UX design, links | Updates related to the pet checkboxes and IF(=Instant Feedback) buttons on IF cardNote for developers: before implementing this story it's required to read the tech solution description. See: [S3] Detect if a Collar is reachable over BLE/internet | Collar reachability displaying on the IF card | Collar reachability scenarios All possible scenarios are displayed within the Table ME05-US59-1 Collar reachability determination logic. Please first review the table. |
|---|---|---|---|---|---|
| ME05-US59-AC01 | IF button can have disabled state. See the conditions below: ME05-US59-AC05/08.Note: no toasts should be displayed after a tap on the disabled IF buttons. |  |
| ME05-US59-AC02 | Pet checkboxes can have 'grayed out' state: the tick should be gray (if displayed),the frame should be dark gray. | https://zpl.io/Am80GYO |
| ME05-US59-AC03 | Pet checkboxes should be grayed out, in case the collar of the pet is not reachable (see ME05-US59-AC11). | - |
| ME05-US59-AC04 | The pet checkbox can be selected-deselected in the 'grayed out' state. | - |
| ME05-US59-AC05 | IF state button (disabled or enabled) depends on:collar(s) reachability (see ME05-US59-AC11) and collar battery state (see ME05-US59-AC12),how many pets are selected. | - |
| ME05-US59-AC06 | If no pets are selected, then: IF buttons should be disabled. | https://zpl.io/Q0exWgWIF btns Scrolledhttps://zpl.io/jZmelB4 |
| ME05-US59-AC07 | If no selected pets are reachable, then: IF buttons should be disabled. | - |
| ME05-US59-AC08 | If at least one pet is selected and reachable, then:IF buttons should be enabled. | https://zpl.io/GEBgzem |
| ME05-US59-AC09 | IF should be sent only to the reachable (see ME05-US59-AC11) AND selected pets. Note: no changes to errors handling for the pets that are reachable and selected at the moment of IF sending. | - |
| ME05-US59-AC10 | The collar reachability should be displayed in the bottom right corner of the pet avatar on IF card. | - |
| ME05-US59-AC11 | There are the following collar reachability states:Reachable states (=IF should sent to the collars in these states):'Bluetooth connected' icon'Wi-Fi connected' icon'LTE connected' iconNot reachable states (=IF should NOT sent to the collars in these states):'Collar discharged' icon'Searching' animation'Not available' icon (='sync' icon) | https://zpl.io/ewNrgXP |
| ME05-US59-AC12 | If the collar is discharged and not reachable over BLE or BLE is disabled on the smartphone, then: THEN'No battery' icon should be displayed near the pet avatar,the tile with the pet should be grayed out,'Tick' icon and frame should be gray, in case the pet is selected OR nothing should be displayed in case the pet isn't selected.'IF' buttons should be disabled in case no other available pets in the account OR 'IF' buttons should be enabled, there is at least one available pet within the account. Note: this status should be displayed continuously | 'Collar discharged' reachability icon |
| ME05-US59-AC13 | If the collar is connected via BLE and no matter connected via Internet or not, then:THEN BLE icon should be displayed near the pet avatar, 'IF' buttons should be enabled, 'Tick' icon and frame should be blue, in case the pet is selected OR nothing should be displayed in case the pet isn't selected. | 'Bluetooth connected' reachability icon |
| ME05-US59-AC14 | If the collar is connected via Wi-Fi only, then:THEN Wi-Fi icon should be displayed near the pet avatar, 'IF' buttons should be enabled, 'Tick' icon and frame should be blue, in case the pet is selected OR nothing should be displayed in case the pet isn't selected. | 'Wi-Fi connected' reachability icon |
| ME05-US58-AС15 | Wi-Fi icon should reflect the strength of Wi-Fi signal. Note: The same logic as implemented on the pet card, see ME07-F03-AC17 in ME03-F01. Collars list. | - |
| ME05-US59-AC16 | If the collar is connected via LTE only, then:THEN LTE icon should be displayed near the pet avatar, 'IF' buttons should be available,'Tick' icon and frame should be blue, in case the pet is selected OR nothing should be displayed in case the pet isn't selected. | 'LTE connected' reachability icon |
| ME05-US59-AC17 | LTE icon should reflect the strength of LTE signal. Note: The same logic as implemented on the pet card, see ME07-F03-AC17 in ME03-F01. Collars list. | - |
| ME05-US59-AC18 | Ifthe collar is not connected via any connection channel at the moment,the Internet is enabled on the smartphone,Bluetooth is enabled on the smartphone,THENSearching animation should be displayed,the tile with the pet should be grayed out,'Tick' icon and frame should be gray, in case the pet is selected OR nothing should be displayed in case the pet isn't selected,IF buttons should be disabled. | Part 2 - Redesign Feedback for All Pets – Selected All - ME05-US59-AC02 (1) (1).mp4'Searching' reachability animation |
| ME05-US59-AC19 | If there is more than 1 pet with Search animation on the IF card, then: all animations should play in sync. | - |
| ME05-US59-AC20 | If the collar is not connected via any connection channel at the moment,the Internet is disabled on the smartphone,Bluetooth is disabled on on the smartphone,THEN'Sync' icon should be displayed,the tile with the pet should be grayed out,'Tick' icon and frame should be gray, in case the pet is selected OR nothing should be displayed in case the pet isn't selected, IF buttons should be disabled. | 'Not available' reachability icon |
| ME05-US59-AC21 | If Halo BE is not available, Bluetooth is disabled on the smartphone or the collar is not reachable via Bluetooth,THEN'Sync' icon should be displayed,the tile with the pet should be grayed out,'Tick' icon and frame should be gray, in case the pet is selected OR nothing should be displayed in case the pet isn't selected, IF buttons should be disabled. | - |# Implementation notes

| IN | Description |
|---|---|
| ME05-US59-IN01 | In case mini-telemetry is turned off, then anyway IF card and sending feature should be available. Note: Data will be updated not so frequently. |
| ME05-US59-IN02 | In case the collar has FW version that doesn't support mini-telemetry, then anyway IF card and sending feature should be available. Note: Data will be updated not so frequently. |Table ME05-US59-1 Collar reachability determination logic

| BLE statuses | Collar is reachable over BLE | Collar is NOT reachable over BLE (priority 2) | BLE is disabled on the smartphone (priority 1) | Internet statuses | Collar is reachable over Internet | Collar is NOT reachable over Internet (collar issue) (priority 4) | Collar battery discharged (priority 3) | BE is not available (BE issue, error 500) (priority 2) | Internet is disabled on the smartphone (priority 1) |
|---|---|---|---|---|---|---|---|---|---|
| BLE icon | Wi-Fi/LTE icon | Wi-Fi/LTE icon + standard message about BLE disabling |
| BLE icon | Search animation | Search animation + standard message about BLE disabling |
| BLE icon | 'Collar discharged' icon | 'Collar discharged' icon + standard message about BLE disabling |
| BLE icon | Sync icon | Sync icon + standard message about BLE disabling |
| BLE icon + 'No internet connection' blue bar | Sync icon + 'No internet connection' blue bar | Sync icon + standard message about BLE disabling (see Zeplin)+ 'No internet connection' blue bar |*priority - sequence of conditions check


