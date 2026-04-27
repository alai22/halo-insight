---
title: "(NA) ME04-US08. Add Fence: Step 4. Edit Fence (optional)"
sidebar_label: "(NA) ME04-US08. Add Fence: Step 4. Edit Fence (optional)"
sidebar_position: 525
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-663/[ios]-add-fence-step-4-edit-fence-optionalAndroid: https://linear.app/fueled/issue/HALO-664/[android]-add-fence-step-4-edit-fence-optional |
| 25 Mar 2025 Mariya Kolyada created the initial version of a user story.15 Apr 2025 added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be able to edit my fence during creation before saving, so I create a fence that fits my needs

# Acceptance criteria

| AC | Description | Designs |
|---|---|---|
| ME04-US08-AC01 | The 'Edit Fence' screen within the 'Add Fence' flow should work the same with (NA) ME04-F02. Edit Fence Borders, except ACs defined below. | FigmaFigma |
| ME04-US08-AC02 | The app should display tooltips explaining how to move and add posts.Hide upon user interaction with the fence. |
| ME04-US08-AC03 | If I tap the 'Cancel' button, then the app should:Display 'Discard fence creation' pop-up:Discard edits - quit Fence Adding and Navigate back to My Fences screenKeep Editing - close pop-up and remain on Edit Fence screen. |
| ME04-US08-AC04 | If I tap the 'Save' button and all validations pass, then the app should:Open (NA) ME04-US09. Add Fence: Step 5. Name+Save Fence. |
| ME04-US08-AC05 | The app should NOT display the overlapping validation toasts on screen opening.NoteIt does NOT make sense because user has already been warned about overlapping with causion objects on the 'Confirm Fence' screen. |Tech details

Here we only need the warning zone, since we are editing it.The validation is expected to be done on the previous screen, so we can use the previous value, so we don't have to calculate a new one

Before opening Fence Name pop-up, you need to check if the fence is valid:

1. Using the last result from(NA) ME04-US14. Edit Fence: Fence app validation and toastscheck for any violations. You don't have to rerun the validation, since the Save button doesn't change the fence
2. Validate the fence by additional request to the backend(NA) ME04-US18. Save Fence Edits: BE validation errors

If the checks are successful, then name entry window open


