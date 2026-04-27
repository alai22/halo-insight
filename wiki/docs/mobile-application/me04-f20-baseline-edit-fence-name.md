---
title: "ME04-F20. Baseline: Edit Fence Name"
sidebar_label: "ME04-F20. Baseline: Edit Fence Name"
sidebar_position: 459
last_modified: "Oct 30, 2024"
author: "Ekaterina Dupanova"
---

| Document type | Document status | Document owners | Link to JIRA Issues | History of changes |
|---|---|---|---|---|
| Baseline story |
| UP-TO-DATE as of 02 Oct 2024 |
| Ekaterina Dupanova |
| No JIRA links |
| As of 04 Oct 2024 Ekaterina Dupanova baselined:[BL] ME04-US74. Fence Name Edit. Update UX to pop-up view[BL] ME04-US72. Fence details. Update fence and name edit + delete |User story Acceptance criteria

# User story

\> As a Halo account owner I want edit fence Name on the Fence Details screen so that I can spend less time to find it and trigger the action.

# Acceptance criteria

| AC | Description | iOs design | Android design | Fence Name Validations | Cancel fence name edit | Save fence name edit |
|---|---|---|---|---|---|---|
| ME04-FE20-AC01 | The app should show a clickable 'Pencil' icon to the right of the centered fence name end on the Fence Details screen.NoteThere is no corner case related to the too-long fence name because it can be a maximum of 20 characters. Thus there is always some space for the 'Pencil' icon. |  |  |
| ME04-FE20-AC02 | If I click the 'Pencil icon' button on the Fence Details screen, then the app should:Display the 'Fence Name Edit' pop-up. |  |  |
| ME04-FE20-AC03 | 'Fence Name Edit' pop-up should consist of the following elements:Title: 'Edit Fence Name'Input field for the Fence Name edit:No header'Fence Name' placeholderButtons:CancelSave |  |  |
| ME04-FE20-AC07 | While editing, the app should display the 'Cross icon' button in the Fence Name Edit field. |  |  |
| ME04-FE20-AC08 | If I click on the 'Cross icon' button, then the app should:Clear the field. |  |  |
| ME04-FE20-AC04 | If I enter not unique fence name (for this account), then:the following field error should be displayed: "You currently have a fence with the same name".Triggers:A user confirms value on the keyboard by tapping a buttonWhen the keyboard is open, a user taps out of it, initiating closing the keyboardA user taps "Done" in the navigation bar |  |  |
| ME04-FE20-AC05 | If I don't enter at least one character, then:the following field error should be displayed: "Сannot be blank".Triggers:A user confirms value on the keyboard by tapping a buttonWhen the keyboard is open, a user taps out of it, initiating closing the keyboard |  |  |
| ME04-FE20-AC06 | The app should not allow entering more than 20 characters. |  |  |
| ME04-FE20-AC09 | If I click on the 'Cancel' button, then the app should:Close the 'Fence Name Edit' pop-up without saving any changes in the fence name.Display the Fence Details screen. |  |  |
| ME04-FE20-AC09 | If I click on the 'Return' keyboard button, then the app should:Behave the same as on the 'Save' button click. |  |  |
| ME04-FE20-AC10 | If I click on the 'Save' button, then the app should:Trigger validations from ME04-FE20-AC04,ME04-FE20-AC05, ME04-FE20-AC06If the edited fence name meets all validation rules, then the app should:Save the updated fence name.Close the 'Fence Name Edit' pop-up.Display the Fence Details screen. |  |  |
