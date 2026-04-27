---
title: "[BL] ME03-US11. Connecting collar to Wi-Fi AP and IoT hub"
sidebar_label: "[BL] ME03-US11. Connecting collar to Wi-Fi AP and IoT hub"
sidebar_position: 38
author: "Galina Lonskaya"
---

| Epic | Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| ME03-EP01 New user / collar provisioning approach |
| REVISED |
| Nicolay Gavrilov |
| HALO-2798 - MOB: ME03-US11. Connecting collar to Wi-Fi AP and IoT hub Closed |
| 22 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# Contents

User story Acceptance criteria

# User story

\> As an Owner I want to see the collar connection progress so that I know why it takes so long to configure the device.

# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US11-AC01 | The app displays the name of the selected Wi-Fi network during the process of connecting the collar to the Wi-Fi AP and IoT hub. |  |
| ME03-US11-AC02 | The app displays the collar connection process. The following collar connection steps are displayed on the screen:Sending settings to the collarConnecting to the access pointConfiguring IP addressConnecting to the InternetConnecting to HALO secure cloud services | The collar provides a 'current state' indicator to the mobile app via BLE.The mobile app should display all previous steps as COMPLETED; one step as 'in progress' (with animated spinner); and subsequent steps as 'not started'See below for chart of 'state value' vs. UI/display according to #2If the collar step # jumps FORWARD (higher value), update the UI according to rule #2 (all earlier steps are completed)If the collar step # goes BACKWARDS (lower value), update the UI according to rule #2 (even if this means marking previously completed steps as 'not started')States are:RSI_WLAN_INITIAL_STATE = 0, (started), "Connecting to AP" not yet startedRSI_WLAN_UNCONNECTED_STATE = 1, "Connecting to AP" in progressRSI_WLAN_CONNECTED_STATE = 2, "Connecting to AP" completed; "Configuring IP address" in progressRSI_WLAN_IPCONFIG_DONE_STATE = 3, "Configuring IP address" completed; "Connecting to Internet" in progressRSI_WLAN_SOCKET_CONNECTED_STATE = 4, "Connecting to Internet" completed; "Connecting to Halo secure cloud services" in progress. |
| ME03-US11-AC03 | Each step of the collar connection process has an asynchronous progress indicator. The indicator appears next to a step when the device reaches it. | N/A |
| ME03-US11-AC04 | If a collar connection step is completed successfully, the app marks it with the corresponding 'success' icon. | N/A |
| ME03-US11-AC05 | If a collar connection step results in an error, the collar automatically repeats all the relevant actions of the collar connection process. At that mobile app EITHER discards all the progress on the screen and goes back to the very first step of the process OR continues asynchronous process indication of the current step. In this case, the user can close the collar connection process pop-up by tapping on the corresponding button. | N/A |
| ME03-US11-AC07 | If all collar connection process steps are successfully completed, the app hides the dialogue window with the list of Wi-Fi networks. | N/A |
