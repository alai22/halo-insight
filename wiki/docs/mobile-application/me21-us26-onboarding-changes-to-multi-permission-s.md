---
title: "ME21-US26. Onboarding: Changes to Multi-permission screen (related to new Bluetooth permission for Android)"
sidebar_label: "ME21-US26. Onboarding: Changes to Multi-permission screen (related to new Bluetooth permission for Android)"
sidebar_position: 262
last_modified: "Dec 08, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA issue | Changes history |
|---|---|---|---|
| APPROVED BY SQ |
| Maria Shikareva [X] Kirill Akulich [X] |
| HALO-13524 - MOB: Upgrade Android Target SDK to the last version Closed HALO-13885 - BA: Describe all cases connected to Location/BLE permissions on Android Open |
| Click here to expand...12 Sep 2022 Maria Shikareva [X] Updated the requirements based on discussion during 2022-09-12 Meeting notes: BA call (Monday).15 Sep 2022 Maria Shikareva [X] Added ME21-US26-AC05 as discussed with Kirill Akulich [X] during development phase.08 Dec 2022 Maria Shikareva [X] Marked the story as implemented. |# General description

Starting from Android 12 a new Bluetooth permission is added. But its behavior differs from the same on iOS. As the app uses BLE for scanning devices which are going to send their location, we have to request a location permission along with a Bluetooth permission. And if the user denies access to location in this case, the app won't be able to scan and search devices using Bluetooth.

See Miro board.

# User story

\> As Halo app account owner I want to view list of permissions required for Halo app so that I can manage permissions required for Halo app and be informed about which permissions are needed for Halo to work properly.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| Android only |
| ME21-US26-AC01 | Preconditions: Location permission wasn't requested yet (or cache was cleared)ORLocation permission previously was allowed once (only while using)ORLocation permission was denied only once (Android allows requesting this access only twice)ANDa user taps 'Enable' button for Location access on the 'Enable Permissions' screenORa user allows access to BluetoothORa user enters the app,then the app should display a M261 Precise Location Required pop-up before showing a request for Location permission. | - | - |
| ME21-US26-AC02 | Precondition: M261 Precise Location Required pop-up is displayed.If a user taps 'Ok', then the app shows a request for Location permission (both for Precise and Approximate).Note: the app can't request for only one type of location permission due to Android restrictions. | - | - |
| ME21-US26-AC03 | Precondition: location permission is displayed.If a user denies access to location OR allows access to approximate location only, then the app:should not request a Bluetooth permission;set an 'OFF' state for Bluetooth access on the 'Enable Permissions' screen. |  |  |
| ME21-US26-AC04 | The app should display M261 Precise Location Required both for the Onboarding flow and for the main flow (adding 2nd, 3rd, etc. collars). | - | - |
| ME21-US26-AC05 | Permission to upgrade Precise location should not be requested at all. |  |  |# Possible cases table

|  | 1st step (assumption - this is the first user action with permissions) | Result (interim) | 2nd step | Result (final) |
|---|---|---|---|---|
| 1 | access to Location (fine) - ALLOWED | Location status - ON | access to BLE - ALLOWED | Location status - ON, BLE status - ON |
| 2 | access to Location (fine) - ALLOWED | Location status - ON | access to BLE - DENIED | Location status - ON, BLE status - OFF |
| 3 | access to Location (coarse) - ALLOWED | Location status - ON, BLE status - OFF | The system doesn't request BLE permission. |
| 4 | access to Location - DENIED | Location status - OFF, BLE status - OFF |
| 5 | access to BLE - ALLOWED | The app shows M261.The app requests Location access. | access to Location (Fine) - ALLOWED | Location status - ON, BLE status - ON |
| 6 | access to BLE - ALLOWED | The app shows M261.The app requests Location access. | access to Location (Coarse) - ALLOWED | Location status - ON, BLE status - OFF |
| 6 | access to BLE - ALLOWEDNote: in this case after user's choice the app will request Location access. | The app shows M261.The app requests Location access. | access to Location - DENIED | Location status - OFF, BLE status - OFF |
| 7 | access to BLE - DENIED | - | access to Location - ALLOWED (no matter which one) | Location status - ON, BLE status - OFF |
| 8 | access to BLE - DENIED | - | access to Location - DENIED | Location status - OFF, BLE status - OFF |
