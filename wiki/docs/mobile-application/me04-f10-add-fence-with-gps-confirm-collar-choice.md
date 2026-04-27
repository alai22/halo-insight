---
title: "ME04-F10 Add fence with GPS: Confirm Collar Choice"
sidebar_label: "ME04-F10 Add fence with GPS: Confirm Collar Choice"
sidebar_position: 110
author: "Nicolay Gavrilov"
---

| Document type | Document status | Document owners | Link to JIRA Issues | Change history |
|---|---|---|---|---|
| Baseline story |
| REVISED |
| Nicolay Gavrilov, Pavel Leonenko, Anastasia Brechko |
| HALO-5357 - Android GOAL: Add/Edit fence with GPS Closed |
| Maria Shikareva [X] 09 Mar 2021 Added ME04-F10-AC25 while baselining the story: ME03-US24. Collars list state in case last telemetry from the collar was sent more than 5 minutes ago. |# Contents

User story Acceptance criteria Collars list Pairing with collar Find collar

# User story

\> As a user I want to choose a collar that will be used to add a fence with GPS so that I could use a specific device for this purpose.

# Acceptance criteria

| AC | Text | iOS design / implementation statusIOS DONE | Android design / implementation statusANDROID TO DO | Collars list | Pairing with collar | Find collar |
|---|---|---|---|---|---|---|
| ME04-F10-AC01 | 'Add fence with GPS: List of collars' screen should show the list of user's collars that are currently in the range of smartphone Bluetooth. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC02 | 'Add fence with GPS: List of collars' screen consists of:"Confirm Collar Choice" headingCancel button"Looking for nearby collars" label + spinnerList of discovered collars |
| ME04-F10-AC03 | The list of discovered collars consists of cards with collar details. Each card shows the following information:Collar photo + Collar Color RingCollar battery level with battery iconDevice nameHalo version |
| ME04-F10-AC04 | If a collar is assigned to a pet, the device name on the card should be as follows: "\<pet name\>'s Halo" (see the screen design) |
| ME04-F10-AC05 | If a collar is not assigned to a pet, the device name on the pet card should be as follows: "(XXXLL)", where:'XXX" are the last 3 digits of the collar serial number "LL" is the manufacturing location code assigned by the company (see BR-10 Serial Number format) |
| ME04-F10-AC06 | If the collar is not assigned to a pet the color ring around the collar icon should be grey. Otherwise, it should have the same color that was assigned to the pet in settings. |
| ME04-F10-AC25 | Battery indicator should be whitened on the Collars list within 'Confirm Collar Choice' screen while adding a fence in case the last telemetry was received from the collar more than 5 minutes ago. | IOS DONENote: see Eva's Halo example. | ANDROID DONENote: see Eva's Halo example. |
| ME04-F10-AC07 | While no collars are discovered, the following information should be displayed instead of the list of collars:Collar icon'Please make sure your mobile device is near a collar that is ON' caption | IOS DONE | ANDROID TO DO |
| ME04-F10-AC08 | If I tap on the Cancel button, then the "Create New Fence" screen should be opened. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC09 | The scanning process should be started right after the screen opening. While the smartphone is scanning for the collars, "Looking for nearby collars" label and spinner should be displayed at the top of the screen. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC10 | The collars list should be sorted by RSSI. The collar with the strongest signal on top.Note: the list is not re-sorted if the RSSI level of the discovered devices changes over time | IOS DONE | ANDROID TO DO |
| ME04-F10-AC11 | The list of collars is updated in real-time. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC12 | If I tap tap on a collar from 'Add fence with GPS: List of collars' screen:the scanning process should be stopped;the process of pairing with the selected collar should be started;the spinner should be displayed on the selected collar card;the screen should be disabled and the overall spinner should be shown until the collar is paired. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC13 | If Bluetooth isn't enabled on the smartphone during the pairing, then the M102 No Bluetooth (fence creation) error should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC14 | If the pairing with the selected collar isn't successful, then the M70. No answer from the collar error should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC15 | The timeout for pairing with the collar should be 10 sec. The timeout should be configurable. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC16 | If the collar is successfully paired with the smartphone, the app shows the 'Find collar' screen. The screen consists of:Back icon"Confirm Collar Choice" title"Done" buttonPicture of the collarText with instructions on how to use 'Find collar' feature to confirm collar choice'Find Collar' button | IOS DONE | ANDROID TO DO |
| ME04-F10-AC17 | If I tap on the Find Collar button, then:the "Find Collar" request should be sent to the collar;the spinner should be displayed on the button while the request is being sent . | IOS DONE | ANDROID TO DO |
| ME04-F10-AC18 | If the "Find Collar" request is sent to the collar successfully, then:the following toast message should be displayed: "We found your collar. It should blink and play a sound for 10 sec."the collar should blink/beep for about 10 seconds. The volume of the beeping is gradually increased;'Stop sound' button should be displayed instead of the 'Find Collar' button should for 10 seconds. | IOS DONE | The design is similar to iOsANDROID TO DO |
| ME04-F10-AC19 | After 10 seconds, the 'Stop Sound' button is automatically replaced with the 'Find Collar' button. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC20 | If the user taps on the 'Stop Sound' button and the request is sent successfully, then:the collar should stop blinking and beeping;the app should show the 'Find Collar' button instead of the 'Stop Sound' button. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC21 | In case the "Find Сollar" request is failed because the collar is not available (for instance, the collar is turned off or is not connected to the smartphone via BT), the app shows the following toast message for 4 seconds:'Your collar was not found. Please try again.' | IOS DONE | ANDROID TO DO |
| ME04-F10-AC22 | If the user taps on the "Find Collar" button and the collar doesn't respond, the "M70. No answer from the collar" error should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC23 | If I tap on the 'Back' button on the 'Find collar' screen, then 'Add fence with GPS: List of collars' screen should be opened. | IOS DONE | ANDROID TO DO |
| ME04-F10-AC24 | If I tap on the Done button, then the TBD Link "Create Fence" screen with the toolbar should be displayed. | IOS DONE | ANDROID TO DO |
