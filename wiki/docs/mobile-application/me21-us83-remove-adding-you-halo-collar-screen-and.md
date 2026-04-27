---
title: "ME21-US83. Remove 'Adding You Halo Collar' screen and update 'Link Collar to Account' screen"
sidebar_label: "ME21-US83. Remove 'Adding You Halo Collar' screen and update 'Link Collar to Account' screen"
sidebar_position: 447
last_modified: "Jan 09, 2025"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Dmitry Kravchuk Kirill Akulich |
| HALO-21315 - [Critical]: MOB: ME21-US83. Remove 'Adding You Halo Collar' screen and update 'Link Collar to Account' screen Closed |
| 06 Sep 2024 a draft story is created by Galina Lonskaya 12 Sep 2024 ME21-US83-AC09 is added by Galina Lonskaya |Table of Contents

Background User story Acceptance criteria

# Background

FTUE Onboarding Alpha testing feedback, see the source.

# User story

\> As a Halo app account owner I want to set up my account and a collar with the decreased number of screens so that I can see the value that the collar can bring me as soon as possible.

# Acceptance criteria

| AC | Description | UI design | AS IS | TO BE | AS IS | TO BE |
|---|---|---|---|---|---|---|
| Logic updates |
| ME21-US83-AC01 | 'Adding Your Halo Collar' screen should be removed from all 'collar attach' flows initiated from any part of the app:Add the 1st collar within FTUE Onboarding Add the 2nd and further collar(s) within FTUE Onboarding Add the 1st and further collar(s) from My Collars list (Settings tab) Add the 1st and further collar(s) from Pet Card (My Map tab)Add the 1st and further collar(s) after pet adding completion (My Map tab) | Figma |
| ME21-US83-AC02 | 'Link Collar to Account' screen should be the first screen of 'collar attach' flow initiated from any part of the app.Note: progress bar is shown only within FTUE Onboarding |
| ME21-US83-AC03 | Precondition 1: iOS - any OS, Android - 12 and higherPrecondition 2: FTUE Onboarding is in progress (note: for 'collar attach' from the app popup error logic should not be changed)If 'Link Collar to Account' screen is opened and BLE permission is not granted, then: M143 "Bluetooth permission denied" message error message should be displayed on 'Link Collar to Account' screen.Note: For Android 11 and lower, M55 Disabled Location should be shown (since there is no Bluetooth permission for Android 11 and lower) |
| ME21-US83-AC04 | Precondition 1: Android - 11 and lowerPrecondition 2: FTUE Onboarding is in progress (note: for 'collar attach' from the app popup error logic should not be changed)If 'Link Collar to Account' screen is opened and BLE permission is not granted, then: M55 Disabled Location error message should be shown (since there is no Bluetooth permission for Android 11 and lower) |
| ME21-US83-AC05 | If 'Link Collar to Account' screen is opened, BLE permission is granted AND Bluetooth is disabled on the smartphone, then: M178 Disabled Bluetooth (Wi-Fi setup, Add Beacon, Update beacon, Add collar) error message should be displayed on 'Link Collar to Account' screen. |
| ME21-US83-AC06 | If I am attaching the 1st collar within FTUE Onboarding, then: 'Don't have a collar?' button should be displayed at the bottom of 'Link Collar to Account' screen. Note: If I add the 2nd and further collar(s), then 'Don't have a collar?' button should not be displayed. For instance: the user can initiate adding of the 2nd collar after tap on 'Add Another Collar' button from 'Congratulations!' screen. |
| ME21-US83-AC07 | 'Don't have a collar?' button should be pinned to the bottom of 'Link Collar to Account' screen. |
| Text updates |
| ME21-US83-AC08 | M178 Disabled Bluetooth (Wi-Fi setup, Add Beacon, Update beacon, Add collar) error popup message text should be updated:AS ISTO BETitle: Bluetooth is DisabledBody: Please turn on Bluetooth function on your mobile device.Button: OKTitle: Bluetooth is DisabledBody: Please enable Bluetooth on your phone.Button: OK | Title: Bluetooth is DisabledBody: Please turn on Bluetooth function on your mobile device.Button: OK | Title: Bluetooth is DisabledBody: Please enable Bluetooth on your phone.Button: OK | - |
| Title: Bluetooth is DisabledBody: Please turn on Bluetooth function on your mobile device.Button: OK | Title: Bluetooth is DisabledBody: Please enable Bluetooth on your phone.Button: OK |
| ME21-US83-AC09 | 'Nothing Happened?' section text should be updated on 'Link Collar to Account' screen: AS ISTO BETap here for troubleshooting help.Make sure the collar is charged. Tap here for charging instructions. | Tap here for troubleshooting help. | Make sure the collar is charged. Tap here for charging instructions. | - |
| Tap here for troubleshooting help. | Make sure the collar is charged. Tap here for charging instructions. |
