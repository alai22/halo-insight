---
title: "ME05-FE00. Instant feedback sheet"
sidebar_label: "ME05-FE00. Instant feedback sheet"
sidebar_position: 681
last_modified: "Jun 29, 2023"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story (checked by dev team) |
| UPDATE REQUIRED as of 6/29/23 |
| Galina Lonskaya, Nicolay Gavrilov, Pavel Leonenko, Anastasia Brechko |
| Android: HALO-4656 - Android: ME05-FE00: Instant feedback sheet (+ sending feedback via Bluetooth) Closed |# User story

\> As an account owner, I would like to apply an instant feedback so that I can quickly apply prevention or encouragement to train my pet.

Contents

User story Acceptance criteria Instant Feedback sheet: entry points Instant Feedback sheet: UI Instant feedback sending: process description Dependencies Diagram ME05-FE00-1 Sending instant feedbacks via BLE (success flow) sequence diagram

### Acceptance criteria

| AC | Text | iOS UI design | Android UI design | Instant Feedback sheet: entry points | Instant Feedback sheet: UI | Instant feedback sending: process description |  |
|---|---|---|---|---|---|---|---|
| ME05-FE00-AC01 | If the card of the pet with the assigned collar is opened, then:the Instant Feedback button should be displayed at the pet card. | - | - |
| ME05-FE00-AC02 | If the basic/behavior training of the pet with the assigned collar is opened, then:the Instant Feedback button should be displayed at the top part of the web-view. | - | - |
| ME05-FE00-AC03 | If I tap on the Instant Feedback button, then:the Instant Feedback sheet should be opened.The Instant Feedback sheet consists of:"Apply Feedback for \<Pet name\>" title"\<Pet's name\>'s feedback settings are available at the bottom of the pet card on My Map" subtitle"Prevention" subtitleButton with "Warning" title and "Warning" iconButton with "Boundary" title and "Boundary" iconButton with "Emergency" title and "Emergency" icon"Encouragement" subtitleButton with "Good Behavior" title and "Good Behavior" iconButton with "Return Whistle" title and "Return Whistle" iconButton with "Heading Home" title and "Heading Home" icon"Close" button (iOS) or Cross icon (Android) | The Instant Feedback sheet consists of:"Apply Feedback for \<Pet name\>" title"\<Pet's name\>'s feedback settings are available at the bottom of the pet card on My Map" subtitle"Prevention" subtitleButton with "Warning" title and "Warning" iconButton with "Boundary" title and "Boundary" iconButton with "Emergency" title and "Emergency" icon"Encouragement" subtitleButton with "Good Behavior" title and "Good Behavior" iconButton with "Return Whistle" title and "Return Whistle" iconButton with "Heading Home" title and "Heading Home" icon"Close" button (iOS) or Cross icon (Android) |  |  |
| The Instant Feedback sheet consists of:"Apply Feedback for \<Pet name\>" title"\<Pet's name\>'s feedback settings are available at the bottom of the pet card on My Map" subtitle"Prevention" subtitleButton with "Warning" title and "Warning" iconButton with "Boundary" title and "Boundary" iconButton with "Emergency" title and "Emergency" icon"Encouragement" subtitleButton with "Good Behavior" title and "Good Behavior" iconButton with "Return Whistle" title and "Return Whistle" iconButton with "Heading Home" title and "Heading Home" icon"Close" button (iOS) or Cross icon (Android) |
| ME05-FE00-AC04 | If I tap on any Instant Feedback button (Warning, Boundary, Emergency, Good Behavior, Return Whistle, Heading Home), then:the selected button should be animated, see the animation in ME05-FE00-AC09/AC10;other UI elements within the action sheet should be disabled; | - | - |
| ME05-FE00-AC05 | If the Instant Feedback is initiated and it's possible to send instant feedback via BLE, then:instant feedback should be sent via BLE. | - | - |
| ME05-FE00-AC06 | If the Instant Feedback is initiated and the app failed to send instant feedback via BLE, due to the following reasons:Bluetooth is disabled on the smartphoneThe collar was not found during the background scanningThe app failed to unlock the collarthen:the app should send Instant Feedback via the internet. |  |  |
| ME05-FE00-AC14 | In case the app failed to send the command via BLE, the mobile app sends it via the internet. It displays the 'success' animation after the command was applied and upon the receipt of the corresponding response from the cloud. | - | - |
| ME05-FE00-AC07 | If the Instant Feedback is initiated and both BLE is disabled and the internet is unavailable on the smartphone, then: the app displays the "Collar is out of Wi-Fi, cellular and Bluetooth range” toast message.Note: The error should not be displayed in case the internet connection is unavailable, but the collar is within the range of smartphone Bluetooth. | - | - |
| ME05-FE00-AC08 | If the Instant Feedback is sent successfully either via BLE or Internet, then: the animation should be completed with a success icon. See the success animation: Success feedback.mp4 | - | - |
| ME05-FE00-AC09 | If the instant feedback is failed either via BLE and the Internet, then:the animation should be completed with a failure icon.See the failure animation: Feedback failed.mp4 | - | - |
| ME05-FE00-AC10 | If I open the "Instant Feedback" sheet and the Bluetooth permission is not granted (e.g. after the user re-installed the app), then:the app should ask for the permission on the first attempt to send instant feedback, see A1-US01. "Bluetooth permission request" message.And in case the user denies the Bluetooth permission the app should only use the internet channel until permission is granted. At that, the app should not request Bluetooth permission on sending instant feedback. | - | - |
| ME05-FE00-AC11 | If I tap outside the Instant Feedback sheet or tap on the Close button (for iOS)/ the Cross icon (for Android), then:the Instant Feedback sheet should be closed. | - | - |
| ME05-FE00-AC12 | Instant Feedback events should not be displayed in the Notification list. | - | - |
| ME05-FE00-AC13 | Instant Feedback should not depend on the Fences On/Off mode. | - | - |### Dependencies

| # | Text | Notes/Links/Wireframes |
|---|---|---|
| ME05-FE00-DP01 | Collar FW has a characteristic to notify the mobile app about the result for instant feedbacks that are sent via BLE. | See the sequence diagram belowMore info: ME05-EP01 Send instant feedbacks via BLE |
| ME05-FE00-DP02 | Collar registers all incoming instant feedbacks in the logs. | More info: ME05-EP01 Send instant feedbacks via BLE |### Diagram ME05-FE00-1 Sending instant feedbacks via BLE (success flow) sequence diagram


