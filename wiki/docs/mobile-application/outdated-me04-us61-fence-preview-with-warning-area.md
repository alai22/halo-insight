---
title: "[Outdated] ME04-US61. Fence preview with warning area step"
sidebar_label: "[Outdated] ME04-US61. Fence preview with warning area step"
sidebar_position: 346
last_modified: "Mar 04, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-17668 - MOB: ME04-US61. Fence preview with warning area step Closed |
| Click here to expand...As of 06 Oct 2023:Mariya Kolyadacreated the initial version of US.As of 24 Oct 2023 Mariya Kolyada updated:ME04-US61-AC02ME04-US61-AC13ME04-US61-AC14ME04-US61-AC15 |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo acount owner I want to view fence preview with warning area after fence auto-generation and edit during fence creation so that I could double-check that my fence look as I expect and where aproximately the warning area begins.

# Acceptance criteria

| AC | Description | iOs design | Android design |
|---|---|---|---|
| ME04-US61-AC01 | After fence auto-generation or leaving edit mode in fence creation flow, the app should:Display the 'Fence preview with warning area' screen. |  |  |
| ME04-US61-AC02 | The 'Fence location positioning' screen should consist of the following elements:'Back' button'Confirm Fence' screen headerMap + 'Compass' button'Question mark' button'Map Settings' buttonAuto-generated fence with warning area.Explanation text about fence auto-generation'Edit Fence' button'Use This Fence' button |  |  |
| ME04-US61-AC03 | If I click the 'Back' button, then the app should:Return back to the (BL) ME04-US58. Fence location positioning step.Display the 'Fence Location Position' pin over the previously chosen location. |  |  |
| ME04-US61-AC04 | A Map should be the same as on the 'My Map' screen (see ME15-F00. View my map) |  |  |
| ME04-US61-AC05 | The app should display/hide the 'Compass' button according to the requirements in ME15-F00. View my map#Compassbutton. |  |  |
| ME04-US61-AC06 | If I click the 'Compass' button, then the app should:Behave according to the requirements defined in ME15-F00. View my map#Compassbutton. |  |  |
| ME04-US61-AC07 | If I click the 'Question mark' button, then the app should:Behave according to the requirements defined in ME04-F06. Baseline: View Fence Tutorial.NoteBut the updated texts should be applied: see [BL] ME04-US60. Update fence tutorial screens with info about auto-generation |  |  |
| ME04-US61-AC08 | If I click the 'Map Settings' button, then the app should:Behave according to the requirements defined in ME15-F01. Map settings card. |  |  |
| ME04-US61-AC09 | The app should display an auto-generated fence in the location chosen by the user on the (BL) ME04-US58. Fence location positioning step |  |  |
| ME04-US61-AC10 | The app should display an edited fence after that has been saved during fence creation on the ME04-US63. Fence edit mode step |  |  |
| ME04-US61-AC11 | The app should display the warning area inside the fence calculated according to the already implemented algorithm. |  |  |
| ME04-US61-AC12 | The app should center the map on the fence and the fence should be fully visible. |  |  |
| ME04-US61-AC13 | The 'Explanation text about fence auto-generation' should be the following:'A Halo Fence has been created that meets our guidelines.' |  |  |
| ME04-US61-AC14 | The app should display the 'Explanation text about fence auto-generation' only if the 'Fence with warning area screen' was opened after fence auto-generation.If the screen was opened after the 'Edit Mode', then the app should hide it. |  |  |
| ME04-US61-AC15 | If I click the 'Edit Fence' button, then the app should:Display the 'Edit Mode' screen (requirements to the screen are described in a separate User Story: ME04-US63. Fence edit mode step) |  |  |
| ME04-US61-AC16 | If I click the 'Use This Fence' button, then the app should:Display the 'Fence Name' step (see ME04-F00. Add fence without GPS#%22CreateNewFence-FenceNamestep%22screen) |  |  |
