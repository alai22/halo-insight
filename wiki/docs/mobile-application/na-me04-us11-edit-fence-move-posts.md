---
title: "(NA) ME04-US11. Edit Fence: Move posts"
sidebar_label: "(NA) ME04-US11. Edit Fence: Move posts"
sidebar_position: 530
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-704/[ios]-edit-fence-move-postsAndroid: https://linear.app/fueled/issue/HALO-705/[android]-edit-fence-move-posts |
| 01 Apr 2025 Mariya Kolyada created the initial version of a user story.14 Apr 2025 added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be able tp move fence Main Posts, so I can adjust the size of my fence.

# Acceptance criteria

| AC | Description | Design | Move post | Undo Move + Redo |
|---|---|---|---|---|
| ME04-US11-AC01 | PreconditionFence Main post is unselectedIf I move the Main post, then the app should:Select the Main post first.Move the post following my finger.NoteThe app should respond to the move action right after a simple tap not the long tap. Tech implementation doesn't matter.The key point so it isn't long from the user's perspective, seems almost like normal tap. | Figma + Check existing (old) Halo app |
| ME04-US11-AC02 | PreconditionFence Main post is selectedIf I move the Main post by holding it, then the app should:Move the Main post following my finger. |
| ME04-US11-AC03 | If I released my finger after moving the Main post, then the app should:Check if moving to this place violates any fence validation rules: (NA) ME04-US14. Edit Fence: Fence app validation and toasts |
| ME04-US11-AC04 | If at least one of the validations is failed, then the app should:Behave according to requirements in (NA) ME04-US14. Edit Fence: Fence app validation and toasts.Keep the Main post selected. |
| ME04-US11-AC05 | If validations have been passed successfully, then the app should:Keep the Main post in a place where the movement has been finished.Keep the Main post selected.Activate 'Undo' and 'Delete Post' buttons (if haven't been activated before) |
| ME04-US11-AC06 | PreconditionMoving of the fence Main post was the latest actionIf I tap the active 'Undo' button in the bottom menu, then the app should:Return the Main Post back to the position before moving.Keep the Main post selected.Check if moving to this place violates any fence validation rules: (NA) ME04-US14. Edit Fence: Fence app validation and toastsActivate 'Redo' buttons (if hasn't been activated before) | Figma |
| ME04-US11-AC07 | If at least one of the validations is failed, then the app should:Behave according to requirements in (NA) ME04-US14. Edit Fence: Fence app validation and toastsOtherwise:No actions needed. |
| ME04-US11-AC08 | PreconditionMoving the fence post was the action before the 'Undo' action.'Undo' was the last action that has been made.If I tap the active 'Redo' button in the bottom menu, then the app should:Behave the same as in ME04-US11-AC03 |
| ME04-US11-AC09 | If user selects any other Main post after moving and taps 'Undo', then the app should:Behave as defined in ME04-US11-AC06NoteThe app should ignore the 'Select' action for Undo/Redo. |Tech details

It would be useful to add a threshold for moving so that you don't have to make unnecessary movements by pressing the button. In the current app, it is set to 3 pixels

For Undo/Redo operations, you can use a list that will store the operations to be applied.In our code, this is implemented through the ReversibleUndoController class in FenceEditorViewModel


