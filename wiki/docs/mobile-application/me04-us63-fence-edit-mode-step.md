---
title: "ME04-US63. Fence edit mode step"
sidebar_label: "ME04-US63. Fence edit mode step"
sidebar_position: 666
last_modified: "Feb 05, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-18049 - MOB: ME04-US63. Fence edit mode step Closed |
| Click here to expand...As of 12 Oct 2023- 16 Oct 2023:Mariya Kolyadacreated the initial version of US.As of 17 Oct 2023- 18 Oct 2023 :Mariya Kolyada Updated US with the final requirements + added Jitra ticket.As of 04 Jan 2024 Mariya Kolyada moved criterion related to absence of cadastral data to https://portal.softeq.com/display/HALO/%5BAnalysis%5D+ME04-US59.+Corner+case.+Not+supported+location+for+fence+auto-generation.As of 05 Feb 2024 Mariya Kolyada updated AC01 – AC03 and AC06, and strikethroughed not relevant anymore requirements. |# Contents

User Story Acceptance criteria Screen entry points Screen elements and actions on buttons click Fence edit process Warning/error toasts

# User Story

\> As a Halo acount owner I want to be able to edit fence during fence creation or from fence details so that I can improve it the way I neeed.

# Acceptance criteria

| AC | Description | iOs design | Android design | Screen entry points | Screen elements and actions on buttons click | Edit screen opened from | No edits have been made | Some edits have been made | Fence edit process | Warning/error toasts |
|---|---|---|---|---|---|---|---|---|---|---|
|  | PreconditionI'm in the process of the Fence creation.I just saw the auto-generated fence.If I click the 'Edit Fence Posts' button on the 'Fence Preview' screen, then the app should:Open the 'Fence edit mode' screen.Display auto-generated fence based on cadastral data and excluding unsafe and forbidden zones (see Auto-generate fences#Fencegenerationalgorithm.).NoteOutdated because of new requirements in [BL] ME04-US89. New fence creation approach when there are no corner cases |  |  |
|  | PreconditionI'm in the process of the Fence creation.I'd already edited the fence before during the same fence creation.If I click the 'Edit Fence Posts' button on the 'Fence Preview' screen, then the app should:Open the 'Fence edit mode' screen.Display fence version saved after the previous edit.NoteOutdated because of new requirements in [BL] ME04-US89. New fence creation approach when there are no corner cases |  |  |
| ME04-US63-AC01 | PreconditionI'm on the 'Fence preview with the Edit New Fence main action' screen (see [BL] ME04-US80. Corner case. Fence overlapping handling with proposing to edit or quit)If I click the Edit New Fence' button on the 'Fence preview with the Edit New Fence main action' screen, then the app should:Open the 'Fence edit mode' screen.Display fence version displayed on Fence preview. |  |  |
| ME04-US63-AC02 | PreconditionI'm on the 'Fence preview with water and/or road' screen (see [BL] ME04-US81. Corner case. Fence intersects water and/or road after autogeneration)If I click the 'Edit Fence' button on the 'Fence preview with water and/or road' screen, then the app should:Open the 'Fence edit mode' screen.Display fence version displayed on Fence preview. |  |  |
| ME04-US63-AC03 | See ME04-US59-AC01 in [BL] ME04-US59. Corner case. Not supported location for fence auto-generation. |  |  |
| ME04-US63-AC04 | PreconditionI'm on the Fence details screen (out of the Fence creation)If I click the 'Edit Fence Posts' button on the 'Fence Details' screen, then the app should:Open the 'Fence edit mode' screen.Display fence version displayed on Fence details. |  |  |
| ME04-US63-AC05 | The Fence edit mode step should consist of the following elements:'Cancel' button;'Edit Fence' screen header;'Save' button;Map + 'Compass' button;'Question mark' button;'Fence adding using collar' button;'Map Settings' button;Fence with posts for edit;Bottom toolbar with buttons:'Undo; button;'Redo' button;'Add (GPS)' button - display only when the Fence edit mode using GPS was triggered;'Delete' button; |  |  |
| ME04-US63-AC06 | If I click the 'Cancel' button, then the app should:Behave according to the following requirements:Edit screen opened fromNo edits have been madeSome edits have been madeFence Details CardDisplay My Map and Opened Fence CardDisplay M100 Cancel fence editing pop-up.Display My Map and Opened Find Card if the user decides to 'Discard'.Creation → Fence preview with the Edit New Fence main actionDisplay M63. Cancel Fence pop-up.Display My Map and Opened Find Card if the user decides to 'Discard'.Creation → Fence preview with water and/or roadCreation → No cadastral data toast | Fence Details Card | Display My Map and Opened Fence Card | Display M100 Cancel fence editing pop-up.Display My Map and Opened Find Card if the user decides to 'Discard'. | Creation → Fence preview with the Edit New Fence main action | Display M63. Cancel Fence pop-up.Display My Map and Opened Find Card if the user decides to 'Discard'. | Creation → Fence preview with water and/or road | Creation → No cadastral data toast | - | - |
| Fence Details Card | Display My Map and Opened Fence Card | Display M100 Cancel fence editing pop-up.Display My Map and Opened Find Card if the user decides to 'Discard'. |
| Creation → Fence preview with the Edit New Fence main action | Display M63. Cancel Fence pop-up.Display My Map and Opened Find Card if the user decides to 'Discard'. |
| Creation → Fence preview with water and/or road |
| Creation → No cadastral data toast |
| ME04-US63-AC07 | If I click on the 'Save' button and some error happens, then the app should:Behave according to the unified error handling mechanism (see ME14-F01 Unified errors handling) | - | - |
| ME04-US63-AC08 | If I click on the 'Save' button and during BE fence square validation it is identified that the fence has more than 1 safe area, then the app should:Display M128 Fence has more than 1 safe zone (BE validation) error pop-up. | - | - |
| ME04-US63-AC09 | If I click on the 'Save' button and during BE fence square validation it is identified that the fence is less than 250 square feet, then the app should:Display M127 Fence is too small (BE validation) error pop-up. | - | - |
|  | PreconditionI'm in the process of the Fence creation.If I click the 'Save' button and there are no error cases, then the app should:Display the 'Fence Preview' screen without the 'Explanation text' with edits applied (see [Outdated] ME04-US61. Fence preview with warning area step).NoteOutdated because of new requirements in [BL] ME04-US89. New fence creation approach when there are no corner cases | - | - |
| ME04-US63-AC10 | PreconditionI triggered the fence edit from the Fence details screen (out of the Fence creation).If I click the 'Save' button and there are no error cases, then the app should:Display the 'Fence details' screen with edits applied. | - |  |
| ME04-US61-AC11 | A Map should be the same as on the 'My Map' screen (see ME15-F00. View my map) | - | - |
| ME04-US63-AC12 | The app should display/hide the 'Compass' button according to the requirements in ME15-F00. View my map#Compassbutton. | - |  |
| ME04-US63-AC13 | If I click the 'Compass' button, then the app should:Behave according to the requirements defined in ME15-F00. View my map#Compassbutton. | - | - |
| ME04-US63-AC14 | If I click the 'Question mark' button, then the app should:Behave according to the requirements defined in ME04-F06. Baseline: View Fence Tutorial.NoteBut the updated texts should be applied: see [BL] ME04-US60. Update fence tutorial screens with info about auto-generation | - | - |
| ME04-US63-AC15 | If I click the 'Fence adding using collar' button, then the app should:Trigger Fence edit mode using GPS (see ME04-F02. Edit Fence Posts#EditfencepostswithGPS). | - | - |
| ME04-US63-AC16 | If I click the 'Map Settings' button, then the app should:Behave according to the requirements defined in ME15-F01. Map settings card. | - | - |
| ME04-US63-AC17 | The app should center the map on the fence and the fence should be fully visible. |  |  |
| ME04-US63-AC18 | Requirements related to the edit using the existing drawing process should remain the same.The app should behave according to the requirements defined in ME04-F00. Add fence without GPS → "Create New Fence - Fence Drawing step" screen: drawing process except for ME04-F00- M5 (should be absent). | - | - |
| ME04-US63-AC19 | Requirements related to the warning/error toasts displaying rules during the editing process should remain the same.The app should behave according to the requirements defined in ME04-F00. Add fence without GPS#TableME04-1Drawafenceerrors/warnings. | - | - |
