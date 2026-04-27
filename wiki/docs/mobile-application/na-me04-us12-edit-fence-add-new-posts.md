---
title: "(NA) ME04-US12. Edit Fence: Add new posts"
sidebar_label: "(NA) ME04-US12. Edit Fence: Add new posts"
sidebar_position: 531
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-706/[ios]-edit-fence-add-new-postsAndroid: https://linear.app/fueled/issue/HALO-707/[android]-edit-fence-add-new-posts |
| 01 Apr 2025 Mariya Kolyada created the initial version of a user story.14 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be able to add new posts, so I can adjust the fence border exactly I need it.

# Acceptance criteria

| AC | Description | Design | Add Post | Undo Adding + Redo |
|---|---|---|---|---|
| ME04-US12-AC01 | Precondition'Edit Fence' screen is opened.The app should display the Adding posts in the middle of each fence line. | Figma + Check existing (old) Halo app |
| ME04-US12-AC02 | If the distance between the line's middle and nearest Main post is less than 6 feet (GET /configuration geoFences.SideMinLengthInMeters), then the app should hide the Adding post on this line. |
| ME04-US12-AC03 | If the line is too short and the map is zoomed out on such a level that there is no space for the Adding post, then the app should hide it.If the user zooms in and there is enough space for the Adding post - display it again. |
| ME04-US12-AC04 | If I tap the Adding post on the line, then the app should:Check if adding is allowed according to fence validation rules: (NA) ME04-US14. Edit Fence: Fence app validation and toasts |
| ME04-US12-AC05 | If at least one of the validations is failed, then the app should:Behave according to requirements in (NA) ME04-US14. Edit Fence: Fence app validation and toasts |
| ME04-US12-AC06 | If validations have been passed successfully, then the app should:Replace the tapped Adding post with the new Main post.Select added Main post.Display the new Adding posts in the middle of the lines containing the newly added and selected Main post.Active 'Undo' and 'Delete Post' buttons (if haven't been activated before). |
| ME04-US12-AC07 | If I tap and begin moving the Adding post by holding it, then the app should:Check if adding and moving is allowed according to fence validation rules: (NA) ME04-US14. Edit Fence: Fence app validation and toasts |
| ME04-US12-AC08 | If at least one of the validations is failed, then the app should:Return the Adding post to the previous state before moving.Behave according to requirements in (NA) ME04-US14. Edit Fence: Fence app validation and toasts |
| ME04-US12-AC09 | If validations have been passed successfully, then the app should:Replace the tapped Adding post with the new Main post.Select added Main post.Display the new Adding posts in the middle of the lines containing the newly added and selected Main post.Check if moving to this place violates any fence validation rules and behave by following rules in (NA) ME04-US14. Edit Fence: Fence app validation and toastsProceed following the requirements defined in (NA) ME04-US12. Edit Fence: Move posts. |
| ME04-US12-AC10 | PreconditionAdding the fence post without moving was the latest action.ORAdding the fence post with moving was the latest action.If I tap the active 'Undo' button, then the app should:Return the fence back to the previous state and display it without the newly added (and moved) Main posts and new Adding posts.Unselect any fence posts.Check if moving to this place violates any fence validation rules: (NA) ME04-US14. Edit Fence: Fence app validation and toasts | - |
| ME04-US12-AC11 | PreconditionAdding the fence post without moving was the latest action.ORAdding the fence post with moving was the latest action.AND'Undo' was the last action that has been madeIf I click the active 'Redo' button in the bottom menu, then the app should:Behave the same as in ME04-US12-AC04 and ME04-US12-AC07. |
| ME04-US12-AC12 | If user selects any other Main post after adding with or without moving and taps 'Undo', then the app should:Behave as defined in ME04-US12-AC10.NoteThe app should ignore the 'Select' action for Undo/Redo. |Tech details

During the initial initialization of the fence, we display additional points (yellow small dots)These points are displayed between two fence points in case the distance between the points is greater than the minimum distance multiplied by 2 (since the point will be in the middle of the line) - the value is taken from GET /configuration geoFences.SideMinLengthInMetersAlso, when displaying them, we need to take into account the zoom of the map. We need the distance between the points to be greater than 45 pixels. In order not to make calculations too often, you can set a threshold for changing the scale (for example, every 0.25)When editing fence points, two neighboring points from the edited one will be recalculated. New addition points will be displayed only after the fence has been successfully modified

In our code, this is presented in the AddPointsController class

For Undo/Redo operations, you can use a list that will store the operations to be applied.In our code, this is implemented through the ReversibleUndoController class in FenceEditorViewModel


