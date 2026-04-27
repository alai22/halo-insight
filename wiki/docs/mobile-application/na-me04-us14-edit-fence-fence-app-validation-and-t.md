---
title: "(NA) ME04-US14. Edit Fence: Fence app validation and toasts"
sidebar_label: "(NA) ME04-US14. Edit Fence: Fence app validation and toasts"
sidebar_position: 533
last_modified: "Apr 16, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-710/[ios]-fence-app-validation-and-toastsAndroid: https://linear.app/fueled/issue/HALO-711/[android]-fence-app-validation-and-toasts |
| 02 Apr 2025 Mariya Kolyada created the initial version of a user story.14 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to view if my fence has some issues, so I can fix them before I stast using the fence with my pet(s).

# Acceptance criteria

| AC | Design | Trigger | Fence elements behavior | Actions that can trigger | Move | Add | Add&Move | Delete | Undo | Redo |
|---|---|---|---|---|---|---|---|---|---|---|
| The app should:validate the fence each time the user somehow adjust the fence OR taps 'Save' on the 'Edit Fence' screen as individual one and within Add Fence flowdisplay required toasts listed below by following general rules from (Native apps) ME14-F06. Toast notifications (general requirements) |
| ME04-US14-AC01 | Figma | If the zoom scale on the map becomes less than 16 after a closer zoom.The minimum zoom value is hard-coded* So it is hard to see the fence position accurately. | Forbid to add/delete Main posts until the zoom level is fixed.Move the Main/Adding post back to the previous state on the post's move attempt. |  |  |  |  |  |  |
| ME04-US14-AC02 | Figma | A user tries to add more than the maximum number of Main posts, see R-13.The value of points is taken from GET /configuration - geoFence.locationPointsMaxCount | The app should keep the existing fence as is without any changes. |  |  |  |  |  |  |
| ME04-US14-AC03 | Figma | There are only 3 Main posts in the fence.User tries to delete the Main post and leaves only 3 Main posts.The value of points is taken from GET /configuration - geoFence.locationPointsMinCount | The app should keep the selected for deletion Main post without any changes. |  |  |  |  |  |  |
| ME04-US14- AC04 | Figma | User tries to put the fence Main/Adding post less than 6 feet to the nearest other one.The minimum distance between points is taken from GET /configuration - geoFence.sideMinLengthInMeters | The app should keep the selected post without any changes when user tries to move or delete it.The app should hide the Adding post on the line if by adding of new Main post user fails the 6 feet rule. |  |  |  |  |  |  |
| ME04-US14- AC05 | Figma | The new Main/Adding post position causes an intersection between another side of the fence and a new line | Move the post back to the previous state on the post's move attempt. |  |  |  |  |  |  |
| ME04-US14- AC06 | Figma | The new Main/Adding post position causes an intersection with other existing fence(s) in the user's account.User clicks the 'Save' button.Display the toast always on the 'Save' button click.See more details in Validation of intersections with objects on the map. | Leave the post in the same place even though an error case exists.If user has NOT fixed the overlap for that they already saw the error - the app should NOT display the toast again.Display again only if the user fixed it and then made it after again. |  |  |  |  |  |  |
| ME04-US14- AC07 | Figma | The fence border intersects the building polygon + buffer that was originally in the fence the fence.See more details in Validation of intersections with objects on the map. | Leave the post in the same place even though a warning case exists.If user has NOT fixed the intersections for that they already saw the error - the app should NOT display the toast again.Display again only if the user fixed it and then made it after again. |  |  |  |  |  |  |
| ME04-US14- AC08 | Figma | At least one of the following conditions is met: The fence border intersects the polygon water object with not buffer (lake or river).The fence border intersects waterway line + buffer.See more details in Validation of intersections with objects on the map. |  |  |  |  |  |  |
| ME04-US14- AC09 | Figma | The fence border intersects the road line + buffer.See more details in Validation of intersections with objects on the map. |  |  |  |  |  |  |Tech details

Loading objects is described in these pages

- [(NA) ME04-US05. Add Fence: Step 2. Fence autogeneration attempt](241316021.mdx)
- [(NA) ME04-F02. Edit Fence Borders](241316063.mdx)

The basic rules and approach are described here Retrieving map objects

Fence validation occurs every time there is a change in fence points.


