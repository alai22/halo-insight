---
title: "(NA) ME04-F12. Fence Feedback Status"
sidebar_label: "(NA) ME04-F12. Fence Feedback Status"
sidebar_position: 553
last_modified: "May 06, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| iOS: https://linear.app/fueled/issue/HALO-826/[ios]-fence-feedback-statusAndroid: https://linear.app/fueled/issue/HALO-827/[android]-fence-feedback-status |
| 11 Apr 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to view Fence Feedback Status so I know if it keeps safe my pet(s).

# Acceptance criteria

| AC | Description | Design | AC | Enable Fence Feedback | Pet Assignement to fence | NO GPS initialization is needed | Live Battery | NO Critical issues on collar | Pet Feedback on collar within Fence | AC | Pet Feedback on collar within Fence | Fence Feedback Status | AC | Pets | Fence Feedback | Pet Assignement to fence | NO GPS initialization is needed | Live Battery | NO Critical issues on collar | Pet Feedback on collar within Fence | Fence Feedback Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-F12-AC01 | The app should display the Fence Feedback Status on:(NA) ME04-F09. Fence Header(NA) ME04-F11. Fence Feedback Settings card | Figma |
| The app should define the Feedback Status of specific Pet withing specific Fence by following teh rules:ACEnable Fence FeedbackPet Assignement to fenceNO GPS initialization is neededLive BatteryNO Critical issues on collarPet Feedback on collar within FenceME04-F12-AC02ActiveME04-F12-AC03Does NOT matter, could be any or InactiveME04-F12-AC04ME04-F12-AC05ME04-F12-AC06At least one of any is Paused | ME04-F12-AC02 |  |  |  |  |  | Active | ME04-F12-AC03 |  |  | Does NOT matter, could be any or | Inactive | ME04-F12-AC04 |  |  | ME04-F12-AC05 |  |  | ME04-F12-AC06 |  |  | At least one of any is | Paused |
| ME04-F12-AC02 |  |  |  |  |  | Active |
| ME04-F12-AC03 |  |  | Does NOT matter, could be any or | Inactive |
| ME04-F12-AC04 |  |  |
| ME04-F12-AC05 |  |  |
| ME04-F12-AC06 |  |  | At least one of any is | Paused |
| The app should define the Feedback Status withing specific Fence by following teh rules:ACPet Feedback on collar within FenceFence Feedback StatusME04-F12-AC07ALL pets = ActiveME04-F12-AC08At least one = ActiveAt least one = Not Active (Paused/Inactive)ME04-F12-AC09At least one = PausedOther = Not Active (Paused/Inactive)ME04-F12-AC10ALL pets = Inactive | ME04-F12-AC07 | ALL pets = Active |  | ME04-F12-AC08 | At least one = ActiveAt least one = Not Active (Paused/Inactive) |  | ME04-F12-AC09 | At least one = PausedOther = Not Active (Paused/Inactive) |  | ME04-F12-AC10 | ALL pets = Inactive |  |
| ME04-F12-AC07 | ALL pets = Active |  |
| ME04-F12-AC08 | At least one = ActiveAt least one = Not Active (Paused/Inactive) |  |
| ME04-F12-AC09 | At least one = PausedOther = Not Active (Paused/Inactive) |  |
| ME04-F12-AC10 | ALL pets = Inactive |  |
| The app should change the Fence Feedback Status by following conditions based on example with 2 pets:ACPetsFence FeedbackPet Assignement to fenceNO GPS initialization is neededLive BatteryNO Critical issues on collarPet Feedback on collar within FenceFence Feedback StatusME04-F12-AC12Pet 1ActiveActivePet 2ActiveME04-F12-AC13Pet 1At least one of any is PausedPartialPet 2ActiveME04-F12-AC14Pet 1At least one of any is PausedPausedPet 2At least one of any is PausedME04-F12-AC15Pet 1ActivePartialPet 2InactiveME04-F12-AC16Pet 1ActivePartialPet 2At least one of any is InactiveME04-F12-AC17Pet 1At least one of any is PausedPausedPet 2InactiveME04-F12-AC18Pet 1Does NOT matter, could be any or InactiveInactivePet 2Does NOT matter, could be any or InactiveME04-F12-AC19Pet 1At least one of any is PausedPausedPet 2At least one of any is InactiveME04-F12-AC20Pet 1At least one of any is InactiveInactivePet 2At least one of any is InactiveME04-F12-AC21Pet 1Does NOT matter, could be any or Does NOT matter, could be any or InactiveInactivePet 2Does NOT matter, could be any or Does NOT matter, could be any or Inactive | ME04-F12-AC12 | Pet 1 |  |  |  |  |  | Active | Active | Pet 2 |  |  |  |  | Active | ME04-F12-AC13 | Pet 1 |  |  | At least one of any is | Paused | Partial | Pet 2 |  |  |  |  | Active | ME04-F12-AC14 | Pet 1 |  |  | At least one of any is | Paused | Paused | Pet 2 |  | At least one of any is | Paused | ME04-F12-AC15 | Pet 1 |  |  |  |  |  | Active | Partial | Pet 2 |  |  |  |  | Inactive | ME04-F12-AC16 | Pet 1 |  |  |  |  |  | Active | Partial | Pet 2 |  | At least one of any is | Inactive | ME04-F12-AC17 | Pet 1 |  |  | At least one of any is | Paused | Paused | Pet 2 |  |  |  |  | Inactive | ME04-F12-AC18 | Pet 1 |  |  | Does NOT matter, could be any or | Inactive | Inactive | Pet 2 |  | Does NOT matter, could be any or | Inactive | ME04-F12-AC19 | Pet 1 |  |  | At least one of any is | Paused | Paused | Pet 2 |  | At least one of any is | Inactive | ME04-F12-AC20 | Pet 1 |  |  | At least one of any is | Inactive | Inactive | Pet 2 |  | At least one of any is | Inactive | ME04-F12-AC21 | Pet 1 |  | Does NOT matter, could be any or | Does NOT matter, could be any or | Inactive | Inactive | Pet 2 | Does NOT matter, could be any or | Does NOT matter, could be any or | Inactive |
| ME04-F12-AC12 | Pet 1 |  |  |  |  |  | Active | Active |
| Pet 2 |  |  |  |  | Active |
| ME04-F12-AC13 | Pet 1 |  |  | At least one of any is | Paused | Partial |
| Pet 2 |  |  |  |  | Active |
| ME04-F12-AC14 | Pet 1 |  |  | At least one of any is | Paused | Paused |
| Pet 2 |  | At least one of any is | Paused |
| ME04-F12-AC15 | Pet 1 |  |  |  |  |  | Active | Partial |
| Pet 2 |  |  |  |  | Inactive |
| ME04-F12-AC16 | Pet 1 |  |  |  |  |  | Active | Partial |
| Pet 2 |  | At least one of any is | Inactive |
| ME04-F12-AC17 | Pet 1 |  |  | At least one of any is | Paused | Paused |
| Pet 2 |  |  |  |  | Inactive |
| ME04-F12-AC18 | Pet 1 |  |  | Does NOT matter, could be any or | Inactive | Inactive |
| Pet 2 |  | Does NOT matter, could be any or | Inactive |
| ME04-F12-AC19 | Pet 1 |  |  | At least one of any is | Paused | Paused |
| Pet 2 |  | At least one of any is | Inactive |
| ME04-F12-AC20 | Pet 1 |  |  | At least one of any is | Inactive | Inactive |
| Pet 2 |  | At least one of any is | Inactive |
| ME04-F12-AC21 | Pet 1 |  | Does NOT matter, could be any or | Does NOT matter, could be any or | Inactive | Inactive |
| Pet 2 | Does NOT matter, could be any or | Does NOT matter, could be any or | Inactive |
| ME04-F12-AC22 | PreconditionAll pet's collars assigned to the fence are NOT reachable (NO connection with them for \>30 sec).The app should:Display the latest known Feedback Status of the Fence.Disable the Feedback Status on the Fence Header - not possible to open the Fence Feedback Settings.NoteIf at least one collar is reachable - NO disability. | Figma |
| ME04-F12-AC23 | PreconditionAt least one pet's collar is still in progress of syncing to update the Fence Feedback Settings.The app should:Replace the lastest know Fence Feedback Status on the Fence Header with the Loader.Allow to open the Fence Feedback Settings on tap of the Loader as well.NoteReplace the Loader with the new Fence Feedback Status only after all the pet's collars are syncronized excluding collars with dead battery / assumed turned off. | Figma |Implementation notes

See the main notes here in the bottom: (NA) ME04-F11. Fence Feedback Settings

To display spinner in the navigation bar (header), the app should check if there are any pets for which petsSync[i].status == .pending && pet[i].reachabilityState != .discharged or .assumedTurnedOff for the fence in the header.


