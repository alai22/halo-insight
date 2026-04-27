---
title: "(NA) ME04-US17. Fence Too Close to Building: Confirm Saving"
sidebar_label: "(NA) ME04-US17. Fence Too Close to Building: Confirm Saving"
sidebar_position: 517
last_modified: "Apr 14, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-712/[ios]-fence-too-close-to-building-confirm-savingAndroid: https://linear.app/fueled/issue/HALO-713/[android]-fence-too-close-to-building-confirm-saving |
| 27 Mar 2025 Mariya Kolyada created the initial version of a user story.14 Apr 2025 added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be asked if I am okay that the fence is too close to the building so I can adjust it and it never corrects my dog inside my house.

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-US17-AC01 | PreconditionFence intersects the main building + buffer (building on registered property where the fence is created)If I tap the 'Save' button on the 'Edit Fence' screen, then the app should:Display the 'Fence Too Close to Building' pop-up. | Figma |
| ME04-US17-AC02 | If I tap 'Proceed Anyway' button, then the app should:Save the fence as is.Close the 'Fence Too Close to Building' pop-up.Display the Fence on My Fences screen. |
| ME04-US17-AC03 | If I tap 'Adjust Fence' button, then the app should:Close the 'Fence Too Close to Building' pop-up.Display the 'Edit Fence screen'. |Tech details

In the validation process (NA) ME04-US14. Edit Fence: Fence app validation and toasts, we will understand if there is an intersection between the fence and the building. This will be the flag for displaying the pop-up


