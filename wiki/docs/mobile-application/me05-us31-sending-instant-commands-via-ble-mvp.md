---
title: "ME05-US31. Sending instant commands via BLE (MVP)"
sidebar_label: "ME05-US31. Sending instant commands via BLE (MVP)"
sidebar_position: 65
last_modified: "May 15, 2020"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| ME05 Manage commands |
| AMENDED |
| Nicolay Gavrilov |
| HALO-3491 - MOB: ME05-US31. Sending instant commands via BLE (MVP) Closed |# User story

\> As an owner I want instant commands to be send via BLE so that they were applied on the collar faster than they are aplied now when they are sent via LTE.

# Acceptance criteria

| AC | Text | Notes/Links/Wireframes |
|---|---|---|
| ME05-US31-AC01 | Instant commands are sent via BLE and via the internet. BLE is used as the primary channel while the internet is used if:Bluetooth is disabled on the smartphoneThe collar was not found during the background scanningThe app failed to unlock the collar | N/A |
| ME05-US31-AC02 | In case the command is successfully sent via BLE, the mobile app displays 'success' animation after the command was applied and upon the receipt of this response via BLE from the collar. | N/A |
| ME05-US31-AC03 | In case the app failed to send the command via BLE, the mobile app sends it via the internet. It displays the 'success' animation after the command was applied and upon the receipt of the corresponding response from the cloud. | N/A |
| ME05-US31-AC05 | In case both BLE is disabled and the internet is unavailable on the smartphone, the app displays the "Collar is out of Wi-Fi, cellular and Bluetooth range” toast message. | The error should not be displayed in case the internet connection is unavailable, but the collar is within the range of smartphone Bluetooth. |
| ME05-US31-AC06 | The new method for sending instant commands is used both in case users send instant commands from the pet card on My Map and in case they send instant commands from the Pet Training screen. | N/A |
| ME05-US31-AC07 | If the Bluetooth permission is not granted (e.g. after the user re-installed the app) the app will ask for it on the first attempt to send instant feedback.And in case the user denies the Bluetooth permission the app should only use the internet channel until permission is granted. At that, the app should not request Bluetooth permission on sending instant feedback. | N/A |# Dependencies

| # | Text | Notes/Links/Wireframes |
|---|---|---|
| ME05-US31-DP06 | Collar FW has a characteristic to notify the mobile app about the result for instant commands that are sent via BLE. | See the sequence diagram belowMore info: ME05-EP01 Send instant commands via BLE |
| ME05-US31-DP08 | Collar registers all incoming commands in the logs. | More info: ME05-EP01 Send instant commands via BLE |# Sending instant commands via BLE (success flow) sequence diagram


