---
title: "ME14-US28. 'Collar is out of Wi-Fi, cellular and Bluetooth range' notifications"
sidebar_label: "ME14-US28. 'Collar is out of Wi-Fi, cellular and Bluetooth range' notifications"
sidebar_position: 185
last_modified: "Jan 12, 2022"
author: "Ekaterina Dupanova"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-9586 Closed |
| Click here to expand...13 Dec 2021 Added requirements04 Jan 2022 Added 'Apply feedback for multiple pets' section12 Jan 2022 Updated requirements - removed apply feedback for multiple pets section, updated preconditions for AC-03, AC-04 |# Contents

User Story Acceptance criteria

# User Story

\> As a user, I want to receive different notifications for each specific case when I can't send a command to my Halo collar so that I can understand what exactly the problem is. At the moment the mobile app shows 'Collar is out of Wi-Fi, cellular and Bluetooth range' if it fails to send a command to a collar due to any reason. As the result it seems that the device does not work properly and Halo Team receves a lot of complaints.

# Acceptance criteria

| AC | Description | iOs screen design | Android screen design | Apply feedback for a pet | Apply feedback for multiple pets |
|---|---|---|---|---|---|
| ME14-US28-AC01 | The acceptance criteria below should be applied for the following scenarios:When the user applies feedback from the pet cardWhen the user applies feedback from the training cardWhen the user changes a pet mode from the pet cardWhen the user taps the' Test on collar' button from:'Emergency feedback' settings screen'Warning feedback' settings screen'Boundary feedback' settings screen'Good behavior feedback' settings screen'Return whistle feedback' settings screen'Heading home feedback' settings screen | - | - |
| ME14-US28-AC02 | Precondition:Bluetooth is enabled on the phoneThe phone is connected to the internetThe expected time of battery discharge has come. Calculation: current time + battery time remaining = expected time of collar's battery dischargeExample:12 o'clock: 22 minutes remaining (the system records that the collar is going to be off at 12:22)12:01: 25 minutes remaining (the system updates the time when the collar is going to be off to 12:26).12:30 collar is probably off, the app will show the messageIf the user performs any of the actions from ME14-US28-AC01 the app should show the toast message "Please check that your collar is turned ON and try again" | - | - |
| ME14-US28-AC03 | Precondition:Bluetooth is enabled on the phoneThe phone is connected to the internetThe expected time of battery discharge has not come. If the user performs any of the actions from ME14-US28-AC01 the app should show the toast message "Your collar is out of Wi-Fi, cellular and Bluetooth range or powered OFF". | - | - |
| ME14-US28-AC04 | Preconditions:Bluetooth is enabled on the phoneThe phone is not connected to the internet Bluetooth connection/unlocking progress is in progressIf the user performs any of the actions from ME14-US28-AC01 the app should show 'Your phone is not connected to the internet and Bluetooth connection is still in progress.' | - | - |
| ME14-US28-AC05 | Same as in ME14-US27. 'Unable to send command to collar' notifications (ME14-US27-AC08 - ME14-US27-AC12) |  |  |
