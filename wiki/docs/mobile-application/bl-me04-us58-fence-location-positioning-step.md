---
title: "(BL) ME04-US58. Fence location positioning step"
sidebar_label: "(BL) ME04-US58. Fence location positioning step"
sidebar_position: 341
last_modified: "Oct 08, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| BASELINED in (In progress) ME04-F00. Baseline: Add fence with auto-generation by Mariya Kolyada in March 2024. |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-17667 - MOB: ME04-US58. Fence location positioning step Closed |
| Click here to expand...As of 29 Aug 2023 - 05 Oct 2023:Mariya Kolyadacreated the initial version of US.As of 12 Oct 2023:Mariya Kolyada finalized US after BA calls and refinements.As of 24 Oct 2023:Mariya Kolyadaupdate the language of 'Explanation text';added criterias related to the 'Compass' button;added criterias related to the clickability of the 'Fence Location Positioning' pin.As of 10 Nov 2023:Mariya Kolyada updated:ME04-US58-AC02ME04-US58-AC15ME04-US58-AC16ME04-US58-AC19As of March 2024:Mariya Kolyada basilined this story in (In progress) ME04-F00. Baseline: Add fence with auto-generation. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo acount owner I want to be able use fence positioning pin so that I could define the place where I would like to generate my fence.

# Acceptance criteria

| AC | Description | iOs design | Android design |
|---|---|---|---|
| ME04-US58-AC01 | If I trigger the fence creation process from any possible place in the app or via a deep link, then the app should:Display the 'Fence location positioning' screen as the first step of the fence creation. | - | - |
| ME04-US58-AC02 | All validations on the fence creation trigger should remain the same as already implemented:ME04-EP01. Add FenceNoteThis means when the user clicks 'Add Fence' before entering the fence creation flow.E.g. if the user already has 20 fences. | - | - |
| ME04-US58-AC03 | The 'Fence location positioning' screen should consist of the following elements:'Back' button'Set Fence Location' screen headerAddress entering fieldMap + Compass button'Fence Location Position' pin'Question mark' button'My Location' button'Map Settings' buttonHelp text about location positioning'Confirm Location' button |  |  |
| ME04-US58-AC04 | If I click the 'Back' button, then the app should:Display the previously opened screen. | - | - |
| ME04-US58-AC05 | If I click the 'Address entering field', then the app should:Behave according to the requirements defined in ME15-US11. Search address (Create new fence/Edit fence posts). In addition, display the 'Fence Location Position' pin over the entered location. | - | - |
| ME04-US58-AC06 | A Map should be the same as on the 'My Map' screen (see ME15-F00. View my map) | - | - |
| ME04-US58-AC07 | The app should display/hide the 'Compass' button according to the requirements in ME15-F00. View my map#Compassbutton. |  |  |
| ME04-US58-AC08 | If I click the 'Compass' button, then the app should:Behave according to the requirements defined in ME15-F00. View my map#Compassbutton. |  |  |
| ME04-US58-AC09 | Preconditions:There is some address in the 'Address entering field'.If I drag the Map to place different from the location in the 'Address entering field', then the app should:Clear the 'Address entering field'. | - |  |
| ME04-US58-AC10 | The app should always display the 'Fence Location Position' pin in the middle of the screen over the Map.Decided to delete this AC during implementation. | - | - |
| ME04-US58-AC11 | By default map should be centered in the user's device location pin.NoteIt means that 'Fence Location Position' pin will be on the user's device location pin | - | - |
| ME04-US58-AC12 | If I click the 'Question mark' button, then the app should:Behave according to the requirements defined in ME04-F06. Baseline: View Fence Tutorial.NoteBut the updated texts should be applied: see [BL] ME04-US60. Update fence tutorial screens with info about auto-generation | - | - |
| ME04-US58-AC13 | If I click the 'My Location' button, then the app should:Behave according to the requirements defined in [BL] ME04-US62. Show user's device location on map | - | - |
| ME04-US58-AC14 | If I click the 'Map Settings' button, then the app should:Behave according to the requirements defined in ME15-F01. Map settings card. | - | - |
| ME04-US58-AC15 | The app should display the following 'Help text about location positioning':"Move the map to choose a fence location." | - | - |
| ME04-US58-AC16 | If I click the 'Confirm Location' button, then the app should:Check if:Location hovered with the 'Fence Location Position' pin is too zoomed out.'Fence Location Position' pin is NOT on the location of existing fence.'Fence Location Position' pin is NOT on the location of the extended road area (see Auto-generate fences#Fencegenerationalgorithm).Location hovered with the 'Fence Location Position' pin is presented in the cadastral data list. | - | - |
| ME04-US58-AC17 | If I click the blue part of the 'Fence Location Positioning' pin, then the app should behave the same as if the user clicks the 'Confirm Location' button. | - | - |
| ME04-US58-AC18 | Save the event by clicking on the blue part of the 'Fence Location Positioning' pin to the Firebase. | - | - |
| ME04-US58-AC19 | If the 'Fence Location Position' pin meet some of the conditions from ME04-US58-AC16, then the app should:Behave according to the requirements defined in [BL] ME04-US66. Fence Positioning. Validation on intersection with road and existing fence + zoom out. | - | - |
| ME04-US58-AC20 | If the chosen location is absent in the cadastral data list, then the app should:Navigate to the 'Fence Edit Mode' step and behave according to requirements defined in ME04-US63-AC02 of ME04-US63. Fence edit mode step.Display the 'Not Supported Location' pop-up over the 'Fence Edit Mode' step (requirements to the screen are described in a separate User Story: [BL] ME04-US59. Corner case. Not supported location for fence auto-generation). | - | - |
| ME04-US58-AC21 | If the chosen location is presented in the cadastral data list, then the app should:Generate the fence based on its location according to Auto-generate fences#Fencegenerationalgorithm. |  |  |
| ME04-US58-AC22 | While the app is generating the fence it should block the screen with a spinner.Note for QAIf the satellite view has been applied for the map - then the app replaces it with the standard view during auto-generation under the spinner. It is not a bug. |
| ME04-US58-AC23 | Once the fence auto-generation process is finished the app should:Display the 'Fence preview with warning area' screen (requirements to the screen are described in a separate User Story: [Outdated] ME04-US61. Fence preview with warning area step). |  |  |
