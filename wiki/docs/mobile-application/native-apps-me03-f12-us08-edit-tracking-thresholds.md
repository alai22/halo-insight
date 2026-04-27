---
title: "(Native apps) ME03-F12-US08. Edit Tracking Thresholds: Save/Cancel Updated Tracking Thresholds"
sidebar_label: "(Native apps) ME03-F12-US08. Edit Tracking Thresholds: Save/Cancel Updated Tracking Thresholds"
sidebar_position: 501
last_modified: "Mar 13, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links to Jira/Linear tickets | Changes history |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-409/[ios]-edit-tracking-thresholds-savecancel-new-thresholds |
| 27 Feb 2025 draft story is created by Galina Lonskaya |# Contents

User story Acceptance criteria

# User story

\> As a Halo app account owner I want to be able to save the min and max GPS thresholds so that the collar can use the chosen GPS settings further.

# Acceptance criteria

| AC | Description | Cancel button functionality | Done button functionality |
|---|---|---|---|
| ME03-F12-US08-AC01 | If the user taps the 'Cancel' button and some changes were made, then:M204 popup Figma should be shown (see the old reference in Confluence M204 Cancel GPS calibration ). |
| ME03-F12-US08-AC02 | If the user taps on the 'Cancel' button and no changes were madeOR the user taps on the "Discard Changes" button on M204 popup, then:the Bluetooth connection with the collar should be brokenthe 'Edit Tracking Thresholds' screen should be closedthe 'Signal Analysis' screen with no changes saved (i.e. the previously saved settings should be applied). |
| ME03-F12-US08-AC03 | The 'Done' button should be shown only in case HIGH and/or LOW GPS slider value(s) are different from the previously saved. |
| ME03-F12-US08-AC04 | If the user taps the 'Done' button, then:the new thresholds to the collar via BLEthe spinner over the whole screen should be shown while sending data to the collar |
| ME03-F12-US08-AC05 | If after tapping the 'Done' button the new thresholds are suссessfully sent to the collar, then:the 'Edit Tracking Thresholds' screen should be closedthe 'Signal Analysis screen with the updated LOW/HIGH GPS thresholds values should be shown. |
| ME03-F12-US08-AC06 | If after tapping the 'Done' button the collar cannot save the updated Low and High GPS values OR the collar doesn't respond during 'BLE pairing MAX time (in seconds)', then:M225 popup Figma should be shown (see the old reference in Confluence M225. Failed to send data) |
| ME03-F12-US08-AC07 | If after tapping CTA button on M225, the popup should be closed. |Tech details

Current GPS Level Characteristic is used to write the valueThe message format for recording is described here - Collar BLE GAP/GATT.The TranCode is obtained from the data we read from the characteristic (2nd byte). It may be best to read the data again before saving to get an up-to-date TranCodeBefore sending data to the collar, we must make sure that the connection to the collar is established. The timeout from the GET /configuration Collar.BlePairingMaxTimeInSeconds field is also used for this purpose. (This is probably just an extra check, since the Done button should be off if the collar is not connected)To get a response from the collar, the collar sends notifications via this characteristic. It is worth subscribing to the notification before sending the data, and waiting for the message after it is sent

In our code, we have this logic in CurrentGpsCharacteristic.SaveBoundariesToCollarAsync


