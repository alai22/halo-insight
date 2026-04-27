---
title: "[BA-task]. Comparing possible closed fence solutions"
sidebar_label: "[BA-task]. Comparing possible closed fence solutions"
sidebar_position: 353
last_modified: "Oct 23, 2023"
author: "Mariya Kolyada"
---

|  | ApproachWhere add/What postWhat to do | ApproachWhat to doWhere add/What post |
|---|---|---|
| Ballpark estimates | 3-5 SP | 2-3 SP |
| Designs |  |  |
| Pros | User always see at least 2 possible actions (Add + Delete, but not Move)There is no need to go to the bottom of the screen to Add a postActions order remains the same - as users got used to: Where add/What postWhat to doMoving and Deleting triggers remain the same - how users got used to them.This solution is expandable in the future (Tooltip menu with Post/Line Move/Delete) - thus no need to reteach users. | User always see at least 2 possible actions (Add + Delete, but not Move)Smaller cost of development - sooner release |
| Cons | Higher cost of development | User need to go to the bottom of the screen to both Add and Delete a postActions order becomes new - not as users got used to: What to doWhere add/What post* We need to think about how to notify them that they need to choose the action first, otherwise, they can be stuck.This solution is expandable in the future (Tooltip menu with Post/Line Move/Delete) - thus we will need to reteach users to the previous approach again |
| Error. Tap on your first fence post | RemoveOr leave for editing using a collar? |
| Greate job notification | Remove? |
| Error. At least 3 posts | Display on one of 3 posts delete attempt | Display on one of 3 posts selection attempt |
| Error. Up to 20 posts | Hide adding elements? / Display an error on adding element click? | Display on Add Post click. |
| Error. Less than 6 feet between posts | Hide adding elements? / Display an error on adding element click? | Display on map click (selection of post place) |
| Change behavior of Undo/Redo/Add/Delete | If click Undo/Redo/Add/Delete by the end of the action app should always close the fence |
| Support 2 types of fence edit | Closed figure + fingerOpen figure + collar |
| Update fence tutorial | Text updates |
| Update support articles |  |
