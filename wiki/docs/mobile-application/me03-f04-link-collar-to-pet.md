---
title: "ME03-F04. Link Collar to Pet"
sidebar_label: "ME03-F04. Link Collar to Pet"
sidebar_position: 623
author: "Nicolay Gavrilov"
---

| Document status | Test cases status | Story owners | Link to JIRA Issues |
|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 14 Oct 2021 |
| Nicolay Gavrilov, Anastasia Brechko, Timofey Burak [X] |
| Click here to expand... HALO-2976 - MOB: ME03-US20. Update "canceling" popup while pet assigning Closed HALO-3132 - MOB: ME03-US31 Add Collar (UI redesign) Pair collar with a pet Closed HALO-3429 - Mob: Invalid design of empty 'Assign Collar to a pet' screen. Add Pet button doesn't display on the screen Closed HALO-4690 - Android: ME03-F04. Pair collar with a pet Closed HALO-6212 - BE: ME03-US40. Disabled "Fence" and "Beacon" modes after the collar to the pet assignment Closed |# Contents

User story Acceptance criteria Pet list Linking available or already assigned collar to a pet with no collar assigned Linking an unassigned collar to a pet that already has a collar assigned Linking a collar that belongs to Pet 1 to another pet with a collar Linking a collar that is already assigned to this pet Empty Pet list

# User story

\> As a Halo account owner I want to have a possibility to pair collar with a pet so that I can apply collar features to my pet.

# Acceptance criteria

