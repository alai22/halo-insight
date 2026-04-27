---
title: "(NA) ME04-F11. Fence Feedback Settings"
sidebar_label: "(NA) ME04-F11. Fence Feedback Settings"
sidebar_position: 552
last_modified: "May 06, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| iOS: https://linear.app/fueled/issue/HALO-824/[ios]-fence-feedback-settingsAndroid: https://linear.app/fueled/issue/HALO-825/[android]-fence-feedback-settings |
| 21 Apr 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be able to adjust the Fence Feedback for each fence so the collar applies the feedback for my dog only when it is needed.

# Acceptance criteria

| AC | Description | Design | Pet qty with assigned collar | Display | Enable Fence Feedback toggle | Pet Assignment Toggle(s) | AC | Toggles state | Enable Fence Feedback toggle | Pet 1 Assignment toggle | Pet 2 Assignment toggle | User action | App response |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-F11-AC01 | If I tap the Fence status at the Fence Header on the My Fence tab, then the app should open Fence Feedback Settings card. | One PetFigmaMultiple PetsFigma |
| ME04-F11-AC02 | The app should:change the Fence Feedback Status value by following the rules defined in(NA) ME04-F12. Fence Feedback Statusdisplay the 'N of M Pets Active' if the feedback status is Partial. |
| ME04-F11-AC03 | The app should display/hide Pet Assignment toggles by following the rules:Pet qty with assigned collarDisplayEnable Fence Feedback togglePet Assignment Toggle(s)0-1\>1 | 0-1 |  |  | \>1 |  |  |
| 0-1 |  |  |
| \>1 |  |  |
| ME04-F11-AC04 | The 'Pet Assignment' toggles assign/unassign fence to pets. |
| ME04-F11-AC05 | The 'Enable Fence Feedback' toggle active/deactivate fence feedback on collars for assigned pets. |
| ME04-F11-AC06 | The 'Pet Assignment' toggle is hidden, then the 'Enable Fence Feedback' toggle both:manage fence Assignment to pet;activate fence feedback on collars for assigned pet. |
| ME04-F11-AC07 | If tap the 'i' button, then the app should:Open the following article:https://support.halocollar.com/hc/en-us/articles/31881918128279-Understanding-Your-Fence-Feedback-StatusURL should be taken from config: support.fenceFeedbackArticleUrl BE task: HALO-23005 - [BE]: Add Fence Support article URL to App configuration Open |
| ME04-F11-AC08 | Pets photos above 'Pet assignment' toggles use the same UI ghosting and status indicator displaying logic described for Unselected Pins in (NA) ME07-F01-US02. Pet Pin: all statuses (incl. unselected). |
| ME04-F11-AC09 | Precondition'Enable Fence Feedback' toggle = True.If I deactivate 'Enable Fence Feedback' toggle, then the app should:Change all pets' 'Assignment' toggles to False.Save pet Assignment state before deactivation.Deactivate Fence feedback on pets' collars previosly assigned to the fence.Implementation note: BE will store pet assignment states automatically (it will not be changed), MOB should render the toggles based on states + fenceIsDisabled. See details below. |
| ME04-F11-AC10 | Precondition'Enable Fence Feedback' toggle = False.If I activate 'Enable Fence Feedback' toggle, then the app should:Based on saved data, change 'Assignment' toggles to True for pets assigned to the fence before 'Enable Fence Feedback' toggle deactivation.Change 'Enable Fence Feedback' to True.Activate Fence feedback on the same pets' collars. |
| ME04-F11-AC11 | Precondition'Enable Fence Feedback' toggle = False.If I activate any pet's 'Assignment' toggle, then the app should:Clear previosly saved Assignment data before 'Enable Fence Feedback' toggle deactivation.Change only this pet's 'Assignment' toggle = True.Change 'Enable Fence Feedback' to True.Activate Fence feedback on this pet's collar. |
| Dependencies between the 'Pet Assignment' and 'Enable Fence Feedback' toggles based on examples with 2 Pets: |
| ACToggles stateEnable Fence Feedback togglePet 1 Assignment togglePet 2 Assignment toggleUser actionApp responseME04-F11-AC12Before action Deactivate 'Enable Fence Feedback' toggleSave pet Assignment state before deactivation.Deactivate'Enable Fence Feedback' toggle on UI.After actionME04-F11-AC13Before action Activate 'Enable Fence Feedback' toggleActivate 'Enable Fence Feedback' toggle on UI.Apply previosly saved pet Assignment on UI.After actionME04-F11-AC14Before action Assign Pet 1Activate Fence Feedback for Pet 1 on collar.Assign Pet 1 on UI.After actionME04-F11-AC15Before action Deactivate Fence FeedbackSave pet Assignment state before deactivation.Unassign all pets on UI.Deactivate 'Enable Fence Feedback' toggle on UI.Deactivate Fence Feedback for Pet 1 on collar.After actionME04-F11-AC16Before action Activate Fence FeedbackActivate Fence Feedback on UI.Apply previosly saved pet Assignment on UI.Activate Fence Feedback for Pet 1 on collar.After actionME04-F11-AC17Before action Assign Pet 2Clear previosly saved pet Assignment on UI.Activate Fence Feedback on UI.Keep Pet 1 unassigned on UI and collar.Assign Pet 2 on UI.Activate Fence Feedback for Pet 2 on collar.After actionME04-F11-AC18Before action Unasign Pet 1Unassign Pet 1 on UI.Deactivate Fence Feedback for Pet 1 on collar.After action | ME04-F11-AC12 | Before action |  |  |  | Deactivate 'Enable Fence Feedback' toggle | Save pet Assignment state before deactivation.Deactivate'Enable Fence Feedback' toggle on UI. | After action |  |  |  | ME04-F11-AC13 | Before action |  |  |  | Activate 'Enable Fence Feedback' toggle | Activate 'Enable Fence Feedback' toggle on UI.Apply previosly saved pet Assignment on UI. | After action |  |  |  | ME04-F11-AC14 | Before action |  |  |  | Assign Pet 1 | Activate Fence Feedback for Pet 1 on collar.Assign Pet 1 on UI. | After action |  |  |  | ME04-F11-AC15 | Before action |  |  |  | Deactivate Fence Feedback | Save pet Assignment state before deactivation.Unassign all pets on UI.Deactivate 'Enable Fence Feedback' toggle on UI.Deactivate Fence Feedback for Pet 1 on collar. | After action |  |  |  | ME04-F11-AC16 | Before action |  |  |  | Activate Fence Feedback | Activate Fence Feedback on UI.Apply previosly saved pet Assignment on UI.Activate Fence Feedback for Pet 1 on collar. | After action |  |  |  | ME04-F11-AC17 | Before action |  |  |  | Assign Pet 2 | Clear previosly saved pet Assignment on UI.Activate Fence Feedback on UI.Keep Pet 1 unassigned on UI and collar.Assign Pet 2 on UI.Activate Fence Feedback for Pet 2 on collar. | After action |  |  |  | ME04-F11-AC18 | Before action |  |  |  | Unasign Pet 1 | Unassign Pet 1 on UI.Deactivate Fence Feedback for Pet 1 on collar. | After action |  |  |  |
| ME04-F11-AC12 | Before action |  |  |  | Deactivate 'Enable Fence Feedback' toggle | Save pet Assignment state before deactivation.Deactivate'Enable Fence Feedback' toggle on UI. |
| After action |  |  |  |
| ME04-F11-AC13 | Before action |  |  |  | Activate 'Enable Fence Feedback' toggle | Activate 'Enable Fence Feedback' toggle on UI.Apply previosly saved pet Assignment on UI. |
| After action |  |  |  |
| ME04-F11-AC14 | Before action |  |  |  | Assign Pet 1 | Activate Fence Feedback for Pet 1 on collar.Assign Pet 1 on UI. |
| After action |  |  |  |
| ME04-F11-AC15 | Before action |  |  |  | Deactivate Fence Feedback | Save pet Assignment state before deactivation.Unassign all pets on UI.Deactivate 'Enable Fence Feedback' toggle on UI.Deactivate Fence Feedback for Pet 1 on collar. |
| After action |  |  |  |
| ME04-F11-AC16 | Before action |  |  |  | Activate Fence Feedback | Activate Fence Feedback on UI.Apply previosly saved pet Assignment on UI.Activate Fence Feedback for Pet 1 on collar. |
| After action |  |  |  |
| ME04-F11-AC17 | Before action |  |  |  | Assign Pet 2 | Clear previosly saved pet Assignment on UI.Activate Fence Feedback on UI.Keep Pet 1 unassigned on UI and collar.Assign Pet 2 on UI.Activate Fence Feedback for Pet 2 on collar. |
| After action |  |  |  |
| ME04-F11-AC18 | Before action |  |  |  | Unasign Pet 1 | Unassign Pet 1 on UI.Deactivate Fence Feedback for Pet 1 on collar. |
| After action |  |  |  |
| ME04-F11-AC19 | While the app is waiting for response from the collar (fence feedback changes has NOT been synchronized yet), it should change the toggle state from Active/Inactive to Active+Syncing or Inactive+Syncing. | Figma |
| ME04-F11-AC20 | If user has only one pet in account it should change the 'Enable Fence Feedback' toggle to Syncing. |
| ME04-F11-AC21 | If user has multiple pets in account it should change the 'Pet Assignment' toggles for corresponding pets to Syncing, NOT 'Enable Fence Feedback' toggle. |
| ME04-F11-AC22 | User can change the state between:Active+Syncing back to Inactive+Syncing.Inactive+Syncing back to Active+Syncing. NoteThis is needed so if user misstapped the toggle for collar which is expectedly is not in range. Let's say users use it only during weekends and all other time it is turned off.And they can revert everything back. |Implementation notes

