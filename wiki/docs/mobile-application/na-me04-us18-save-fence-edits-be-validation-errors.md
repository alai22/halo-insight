---
title: "(NA) ME04-US18. Save Fence Edits: BE validation errors"
sidebar_label: "(NA) ME04-US18. Save Fence Edits: BE validation errors"
sidebar_position: 534
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-714/[ios]-save-fence-edits-be-validation-errorsAndroid: https://linear.app/fueled/issue/HALO-715/[android]-save-fence-edits-be-validation-errors |
| 27 Mar 2025 Mariya Kolyada created the initial version of a user story.14 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to errors if my fence is not alloed to be saved so I can understand how I should adjust it.

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-US18-AC01 | If qty of fence safe zones validation on the BE side is failed, the app should display the following errors:M128 Fence has more than 1 safe zone (BE validation) | Figma |
| ME04-US18-AC02 | If the smalest fence size validation on the BE side is failed, the app should display the following errors:M127 Fence is too small (BE validation) | Figma |Tech details

To check the validity of the fence, you need to call POST /geo-fence/safe-zones before saving the changesThe array of safe zones is returned in the response. If the number in the array is greater than one, the 1st criterion is met. It can be obtained by making an hourglass-shaped fenceThe zone also returns the area of the fence (field AreaInSquareMeters). If its value is less than geoFence.minSafeAreaInSquareMeters from GET /configuration, then the second criterion is executedIn case of unexpected exceptions (Native apps) ME14-F01 Unified errors handling: general rules are used.


