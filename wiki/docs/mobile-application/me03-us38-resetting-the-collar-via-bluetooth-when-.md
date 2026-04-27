---
title: "ME03-US38 Resetting the collar via Bluetooth when binding to pet"
sidebar_label: "ME03-US38 Resetting the collar via Bluetooth when binding to pet"
sidebar_position: 640
last_modified: "Jun 10, 2020"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| ME03 Manage collars |
| APPROVED |
| Nicolay Gavrilov |
| Mobile part: TBDBE part: HALO-3970 - BE: CVS support for resetting the collar via Bluetooth when binding to pet Closed Related bugs: HALO-3605 - BE should not process/save telemetry from old pet when collar was disconnected and linked to another pet Open HALO-3843 - FW: The stats from the previous Pet displays for the new one for the case when the user re-assign the collar to another pet during the day Closed |# User story

\> As a user I want Halo system to reset outdated collar config via Bluetooth right after it's bound to a new pet so that I could be sure it will work according to my expectations. Right now if I move an offline device to another another pet, I may forget that I need wait until the collar goes back online in order to download the new settings. As the result I am confused because the collar works differently from the settings that I can observe in the mobile app, because it was not synchronized with Halo BE. I also don't want the app to display the telemetry that belongs to pet #1 for the pet #2, in case I transfer the collar from pet#1 to pet#2 when the device is in offline.

# Acceptance criteria

| AC | Description | Notes / Links / Wireframes | Binding collar to a new pet | Handling the inability to connect to a collar via BT when binding a pet | Handling Bluetooth connection issues when binding the collar a pet | Automatic BT reconnection |
|---|---|---|---|---|---|---|
| ME03-US38-AC01 | The collar changes the logo color to white upon unbinding from the current pet. | FW part will be implemented by Michael Ehrman |
| ME03-US38-AC02 | The collar also changes the LED color from white to the new pet color upon successful binding to the new pet. |
| ME03-US38-AC03 | So as to make sure an offline collar resets the obsolete configuration after it is moved from one pet to another, the app sends an unbinding command via Bluetooth when the collar is bound to a new pet. | Collar to Pet binding |
| ME03-US38-AC07 | The app attempts to connect to the collar and shows the spinner after the user selects a pet and taps the 'Done' button. The spinner is displayed during the whole process of connecting to the collar via BT and binding the collar to the pet. |  |
| ME03-US38-AC08 | The user can tap on the 'Cancel' button before the smartphone is connected and paired with the collar. In this case, the app closes the pairing screen without showing any pop-up messages. | N/A |
| ME03-US38-AC09 | The 'Cancel' button is disabled after the smartphone is connected to the collar and sends the binding request to BE. | N/A |
| ME03-US38-AC10 | In case the collar is reset via BT but it takes more time for BE to synchronize the new configuration with the device, the user should see M141 Successfully linked collar to pet when the user successfully assigns the collar to a pet in the following cases:Linking collar to a pet from collars listLinking collar to a pet from pet cardLinking collar to a pet when creating a new petLinking collar to a pet when adding a new collar to a user accountLinking collar to a pet when tapping 'Test on collar' on a feedback settings screenUpon tapping on the "Ok" button the app closes the message and the dialogue window. | see Collar to Pet binding |
| ME03-US38-AC11 | If the collar is assigned to a new pet on BE side, and this change is synchronized with the device before the collar receives the 'unbind command' via BT command, the app should complete binding to a new pet without showing any messages. |
| ME03-US38-AC04 | To make sure the collar resets the obsolete configuration, binding it to a pet or a user is only possible in case the collar is connected to the smartphone via Bluetooth. In case the collar is not connected to the smartphone after 10 seconds, the app displays the M29 Unable to Pair message in the following cases:Linking collar to a pet from collars listLinking collar to a pet from pet cardLinking collar to a pet when creating a new petLinking collar to a pet when adding a new collar to a user accountLinking collar to a pet when tapping 'Test on collar' on a feedback settings screen | Appendix 3 – Error, Success, Warning Messages |
| ME03-US38-AC05 | In case the Bluetooth is disabled on the smartphone in one of the abovementioned cases, the app displays the M45 Disabled Bluetooth error message. |  |
| ME03-US38-AC16 | The user sees M124 Security error for provisioning in case the app fails to unlock the collar with Rolling Codes. Tapping on 'Ok' buttons closes the pop-up window. | ME03-US17. Provisioned collar error notifications |
| ME03-US38-AC17 | If the smartphone is offline when the app is connecting to the collar and there are to RC's cached, the app displays the M125 Connection error. If the user taps on the 'Cancel' button the app closes the pop-up message. If the user taps 'Try again' button the app sends another request to the Halo BE. | ME03-US22. Enable BLE communication in offline (caching Rolling Codes) |
| ME03-US38-AC20 | The user sees M142 "Bluetooth permission request" message when the user attempts to bind the collar to a pet and given the app has no Bluetooth permission and the user was never asked to provide it. | N/A |
| ME03-US38-AC21 | The user sees M143 "Bluetooth permission denied" message when the user attempts to bind the collar to a pet and given the app has no Bluetooth permission and the user refused to provide it. | N/A |
| ME03-US38-AC22 | When the user links the collar to a pet and the BT connection is lost before the app receives the response for 'unbind via BT' command from the collar, the app initiates automatic reconnection with the collar. And shows the spinner in the middle of the screen. | N/A |
| ME03-US38-AC23 | "Reconnecting with collar" panel is displayed in case the Bluetooth connection is not restored after 3 seconds of automatic reconnection attempts. |  |
| ME03-US38-AC24 | If the app failed to re-establish BT connection with the collar in 10 seconds and the collar is successfully bound to the new pet on BE, the app stops the reconnection attempts and displays M141 Successfully linked collar to pet. Upon tapping on the 'Ok' button the app completes the linking/reassigning process and closes the pop-up message. | N/A |
| ME03-US38-AC25 | If the automatic reconnection is in progress and no response is received from the BE for 15 seconds, the app displays M125 Connection error. If the user taps on the 'Cancel' button the app closes both the pop-up message and the collar/pet assignment screen. If the user taps 'Try again' button the app sends another request to BE. | N/A |
