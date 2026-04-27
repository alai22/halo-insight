---
title: "(Native apps) ME03-F12-US02. Edit Tracking Thresholds: 'Edit Ttracking Tresholds' screen general description + set up connection with collar"
sidebar_label: "(Native apps) ME03-F12-US02. Edit Tracking Thresholds: 'Edit Ttracking Tresholds' screen general description + set up connection with collar"
sidebar_position: 497
last_modified: "Mar 13, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links to Jira/Linear tickets | Changes history |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-403/[ios]-edit-tracking-thresholds-set-up-connection-with-collar |
| 27 Feb 2025 draft story is created by Galina Lonskaya |# Contents

User story Acceptance criteria

# User story

\> As a Halo app account owner I want to be able to adjust GPS signal levels thresholds so that the GPS status of my collar will be identified more precisely by the collar.

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-F12-US02-AC01 | Precondition: 'Advanced Settings' is openedIf I tap the 'Edit Tracking Threshold' button and Bluetooth permission is denied, then:M143 figma popup should be shown (see the old reference in Confluence M143). |
| ME03-F12-US02-AC02 | If I tap the 'Edit Tracking Threshold' button and Bluetooth is disconnected on the smartphone, then:M178 if Bluetooth is disconnected on the smartphone (see the old reference in Confluence M178)seeiOS Figmasee Android Figma |
| ME03-F12-US02-AC03 | If I tap the 'Edit Tracking Threshold' and the connection with collar is not set up, then: the 'Edit Tracking Threshold' screen should be shown, see Figma, waiting UI design from Ryanthe process of pairing via Bluetooth with the required collar should be started;the spinner should be shown |
| ME03-F12-US02-AC04 | The spinner timeout should be 10 seconds. |
| ME03-F12-US02-AC05 | If the connection is the collar is set up, then: the spinner should not be shown instead of the spinner GPS level bar should be shown, this screen state will be described within the separate user story: (Native apps) ME03-F12-US03. Edit Tracking Thresholds: 'High/Low |
| ME03-F12-US02-AC06 | If the pairing with the required collar isn't successful due the collar isn't found OR the app didn't receive data during standard timeout (i.e. 10 sec), then the system should:M70 popup Figma should be shown (see the old reference in Confluence M70. No answer from the collar)GPS bar should not be shown |
| ME03-F12-US02-AC07 | If the app fails to unlock the collar with Rolling Codes, then:M124 popup Figma should be shown (see the old reference in Confluence M124 Security error for provisioning) GPS bar should not be shown |
| ME03-F12-US02-AC08 | If too many rolling codes are requested, then:M136 popup Figma should be shown (see the old reference in Confluence M136 Error for reaching the daily limit for rolling codes)GPS bar should not be shown |
| ME03-F12-US02-AC09 | If I tap on CTA on M70, M124, M136 popup, then: the popup should be closed the connection process with the collar should be stoppedthe 'Signal Analysis' screen with the map should be opened. |Tech details

Timeout to connect to the collar and get initial data on this screen = 10 seconds. This is separate from the overall timeout for connecting to the collar.The timeout to connect to the collar is taken from the config GET /configuration Collar.BlePairingMaxTimeInSeconds field


