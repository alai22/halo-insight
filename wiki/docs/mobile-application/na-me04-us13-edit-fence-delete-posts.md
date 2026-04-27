---
title: "(NA) ME04-US13. Edit Fence: Delete posts"
sidebar_label: "(NA) ME04-US13. Edit Fence: Delete posts"
sidebar_position: 532
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-708/[ios]-edit-fence-delete-postsAndroid: https://linear.app/fueled/issue/HALO-709/[android]-edit-fence-delete-posts |
| 02 Apr 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be able to delete fence Main Posts, so I can adjust the size of my fence.

# Acceptance criteria

| AC | Description | Design | Delete Post | Undo Deletion + Redo |
|---|---|---|---|---|
| ME04-US13-AC01 | PreconditionNo fence post is selectedThe app should:Disable and display the inactive 'Delete Post' button. | Figma + Check existing (old) Halo app |
| ME04-US13-AC02 | PreconditionOne Main fence post is selected.If I tap the 'Delete Post' button in the bottom menu, then the app should:Check if is deletion allowed according to fence validation rules: (NA) ME04-US14. Edit Fence: Fence app validation and toasts |
| ME04-US13-AC03 | If at least one of the validations is failed, then the app should:Behave according to requirements in (NA) ME04-US14. Edit Fence: Fence app validation and toasts |
| ME04-US13-AC04 | If validations have been passed successfully, then the app should:Delete the selected Main post and the lines connecting it with the nearest 2 posts.Draw the new line between the nearest 2 posts.Display all fence posts unselected.Disable the 'Delete Post' button.NoteThe key point here is that the fence should remain closed, with no open figure anymore. |
| ME04-US13-AC05 | PreconditionDelete of the fence Main post was the latest action.If I tap the active 'Undo' button in the bottom menu, then the app should:Return back and display the deleted lines and post.Select the Main post that was previously deleted.Activate 'Redo' and 'Delete' button (if haven't been activated already). | Figma + Check existing (old) Halo app |
| ME04-US13-AC06 | PreconditionDelete of the fence Main post was the action before the 'Undo' action'Undo' was the last action that has been madeIf I click the active 'Redo' button in the bottom menu, then the app should:Behave the same as in ME04-US13-AC02. |
| ME04-US13-AC07 | If user selects any other Main post after deletion and taps 'Undo', then the app should:Behave as defined in ME04-US12-AC05.NoteThe app should ignore the 'Select' action for Undo/Redo. |Tech details

For Undo/Redo operations, you can use a list that will store the operations to be applied.In our code, this is implemented through the ReversibleUndoController class in FenceEditorViewModel


