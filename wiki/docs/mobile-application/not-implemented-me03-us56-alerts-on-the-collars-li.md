---
title: "[Not implemented] ME03-US56. Alerts on the 'Collars' list"
sidebar_label: "[Not implemented] ME03-US56. Alerts on the 'Collars' list"
sidebar_position: 150
last_modified: "Aug 25, 2021"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X], Eugene Paseka (BE), Anastasia Brechko (QA), Pavel Leonenko (MOB) |
| HALO-7259 - MOB: Alert scheme on collars list Ready for Development HALO-7618 - BE: Alert scheme on collars list Ready for Development |
| 06 Jul 2021 Maria Shikareva [X] ME03-US56-AC01, ME03-US56-AC06 are changes based on the changes to the main US: ME08-US20. Get the notifications about LTE/ Wi-Fi not connected.Document status is changed (Approved on 2021-07-05 Meeting notes: BA+UX call).25 Aug 2021 Maria Shikareva [X] Added links to Zeplin. |# User story

\> As an account owner I want to see visual marks if LTE/Wi-Fi are not connected for too long so that to be notified about it and fix it.

# Acceptance criteria

| AC | Description | iOS screen designs/ implementation status | Android screen designs/ implementation status |
|---|---|---|---|
| Cellular alerts |
| ME03-US56-AC01 | The app should display the alert icon next to the Cellular icon in the collars list if the collar was connected to LTE more than 2 days ago (see screen designs).Note: the icon should be displayed every time the mobile app gets corresponding information from BE. | Pic ME03-US56-P01 'Alert for Cellular' iconLink to Zeplin | Link to Zeplin |
| ME03-US56-AC02 | The icon should disappear when the mobile app gets info from BE that:the collar is connected to LTE right nowORthe collar was connected to LTE less than 2 days ago. | - | - |
| ME03-US56-AC03 | Precondition: the collar is online AND there's info about last Cellular connection in the DB.If according to the last received data the collar is now using Wi-Fi, the app should display the Cellular connection information in the following way:crossed Cellular icon;Last connected to 'Last Cellular Network';Last time LTE was connected - 'X time ago'. | See ME03-F01-AC50 in the ME03-F01. Collars list. | - |
| ME03-US56-AC04 | 'Last Cellular Network' label displays the name of the cellular network that was received from the collar in the last message. | - | - |
| ME03-US56-AC05 | Last time LTE was connected shows how long ago LTE was connected based on the data received from the collar. The format is described in BR-16 Passed time format.Note: The time is derived from the timestamp of the last message in which the collar reported when it was last connected to cellular (CollarResponseDto.CellularSettings.LastConnected). | - | - |
| Wi-Fi alerts |
| ME03-US56-AC06 | The app should display an alert icon next to the Wi-Fi icon in the collars list in one of the following cases:the collar was connected to Wi-Fi more than 2 days ago;Wi-Fi hasn't been configured yet (i.e. no Wi-Fi networks added).Note: the icon should be displayed every time the mobile app gets corresponding information from BE. | - | - |
| ME03-US56-AC07 | The icon should disappear when the mobile app gets info from BE that:the collar is connected to Wi-Fi right nowORthe collar was connected to Wi-Fi less than 2 days ago. | - | - |
| ME03-US56-AC08 | Precondition: the collar is online AND there's info about last Wi-Fi connection in the DB (i.e. Wi-Fi is configured for the collar).If according to the last received data the collar is now using LTE, the app should display the Wi-Fi connection information in the following way:crossed Wi-Fi icon;Last connected to 'Last Wi-Fi SSID';Last time Wi-Fi was connected - 'X time ago'. | See ME03-F01-AC50 in the ME03-F01. Collars list. | - |
| ME03-US56-AC09 | 'Last Wi-Fi SSID' label displays the name of the Wi-Fi network that was received from the collar in the last message. | - | - |
| ME03-US56-AC10 | Last time Wi-Fi was connected shows how long ago Wi-Fi was connected based on the data received from the collar. The format is described in BR-16 Passed time format.Note: The time is derived from the timestamp of the last message in which the collar reported when it was last connected to Wi-Fi (CollarResponseDto.WiFiSettings.LastConnected). | - | - |
| ME03-US56-AC11 | Other texts for LTE/ Wi-fi connection statuses should remain without changes as described in the "Different cases for Wi-Fi/ LTE connection" table below. | - | - |
| ME03-US56-AC12 | 2 days for LTE/ Wi-Fi should be configurable values. |  |  |
| Alerts on the 'Collars list' |
| ME03-US56-AC13 | The app should display the alert icon on the collar photo on the collars list if at least one alert is displayed as described in the ACs above (see screen designs, "Molly's Halo" as an example). | Pic ME03-US56-P02 'Alert on Collars list' iconLink to Zeplin | Link to Zeplin |
| ME03-US56-AC14 | If there's another icon on the collar's photo, then the alert icon should be displayed near the collar photo on the collars list (see 'Alert on Collars list' icon, "Buddy's Halo" as an example). | - | - |# Different cases for Wi-Fi/ LTE connection

|  | LTE is connected right now | LTE was connected several time ago | LTE was never connected | Wi-Fi is connected right now | Wi-Fi was connected several time ago | Wi-Fi was never connected | LTE was connected several time ago | No info about LTE | Wi-Fi was connected several time ago | No info about Wi-Fi |
|---|---|---|---|---|---|---|---|---|---|---|
|  | Collar online | Collar offline |
|  | LTE | Wi-Fi | LTE | Wi-Fi |
| as is | Connected to Verizon | Paused. Currently using Wi-Fi | Cellular is not available | Connected to Softeq 5G | Softeq 5GH is not available | No Wi-Fi network added yet | Last connected to Verizon 7 hours ago | Cellular is not available | Last connected to Softeq 7 hours ago | Wi-Fi hasn't been connected. Please, configure Wi-Fi |
| to be | Connected to Verizon | Last connected to Verizon 7 hours ago | Cellular is not available | Connected to Softeq 5G | Last connected to Softeq 7 hours ago | No Wi-Fi network added yet | Last connected to Verizon 7 hours ago | Cellular is not available | Last connected to Softeq 7 hours ago | Wi-Fi hasn't been connected. Please, configure Wi-Fi |
