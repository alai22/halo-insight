---
title: "ME04-US46. \"Create a fence/Edit fence posts\" improvements"
sidebar_label: "ME04-US46. \"Create a fence/Edit fence posts\" improvements"
sidebar_position: 82
author: "Galina Lonskaya"
---

| Role | Epic | Document status | BA story owner | DEV, QA story owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| Owner |
| ME04 Manage fences |
| APPROVED |
| Galina Lonskaya |
| Pavel Leonenko, Anastasia Brechko |
| HALO-4270 - MOB GOAL: "Create a fence" improvements (post is above pet pin, toast text update in accordance with Ken's comment) Closed |# User story

\> As owner, I want to get the clear messages about the first fence post creation so that I can understand how to add posts manually and/or using collar GPS. Also, a tip message at the Find screen could help me understand why I need to pair a collar while the fence creation. One more thing, I want to view a fence post in front of collar's pin so that I can easily close a fence.

# Acceptance criteria

| AC | Text | Links/Wireframes/Notes |
|---|---|---|
| ME04-US46-US01 | If :"Create New Fence" screen is displayed;the collar ISN'T paired via BLE;no fence posts added,then:until at least 1 fence post is added, the tile with the updated text should be displayed: "Please tap on the map or select a collar to create your first fence post". | See the initial requirements for the toast message in ME04-M6 ME04-US03. Create a fence |
| ME04-US46-US02 | If :"Create New Fence" screen is displayed;the collar IS paired via BLE;no fence posts added,then:until at least 1 fence post is added, the blue tile with the following text should be displayed: "Please tap on the map or tap "Add (GPS)" to create your first fence post". | - |
| ME04-US46-US03 | Precondition: "Create New Fence"/"Edit Fence Posts" flow is initiated, the collar is paired via BLE, at least one fence post is added.The fence post should be always in the front of the collar pin in case they overlap each other. This rule doesn't relate to the fence edge.Note: The reason for this update is the following: Collar pin can hide the last fence post and the app user can't close a fence. Also, the collar pin might hide any fence post, and I can't select it easily. |  |
