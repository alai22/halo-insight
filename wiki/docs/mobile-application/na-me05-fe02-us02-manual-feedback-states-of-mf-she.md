---
title: "(NA) ME05-FE02-US02. Manual Feedback: States of MF sheet with 1 pet"
sidebar_label: "(NA) ME05-FE02-US02. Manual Feedback: States of MF sheet with 1 pet"
sidebar_position: 562
author: "Galina Lonskaya"
---

| Document owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-805/[ios]-manual-feedback-states-of-mf-sheet-with-1-pet HALO-23074 - [iOS] Manual Feedback: States of MF sheet with 1 pet Open HALO-23075 - [Android] Manual Feedback: States of MF sheet with 1 pet Open |
| 16 Apr 2025 draft is created |# User story

\> As an account owner, I would like to apply an instant feedback so that I can quickly apply prevention or encouragement to train my pet.

Contents

User story Acceptance criteria

### Acceptance criteria

| AC | Text | Pet on MF sheet | Selected/Unselected states of Pet Pin on MF sheet | MF buttons on MF sheet |  |
|---|---|---|---|---|---|
| AC01 | Pet shown on MF sheet should consist of:\<Pet avatar or placeholder\> with Halo ring Circle that reflects selection stateCollar reachability icon |
| AC02 | Pet on MF sheet can have 2 states:selected unselectedFigma |
| AC03 | If there is one pet with the assigned collar only in the account, then:the pet should be always shown as selected. Note: It is not possible to select/deselect pet in case there is one pet only in the account. |
| AC04 | The pet cannot be selected/deselected in the 'not reachable' state. |
| AC05 | When the pet becomes reachable again, then the previous 'selection' state should be shown. |
|  | Precondition: there are more than 1 pet with the linked collar in the account If I tap on any unselected reachable pet on the MF sheet, then: the pet should become selected. Note: see what means 'reachable' in (NA) ME05-FE02-US03. Manual Feedback: Collar Reachability Status |
| AC06 | Precondition: there are more than 1 pet with the linked collar in the account If I tap on any selected reachable pet on MF, then: the pet should become unselected. |
| AC07 | The pointer should be shown only for selected pets. |
| AC08 | Precondition: there are several pets with the linked collars in the account. If I deselect all pets, then MF buttons should become disabled. See Figma |
| AC09 | MF buttons should be displayed as a non-cyclic carousel with horizontal swipe availability. |
| AC10 | The horizontal scroll indicator should show the current position within the MF buttons carousel. |
| AC11 | The sequence of the MF buttons should be the following:RecallLevel 1Level 2Level 3Custom 1Custom 2 |
| AC12 | Ifonly one pet is reachable OR there is one pet with the linked collar only in the account, then under each MF icon should be shown:MF type (Recall, Level 1, Level 2, Level 3, Custom 1, Custom 2)Chosen feedback for Sound and Vibration Static: Signal StrengthSound/Vibration: Name; сan be displayed in shortened form, see the details in:Appendix 18 - Sound/Vibration Naming and CategorizationRelated BE task: HALO-22951 - BE: Provide prevention (correction rule) sync status to the mobile app Ready for Development |
| AC13 | If I tap on the Cross icon on MF sheet, then:MF bottom sheet should be closed. |
| AC14 | Precondition: MF is shown If I tap on the MF icon (disabled or enabled) in the top navigation bar, then:MF bottom sheet should be closed. |Implementation notes

The shortened names of particular feedbacks (for sounds and vibrations) can be retrieved using /correction-rule/configuration-v2 endpoint - the field will be called userFriendlyShortName, or similar, but it's not implemented on BE yet.

- Note: this endpoint is needed here only in case of a single pet. In general, for multiple pets it's not possible to show the name of the feedback, because different pets can have different settings - so there is no need to show them.

For static feedback, the format should be "Static: \<level\>".

Feedback settings for particular pet can be retrieved using /pet/\{\{id\}\}/correction-rules endpoint. bool IsSynchronizedWithCollar will be added to the response. If at least one feedback is being synchronized for the pet, we should show a spinner around the pet photo.


