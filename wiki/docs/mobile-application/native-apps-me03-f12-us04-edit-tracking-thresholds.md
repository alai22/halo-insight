---
title: "(Native apps) ME03-F12-US04. Edit Tracking Thresholds: 'Current GPS Level' pin and status"
sidebar_label: "(Native apps) ME03-F12-US04. Edit Tracking Thresholds: 'Current GPS Level' pin and status"
sidebar_position: 502
author: "Galina Lonskaya"
---

| Document owners | Links to Jira/Linear tickets | Changes history |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-405/[ios]-edit-tracking-thresholds-current-gps-level-pin-and-status |
| 27 Feb 2025 draft is created by Galina Lonskaya |# Contents

Acceptance criteria

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-F12-US04-AC01 | The app should not allow to drag the 'current GPS level' pin. |
| ME03-F12-US04-AC02 | The 'current GPS level' pin and value should be the same UI as shown on 'Signal Analysis' screen. |
| ME03-F12-US04-AC03 | The 'current GPS level' pin should be dynamically changed in real-time on the basis of chosen GPS thresholds. |
| ME03-F12-US04-AC04 | '\<X\> sec ago ' label should reflect when the last GPS data was received from the collar, follow the universal rule BR-16 Passed time format |Tech details

Current GPS Level also comes from the Current GPS Level Characteristic - GPSLastSample. We should read the value from the characteristic continuously, with a 1 second delay between readingsThis value may need to be converted to conventional units to be displayed on the scale. In this case, the converted values are only used for displaying

X sec ago should start counting when we are not receiving data from the collar. This is only possible when the collar is not connected to the phone or cannot read data from the characteristic. We should use a threshold of 2 seconds, since we read BLE data every second


