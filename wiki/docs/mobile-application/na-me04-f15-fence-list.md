---
title: "(NA) ME04-F15. Fence List"
sidebar_label: "(NA) ME04-F15. Fence List"
sidebar_position: 546
last_modified: "May 06, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| iOS: https://linear.app/fueled/issue/HALO-830/[ios]-fence-listAndroid: https://linear.app/fueled/issue/HALO-831/[android]-fence-list |
| 10 Apr 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria Fence List sorting and loading

# User story

\> As Halo app account owner, I want to be able to adjust the Fence Feedback for each fence so the collar applies the feedback for my dog only when it is needed.

# Acceptance criteria

| AC | Description | Design | Fence List sorting and loading | Fence List Card Height and Add Fence | Fence List Item Elements | Select, Edit Fence and Name, Delete Fence |
|---|---|---|---|---|---|---|
| ME04-F15-AC01 | If I tap the 'Fences' title or Fence Name in the Header on My Fences screen, then the app should expand/collapse the Fence List Card. | FigmaFigma |
| ME04-F15-AC02 | The app should hide 'up'/'down' arrow if there is no fences in user account. |
| ME04-F15-AC03 | The app should sort fences from oldest to latest creation datetime. |
| ME04-F15-AC04 | By default the app should display only 20 fences in the Fence List until user scrolls down. |
| ME04-F15-AC05 | By default with no user actions, the app should update the Fence List each 15 sec. |
| ME04-F15-AC06 | Each time user scrolls below new 20 fences in the list - display the next 20 fences in the list.NoteThe key idea here is request new 20 fences from BE only after user scrolled till the end of previously displayed 20 fences. |
| ME04-F15-AC07 | The app should change the height of Fences List Card and position if of the Add Fence button depending on the number of the fences in the list.If the list is so long that it doesn't fit on the screen, then the app should fix the Add Fence button above the bottom tabbar. |
| ME04-F15-AC08 | If I tap the Add Fence, then the app should:Start (NA) ME04-F01. Add Fence process. |
| ME04-F15-AC09 | The app should display the fence thumbnail in Active state for each fence in the list. |
| ME04-F15-AC10 | If a fence is current for a particular pet, the app should display this Pet below the Fence Address.See the definition of current fence in the implementation notes below. |
| ME04-F15-AC11 | The app should apply for Pets UI ghosting and status indicator displaying logic described for Unselected Pins in (NA) ME07-F01-US02. Pet Pin: all statuses (incl. unselected). |
| ME04-F15-AC12 | If I tap on the fence item in the list, then the app should:(NA) ME04-F10. Select Fence | - |
| ME04-F15-AC13 | If I tap '...' → 'Edit Name', the the app should:Open (NA) ME04-F03. Edit Fence Name pop-up. | Figma |
| ME04-F15-AC14 | If I tap '...' → 'Edit Fence', the the app should:Open (NA) ME04-F02. Edit Fence Borders screen. |
| ME04-F15-AC15 | If I tap '...' → 'Delete Fence', the the app should:Open (NA) ME04-F16. Delete Fence pop-up. |
| ME04-F15-AC16 | Upon Edit Name, Fence Edit - the app should collapse the Fence List Card.NotesCollase is needed because this fences will be automatically selected upon ending (see details in (NA) ME04-F10. Select Fence)No need to collapse after deletion because there is nothig to be displayed.The list update is needed for all cases. |
| ME04-F15-AC17 | PreconditionThe menu list with 'Edit Name', 'Edit Fence' and 'Delete Fence' is displayed.If I tap anywhere on the screen then the app should close the menu. |Implementation notes

Current Fence

The new apps will have new term called currentFence:

- **Logic for currentFence on BE**. A collar reports a fence or a beacon inside telemetry. If it reports a fence - this is considered as`currentFence`. If it reports a beacon -`currentFence`remains the same. If it reports`null`-`currentFence`becomes`null`.[HALO-23048](https://jira.softeq.com/browse/HALO-23048?src=confmacro)-BE: Provide current fence ID to the mobile appReady for Development
- **Logic for currentFence on MOB**. On top of that, MOB can receive telemetry via BLE directly in offline. If`telemetry.currentLandmark`is a fence, this fence should be considered as`currentFence`. Otherwise,`currentFence`calculated by BE should be used.

Fence Address

BE will return FenceAddress inside each Fence DTO (field address) - TODO confirm with Alexei Zhukov. HALO-23047 - [BE]: Provide fence address to the mobile app Ready for Development

Thumbnail

TODO choose option to implement:

1 - single thumbnail:

BE will generate/recreate thumbnails each time a fence is created/edited. BE will return URL to the image inside each FenceDTO - TODO agree on property name.

2 - thumbnail with options:

The app should track all the pets states (telemetry - Bring Outside warning + is battery dead or not or assumed powered off) and critical issues on their collars. When anything of these changes, or when a fence is enabled/disabled or assigned/unassigned to/from pet, the app should recalculate status of each fence (Active/Partial/etc.) and change thumbnail accordingly. There will be 3 URLs inside Fence DTO - TODO agree on naming.

HALO-22361 - Manage geo fence thumbnails Open

Fence list

HALO-22245 - BE: Fence list logic: partial loading + sorting (Post-MRGP) Ready for Development


