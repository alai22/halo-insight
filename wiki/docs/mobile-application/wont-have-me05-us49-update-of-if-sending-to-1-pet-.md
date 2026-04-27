---
title: "[Won't have] ME05-US49. Update of IF sending to 1 pet (My Map)"
sidebar_label: "[Won't have] ME05-US49. Update of IF sending to 1 pet (My Map)"
sidebar_position: 222
last_modified: "Aug 29, 2023"
author: "Galina Lonskaya"
---

| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya |
| HALO-10222 - MOB: ME05-US49 + US50. Update of IF sending to 1 pet and 2+ pets (My Map) Closed |
| Galina Lonskaya created a story 01 May 2022 |# User story

\> As a Halo account owner, I want to have less steps in order to send instant feedback (IF) so that I can quicker send IF to my pet and prevent unwanted behavior.

# Acceptance criteria

| AC | Text | iOS screens | Android screens | Precondition for all AC above: the top bar with IFs and the bottom 'Send Feedback to Pet(s)' card is displayed |
|---|---|---|---|---|
| ME05-US49-AC01 | Precondition: My Map tab is opened. 'Hand' icon (=send instant feedback (IF)) should be always displayed at the top right corner. | See Zeplin | The same as for iOS |
| ME05-US49-AC02 | Precondition: I have 1 Pet with Halo collar assigned to the account. If I tap 'Hand' icon, then: the top bar with the IF buttons should be displayed: "Emergency" button "Boundary" button"Warning" button "Whistle" button "Close" buttonthe bottom 'Send Feedback to Pet(s)' card should be displayed:'Send Feedback to Pet(s)' headerPet with the connection icon | See Zeplin See video | The same as for iOS |
| ME05-US49-AC03 | Precondition: I have 0 Pets with Halo collar assigned to the account. If I tap 'Hand' icon, then: the top bar with the IF should be displayed in "translucent" view: see the previous ACthe bottom 'Send Feedback to Pet(s)' card should be displayed:'Send Feedback to Pet(s)' header"You don't have pets with the assigned collars."Note: see the logic of the "My Map"cards behavior in ME05-US49-AC04. | See Zeplin | The same as for iOS |
| ME05-US49-AC04 | If 'Send Feedback to Pet(s)' card is opened, then: all other cards should be closed, see below the diagram: Diagram 1 - Card logic on My Map. | - | - |
| ME05-US49-AC05 | When there is no pets and I tap on a feedback button the following toast message should be displayed:No pet selectedADD THE TOAST ID | - | - |
| ME05-US49-AC06 | If there is no Bluetooth connection, then: "Phone Bluetooth is disabled" bar should be displayed. Note: this UI element has been already implemented, see ME07-US51-AC01 in ME07-US51. 'Bluetooth is disabled' indication for various cards and screens. | See Zeplin | The same as for iOS |
| ME05-US49-AC07 | If the collar is connected via BLE, LTE and Wi-Fi, then: the corresponding icon should be displayed along with the pet icon: BLE icon Wi-FI icon LTE icon Note: similar logic is used on Leash tab, see [MVP] ME11-US03. Map details | See Zeplin | The same as for iOS |
| ME05-US49-AC08 | If the collar isn't connected via BLE, LTE and Wi-Fi, then the "Disconnected" icon should be displayed on the pet pin AND the pet should be greyed out.Note: The same requirement as for Leash, see ME11-US03-AC35, [MVP] ME11-US03. Map details |
| ME05-US49-AC09 | Additional precondition: bottom 'Send Feedback to Pet(s)' card is fully displayedI can minimize the 'Send Feedback to Pet(s)' card using "Swipe down" gesture. | See Zeplin See video | - |
| ME05-US49-AC10 | Additional precondition: bottom 'Send Feedback to Pet(s)' card is displayed the minimized state. I can initiate a full view of the 'Send Feedback to Pet(s)' card using "Swipe up" gesture. | - | - |
| ME05-US49-AC11 | If I tap on Close button, then: Instant Feedback button should be displayed the top bar with the IF should NOT be displayedthe bottom 'Send Feedback to Pet(s)' card should NOT be displayedFind card should be displayed, see the diagram below: Diagram 1 - Card logic on My Map | - | - |
| ME05-US49-AC12 | If I tap on any of IF buttons, then: the spinner should be displayed until the feedback sending result is received. Note: the logic of the IF sending should stay the same as it was before, see ME05-US31. Sending instant commands via BLE (MVP) | - | - |
| ME05-US49-AC13 | If the IF sending is failed, then: the spinner should not be displayedthe corresponding error should be displayed, see ME14-US27. 'Unable to send command to collar' notifications ME14-US27-AC02ME14-US27-AC03ME14-US27-AC04ME14-US27-AC05ME14-US27-AC06ME14-US27-AC07Note: the error toast message should have Close icon, see the story MEXX-USXX. Сlose toast messages by the app user. | - | - |
| ME05-US49-AC14 | If the IF sending is successful, then: the spinner should not be displayedthe tick should be displayed. | See video | The same as for iOS |Diagram 1 - Card logic on My Map


