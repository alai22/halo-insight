---
title: "ME04-US77. Fence edit. Update Delete and Move action with their Undo/Redo logic"
sidebar_label: "ME04-US77. Fence edit. Update Delete and Move action with their Undo/Redo logic"
sidebar_position: 362
last_modified: "Apr 24, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Kirill Akulich |
| HALO-17743 - MOB: ME04-US77. Fence edit. Update Delete and Move action with their Undo/Redo logic Closed HALO-20111 - MOB: ME04-US77-AC17. Fence edit. Move on tap instead of long tap Closed |
| Click here to expand...As of 13 Dec 2023- 20 Dec 2023:Mariya Kolyadacreated the initial version of US.As of 20 Dec 2023:Mariya Kolyada Updated US with the final requirements + added Jitra ticket.As of 24 Apr 2024 Mariya Kolyada added ME04-US77-AC17. |# Contents

User Story Acceptance criteria Delete post Delete post: Undo/Redo Move post Move post: Undo/Redo

# User Story

\> As a Halo acount owner I want that my fence remain closed when I delete the fence post so that I faces less error cases when edit my fence.

# Acceptance criteria

| AC | Description | iOs design | Android design | Delete post | Move post | Move clicks |
|---|---|---|---|---|---|---|
| ME04-US77-AC01 | PreconditionNo fence post is selectedThe app should:Disable and display the inactive 'Delete' button. | Note for developer'Adding' yellow solid posts should be implemented within another user story: ME04-US78. Fence edit. Update 'Add' action |  |
| ME04-US77-AC02 | PreconditionAny fence post is selectedIf I click the 'Delete' button in the bottom menu, then the app should:Check if is deletion allowed according to fence validation rules: Table ME04-F00 Fence edit errors/warnings |
| ME04-US77-AC03 | If at least one of the validations is failed, then the app should:Behave according to requirements in Table ME04-F00 Fence edit errors/warnings. |
| ME04-US77-AC04 | If validations have been passed successfully, then the app should:Delete the selected post and the lines connecting it with the nearest 2 posts.Draw the new line between the nearest 2 posts.Display all fence posts unselected.NoteThe key point here is that the fence should remain closed, with no open figure anymore. |
| Delete post: Undo/Redo |
| ME04-US77-AC05 | PreconditionDelete of the fence post was the latest actionIf I click the active 'Undo' button in the bottom menu, then the app should:Return back and display the deleted lines and post.Select the post that was previously deleted. |  |  |
| ME04-US77-AC06 | PreconditionDelete of the fence post was the action before the 'Undo' action'Undo' was the last action that has been madeIf I click the active 'Redo' button in the bottom menu, then the app should:Behave the same as in ME04-US74-AC03. |
| ME04-US77-AC07 | If user selects any other post after deletion and clicks 'Undo', then the app should:Behave as defined in ME04-US77-AC05.NoteThe app should ignore the 'Select' action for Undo/Redo. |
| ME04-US77-AC08 | PreconditionFence post is unselectedIf I hold and move the post, then the app should:Select the post first.Move the post following my finger. |  |  |
| ME04-US77-AC09 | PreconditionFence post is selectedIf I hold and move the post, then the app should:Move the post following my finger. |
| ME04-US77-AC10 | PreconditionFence post was unselected OR selected before the 'Move' action began.If I released my finger after moving the post, then the app should:Check if moving to this place violates any fence validation rules: Table ME04-F00 Fence edit errors/warnings |
| ME04-US77-AC11 | If at least one of the validations is failed, then the app should:Behave according to requirements in Table ME04-F00 Fence edit errors/warnings.Keep the post selected. |
| ME04-US77-AC12 | If validations have been passed successfully, then the app should:Keep the post in a place where the movement has been finished.Keep the post selected. |
| Move post: Undo/Redo |
| ME04-US77-AC13 | PreconditionMoving of the fence post was the latest actionIf I click the active 'Undo' button in the bottom menu, then the app should:Return the post back to the position before moving.Keep the post selected.Check if moving to this place violates any fence validation rules: Table ME04-F00 Fence edit errors/warnings | - | - |
| ME04-US77-AC14 | If at least one of the validations is failed, then the app should:Behave according to requirements in Table ME04-F00 Fence edit errors/warnings.Otherwise:No actions needed. |
| ME04-US77-AC15 | PreconditionMoving the fence post was the action before the 'Undo' action.'Undo' was the last action that has been made.If I click the active 'Redo' button in the bottom menu, then the app should:Behave the same as in ME04-US74-AC10. |
| ME04-US77-AC16 | If user selects any other post after moving and clicks 'Undo', then the app should:Behave as defined in ME04-US77-AC13.NoteThe app should ignore the 'Select' action for Undo/Redo. |
| ME04-US77-AC17 | The app should respond to the move action right after a simple tap instead of the current long tap.Implementation noteFor Android less long tap can be used instead, a key point so it wasn't long from the user's perspective, seems almost like normal tap. | - | - |
