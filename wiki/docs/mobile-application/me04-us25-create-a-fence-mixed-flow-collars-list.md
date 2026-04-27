---
title: "ME04-US25. Create a fence (mixed flow): collars list"
sidebar_label: "ME04-US25. Create a fence (mixed flow): collars list"
sidebar_position: 12
author: "Galina Lonskaya"
---

| Role | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| Owner |
| REVISED |
| Galina Lonskaya |
| HALO-2014 - [ME04-US25]: Create a fence (mixed flow): collars list Closed |# User story IMPLEMENTED

\> As owner, I want to view the scanned collars list so that I can select a necessary one.

# Acceptance criteria

| AC | Text |
|---|---|
| ME04-US25- AC01 | The "Add Collar for GPS" screen should consist of the scanned via BLE user's collars. Pic 1 Add Collar for GPS - collars listThe screen consists of:"Add Collar for GPS" headingCancel button"Scanning" label + spinnerEach card with collar's details should contain:Collar's photo + Collar RingCollar's battery level with iconDevice Nickname - if the collar is linked to a petDevice Product Name | Pic 1 Add Collar for GPS - collars list | The screen consists of:"Add Collar for GPS" headingCancel button"Scanning" label + spinnerEach card with collar's details should contain:Collar's photo + Collar RingCollar's battery level with iconDevice Nickname - if the collar is linked to a petDevice Product Name |
| Pic 1 Add Collar for GPS - collars list | The screen consists of:"Add Collar for GPS" headingCancel button"Scanning" label + spinnerEach card with collar's details should contain:Collar's photo + Collar RingCollar's battery level with iconDevice Nickname - if the collar is linked to a petDevice Product Name |
| ME04-US25- AC02 | If I tap on the Cancel button, then "Create New Fence" screen should be opened. |
| ME04-US25- AC03 | The scanning process should be started right after the screen opening.Note: During scanning, the "Scanning" label and spinner should be displayed. |
| ME04-US25- AC04 | The collars list should be sorted by RSSI. The collar with the strongest signal on top. |
| ME04-US25- AC05 | No real-time resorting. |
| ME04-US25- AC06 | The scanned collars set is updated in real-time. |
| ME04-US25- AC07 | If the smartphone doesn't find the collars, "No found collars" text should be displayed instead of the cards. Note: "Scanning" label and spinner should be displayed.The scanning process doesn't stop. |
| ME04-US25-AC08 | If I tap on the collar card, thenthe scanning process should be stopped;the pairing process should be started. See the details in ME04-US26. Create a fence (mixed flow): pair the collar via BLE;the spinner should be displayed during the pairing;the other part of the screen should be frozen. |
| ME04-US25-AC09 | If the pairing is successfully performed, then the Add Collar for GPS - Confirmation screen should be displayed. See continuation in ME04-US27. Create a fence (mixed flow): confirm the correct collar pairing. |
| ME04-US25-AC10 | Only one collar can be paired in one moment of time. |
| ME04-US25-AC11 | If the collar doesn't have a pet, then grey HALO ring should be displayed. |
