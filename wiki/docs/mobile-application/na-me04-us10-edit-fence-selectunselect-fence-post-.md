---
title: "(NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redo"
sidebar_label: "(NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redo"
sidebar_position: 528
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-702/[ios]-edit-fence-selectunselect-fence-post-undoredoAndroid: https://linear.app/fueled/issue/HALO-703/[android]-edit-fence-selectunselect-fence-post-undoredo |
| 01 Apr 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to select/unselect toast, so I can define which post I am planning to do something.

# Acceptance criteria

| AC | Description | Design | Select/Unselect | Undo/Redo |
|---|---|---|---|---|
| ME04-US10-AC01 | By default on the 'Fence Edit' screen opening the app should:Display all Main post in the Unselected state (white+yellow border). | Figma |
| ME04-US10-AC02 | The app should disable the 'Delete' button until the user selects any Main post. |
| ME04-US10-AC03 | If I tap the Unselected Main post, then the app shoud:Make it Selected (blue+white border). |
| ME04-US10-AC04 | Only one Main post can be Selected at the same time.This if one Main post is already selected and I tap on another one, then the app should:Unselect previosly Selected post.Select tapped post. |
| ME04-US10-AC05 | If I tap the Selected Main post, then NOTHING should happen. |
| ME04-US10-AC06 | If I click anywhere else on the map except the fence itself, then the app should:Unselect previously Selected Main post. |
| ME04-US10-AC07 | The app should NOT activate 'Undo'/'Redo' buttons on Main post selection. | - |
| ME04-US10-AC08 | Only fence post edits (Add, Move or Delete) activate the 'Undo' button and logic is defined in each corresponding user story separately. |
| ME04-US10-AC09 | In general, the user can make the same amout of 'Undo' taps as post edits performed. |
| ME04-US10-AC10 | 'Undo' action actives the 'Redo' button. |
| ME04-US10-AC11 | In general, the user can make the same amout of 'Redo' taps as 'Undo' performed. |Tech details

For Undo/Redo operations, you can use a list that will store the operations to be applied.In our code, this is implemented through the ReversibleUndoController class in FenceEditorViewModel


