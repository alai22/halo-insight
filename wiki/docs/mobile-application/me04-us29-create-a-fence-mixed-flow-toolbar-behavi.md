---
title: "ME04-US29. Create a fence (mixed flow): toolbar behavior updates (\"Add\")"
sidebar_label: "ME04-US29. Create a fence (mixed flow): toolbar behavior updates (\"Add\")"
sidebar_position: 15
last_modified: "Nov 23, 2020"
author: "Galina Lonskaya"
---

| Role | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| Owner |
| TEAM REVIEW |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| HALO-2018 - [ME04-US29]: Create a fence (mixed flow): toolbar behavior updates ("Add with GPS") Closed |# User story

\> As an account owner, I want to create a fence using different tools so that I can do it quickly and in a convenient way.

# Acceptance criteria

| AC | Text | iOS implementation status | Android implementation status |
|---|---|---|---|
| ME04-F11- AC01 | The "Tap anywhere on map to place fence posts with your finger. You can also use a collar to create fence posts with GPS " card should be displayed until the first dot is placed. |  |  |
| ME04-F11- AC02 | If the "Tap anywhere..." card is displayed, then no toolbar should be displayed. |  |  |
| ME04-F11- AC03 | If I remove the last dot (no dots left on map), then the toolbar will still be visible and the "Tap anywhere..." card shouldn't be displayed. |  |  |
| ME04-F11- AC04 | If the collar isn't paired, then the toolbar: undo, redo, clear should be displayed. |  |  |
| ME04-F11- AC05 | If the collar is paired and no dots are selected, then the toolbar: undo, redo, add with GPS, clear should be displayed. |  |  |
| ME04-F11- AC06 | If I tap on the Add with GPS button, then the location data should be gathered from the collar and a new dot should be added. |  |  |
| ME04-F11- AC07 | If :"Create New Fence" screen is displayed;the collar IS paired via BLE;no fence posts added,then:until at least 1 fence post is added, the blue tile with the following text should be displayed: "Please tap on the map or tap "Add (GPS)" to create your first fence post". |  |  |
