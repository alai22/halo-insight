---
title: "ME03-US39 Resetting the collar via Bluetooth when binding to user account"
sidebar_label: "ME03-US39 Resetting the collar via Bluetooth when binding to user account"
sidebar_position: 641
last_modified: "Jun 10, 2020"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| ME03 Manage collars |
| APPROVED |
| Nicolay Gavrilov |
| Mobile part: TBDBE part: HALO-3969 - BE: CVS support for resetting the collar via Bluetooth when binding to user account Closed |# User story

\> As a user I want Halo system to reset outdated collar config via Bluetooth right after it's bound to my account so that I could be sure that it will work according to my expectations. Right now if an offline device is removed from an account it keeps the obsolete configuration until it goes online and synchronizes with the Halo BE. I may be unaware about this, and as the result I will not know why the collar works as if it is bound to the previous account although I've added it to mine. I also don't want the app to display the telemetry that belongs to the pet from the previous acccount for my pet when the unsynchronized collar goes online.

# Acceptance criteria

| AC | Description | Notes / Links / Wireframes | Handling binding of a non-synchronized offline device to a user account | Binding collar to a new user account | Handling the inability to connect to the collar via BT when binding to a user account | Automatic BT reconnection |
|---|---|---|---|---|---|---|
| ME03-US39-AC01 | The collar changes the color of the logo to white when the device is removed from the user account and this change is synchronized with the device. | FW part will be implemented by Michael Ehrman |
| ME03-US39-AC02 | So as to make sure an offline collar resets the obsolete configuration after it is moved from one user account to another, the app sends an unbinding command via Bluetooth when the collar is bound to a new user. | Collar Provisioning |
| ME03-US39-AC03 | In case the collar is unbound from the previous owner on BE side, but the device is offline and not synchronized with BE, the collar cannot be unlocked by the new owner because ESN is not available. To handle this case, the collar should allow reading ESN even before it is unlocked with a Rolling Code. | FW part will be implemented by Michael Ehrmansee also Collar Provisioning |
| ME03-US39-AC04 | As an additional security measure, the collar should limit the number of times the ESN could be read by 50 times per day. In case the limit is exceeded, the app should display M17 Technical error message. | FW part will be implemented by Michael Ehrman |
| ME03-US39-AC05 | The "Pairing" screen is displayed during the process of binding the collar to the user account, caching a set of rolling codes, and when the app is sending the "unbind" command via BT. |  |
| ME03-US39-AC06 | The user can tap on the 'Back' button before the smartphone is connected and paired with the collar. In this case, the app closes the pairing screen. | N/A |
| ME03-US39-AC07 | Both the 'Back' button and the "back swipe" gesture are disabled after the smartphone is connected to the collar and sends the binding request to BE. | N/A |
| ME03-US39-AC08 | The app no longer has the "Done" button and "\<collar serial number\> Connected" caption on the "Successfully Paired" screen. |  |
| ME03-US39-AC09 | "Successfully paired" screen is displayed upon successful binding the collar to the user account and if the collar either successfully synchronized the new configuration with the Halo BE OR successfully completed unbinding from the previous owner via BT. | see Collar Provisioning |
| ME03-US39-AC10 | The user is automatically redirected from the "Successfully paired" screen to the next screen after 2 seconds timeout. | N/A |
| ME03-US39-AC11 | To make sure the collar resets the obsolete configuration, binding it to a new user is only possible in case the collar is connected to the smartphone via Bluetooth. In case the smartphone fails to connect to the collar from the first attempt, the app displays the M29 Unable to Pair message when adding a new collar to a user account. | N/A |
| ME03-US39-AC12 | In case the Bluetooth is disabled on the smartphone when adding a new collar to a user account, the app displays the M45 Disabled Bluetooth error message. Tapping on 'Ok' button closes both the pop-up window and the pairing screen. | N/A |
| ME03-US39-AC13 | If the smartphone is offline when the app is connecting to the collar via BLE and there are to RC's cached, the app displays the M125 Connection error. If the user taps on the 'Cancel' button the app closes both the pop-up message and the pairing screen. If the user taps 'Try again' button the app sends another request to the Halo BE. | ME03-US22. Enable BLE communication in offline (caching Rolling Codes) |
| ME03-US39-AC14 | The user sees M142 "Bluetooth permission request" message when the user attempts to bind the collar to a pet and given the app has no Bluetooth permission and the user was never asked to provide it. Tapping on the 'Don't allow' button closes both the pop-up window and the pairing screen. | A1-US01. "Bluetooth permission request" message |
| ME03-US39-AC15 | The user sees M143 "Bluetooth permission denied" message when the user attempts to bind the collar to a pet and given the app has no Bluetooth permission and the user refused to provide it. Tapping on the 'Cancel' button closes both the pop-up window and the pairing screen. | A1-US02. "Bluetooth permission denied" message |
| ME03-US39-AC16 | The user sees M124 Security error for provisioning in case the app fails to unlock the collar with Rolling Codes. Tapping on 'Ok' buttons closes the pop-up window. | ME03-US17. Provisioned collar error notifications |
| ME03-US39-AC17 | When a collar is bound to the user account and the BT connection is lost before the app receives the response for 'unbind via BT' command from the collar, the app initiates automatic reconnection with the collar. At that, the user remains on the "Pairing" screen. | N/A |
| ME03-US39-AC18 | If the automatic reconnection is in progress and the collar is successfully added to the user account on the BE side and the device synchronized the new configuration, the app displays the "Successfully paired" screen. | N/A |
| ME03-US39-AC19 | If the automatic reconnection is in progress and no response is received from the BE for 15 seconds, the app displays M125 Connection error. If the user taps on the 'Cancel' button the app closes both the pop-up message and the collar binding screen. If the user taps 'Try again' button the app sends another request to the Halo BE. | N/A |
| ME03-US39-AC20 | If the automatic reconnection is in progress and BE returns 400, 500, 409, 404 or 401 errors, the app displays M126 Communication error. If the user taps on the 'Ok' button the app closes both the pop-up message and the collar binding screen. | N/A |
