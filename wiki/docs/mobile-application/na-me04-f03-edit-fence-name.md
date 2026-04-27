---
title: "(NA) ME04-F03. Edit Fence Name"
sidebar_label: "(NA) ME04-F03. Edit Fence Name"
sidebar_position: 518
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-665/[ios]-edit-fence-nameAndroid: https://linear.app/fueled/issue/HALO-666/[android]-edit-fence-name |
| 26 Mar 2025 Mariya Kolyada created the initial version of a user story.15 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to manage my fence name so I can name as I want.

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-F03-AC01 | By default, the 'Fence Name field' should have the saved name value inside. | FigmaFigma |
| ME04-F03-AC02 | If the 'Name' field has at least one character, then the app should: Display the Cross button inside the field. |
| ME04-F03-AC03 | If I tap on the Cross button, then the app should: Clear the 'Name' field. |
| ME04-F03-AC04 | The app should forbid entering more than 20 characters. |
| ME04-F03-AC05 | If I tap the 'Save' button OR 'Confirmation button on the keyboard', then the app should:Trigger the entered Name validationIf validation is passed:Save the name updates.Close 'Name Your Fence' pop-up.Display My Fences screen.Display the fence with the updated name on the map. |
| ME04-F03-AC06 | The app should display the validation error if the Name field is empty. | Figma |
| ME04-F03-AC07 | The app should display the validation error if the entered name duplicates the name of another fence in user's account. | Figma |Tech details

API for name editing - PUT /geo-fence/\{id\}In case the name is duplicated, there will be a response with code 400. The response will contain the field invalidOperationType = 19There is also a separate endpoint to check name uniqueness - PUT /geo-fence/check-name-uniqueness - it accepts the name and id of the fence being edited. Can be useful if validators are used


