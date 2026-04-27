---
title: "ME05-FE05. Test on Collar"
sidebar_label: "ME05-FE05. Test on Collar"
sidebar_position: 685
last_modified: "Sep 17, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story (checked by dev team) |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| TBD |### User story

\> As an account owner, I want to test on collar the choosen setting of the command so that I can check if this configuration works for my pet.

### Acceptance Criteria

| AC | Description | iOS impl-n/UI design | Android impl-n UI design |
|---|---|---|---|
| ME05-FE05-AC01 | "Test on Collar" should be possible to initiate out of the following screens:Warning FeedbackBoundary FeedbackEmergency FeedbackGood BehaviorReturn WhistleHeading HomeSee the screen description in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE05-AC02 | If I tap on the Test on Collar button and there is no assigned collar to a pet, then:the M79 No collar for testing message should be displayed.The "Add collar" button \> Screen "Assign a collar should be displayed".The "Cancel" button \> the popup is closed. | IOS DONE | ANDROID TO DO |
| ME05-FE05-AC03 | If the testing on the collar is initiated and it's possible to send Test on Collar via BLE, then:"Test on Collar" should be sent via BLE. | IOS DONE | ANDROID TO DO |
| ME05-FE05-AC04 | If the Test on Collar is initiated and the app failed to send Test on Collar via BLE, due to the following reasons:Bluetooth is disabled on the smartphoneThe collar was not found during the background scanningThe app failed to unlock the collarthen:the app should send the Test on Collar via the internet. | IOS DONE | ANDROID TO DO |
| ME05-FE05-AC05 | If the Test on Collar is initiated and both BLE is disabled and the internet is unavailable on the smartphone, then:the app displays the "Collar is out of Wi-Fi, cellular and Bluetooth range” toast message.Note: The error should not be displayed in case the internet connection is unavailable, but the collar is within the range of smartphone Bluetooth. | IOS DONE | ANDROID TO DO |
| ME05-FE05-AC06 | While sending the Test on Collar command, the standard app spinner should be displayed at the screen. |  |  |
| ME05-FE05-AC07 | If I open the "Test on Collar" sheet and the Bluetooth permission is not granted (e.g. after the user re-installed the app), then:the app should ask for the permission on the first attempt to send Test on Collar, see A1-US01. "Bluetooth permission request" message.And in case the user denies the Bluetooth permission the app should only use the internet channel until permission is granted. At that, the app should not request Bluetooth permission on sending Test on Collar. | IOS DONE | ANDROID TO DO |
| ME05-FE05-AC08 | See the logic of Bluetooth reconnection here: ME14-EP01 Automatic Bluetooth reconnection. | IOS DONE | ANDROID OPTIONALNote: Blue tile should not be displayed |
