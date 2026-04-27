---
title: "(Native apps) ME03-F12-US05. Edit Tracking Thresholds: Reconnection with collar"
sidebar_label: "(Native apps) ME03-F12-US05. Edit Tracking Thresholds: Reconnection with collar"
sidebar_position: 500
author: "Galina Lonskaya"
---

| Document owners | Links to Jira tickets | Changes history |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-406/[ios]-edit-tracking-thresholds-reconnection-with-collar |
| 27 Feb 2025 draft user story is created by Galina Lonskaya |# Contents

User story Acceptance criteria

# User story

\> As a Halo app account owner I want to see if the BLE connection with collar is broken so that I can be aware about Bluetooth connection issues with collar

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-F12-US05-AC01 | In case the Bluetooth connection with the collar is lost, then: the app should start the process of automatic reconnection with the collar, see the requirements in https://linear.app/fueled/issue/HALO-287/[ios]-reconnecting-with-collar-panela spinner should be displayed over 'Edit Tracking Thresholds' screen, see Figma |
| ME03-F12-US05-AC02 | The spinner timeout should be 10 seconds. |
| ME03-F12-US05-AC03 | While the spinner is shown, 'Done' button should be disabled. |
| ME03-F12-US05-AC04 | If any Bluetooth connection error happens OR the timeout is expired, then the app should:hide the "Reconnecting with collar" panel;M70 popup Figma should be shown (see the old reference in Confluence M70. No answer from the collar)GPS bar should not be shown |
| ME03-F12-US05-AC05 | If I tap on CTA on M70 popup, then: the popup should be closed the connection process with the collar should be stoppedthe 'Signal Analysis' screen with the map should be opened. |Tech details

When reconnecting, we do not make a direct connection to the collar, but wait for the status to change. To do this, we subscribe to the collar's connection status changes.If the status changes to not ready - we use a 10 second timeout for the status to change.Since we don't make a direct connection, we don't expect various errors from the collar, so we show the M70 popup anyway (and after the timeout expires)See ManualCalibrationSettingsViewModel.GetCollarSubscriptions for details


