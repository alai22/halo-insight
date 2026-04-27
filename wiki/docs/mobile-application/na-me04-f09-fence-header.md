---
title: "(NA) ME04-F09. Fence Header"
sidebar_label: "(NA) ME04-F09. Fence Header"
sidebar_position: 539
last_modified: "May 06, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| iOS: https://linear.app/fueled/issue/HALO-820/[ios]-fence-headerAndroid: https://linear.app/fueled/issue/HALO-821/[android]-fence-header |
| 08 Apr 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to view Fence header of displaying fence so I view it

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-F09-AC01 | PreconditionThere is NO fences in user account.ORThere is NO fences on the map part displayed currently on the screen.The app should display (Native apps) ME15-F05. My Fences default header. | Figma |
| ME04-F09-AC02 | PreconditionThere is at least one fence on the map part displayed currently on the screen.The app should diplay the 'Fence Header' by following the rules defined below. | Figma |
| ME04-F09-AC03 | PreconditionThere is only one fence on the map part displayed currently on the screen.The app should display the 'Fence Header' of this fence (with its Status and Name). |
| ME04-F09-AC04 | PreconditionThere is more than one fence on the map part displayed currently on the screen.ANDThere are NO pets in any of this fences.By default, the app should display the 'Fence Header' of any from these fence. |
| ME04-F09-AC05 | PreconditionThere is more than one fence on the map part displayed currently on the screen.ANDEach fence has its own different pet inside.By default, the app should display the 'Fence Header' of any from these fence. |
| ME04-F09-AC06 | PreconditionThere is more than one fence on the map part displayed currently on the screen.ANDOnly one fence has a pet inside.By default, the app should display the 'Fence Header' of the fence with the dog. |
| ME04-F09-AC07 | If user/app selects any other fence, then the app should:Change the 'Fence Header' of the default fence to selected one.See how to select the fence in (NA) ME04-F10. Select Fence. |
| ME04-F09-AC06 | If I tap the Fence Feedback Status, then the app should:Open (NA) ME04-F11. Fence Feedback Settings. |
| ME04-F09-AC07 | The app should change the Fence Feedback Status by following the rules defined in(NA) ME04-F12. Fence Feedback Status. |
| ME04-F09-AC08 | If I tap the 'Fences' title or Fence Name, then the app should expand/collapse the (NA) ME04-F15. Fence List card. |
| ME04-F09-AC09 | If I tap the 'Manual Feedback' button, then the app should:Open (Native Apps) ME05-FE02. Manual Feedback (MF) for 1 Pet. |
