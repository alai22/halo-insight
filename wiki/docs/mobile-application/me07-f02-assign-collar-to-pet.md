---
title: "ME07-F02. Assign collar to pet"
sidebar_label: "ME07-F02. Assign collar to pet"
sidebar_position: 712
author: "Galina Lonskaya"
---

| Document status | Test cases status | Document owners | Links to JIRA Issues | Changes history |
|---|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 28 Oct 2021 |
| Galina Lonskaya, Pavel Leonenko, Maria Levko [X], Nicolay Gavrilov |
| HALO-3474 - MOB: ME16-US20. Assign a collar to the pet (UI redesign) Closed HALO-4668 - Android: ME07-F02 Assign collar to pet Closed |
| Click here to expand...Maria Shikareva [X] 09 Mar 2021 Added ME07-F02-AC15 while baselining the story: [BL] ME03-US24. Collars list state in case last telemetry from the collar was sent more than 5 minutes ago. |# Contents

User story As an owner I want to assign a pet to a collar so that I can manage collar using Halo app. Acceptance Criteria Implementation notes

# User story

\> As an owner I want to assign a pet to a collar so that I can manage collar using Halo app.

# Acceptance Criteria

| AC | Description | iOS Design / Implementation status IOS DONE | Android Design / Implementation status ANDROID DONE |
|---|---|---|---|
| ME07-F02-AC01 | The mobile app should open an 'Assign a Collar' screen in the following cases:when the user taps on the "Done" button on the "Add Pet - Step 2" screen;For more details refer to ME07-F01. Add a pet (breed, BD, weight).when the user taps on the "Add collar" button on the M79 No collar for testing error message;For more details refer to ME05-FE05. Test on Collar.when the user taps on the "Add collar" button on the Pet Card with no assigned collars.For more details refer to Pet card for a pet with no collar. | - | - |
| ME07-F02-AC02 | Precondition: the user has at least 1 collar in the account.'Assign a Collar' screen should consist of:'Cancel' button (for iOS)/ 'Cross' icon (for Android)'Assign a Collar' title'Done' buttonNot visible by default.'Please Choose a Collar for \<Pet Name\>' heading'Add New Collar' buttonA list of collars without the connected pets. See the detailed description in ME03-F01-AC02.'Assigned Collars' titleIt's displayed if at least one collar is assigned to the other pet.A list of collars with the connected pets. See the detailed description in ME03-F01-AC02. | Pic 1 - 'Assign a Collar' screenSee the screen in Zeplin | Pic 1 - 'Assign a Collar' screenSee the screen in Zeplin |
| ME07-F02-AC03 | A list of collars (with or without the connected pets) should be sorted so that the last provisioned collar is at the top. | - | - |
| ME07-F02-AC04 | By default the last provisioned available collar should be selected with a 'tick' icon.Note: if the user has "No Plan", then all available collars should be unselected (see ME07-F02-AC13 below). | - | - |
| ME07-F02-AC05 | If there are no available collars, then all collars in the assigned collars list should be displayed without ticks. |  |  |
| ME07-F02-AC06 | Precondition: there's no collars in the account.'Assign a Collar' screen should consist of:'Cancel' button (for iOS)/'Cross' button (for Android)'Assign a Collar' title'Please choose a Collar for \<Pet Name\>' heading.a Collar Icon + 'No collars added yet' label.'Add Collar' button. | Pic 2 - 'Assign a Collar' screen with no collarsSee the screen in Zeplin | The same screen as for iOS.See the screen in Zeplin |
| ME07-F02-AC07 | When the user taps on the 'Cancel' button (for iOS)/'Cross' button (for Android), then the app should display the following message M129 Cancel assigning a collar. | - | - |
| ME07-F02-AC08 | Precondition: M129 Cancel assigning a collar is displayed.When the user taps on the "Choose a Collar" button, then the app should:close the error pop-up;leave a user on the 'Assign a Collar' screen. | - | - |
| ME07-F02-AC09 | Precondition: M129 Cancel assigning a collar is displayed.When the user taps on the "Confirm" button, then the app should:close the error pop-up;close the 'Assign a Collar' screen;open the initial screen from which the assigning a collar flow was initiated (see ME07-F02-AC01). |  |  |
| ME07-F02-AC10 | When the user taps on the 'Add New Collar' button on the screen with collars OR the 'Add Collar' button on the screen without collars, then the app should perform actions as described in ME03-F00. Add collar. | - | - |
| ME07-F02-AC11 | Precondition: the 'Add New Collar' flow was initiated as described in ME07-F02-AC10.When the user gets back AND the collar is successfully added, then:the system should assign a newly added collar to the created pet;the app should close the 'Assign a Collar' screen. | - | - |
| ME07-F02-AC12 | Precondition: the 'Add New Collar' flow was initiated as described in ME07-F02-AC10.When the user gets back AND the collar is not added, then the app should display the 'Assign a Collar' screen. | - | - |
| ME07-F02-AC13 | Precondition: the user has "No Plan" subscription.When the user taps on any collar tile, then the app should:display ME19-US16 Subscription plan upgrade prompting screen.Note: it should not be allowed to link the collar to the pet, for more details see ME19-F02 Subscription plans. | - | - |
| ME07-F02-AC14 | Precondition: the user has any subscription plan.When the user taps on the Available collar, then the app should:display a tick on the collar tile;display a "Done" button. | - | - |
| ME07-F02-AC15 | Precondition: the user has selected Available collar.When the user taps on the 'Done' button, then:the pet should be assigned to the selected collar;the pet's settings should be sent to the new collar;the app should close the 'Assign a Collar' screen;the app should display a "synchronized" message:if the user binds the collar to the newly created pet, then → a M188 Wait until the collar is synchronized (binding new pet to a collar);if the user assigns a collar to the existing pet, then → a M189 Wait until the collar is synchronized (binding existing pet to a collar).Note 1: for a newly created pet the system should ensure that both of the pet modes will be set to 'ignore' right after the collar is synchronized with the Halo BE. This should work even if the collar was offline when the user assigned it to a new pet (see ME07-F01-IN01).Note 2: for existing pets the system should make sure the current pet mode settings will not be changed for the pet that gets the new collar. This should work even if the collar was offline when the user assigned it to a new pet. Otherwise after implementation of the ME07-US41. [MOB+BE] 'Instant' pet modes (Copy) the collar would keep the configuration of the previous pet that is saved on the collar after synchronization with BE. |  |  |
| ME07-F02-AC16 | Precondition: the user has selected Assigned collar.When the user taps on the collar that belongs to another pet, then the app should display M2 Change collar from Pet 1 to Pet 2. | - | - |
| ME07-F02-AC17 | Precondition: 'M2 Change collar from Pet 1 to Pet 2' pop-up is displayed.When the user taps on the "Confirm" button, then:the selected collar should be reassigned to Pet 2;the pet's settings should be sent to the new collar;Pet 1 should be left without a collar assigned;the app should close the message;the app should close the 'Assign a Collar' screen;the app should display a "synchronized" message:if the user binds the collar to the newly created pet, then → a M188 Wait until the collar is synchronized (binding new pet to a collar);if the user assigns a collar to the existing pet, then → a M189 Wait until the collar is synchronized (binding existing pet to a collar).Note 1: for a newly created pet the system should ensure that both of the pet modes will be set to 'ignore' right after the collar is synchronized with the Halo BE. This should work even if the collar was offline when the user assigned it to a new pet (see ME07-F01-IN01).Note 2: for existing pets the system should make sure the current pet mode settings will not be changed for the pet that gets the new collar. This should work even if the collar was offline when the user assigned it to a new pet. Otherwise after implementation of the ME07-US41. [MOB+BE] 'Instant' pet modes (Copy) the collar would keep the configuration of the previous pet that is saved on the collar after synchronization with BE. | - | - |
| ME07-F02-AC18 | Precondition: 'M2 Change collar from Pet 1 to Pet 2' pop-up is displayed.When the user taps on the "Cancel" button, then the app should:close the pop-up;display the 'Assign a Collar' screen with the previous collar still selected. | - | - |
| ME07-F02-AC19 | Connection and communication errors should be handled according to ME14-F01 Unified errors handling. | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME07-F01-IN01 | The direct message that'll set Beacons + Fences OFF during the pet/collar bind synchronization process on BE for newly created pets should be added. |
