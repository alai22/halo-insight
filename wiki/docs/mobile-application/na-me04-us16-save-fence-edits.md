---
title: "(NA) ME04-US16. Save Fence Edits"
sidebar_label: "(NA) ME04-US16. Save Fence Edits"
sidebar_position: 556
last_modified: "Apr 22, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-776/[ios]-save-fence-editsAndroid: https://linear.app/fueled/issue/HALO-777/[android]-save-fence-edits |
| 14 Apr 2025 Mariya Kolyada created the initial version of a user story.15 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to save my fence after I edited it.

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-US16-AC01 | If I tap the 'Save Fence' button on the 'Edit Fence' screen, then the app should:Trigger the following required for saving validations on the app side:Fence building intersectionOther fences overlappingSee (NA) ME04-US14. Edit Fence: Fence app validation and toasts. | Figma |
| ME04-US16-AC02 | If fence overlaps other fence(s), then the app should:Display corresponding toast.FORBID to:Entry point 1 - Save the fence updates.Entry points 2 and 3 - Proceed with Fence Naming step. |
| ME04-US16-AC03 | If fence overlaps the building, then the app should:NO caution area intersection toast.Behave according to (NA) ME04-US17. Fence Too Close to Building: Confirm Saving |
| ME04-US16-AC04 | If required for saving validations on the app side passed successfully, then the app should:Entry point 1 - Try to save the fence updates.Entry points 2 and 3 - Try to proceed with the Fence Naming step. |
| ME04-US16-AC05 | If validation on the BE side is failed, the app should display corresponding error (see (NA) ME04-US18. Save Fence Edits: BE validation errors) |
| ME04-US16-AC06 | If there is some unexpected error during communication with BE, then the app should behave according to (Native apps) ME14-F04. Unified errors handling (REST API, screens with lists). |
| ME04-US16-AC07 | If required for saving validations on the BE side passed successfully, then the app should:Entry point 1:Save the fence updates.(NA) ME04-F13. Calculate minimal distances/areas of intersection with hazardsSend:(NA) ME04-F14. Fence Analytics in Operational DBs(NA) ME04-F??. Fence analytics in AmplitudeDisplay My Fences screen.(NA) ME04-F10. Select FenceDisplay the (NA) ME04-F04. Unique Fence: Recommend to read the article (only if relevant).Entry points 2 and 3 - Proceed with Fence Naming step. |Tech details

Before saving, you need to check if the fence is valid:

1. Using the last result from[(NA) ME04-US14. Edit Fence: Fence app validation and toasts](249004697.mdx)check for any violations. You don't have to rerun the validation, since the Save button doesn't change the fence
2. Validate the fence by additional request to the backend[(NA) ME04-US18. Save Fence Edits: BE validation errors](249005340.mdx)

API to update fence points - PUT /geo-fence/\{id\}/location

In this story, we send only LocationPointsThe Analytics field in the request will be filled in a separate store (NA) ME04-F14. Fence Analytics in Operational DBs.


