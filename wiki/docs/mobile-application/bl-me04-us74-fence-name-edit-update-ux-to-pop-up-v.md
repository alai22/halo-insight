---
title: "[BL] ME04-US74. Fence Name Edit. Update UX to pop-up view"
sidebar_label: "[BL] ME04-US74. Fence Name Edit. Update UX to pop-up view"
sidebar_position: 376
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| BASELINED in ME04-F20. Baseline: Edit Fence Name by Ekaterina Dupanova on 02 Oct 2024 |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Kirill Akulich |
| HALO-18857 - MOB: ME04-US74. Fence Name Edit. Update UX to pop-up view Closed |
| Click here to expand...As of 08 Dec 2023:Mariya Kolyadacreated the initial version of US with links to draft designs in Figma.As of 02 Oct 2024 Ekaterina Dupanova baselined the US |# Contents

User Stories Acceptance criteria

# User Stories

\> As a Halo acount owner I want to partially see the Fence details screen when edit the Fence Name so that I can always see for what fence I edit the name.

# Acceptance criteria

| AC | Description | iOs design | Android design |
|---|---|---|---|
| ME04-US74-AC01 | If I click the 'Pencil icon' button on the Fence Details screen, then the app should:Display the 'Fence Name Edit' pop-up instead of the currently implemented full-screen modal window. |  |  |
| ME04-US74-AC02 | 'Fence Name Edit' pop-up should consist of the following elements:Title: 'Edit Fence Name'Input field for the Fence Name edit:No header'Fence Name' placeholderButtons:CancelSave |
| ME04-US74-AC03 | The Fence Name validation and restrictions rules should remain without changes.See ME04-F00. Add fence without GPS#%22CreateNewFence-FenceNamestep%22screen:ME04-FE00-AC30ME04-FE00-AC31ME04-FE00-AC32 |
| ME04-US74-AC04 | While editing, the app should display the 'Cross icon' button in the Fence Name Edit field. |
| ME04-US74-AC05 | If I click on the 'Cross icon' button, then the app should:Clear the field. |
| ME04-US74-AC06 | If I click on the 'Cancel' button, then the app should:Close the 'Fence Name Edit' pop-up without saving any changes in the fence name.Display the Fence Details screen. |
| ME04-US74-AC07 | If I click on the 'Save' button, then the app should:Trigger validations from ME04-US74-AC03.If the edited fence name meets all validation rules, then the app should:Save the updated fence name.Close the 'Fence Name Edit' pop-up.Display the Fence Details screen. |
| ME04-US74-AC08 | If I click on the 'Return' keyboard button, then the app should:Behave the same as on the 'Save' button click. |  |  |
