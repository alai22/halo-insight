---
title: "[BL] ME03-US09 View all available 2.4 GHz WiFi hotspots"
sidebar_label: "[BL] ME03-US09 View all available 2.4 GHz WiFi hotspots"
sidebar_position: 36
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| ME03-EP02 Collar network connection setup |
| REVISED |
| Nicolay Gavrilov |
| HALO-2626 - ME03-US09 View all available 2.4 GHz WiFi hotspots Closed |
| 22 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# Contents

User story Acceptance criteria General criteria

# User story

\> As an Owner I want to configure Wi-Fi connection for my collars so that the devices could use my Wi-Fi AP to access the internet.

# Acceptance criteria

### General criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US09-AC15 | The mobile app and the collar support working with the following Wi-FI security protocols:WPAWPA2WEP64WEP128WPA_WPA2_MIXED | N/A |
| ME03-US09-AC01 | When configuring Wi-Fi connection parameters for a collar, users can see the list of all 2.4 GHz Wi-Fi APs that are available for the configured device. | Royaltek implemented scanning and transferring all 2.4 GHz APs that are visible for the configured collar over BLE. |
| ME03-US09-AC13 | Wi-Fi connection parameters configuring screen has 'Can't find your network?' link. Upon tapping on 'Can't find your network?' link the users are redirected to the web-site with instructions in the mobile browser. | We need the explanations about what is Wi-Fi bandwidth, why the collar might not see the networks. It also should have the instructions on how to make sure your Wi-Fi router is 2.4 GHz or enable 2.4 in case it is a dual-band one, etc. |
| ME03-US09-AC02 | The app has an asynchronous progress indication for the process of communicating with the collar to get the list of available Wi-Fi networks. |  |
| ME03-US09-AC03 | When the collar returns the list of available Wi-Fi networks, the user can select a Wi-Fi AP and enter the password for it. | N/A |
| ME03-US09-AC04 | Users can perform pull-to-refresh to update the list of available 2.4 GHz Wi-Fi AP. | N/A |
| ME03-US09-AC05 | If no Wi-Fi APs are visible for the collar, the app displays 'No 2.4 GHz Wi-Fi access points are visible for your collar. Pull to retry' text instead of the list of Wi-Fi networks. |  |
| ME03-US09-AC06 | In case the app fails to get the list of available Wi-Fi AP from the collar, it displays 'Unable to get the list of available Wi-Fi access points. Pull to retry' instruction. On pull-to-refresh, the app makes another attempt to get the list of Wi-Fi AP from the device. |  |
| ME03-US09-AC11 | Users can cancel the process of Wi-Fi configuring by tapping on the corresponding button. |  |
| ME03-US09-AC09 | When configuring Wi-Fi AP for a new collar, users can skip Wi-Fi AP configuring step and move right to the next step of the setup process. In this case, the collar will use the LTE module to connect to the internet. This option is not available when the user configures Wi-Fi for a previously added collar. | Configuring Wi-Fi for a previously added collar: |
| ME03-US09-AC10 | When configuring Wi-Fi AP for a new collar, upon tapping on the 'Skip' button, the user sees the 'M33 Wi-Fi is not connected' notification. | N/A |
