---
title: "ME04-US30. Create a fence (mixed flow): toolbar behavior updates (\"Move\")"
sidebar_label: "ME04-US30. Create a fence (mixed flow): toolbar behavior updates (\"Move\")"
sidebar_position: 21
last_modified: "Nov 05, 2020"
author: "Galina Lonskaya"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| TEAM REVIEW |
| Galina Lonskaya |
| HALO-2019 - [ME04-US30]: Create a fence (mixed flow): toolbar behavior updates ("Move") Closed |# User story

\> As owner, I want to tap on Move button so that I can update the dot placement via GPS.

# Acceptance criteria

| AC | Text |
|---|---|
| AC01 | Precondition: The user closes a fence during the Create new fence flow. If the collar is paired, then the toolbar: undo, redo, move, clear should be displayed. |
| AC02 | Precondition: The user initiates Edit fence flow. If the collar is paired, then the toolbar: undo, redo, move, clear should be displayed. |
| AC03 | If I tap on the Move button, then the location data should be gathered from the collar and the selected dot location should be updated. |
| AC04 | Precondition: The fence is closed and the user has no connected collar which is being used for GPS in the Create new fence flow or Edit Fence flow"If I tap on the Undo button and the fence becomes unclosed, then the toolbar: undo, redo, clear should be displayed again. |
| AC05 | Precondition: The fence is closed and the user has connected collar which is being used for GPS in the Create new fence flow or Edit Fence flow"If I tap on the Undo button and the fence becomes unclosed, then the toolbar: undo, redo, add with GPS, clear should be displayed again. |
