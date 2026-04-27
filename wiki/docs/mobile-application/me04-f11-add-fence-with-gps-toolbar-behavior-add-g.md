---
title: "ME04-F11. Add fence with GPS: Toolbar behavior (Add (GPS), Move buttons)"
sidebar_label: "ME04-F11. Add fence with GPS: Toolbar behavior (Add (GPS), Move buttons)"
sidebar_position: 111
last_modified: "Dec 14, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issue |
|---|---|---|---|
| Baseline story |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| HALO-2018 - [ME04-US29]: Create a fence (mixed flow): toolbar behavior updates ("Add with GPS") Closed HALO-5357 - Android GOAL: Add/Edit fence with GPS Closed |# User story

\> As an account owner, I want to create/edit a fence using GPS so that I can create it using the current collar location.

# Acceptance criteria

| AC | Text | iOS implementation statusIOS DONE | Android implementation status ANDROID TO DO |  |
|---|---|---|---|---|
| See the initial story (creating without GPS) in ME04-F00. Add Fence (without GPS). Acceptance criterias from this story is still valid. |
| ME04-F11-AC01 | If :"Create New Fence" screen is displayed;the collar IS paired via BLE;no fence posts added,then:until at least 1 fence post is added, the blue tile with the following text should be displayed: "Please tap on the map or tap "Add (GPS)" to create your first fence post". | See the screen in Zeplin. | See the screen in Zeplin |
| ME04-F11- AC02 | If the collar is paired and no fence posts are selected, then the toolbar: Undo, Redo, Add (GPS), Delete should be displayed. | See the screen in Zeplin | See the screen in Zeplin. |
| ME04-F11- AC03 | If I tap on the Add (GPS) button, then the current location data should be gathered from the collar and a new fence post should be added to the fence. | - | - |
| ME04-F11-AC04 | If the collar isn't paired and the blue tile (see ME04-F11-AC01) is displayed , then the toolbar should not be displayed. | - | - |
| ME04-F11-AC05 | If I remove the last fence post (no fence posts left on map), then the toolbar will still be visible and the blue tile (see ME04-F11-AC01) shouldn't be displayed. | - | - |
| ME04-F11- AC06 | Precondition: The user closes a fence during the Create new fence flow.If the collar is paired, then the toolbar: Undo, Redo, Move, Delete should be displayed. | See the screen in Zeplin. | See the screen in Zeplin. |
| ME04-F11- AC07 | Precondition: The user initiates Edit fence flow.If the collar is paired, then the toolbar: Undo, Redo, Move, Delete should be displayed. | - | - |
| ME04-F11- AC08 | If I tap on the Move button, then the location data should be gathered from the collar and the selected fence post location should be updated. | - | - |
| ME04-F11- AC09 | Precondition: The fence is closed and the user has no connected collar which is being used for GPS in the Create new fence flow If I tap on the Undo button and the fence becomes unclosed, then the toolbar: Undo, Redo, Delete should be displayed again. | - | - |
| ME04-F11- AC10 | Precondition: The fence is closed and the user has connected collar which is being used for GPS in the Create new fence flow If I tap on the Undo button and the fence becomes unclosed, then the toolbar: Undo, Redo, Add(GPS), Delete should be displayed again. | - | - |
