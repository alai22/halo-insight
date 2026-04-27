---
title: "(NA) ME05-FE01-US05. 'Test on Collar' button on Feedback Details screen"
sidebar_label: "(NA) ME05-FE01-US05. 'Test on Collar' button on Feedback Details screen"
sidebar_position: 569
last_modified: "May 05, 2025"
author: "Galina Lonskaya"
---

| Document owners | Link to JIRA Issues | History of Changes |
|---|---|---|
| Galina Lonskaya, Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-884/ios-test-on-collar-button-on-feedback-details-screen |
| 25 Apr 2025 draft is created |### User story

\> As Halo app account owner, I want to test on collar the chosen feedback so that I can check if this feedback works for my pet.

### Acceptance Criteria

| AC | Description | UI design |
|---|---|---|
| AC01 | The acceptance criteria below should be applied for the following scenarios:When the user taps the' Test on collar' button from the 'Feedback Setting' screens of the pet with the assigned collars:'Recall' settings screen'Level 1' settings screen'Level 2' settings screen'Level 3' settings screen'Custom 1' settings screen'Custom 2' settings screen |  |
| AC02 | If 'Test on Collar' is tapped and it's possible to send Test on Collar via BLE, then:"Test on Collar" should be sent via BLE. |  |
| AC03 | If the Test on Collar is tapped and the app failed to send Test on Collar via BLE, due to the following reasons:Bluetooth is disabled on the smartphoneThe collar was not found during the background scanningThe app failed to unlock the collarthen:the app should send the Test on Collar via the internet. |  |
| AC04 | While sending the Test on Collar command, the standard app spinner should be displayed at the screen. |  |
| AC05 | If I tap on the Test on Collar button and there is no assigned collar to a pet, then:M17 popup should be shown. Note: agreed to show it to simplify dev-t and it's very rare case |  |
| AC06 | All other errors should be implemented within the separate user story:(NA) ME05-FE01-US06. 'Test on Collar' button: error handling |  |
