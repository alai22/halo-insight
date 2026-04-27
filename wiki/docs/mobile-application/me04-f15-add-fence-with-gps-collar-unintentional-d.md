---
title: "ME04-F15. Add fence with GPS: Collar unintentional disconnection"
sidebar_label: "ME04-F15. Add fence with GPS: Collar unintentional disconnection"
sidebar_position: 114
last_modified: "Nov 25, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| Baseline story |
| REVISED |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko |
| HALO-2031 - [ME04. Create Fence with a collar] : ME04-US35. Be aware of the collar unintentional disconnection Closed HALO-5357 - Android GOAL: Add/Edit fence with GPS Closed |# User story

\> As owner, I want to view that the collar is disconnected at the moment and tries to reconnect so that I can see that I can not add fence posts at the moment, but the app tries to fix it.

# Acceptance criteria

| AC | Description | iOS implementation status / UI design | Android implementation status / UI design | Restoring Bluetooth connection when creating a fence with a collar |
|---|---|---|---|---|
| ME04-F15-AC01 | Precondition: The collar is paired, Create New Fence flow is in progressIf Bluetooth becomes disabled on the smartphone, then the M102 No Bluetooth (fence creation) error should be displayed. | - | - |
| ME14-F15-AC02 | In case the Bluetooth connection with the collar is lost, when the user creates a fence with the collar the app initiates the process of automatic reconnection with the collar. | - | - |
| ME14-F15-AC03 | In case the connection with the collar is lost and the user taps on 'Select a collar' icon on the map screen, the app stops automatic reconnection attempts and displays the Confirm Collar Choice screen. See ME04-F10 Add fence with GPS: Confirm Collar Choice. | - | - |
| ME14-F15-AC04 | In case after 3 seconds of automatic reconnection attempts the Bluetooth connection with the collar is not restored, the app:displays "Reconnecting with collar" panel,removes the 'Add(GPS)' button from the toolbarand changes the collar pin to the 'Outdated' state right after losing Bluetooth connection with the collar | Pic 1 - Create New Fence: reconnecting with collarSee the screen in Zeplin. | See the screen in Zeplin. |
| ME14-F15-AC05 | In case the user taps 'Add (GPS)' button within 3 seconds since the smartphone lost connection with the collar, no fence post is added and the app shows the 'Create new fence' screen in the reconnecting state (see ME14-F15-AC04). | - | - |
| ME14-F15-AC06 | In case the Bluetooth connection with the collar is restored, the app hides the "Reconnecting with collar" panel, changes the state of the collar pin back to normal, and shows the 'Add(GPS)' button on the toolbar. | - | - |
| ME14-F15-AC07 | The app discontinues automatic attempts to reconnect with the collar upon tapping on the "Cancel" button on the "Create New Fence" screen. | - | - |
| ME14-F15-AC08 | The app discontinues automatic attempts to reconnect with the collar and displays the Confirm Collar Choice screen (see ME04-F10 Add fence with GPS: Confirm Collar Choice) upon tapping on the 'Select collar' icon. | - | - |
| ME14-F15-AC09 | In case the app fails to unlock the collar with Rolling Codes on the fence creation screen, it stops the automatic reconnection attempts, hides the "Reconnecting with collar" panel and the user sees M124 Security error for provisioning. If the user taps on the 'Ok' button the app closes the error pop-up and the user remains on the fence creation screen. | - | - |
| ME14-F15-AC10 | If the smartphone is offline when the app reconnecting with the collar and there are no RCs cached, the app stops the automatic reconnection attempts, hides the "Reconnecting with collar" panel, and displays the M125 Connection error. If the user taps on the 'Cancel' button the app closes both the pop-up message. If the user taps 'Try again' button the app sends another request to the Halo BE. | ME03-US22. Enable BLE communication in offline (caching Rolling Codes) | - |
