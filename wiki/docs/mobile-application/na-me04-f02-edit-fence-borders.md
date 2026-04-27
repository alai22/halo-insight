---
title: "(NA) ME04-F02. Edit Fence Borders"
sidebar_label: "(NA) ME04-F02. Edit Fence Borders"
sidebar_position: 515
last_modified: "Apr 15, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-700/[ios]-edit-fence-bordersAndroid: https://linear.app/fueled/issue/HALO-701/[android]-edit-fence-borders |
| 31 Mar 2025 Mariya Kolyada created the initial version of a user story.14 Apr 2025 added tech details. |# Contents

Contents User story Acceptance criteria Top Navigation Bar

# User story

\> As Halo app account owner, I want to confirm if I satisfied with atogenerated, so I use the fence that suits my needs.

# Acceptance criteria

| AC | Description | Design | Top Navigation Bar | Map | Posts | Description | Action | Description | Bottom Navigation Bar |
|---|---|---|---|---|---|---|---|---|---|
| ME04-F02-AC01 | The app should navigate to edit mode from one of the following entry points:My Fence → Fence List → Fence Management actions → Edit Fence (see details in this user story).Add Fence → Simple square has been autogenerarted (see (NA) ME04-US06. Add Fence: Step 3a. Simple square fence edit).Add Fence → Non-simple square has been autogenerarted → Confirm Fence → Edit Fence (see (NA) ME04-US08. Add Fence: Step 4. Edit Fence (optional)). | Figma |
| ME04-F02-AC02 | If some error between the app and the backend happens, follow rules from (Native apps) ME14-F01 Unified errors handling: general rules |
| ME04-F02-AC03 | The app should trigger fence validation on screen opening and display toasts if some error presented (see (NA) ME04-US14. Edit Fence: Fence app validation and toasts) |
| ME04-F02-AC04 | If I tap the 'Cancel' button, then the app should:Enry point 1 - Navigate back to the 'My Fences' screenEntry points 2 and 3 - defined in corresponding user stories. |
| ME04-F02-AC05 | If I tap the 'Questionmark' icon, then the app should:Open the 'Need Help?'The functionality should be implemented later within a separate user story: HALO-220 |
| ME04-F02-AC06 | The app should display the User location pin on the map (see (Native apps) ME15-F02. User location pin) |
| ME04-F02-AC07 | The app should display the same 'Center on User Location' button as on the My Fences screen (see (Native Apps) ME15-F07. Center on User Location) |
| ME04-F02-AC08 | If I tap the 'Fence Tutorial' button, then the app should:Open Fence Tutorial (see (NA) ME04-F05. Fence tutorial) |
| ME04-F02-AC09 | The app should center the map camera by following the rules:Fence is fully visible on the screen.Center of the fence is the center of the screen. |
| ME04-F02-AC10 | The app should display the fence border WITHOUT the warning zone for fence that will be edited. |
| ME04-F02-AC11 | The app should display other fences saved in user account by following the rules from (NA) ME04-US19. View Active Fence on the Map.User cannot edit them, only the fence selected for edit. |
| ME04-F02-AC12 | The app should diplay fence posts on fence border by following the rules:PostsDescriptionMain postsSee details in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redoAdding postsSee details in (NA) ME04-US12. Edit Fence: Add new posts | Main posts | See details in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redo | Adding posts | See details in (NA) ME04-US12. Edit Fence: Add new posts |
| Main posts | See details in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redo |
| Adding posts | See details in (NA) ME04-US12. Edit Fence: Add new posts |
| ME04-F02-AC13 | The app should display the building inside fence, roads, water and other fences by following the rules defined in (NA) ME04-F06. Display overlapping of fence with hazards. |
| ME04-F02-AC14 | User can perform the following actions by managing fence figure on the map:ActionDescriptionSelect/Unselect postsSee details in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redoMove postsSee details in (NA) ME04-US11. Edit Fence: Move postsAdd new postsSee details in (NA) ME04-US12. Edit Fence: Add new postsDelete main postsSee details in (NA) ME04-US13. Edit Fence: Delete postsUndo/Redo actions aboveGeneral logic in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redoDetails regarding each action are defined separately in corresponding user stories. | Select/Unselect posts | See details in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redo | Move posts | See details in (NA) ME04-US11. Edit Fence: Move posts | Add new posts | See details in (NA) ME04-US12. Edit Fence: Add new posts | Delete main posts | See details in (NA) ME04-US13. Edit Fence: Delete posts | Undo/Redo actions above | General logic in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redoDetails regarding each action are defined separately in corresponding user stories. |
| Select/Unselect posts | See details in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redo |
| Move posts | See details in (NA) ME04-US11. Edit Fence: Move posts |
| Add new posts | See details in (NA) ME04-US12. Edit Fence: Add new posts |
| Delete main posts | See details in (NA) ME04-US13. Edit Fence: Delete posts |
| Undo/Redo actions above | General logic in (NA) ME04-US10. Edit Fence: Select/unselect fence post + Undo/redoDetails regarding each action are defined separately in corresponding user stories. |
| ME04-F02-AC15 | Undo/Redo actions active/disabled state depends on actions performed with the fence. |
| ME04-F02-AC16 | The Delete Posts active/inactive state and action on tap is defined in (NA) ME04-US13. Edit Fence: Delete posts. |
| ME04-F02-AC17 | If I tap the 'Save Fence' button, then the app should:Behave according to (NA) ME04-US16. Save Fence Edits |Tech details

If we are editing an existing fence (case 1), we use points from the model with type Warning during the edit.It will also be helpful to obtain the parcel on which the fence in question was built. It is expected to be taken from the cache.The parcel will be saved locally in the cache when the fence is created.The parcel is then selected from the cache if it has an intersection with the fence. If there are several of them, the one with the largest intersection area is taken.

In the second or third scenario, these points will be generated during the fence creation process.

Main points (white with yellow border) are points that are built by coordinates that we already have (from the model or obtained during creation)Yellow small points are addition points, they appear automatically between the main points.

This screen also displays existing fences (Safe and Warning zones are displayed). You can use values from the previous screen or the cache

For fence validation, we will need object data from the map

- In case of editing an existing fence (the first scenario), we get objects from their`GET /geo-fence/fence-zone-info`, where we pass the id of the current fence and the map scale level as parameters (the default and minimum is 16, but it may be necessary to use a different one for more correct data). This request must be performed before opening the edit screen. If a data fetch error occurs,(Native apps) ME14-F01 Unified errors handling: general rulesis used, and the screen does not open.
- In case of editing a created fence (scenario 2-3), we need to get the data from the previous step, so it is enough to get the objects from the map.


