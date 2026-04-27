---
title: "[BL] ME03-US24. Collars list state in case last telemetry from the collar was sent more than 5 minutes ago"
sidebar_label: "[BL] ME03-US24. Collars list state in case last telemetry from the collar was sent more than 5 minutes ago"
sidebar_position: 123
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED + REVISED |
| Maria Shikareva [X], Anastasia Brechko (QA), Eugene Paseka (BE) |
| HALO-5908 - BE: ME03-US24. Collars list state in case last telemetry from the collar was sent more than 5 minutes ago Closed HALO-6255 - MOB: ME03-US24. Collars list state in case last telemetry from the collar was sent more than 5 minutes ago Closed |
| Maria Shikareva [X] 23 Feb 2021 Updated the design for Wi-Fi status (extended the Wi-Fi panel in case if there are 2 rows). |# User story

\> As a User I want to see battery, Wi-Fi and LTE indicators whitened with updated statuses for the last Wi-Fi/ LTE connection when the last collar's telemetry was sent more than 5 minutes ago so that not to see the outdated information.

# Acceptance criteria

| AC | Description | iOS screen design / implementation statusIOS TO DO | Android screen design / implementation statusANDROID TO DO | Battery indicator | Wi-Fi indicator | LTE (cellular) indicator |
|---|---|---|---|---|---|---|
| ME03-US24-AC01 | Battery indicator should be whitened in the minimized view on the Collars list within Settings tab in case the last telemetry was received from the collar more than 5 minutes ago. | Note: see Eva's Halo example. | Design is similar to iOS |
| ME03-US24-AC02 | Battery indicator should be whitened in the expanded view on the Collars list within Settings tab in case the last telemetry was received from the collar more than 5 minutes ago. | Note: see Richard's Halo example. | Design is similar to iOS |
| ME03-US24-AC03 | Battery indicator should be whitened on the Collars list within 'Assign a Collar' screen while adding a pet in case the last telemetry was received from the collar more than 5 minutes ago. | Note: see Richard's Halo example in Assigned Collars area. | Note: see 'Richard's Halo example in Assigned Collars area. |
| ME03-US24-AC04 | Battery indicator should be whitened on the Collars list within 'Confirm Collar Choice' screen while adding a fence in case the last telemetry was received from the collar more than 5 minutes ago. | Note: see Eva's Halo example. | Note: see Eva's Halo example. |
| ME03-US24-AC05 | If the last telemetry was received from the collar more than 5 minutes ago, Wi-Fi tile on the Collars list within Settings tab should be displayed according to the given screen design:crossed Wi-Fi icon;Last connected to 'Last Wi-Fi SSID';Last time Wi-Fi was connected - 'X time ago'. | See the design here. | Design is similar to iOS |
| ME03-US24-AC06 | 'Last Wi-Fi SSID' label displays the name of the Wi-Fi network that was received from the collar in the last telemetry message. | - | - |
| ME03-US24-AC07 | Last time Wi-Fi was connected shows how long ago Wi-Fi was connected based on the telemetry received. The format is described in BR-16 Passed time format.Note: The time is derived from the timestamp of the last telemetry message in which the collar reported that it is connected to Wi-Fi. | - | - |
| ME03-US24-AC08 | If there is no information about last Wi-Fi connection, then the app should display the network connection information according to the given screen design. |  | Design is similar to iOS |
| ME03-US24-AC09 | If the last telemetry was received from the collar more than 5 minutes ago, Cellular tile on the Collars list within Settings tab should be displayed according to the given screen design:crossed Cellular icon;Last connected to 'Last Cellular Network';Last time LTE was connected - 'X time ago'. |  | Design is similar to iOS |
| ME03-US24-AC10 | 'Last Cellular Network' label displays the name of the cellular network that was received from the collar in the last telemetry message. | - | - |
| ME03-US24-AC11 | Last time LTE was connected shows how long ago LTE was connected based on the telemetry received. The format is described in BR-16 Passed time format.Note: The time is derived from the timestamp of the last telemetry message in which the collar reported that it is connected to cellular. | - | - |
| ME03-US24-AC12 | If there is no information about last Cellular connection, then the app should display the network connection information according to the given screen design. |  | Design is similar to iOS |
| ME03-US24-AC13 | The battery/ Wi-Fi/ LTE indicator state should be updated on refreshing the page only. | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME03-US24-IN1 | The logic for Wi-Fi/ LTE last connection should be similar to what is described here: AE03-US33. Details about collar last connection. |