| AC | Text | iOS screen designs/ implementation status IOS DONE | Android screen designs/ implementation status ANDROID DONE | Pet list | Linking available or already assigned collar to a pet with no collar assigned | Linking an unassigned collar to a pet that already has a collar assigned | Linking a collar that belongs to Pet 1 to another pet with a collar | Linking a collar that is already assigned to this pet | Empty Pet list |
|---|---|---|---|---|---|---|---|---|---|
| ME03-F04-AC01 | The 'Pair collar with a pet screen' is available in the following cases:When adding a new collar to the account right after the account is created (see ME03-F00. Add collar)When adding a new collar from the collars list (see ME03-F00. Add collar)When assigning an unassigned collar to a pet (see ME03-F01. Collars list)When reassigning assigned collar to another pet (see ME03-F01. Collars list) | Pic 1 - Pair collar with a petSee the screen in Zeplin | Pic 1 - Pair collar with a petSee the screen in Zeplin |
| ME03-F04-AC02 | The 'Pair collar with a pet' screen should consist of:"Cancel" button (for iOS) or "Cross" icon (for Android)'Pair Collar With a Pet' heading'Done' button (see ME03-F04-AC04)The button is visible only in case a pet is selected.'Please Choose Which Pet Should Use This Collar' title'Add New Pet' buttona list of Pets without Collars'Pet With Collars' subtitlea list of Pets with CollarsEach pet tile both in the Pets without Collars and Pets with Collars lists consists of:Pet avatar or Paw icon (if pet avatar was not set)+ HALO ringPet's name. |
| ME03-F04-AC03 | Both of the lists of available pets on the 'Pair Collar with a Pet' screen are sorted alphabetically (ascending order). | - | - |
| ME03-F04-AC04 | When the user taps on the "Cancel" button/ "Cross" icon, then the app should display M130 Cancel assigning a pet pop-up. | - | - |
| ME03-F04-AC05 | Precondition: M130 Cancel assigning a pet is shown.If the user taps the "Choose a Pet" button, then the system should display a "Pair Collar With a Pet" screen with the previously selected pet (if applicable). | - | - |
| ME03-F04-AC06 | Precondition: M130 Cancel assigning a pet is shown.If the user taps the "Confirm" button, then the system should open the previous screen (see ME03-F04-AC01). | - | - |
| ME03-F04-AC07 | When the user selects a pet from the list, the corresponding checkmark appears on the pet's tile and the 'Done' button becomes available. | - | - |
| ME03-F04-AC08 | If the user selects a pet from the list of pets without collars and taps the 'Done' button, then:the app displays the spinner;the app shows the M189 Wait until the collar is synchronized (binding existing pet to a collar) pop-up right after the collar is successfully bound to the pet. | - | - |
| ME03-F04-AC09 | Precondition: M189 Wait until the collar is synchronized (binding existing pet to a collar) is shown.When the user taps "I understand" button, then:the system links the collar to the selected pet;BE initiates uploading the new configuration to the device.The system should make sure the current pet mode settings will not be changed for the pet that gets the new collar. This should work even if the collar was offline when the user assigned it to a new pet.Note: otherwise, after implementation of the ME07-US41. [MOB+BE] 'Instant' pet modes the collar would keep the configuration of the previous pet that is saved on the collar after synchronization with BE.the app displays the initial screen from which the user entered the 'Pair collar with a pet' flow. | - | - |
| ME03-F04-AC10 | Right after a collar is bound to an existing pet, the app should disable the pet mode switchers in the pet card until the collar is synchronized with the Halo BE. | - | - |
| ME03-F04-AC11 | When a user selects a pet that already has a collar, then the app should show M69. Assign a collar to connected pet pop-up. | - | - |
| ME03-F04-AC12 | Precondition: M69. Assign a collar to connected pet is shown.If a user taps the "Confirm" button, then:the system links the collar to the selected pet;the system unlinks the current collar from the pet;BE initiates uploading the new configuration to the device.The system should make sure the current pet mode settings will not be changed for the pet that gets the new collar. This should work even if the collar was offline when the user assigned it to a new pet.the pet's stats in the app should remain;the app displays the initial screen from which the user entered the 'Pair collar with a pet' flow. | - | - |
| ME03-F04-AC13 | When the user wants to give the collar assigned on Pet 1 to Pet 2 and selects Pet 2 in the list, the app will show the M2 Change collar from Pet 1 to Pet 2 pop-up. | - | - |
| ME03-F04-AC14 | Precondition: M2 Change collar from Pet 1 to Pet 2 is shown.If a user taps the "Confirm" button on the M2 Change collar from Pet 1 to Pet 2 message, then:the system unlinks the current collar from the Pet 1 (Pet 1 will appear in the list of pets without a collar)the system links the collar to the Pet 2;the previous collar from Pet 2 will not be connected to any petBE initiates uploading the new configuration to the device.The system should make sure the current pet mode settings will not be changed for the pet that gets the new collar. This should work even if the collar was offline when the user assigned it to a new pet.the pet's stats in the app should remain;the app displays the initial screen from which the user entered the 'Pair collar with a pet' flow. | - | - |
| ME03-F04-AC15 | In case the user tries to select a pet that is already linked to this collar, the app shows the M68. The same pair of pet and collar pop-up. | - | - |
| ME03-F04-AC16 | Precondition: M69 or M2 or M68 is shown.If a user taps the "Cancel" button ("OK" button for M68), then the system should:close the pop-up;display "Pair Collar With a Pet" screen with no selected pets. |  |  |
| ME03-F04-AC17 | If the user has no pets, an empty screen with the "Add Pet" button should be displayed instead of the list of pets.The screen with no pets should consist of:Cancel button'Pair Collar With a Pet' headingDone button'Please Choose Which Pet Should Use This Collar' titlePaw icon + 'You do not have any pets yet' text'Add Pet' button | Pic 2 - No pets to be paired with a collarSee the screen in Zeplin | The same screen as for iOS. |
| ME03-F04-AC18 | When the user taps on the 'Add Pet' button, then the system should initiate the corresponding flow (see ME07-EP01. Add Pet). | - | - |
| ME03-F04-AC19 | Connection and communication errors are handled according to ME14-F01 Unified errors handling. | - | - |
