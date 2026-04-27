---
title: "(NA) ME04-F10. Select Fence"
sidebar_label: "(NA) ME04-F10. Select Fence"
sidebar_position: 545
last_modified: "May 06, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| iOS: https://linear.app/fueled/issue/HALO-822/[ios]-select-fenceAndroid: https://linear.app/fueled/issue/HALO-823/[android]-select-fence |
| 08 Apr 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be able to select My Fence so I can open it's header without map paning to view feedback status and manage it's feedback settings.

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-F10-AC01 | I can select the fence by performing one of the following actions:Tap on the fence on the Map (see (NA) ME04-F08. View Fence on the Map).Tap on the fence on the Fence List (see ).Tap on the Pet pin inside the Fence (excluding Protection zone). | Figma |
| ME04-F10-AC02 | The app should select the fence automatically upon it's saving after:Adding;Borders Edit;Name Edit. |
| ME04-F10-AC03 | PreconditionThere is at least one fence in user accountANDAll pets inside one fence.On My Fences first opening after the app launch, the app should select this fence with pets inside it. |
| ME04-F10-AC04 | Preconditions:At least one of the following conditions is met:There is at least one fence in user account & Different Pets iniside different fencesThere is at least one fence in user account & Pets outside any fencesThere is at least one fence in user account & No Pets with assigned collarsNo FencesOn My Fences first opening after the app launch, the app should behave by following rules from: (Native apps) ME15-F04. Automatic map camera moving and style set up on app launch |
| ME04-F10-AC05 | If the fence is selected, then the app should:Zoom in/out so the fence fully visible on the screen.Center the map on this fence (so fence center = screen center).Change the 'Fence Header' to this selected fence. |
| ME04-F10-AC06 | If user/app pans map camera, then the app unselect previosly selected fence and follow rules from (NA) ME04-F09. Fence Header |
