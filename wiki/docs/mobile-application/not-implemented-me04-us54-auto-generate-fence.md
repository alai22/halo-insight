---
title: "[Not implemented] ME04-US54. Auto generate fence"
sidebar_label: "[Not implemented] ME04-US54. Auto generate fence"
sidebar_position: 197
last_modified: "Feb 04, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issues | Changes history |
|---|---|---|---|
| DRAFT |
| Maria Shikareva [X] |
| HALO-10335 - MOB+QA: Update and test the final auto-generation and intersection validation algorithms Closed HALO-10568 - MOB [NT]: Investigate auto-generate fences Closed |
| Click here to expand... |# General description

As of 03 Feb 2022 a lot of people build their fences wrong. We need to have a tool that would help the users to draw fences automatically on the basis of existing perimeters (use DB: OpenStreetMap, they provide several polygons). We should also consider all rules applicable for fences (e.g. 10ft from the road, 10ft from the house, etc.).

This feature might solve several issues:

1. simplify the process of fence creation as it will be as immediate and automatic as it can be (this feature will work out of the box and require less user's work);
2. prevent users from mistakes during fence creation as soon as automatic fence creation will comply with our rules.

# User story

\> As a Halo app owner I want to have fences built automatically based on my current location so that to minimize risks of incorrect fences drawing and simplify the process a lot.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| See the initial story (creating without GPS) in ME04-F00. Add Fence (without GPS). Acceptance criteria from this story is still valid. |
|  | Auto fence drawing on the basis of existing perimeters (use DB: OpenStreetMap (they provide several polygons) |  |  |
|  | The following button should be available within "Fence creation/Fence editing" flows: build the fence on the basis of my location. |  |  |
|  | After a tap on this button the fence perimeter should be created automatically |  |  |
|  | Also, Halo logic rules should be applied for this fence creation |  |  |
|  | Leave in "edit" mode → the user has to tap "Next". |  |  |
|  |  |  |  |
|  |  |  |  |
|  | Handle cases:there is no internet connection (M125 Connection error)no collars in the account?BLE permission isn't granted/denied? (A1-US01. "Bluetooth permission request" message, A1-US02. "Bluetooth permission denied" message)BLE isn't enabled on the smartphone (M102 No Bluetooth (fence creation)) | - | - |
|  | The spinner should be displayed during the checking process. | - | - |
