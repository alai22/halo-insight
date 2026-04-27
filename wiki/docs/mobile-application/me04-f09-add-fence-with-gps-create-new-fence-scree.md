---
title: "ME04-F09. Add fence with GPS: \"Create New Fence\" screen description (without \"paired collar\" state)"
sidebar_label: "ME04-F09. Add fence with GPS: \"Create New Fence\" screen description (without \"paired collar\" state)"
sidebar_position: 11
last_modified: "Dec 14, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| HALO-5357 - Android GOAL: Add/Edit fence with GPS Closed |# User story

\> As owner, I want to have access to the "Select a collar" icon so that I can start creation of the fence with GPS.

# Acceptance criteria

| AC | Text | iOS implementationIOS DONE | AndroidimplementationANDROID DONE |
|---|---|---|---|
| See the initial story (creating without GPS) in ME04-F00. Add Fence (without GPS). Acceptance criterias from this story is still valid. |
| ME04-F09-AC01 | The "Select a collar" icon should be displayed at the Create New Fence screen. | Pic 1 - Create new fence (mixed flow) | See the link on Android screen. |
| ME04-F09-AC02 | If :"Create New Fence" screen is displayed;the collar ISN'T paired via BLE;no fence posts added,then:until at least 1 fence post is added, the tile with the updated text should be displayed: "Please tap on the map or select a collar to create your first fence post" | - | - |
| ME04-F09-AC04 | If I tap on the "Select a collar" icon and there is no internet connection, then: the error message should be displayed: M125 Connection error. | - | - |
| ME04-F09-AC05 | If I tap on the "Select a collar" icon and there are no collars in my account, then:the M101 No collars for selection error should be displayed. | - | - |
| ME04-F09-AC10 | If I tap on the "Select a collar" icon and BLE permission isn't granted/denied, then: see the continuation in A1-US01-AC01 in A1-US01. "Bluetooth permission request" message. | - | - |
| ME04-F09-AC11 | If I tap on the "Select a collar" icon and BLE permission is denied, then:see the continuation in A1-US02-AC01 in A1-US02. "Bluetooth permission denied" message. | - | - |
| ME04-F09-AC06 | If I tap on the "Select a collar" icon and BLE isn't enabled on the smartphone, then:the M102 No Bluetooth (fence creation) error should be displayed. | - | - |
| ME04-F09-AC07 | If:I tap on the "Select a collar" icon;andthere is one collar in the user account at least;andBLE is enabled on the smartphone;andthere are no paired collars,thenthe Collars list should be displayed. | - | - |
| ME04-F09-AC08 | If:I tap on the "Select a collar" icon; and there is a paired collar,then:then the "Disconnect collar" card should be displayed (see ME04-F13 Add fence with GPS: Disconnect collar) | - | - |
| ME04-F09-AC09 | The spinner should be displayed at "Select a collar" icon during the checking process. | - | - |
