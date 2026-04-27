---
title: "ME04-F12. Add fence with GPS: View the paired collar icon on map"
sidebar_label: "ME04-F12. Add fence with GPS: View the paired collar icon on map"
sidebar_position: 16
last_modified: "Nov 25, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issue |
|---|---|---|---|
| Baseline story |
| REVISED |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko |
| HALO-2020 - [ME04-US31]: Create a fence (mixed flow): view the paired collar icon on map Closed HALO-5357 - Android GOAL: Add/Edit fence with GPS Closed |# User story

\> As owner, I want to view the collar icon on the map so that I can observe the pair collar location.

# Acceptance criteria

| AC | Text | iOS implementation statusIOS DONE | Android implementation statusANDROID TO DO |
|---|---|---|---|
| Precondition for all AC above: "Create New Fence"/"Edit Fence Posts" flow is initiated |
| ME04-F12-AC01 | If the collar is paired, then the collar pin should be displayed on a map. | See the screen in Zeplin. | The same screen as for iOS |
| ME04-F12-AC02 | Precondition: at least one fence post is added.The fence post should be always in the front of the collar pin in case they overlap each other. This rule doesn't relate to the fence edge.Note: The reason for this update is the following: Collar pin can hide the last fence post and the app user can't close a fence. Also, the collar pin might hide any fence post, and I can't select it easily. | See the pic 1. | - |
| ME04-F12-AC03 | Collar pin should display the collar location. | - | - |
| ME04-F12-AC04 | The collar pin location should be updated automatically in real-time. | - | - |
| ME04-F12-AC05 | If the collar pin is displayed on my map, then:my location pin should not be displayed on my map. | - | - |
| ME04-F12-AC06 | If I disconnect my collar, my location pin should appear again. | - | - |
| ME04-F12-AC07 | The collar ring reflects pet color. | - | - |
