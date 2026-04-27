---
title: "ME04-US78. Fence edit. Update 'Add' action"
sidebar_label: "ME04-US78. Fence edit. Update 'Add' action"
sidebar_position: 363
last_modified: "May 01, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X], Kirill Akulich |
| HALO-17742 - MOB: ME04-US78. Fence edit. Update 'Add' action Closed |
| Click here to expand...As of 13 Dec 2023- 20 Oct 2023:Mariya Kolyadacreated the initial version of US.As of 20 Dec 2023 Mariya Kolyada Updated after refinement. |# Contents

User Story Acceptance criteria Add post Add post: Undo/Redo

# User Story

\> As a Halo acount owner I want that my fence remain closed when I add the fence posts so that I faces less error cases when edit my fence.As a Halo acount owner I want to view the Adding posts on the fence so that I can understand how to add the posts to closed fence.

# Acceptance criteria

| AC | Description | iOs design | Android design | Add post |
|---|---|---|---|---|
| ME04-US78-AC01 | PreconditionFence edit mode screen is opened.The app should display the 'Adding' posts in the middle of each fence line. |  |  |
| ME04-US78-AC02 | If the distance between the line's middle and nearest posts is less than 6 feet, then the app should hide the 'Adding' post. |
| ME04-US78-AC02 | If the line is too short and the map is zoomed out on such a level that there is no space for the 'Adding' post, then the app should hide it.If the user zooms in and there is enough space for the 'Adding' post - display it again. |
| ME04-US78-AC04 | If I click the 'Adding' post on the line, then the app should:Check if adding is allowed according to fence validation rules: Table ME04-F00 Fence edit errors/warnings |
| ME04-US78-AC05 | If at least one of the validations is failed, then the app should:Behave according to requirements in Table ME04-F00 Fence edit errors/warnings. |
| ME04-US78-AC06 | If validations have been passed successfully, then the app should:Replace the clicked 'Adding' post with the new fence post.Select added post.Display the new 'Adding' post in the middle of the lines containing the newly added and selected post. |
| ME04-US78-AC07 | If I hold and begin moving the 'Adding' post, then the app should:Check if adding is allowed according to fence validation rules: Table ME04-F00 Fence edit errors/warnings |
| ME04-US78-AC08 | If at least one of the validations is failed, then the app should:Return the 'Adding' post to the previous state before holding and moving.Behave according to requirements in Table ME04-F00 Fence edit errors/warnings |
| ME04-US78-AC09 | If validations have been passed successfully, then the app should:Replace the clicked 'Adding' post with the new fence post.Select added post.Display the new 'Adding' post in the middle of the lines containing the newly added and selected post.Check if moving to this place violates any fence validation rules: Table ME04-F00 Fence edit errors/warningsProceed following the requirements defined in ME04-US77. Fence edit. Update Delete and Move action with their Undo/Redo logic#Movepost. |
| Add post: Undo/Redo |
| ME04-US78-AC10 | PreconditionAdding the fence post without moving was the latest action.ORAdding the fence post with moving was the latest action.If I click the active 'Undo' button in the bottom menu, then the app should:Return the fence back to the previous state and display it without the newly added (and moved) fence and 'Adding' posts.Unselect any fence posts. | - | - |
| ME04-US78-AC11 | PreconditionAdding the fence post without moving was the latest action.ORAdding the fence post with moving was the latest action.AND'Undo' was the last action that has been madeIf I click the active 'Undo' button in the bottom menu, then the app should:If I click the active 'Redo' button in the bottom menu, then the app should:Behave the same as in ME04-US78-AC04 or ME04-US78-AC07. |
| ME04-US78-AC13 | If user selects any other post after adding and clicks 'Undo', then the app should:Behave as defined in ME04-US78-AC10.NoteThe app should ignore the 'Select' action for Undo/Redo. |
