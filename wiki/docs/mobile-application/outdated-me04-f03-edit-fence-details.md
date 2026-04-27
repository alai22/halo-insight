---
title: "(Outdated) ME04-F03. Edit Fence Details"
sidebar_label: "(Outdated) ME04-F03. Edit Fence Details"
sidebar_position: 100
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| No JIRA links |### User story

\> As an account owner, I want to view fence details screen so that I can edit fence name or delete a fence.

### Contents

User story Contents The entry point to the Edit Fence Details screen Edit Fence Name Delete Fence Cancel editing Save changes

Acceptance criteria

| AC | Text | iOS screens / impl-n status | Android screens / impl-n status | The entry point to the Edit Fence Details screen | Edit Fence Name | Delete Fence | Cancel editing | Save changes |
|---|---|---|---|---|---|---|---|---|
| ME04-FE03-AC01 | Precondition: Fence card in the default view is displayed.If I tap on the Edit Fence Details button, then:the Edit Fence Details screen should be opened. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC02 | The fence name can be edited. See the same requirements for the fence field as described in ME04-FE00. Add Fence (without GPS), ME04-FE00-AC30-34. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC03 | If I tap on the Delete Fence button, then:the M41 Delete Fence error message should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC04 | Precondition: the M41 Delete Fence error message is displayed. If I tap on the Cancel button, then: the error message should be closed. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC05 | Precondition: the M41 Delete Fence error message is displayed; there are 2 or more fences in the account OR there is 1 fence in the account, but Fences OFF mode is enabled for all pets in the account.If I tap on the Delete button, then:the fence should be deleted;the Edit Fence Details screen should be closed;my map with the Find card in the last used state should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC06 | Precondition: the M41 Delete Fence error message is displayed, there is 1 fence in the account AND Fences ON mode is enable at least for one pet in the account.If I tap on the Delete button, then:the M82 Updates for the last fence error message should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC07 | Precondition: the M82 Updates for the last fence error message is displayed.If I tap on the Never Mind button, then: the error message should be closed.TBD pay attention while baseliningBE no longer switches the fences OFF for all pets in the account when the user deletes the last fence. And M82 Updates for the last fence message is no longer needed. Instead, the app should show M41 Delete Fence.See ME07-US41. [MOB+BE] 'Instant' pet modes | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC08 | Precondition: the M82 Updates for the last fence error message is displayed.If I tap on the Delete button, then:the fence should be deleted;Fences Off mode should be enabled for all pets within the account;the Edit Fence Details screen should be closed;my map with the Find card in the last used state should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC09 | Precondition: the Edit Fence Details screen is displayed, no matter if the name was edited or not.If I tap on the Cancel button, then:the Edit Fence Details screen should be closed;no changes should be saved. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC10 | Precondition: the Edit Fence Details screen is displayed with the Done button.If I tap on the Done button and the fence name is successfully updated, then:the Fence card in the default view with the updated fence name should be displayed;My Map should be centered on the fence. | IOS DONE | ANDROID TO DO |
| ME04-FE03-AC11 | Precondition: the Edit Fence Details screen is displayed with the Done button.If I tap on the Done button and some error happens, then:unified error handling mechanism should be applied, see ME14-F01 Unified errors handling. | IOS DONE | ANDROID TO DO |