BE stores two things:

1) Each fence has isEnabled property, which corresponds to "Enable Fence Feedback" toggle. It is returned inside FenceDto in response to /fence/my or /account/my/map.

2) Pet-fence assignments table - contains flags isAssigned, one flag per each pet-fence combination. It corresponds to petsSync[i].isEnabled (or .isAssigned, depends on BE devs).

When a fence gets disabled, pet-fence assignment values remain the same. In order to display pet toggles as disabled, we need to set it to isEnabled && petsSync[i].isEnabled.

Fence can be enabled or disabled using the endpoint geo-fence/\{id\}/set-is-enabled - see details in HALO-22928 - BE: Fence to pet assignment. Use ubiquitous language In Code Review .

Fence can be assigned or unassigned to/from pet using geo-fence/\{id\}/set-is-assigned/\{petId\}.

For a case when a fence is disabled but some pets are assigned to it, there can be three scenarios:

- User taps on "Enable Fence Feedback" - the app should call`set-is-enabled`and then redraw all the toggles according to the new`isEnabled`state. Some pet toggles will become enabled again, if those pets had this fence assigned.
- When user enables a toggle of a pet which was not assigned to this fence:
  - The app should call`set-is-assigned`for this pet;
  - BE will enable the fence automatically;
  - BE will assign this pet to the fence, and unassigned all other pets automatically;
  - The app should refresh all the toggles accordingly.

- When user enables a toggle of a pet which already was assigned: the app should call`set-is-assigned`for this pet anyway, even though it's already assigned. All the steps from the previous case are the same.

The app should display a spinner on top of a pet toggle in case petsSync[i].status == pending. This status will be set to pending every time petsSync[i].isEnabled or fence.isEnabled changes.


