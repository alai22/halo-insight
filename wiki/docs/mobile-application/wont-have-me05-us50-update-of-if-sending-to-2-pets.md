---
title: "[Won't have] ME05-US50. Update of IF sending to 2+ pets (My Map)"
sidebar_label: "[Won't have] ME05-US50. Update of IF sending to 2+ pets (My Map)"
sidebar_position: 223
last_modified: "Aug 29, 2023"
author: "Galina Lonskaya"
---

| Document status | Story owners | Link to JIRA Issue | Initial requirements: |
|---|---|---|---|
| DRAFT |
| Valeryia Chyrkun [X]Galina Lonskaya |
| HALO-10222 - MOB: ME05-US49 + US50. Update of IF sending to 1 pet and 2+ pets (My Map) Closed |
| ME05-EP02. Apply feedback for multiple pets |# General description

-

# User story

\> As a Halo account owner, I want to be able to manage sending instant feedback only to the chosen pet/(s), so the feedback will be applied to the right dog/(s).

# Acceptance criteria

| AC | Text | Notes/Links/Screens | All pets are un-selected | 'Pets selection' section |
|---|---|---|---|---|
| ME05-US50-AC01 | Precondition: User has more than 1 Pet with Halo collar assigned to the account. User clicks Hand icon to send instant feedbackIf I click 'Hand' icon, then I see the 'Select Pets to Apply Feedback' card with the following elements:'Select Pets to Apply Feedback' header'Select all' button - disabled if all the pets are already selected. If at least one pet is un-selected then button is enabled.'X pets selected' field on the top right area of the action sheet, where X is a number of selected pets'Pets selection' sectionAnd the toolbar with Whistle, Warning, Boundary and Emergency feedback reactions described in details on [Won't have] ME05-US49. Update of IF sending to 1 pet (My Map) | Video: Send IF |
| ME05-US50-AC02 | All the Pets are chosen by default for applying feedback when user goes to that card at the beginning of the session. |  |
| ME05-US50-AC03 | To select (un-select) a pet users should tap on the button with it's icon. At that the check mark should appear in (disappear from) the checkbox on the button. |  |
| ME05-US50-AC04 | If pet doesn't have assigned collar then it is not displayed under 'Select Pets to Apply Feedback' section |  |
| ME05-US50-AC05 | If I pull down the 'Send Feedback to Pet(s)' card then it is minimized and just the following elements are displayed:Select Pets to Apply Feedback' header'Select all' button - disabled if all the pets are already selected. 'X pets selected' field, where X is a number of selected petsIf I pull up the minimized view then I see the ME05-US50-AC01 | Video: Minimized view |
| ME05-US50-AC06 | If I un-select all the pets than the toolbar icons becomes disabled and I cannot send any feedback to pets. | Video: No pets selected |
| ME05-US50-AC07 | When none of the pets are selected and the user taps on a feedback button the following toast message should be displayed:No pet selected |  |
| ME05-US50-AC08 | Each pet in the 'Pets selection' section should be presented with a button that has:\<Pet avatar\> + \<Halo ring\> + \<Pet name\>+ \<Communication type icon (Wi-fi, BLE, LTE)\>;checkbox. |  |
| ME05-US50-AC09 | Pets that are online should be displayed first in A→Z order, those pets that are offline should be displayed next to inline pets in the A→Z order. |  |
| ME05-US50-AC10 | When users taps on a feedback button the command should be sent only to those pets, that are selected. |  |
| ME05-US50-AC11 | The app should remember the selection state of the pets on the action sheet and the user should see the same pets selected when the action sheet is reopened within one session. |  |
| ME05-US50-AC12 | If there are at least 5 pet buttons on the action sheet, they should be displayed in two rows |  |
| ME05-US50-AC13 | See the rest of requirements in ME05-US24 [AFFMP]: 'Apply feedback for multiple pets' action sheet ME05-US24-AC05ME05-US24-AC08ME05-US24-AC07ME05-US24-AC12ME05-US24-AC35ME05-US24-19ME05-US24-22ME05-US24-23ME05-US24-24ME05-US24-25ME05-US24-36ME05-US24-28ME05-US24-30 |  |
