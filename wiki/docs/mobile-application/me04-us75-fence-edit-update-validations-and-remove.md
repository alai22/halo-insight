---
title: "ME04-US75. Fence edit. Update validations and remove edit using collar"
sidebar_label: "ME04-US75. Fence edit. Update validations and remove edit using collar"
sidebar_position: 668
last_modified: "Apr 02, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Kirill Akulich |
| HALO-17744 - MOB: ME04-US75. Fence edit. Update validations and remove edit using collar Closed |
| Click here to expand...As of 13 Dec 2023- 20 Dec 2023:Mariya Kolyadacreated the initial version of US.As of 20 Oct 2023 :Mariya Kolyada Updated US with the final requirements + added Jitra ticket. |# Contents

User Story Acceptance criteria Table ME04-US75 Fence edit validation rules

# User Story

\> As a Halo acount owner I want to view only errors and warnings that may be helpful when I edit fence using figure that is imposible to open so that I can edit fence without confusing.

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US75-AC01 | Remove the fence creation/edit approach using the collar from the Fence Creation and Edit screen.NoteConsider the possibility of easily reverting it back with a lack of full redevelopment in case we will see from user feedback that they need it back. |
| ME04-US75-AC02 | Remove validation and toast message 'Tap on your first fence post to complete your fence'.NoteConsider the possibility of easily reverting it back just for the fence creation/edit using collar with a lack of full redevelopment in case we will see from user feedback that they need it back. |
| ME04-US75-AC03 | Remove validation and toast message 'Please tap on the map or select a collar to create your first fence post'.NoteConsider the possibility of easily reverting it back just for the fence creation/edit using collar with a lack of full redevelopment in case we will see from user feedback that they need it back. |
|  | Remove M139 Great job with the fence creation |
| ME04-US75-AC04 | Update the triggers and actions that can initiate this trigger for validation rules and toasts displaying according to Table ME04-F00 below. |
| ME04-US75-AC05 | Validations on the 'Save' button click should remain without changes:128 Fence has more than 1 safe zone (BE validation)M127 Fence is too small (BE validation)ME14-F01 Unified errors handling |### Table ME04-US75 Fence edit validation rules

| ID | Icon | Messages/errors on the screen | Displaying time | Trigger | Fence elements behavior | Actions that can trigger | Move | Add | Add&Move | Delete | Undo | Redo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-US75-M1 |  | Please zoom in to place a fence post accurately | Temporarily toast (4 seconds) | If the zoom scale on the map becomes less than 16 after a closer zoom.* So it is hard to see the fence position accurately. | Forbid to add/delete posts until the zoom level is fixed.Move the post back to the previous state on the post's move attempt. |  |  |  |  |  |  |
| ME04-US75-M2 |  | Your fence can include up to \{0\} fence posts. You can adjust existing fence posts with your finger or using toolbar. | A user tries to add more than the maximum number of posts, see R-13. | The app should keep the existing fence as is without any changes. |  |  |  |  |  |  |
| ME04-US75-M3 |  | Your fence must have at least \{0\} fence posts | There are only 3 posts in the fence.User tries to delete the post and leaves only 3 posts. | The app should keep the selected for deletion post without any changes. |  |  |  |  |  |  |
| ME04-US75- M4 |  | Please make sure fence posts are at least 6 feet apart | User tries to put the fence post less than 6 feet to the nearest other one. | The app should keep the selected post without any changes when user tries to move or delete it.The app should hide the 'Add" button on the line if by adding user fails the 6 feet rule. |  |  |  |  |  |  |
| ME04-US75- M5 |  | Fence lines cannot cross each other | The new post position causes an intersection between another side of the fence and a new line | Move the post back to the previous state on the post's move attempt. |  |  |  |  |  |  |
| ME04-US75- M6 |  | Fences cannot overlap | The new post position causes an intersection with other existing fence(s) in the user's account.If user has NOT fixed the overlap for that they already saw the error - the app should NOT display the toast again.Display again only if the user fixed it and then made it after again.User clicks the 'Save' button.Display the toast always on the 'Save' button click. | Leave the post in the same place even though an error case exists. |  |  |  |  |  |  |
| ME04-US75- M7 |  | Your fence appears to be closer than 15 feet from a house/building | The fence border is less than 15 feet from or intersects the building inside the fence.If user has NOT fixed the building intersection for that they already saw the error - the app should NOT display the toast again.Display again only if the user fixed it and then made it after again. | Leave the post in the same place even though a warning case exists. |  |  |  |  |  |  |
| ME04-US75- M8 |  | There appears to be water inside your fence safe area | The fence border intersects the water object (lake or river).If user has NOT fixed the water intersection for that they already saw the error - the app should NOT display the toast again.Display again only if the user fixed it and then made it after again. |  |  |  |  |  |  |
| ME04-US75- M9 |  | Your fence appears to be too close to the road. | The fence border intersects the road.If user has NOT fixed the road intersection for that they already saw the error - the app should NOT display the toast again.Display again only if the user fixed it and then made it after again. |  |  |  |  |  |  |
