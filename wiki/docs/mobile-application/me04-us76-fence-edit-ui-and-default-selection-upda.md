---
title: "ME04-US76. Fence edit. UI and default selection updates"
sidebar_label: "ME04-US76. Fence edit. UI and default selection updates"
sidebar_position: 669
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Kirill Akulich |
| HALO-17746 - MOB: ME04-US76. Fence edit. UI and default selection updates Closed |
| Click here to expand...As of 13 Dec 2023- 20 Dec 2023:Mariya Kolyadacreated the initial version of US.As of 20 Dec 2023:Mariya Kolyada Updated US with the final requirements + added Jitra ticket. |# Contents

User Story Acceptance criteria UI updates Select/Unselect post

# User Story

\> As a Halo acount owner I want to view the updated UI on the Fence edit screen so that I easier understand logic of the actions.

# Acceptance criteria

| AC | Description | iOs design | Android design | UI updates | Button | Condition to be active | Post state | View | Select/Unselect post |
|---|---|---|---|---|---|---|---|---|---|
| ME04-US76-AC01 | Hide the user's pin on the Fence Edit screen. | Note for developer'Adding' yellow solid posts should be implemented within another user story: ME04-US78. Fence edit. Update 'Add' action |  |
| ME04-US76-AC02 | Update the bottom navigation bar with 'Undo', 'Redo', 'Delete' action from a fully expanded white area to a floating limited area in the shape of a rectangle with rounded corners. |
| ME04-US76-AC03 | Rename the 'Delete' button to 'Delete Post' |
| ME04-US76-AC04 | Add the Active (blue) / Inactive (gray) state of the 'Undo', 'Redo', and 'Delete' buttons:ButtonCondition to be activeUndoAny action has been made with the fence postsRedoUndo has been madeDeleteAny fence post has been selected | Undo | Any action has been made with the fence posts | Redo | Undo has been made | Delete | Any fence post has been selected |
| Undo | Any action has been made with the fence posts |
| Redo | Undo has been made |
| Delete | Any fence post has been selected |
| ME04-US76-AC05 | If I click the inactive 'Undo', 'Redo', and 'Delete' buttons - nothing should happen. |
| ME04-US76-AC06 | Replace the posts view in unselected and selected state:Post stateViewUnselectedWhite with yellow borderSelectedWhite with blue border | Unselected | White with yellow border | Selected | White with blue border |
| Unselected | White with yellow border |
| Selected | White with blue border |
| ME04-US76-AC07 | If I open the Edit Mode, then the app should by default:Have NO selected posts.Have inactive 'Undo', 'Redo', and 'Delete' buttons. | - | - |
| ME04-US76-AC08 | Remove the automatic post selection after user makes ANY action.NoteAutomatic post selection will be defined separately specifically for each action. | - | - |
| ME04-US76-AC09 | If I click anywhere else on the map except the fence itself, then the app should:Unselect previously selected post. | - | - |
