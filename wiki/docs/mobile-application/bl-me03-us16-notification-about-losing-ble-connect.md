---
title: "[BL] ME03-US16 Notification about losing BLE connection with the collar"
sidebar_label: "[BL] ME03-US16 Notification about losing BLE connection with the collar"
sidebar_position: 44
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue | Revision History |
|---|---|---|---|---|
| ME03. Manage collars |
| REVISED |
| Nicolay Gavrilov |
| HALO-2769 - MOB: ME03-US16 Notification about losing BLE connection with the collar Closed |
| 1/8/2020 - AC01 is updated. Error displaying is changed on 'Lost connection with the collar' screen. Michael has approved at Action Item list22 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# Contents

User story Acceptance criteria General criteria

# User story

\> As an Owner I want to see an error in case the collar lost connection with my smartphone so that I know the reason why can't I continue the Wi-Fi setup process.

# Acceptance criteria

### General criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US16-AC01 | When on the 'Choose a network' screen, in case the connection with the collar is lost before the smartphone gets the list of networks from the collar, the app displays 'Lost connection with the collar' notification. At that, the app continues the attempts to reconnect to the collar. In case the connection is restored, the app automatically closes the notification and updates the list of networks. | [BL] ME03-US11. Connecting collar to Wi-Fi AP and IoT hub |
| ME03-US16-AC02 | Precondition: the app didn't receive the list of Wi-Fi networks (the collar is disconnected right after entering SN).If the user closes the pop-up message in this case, the app discontinues the attempts of automatic reconnecting and displays the corresponding error. | [BL] ME03-US09 View all available 2.4 GHz WiFi hotspots |
| ME03-US16-AC02 | Precondition: the app received the list of Wi-Fi networks and the connection is lost when the user tries to refresh it.If the user closes the pop-up message in this case, the app discontinues the attempts of automatic reconnecting and displays the previously received list of Wi-Fi networks. | N/A |
| ME03-US11-AC06 | The M122 Lost connection with the collar is displayed in case the smartphone loses connection with the collar in the process of Connecting collar to Wi-Fi AP and IoT hub. The app displays the error in 2 seconds after the connection is lost. At that, the collar continues the process of connecting to the Wi-Fi AP and IoT hub in the background. At the same time, the app continues the attempts to reconnect to the collar. In case the connection is restored, the pop-up is automatically closed and the user will EITHER see the actual progress of the collar connection process if it is not completed OR will be redirected to the next step.When the user closes the pop-up message the app aborts the connection process. | [BL] ME03-US11. Connecting collar to Wi-Fi AP and IoT hub |
