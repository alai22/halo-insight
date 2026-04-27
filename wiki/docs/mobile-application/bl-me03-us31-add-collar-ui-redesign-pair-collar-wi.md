---
title: "[BL] ME03-US31 Add Collar (UI redesign) Pair collar with a pet"
sidebar_label: "[BL] ME03-US31 Add Collar (UI redesign) Pair collar with a pet"
sidebar_position: 61
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| ME03. Manage collars |
| REVISED |
| Nicolay Gavrilov |
| HALO-3132 - MOB: ME03-US31 Add Collar (UI redesign) Pair collar with a pet Closed |
| 14 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As an owner I want to have good looking mobile app UI so that I have a better general impression about the app.

# UI design

| Current design | New design |
|---|---|
|  |  |# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US30-AC01 | "Pair collar with a pet" screen is changed according to the new design. Screens with the new design are shown in the following cases:When adding a new collar to the account right after the account is createdWhen adding a new collar from the collars listWhen assigning an unassigned collar to a pet | Screen design in Zeplin |
| ME03-US30-AC02 | 'Add New Pet button' is relocated according to the new design | N/A |
| ME03-US30-AC03 | 'Pet without collars' label is removed from the "Pair collar with a pet" screen. | N/A |
| ME03-US30-AC04 | 'Done' button is relocated according to the new design. The button is visible only in case a pet is selected. | N/A |
| ME03-US30-AC05 | If the user attempts to assign the collar to a pet that already has been assigned to a collar, the app displays 'M69. Assign a collar to a connected pet' confirmation message. | M69. Assign a collar to connected petWe no longer forbid users to assign a collar to a pet that already has another collar assigned. |
| ME03-US30-AC06 | If the user decides to close 'M69. Assign a collar to connected pet' message without assigning the collar for the pet, the app closes the pop-up and:in case no pets were selected, the app displays the screen with no selected petsin case a pet without a collar was selected, the app displays the screen with the previously selected pet | Related bug: HALO-2337 - The checkmark doesn't display on selected pet on Step 4 of Collar Creation flow Closed || AC | Text |
|---|---|
| ME03-US02-AC12 | A user can link the collar to another pet from this screen or just unlink the collar. 1. Choose to disconnect or link another pet. By tapping "Change" a user will see the action sheet : disconnect a pet or give a collar to another pet. (note: if a collar is not linked to any pet, the app should skip this step and show Screen ME03-11 - Pets list to connect a collar by tapping "Change")2. Disconnect a collar. By tapping "Disconnect only" on M27 Disconnect Collar a user will disconnect a collar from a pet. The app will change a status and display "Currently Not Linked to a Pet" in expanded view, see ME03-US02-AC13. The app should send a request to the backend to start sync automatically and erase corrections, fences and etc from the previous pet. Pet history in the app should remain.3. Give a collar to another pet. If a user would like to change a pet he should choose to give a collar option on M27 Disconnect Collar and see the list with his pets see Screen ME03-11 - Pets list to connect a collar.A user should see 2 lists with headings:Pets without collarsPets with collarsButton to add a pet A user could select one pet, create new pet or go back to the previous screen.If a user selects a pet without a collar, this collar should be assigned to new pet. The app should update the state and send a request to the backend to start sync automatically to update fences, corrections and etc on the collar. 4.1 Give available collar to a pet with collar. If a user selects a pet that already has a collar, the app should show M69. Assign a collar to connected pet. If a user would like to proceed and change a collar, the app should send a request to the backend to start sync automatically to update fences, corrections and etc on the collar. Updates should be made for 2 collars. Pets' history in the app should remain.4.2 Give already connected (to Pet 1) collar to Pet 2 with collar. If a user selects Pet 2 that already has a collar, the app should show M2 Change collar. If a user would like to proceed and change a collar, the app should send a request to the backend to start sync automatically to update fences, corrections and etc on the collar. Updates should be made for both Pet 1 and Pet 2.In this case:selected collar will be connected to Pet 2Pet 1 will appear without a collarprevious collar from Pet 2 will not be connect to any petPets' history in the app should remain5. A user chooses a pet from the list, that already has the same collarThe app should show M68. The same pair of pet and collar to inform a user. || Link collar to a pet |
|---|
|  | The list of available pets is sorted alphabetically (ascending order). |  |  |
|  | If a user taps a pet that has a collar, the app should show the M69. Assign a collar to connected pet message. See the details in ME03-US31 Add Collar (UI redesign) Pair collar with a pet |  |  |
|  | If the user has no pets, an empty screen with "Add Pet" button should be displayed. | IOS DONE | Design is similar to iOsANDROID TO DO |
|  | Users can cancel the process of linking collar to a pet by tapping on the corresponding button. | IOS DONE | ANDROID TO DO |
|  |  |  |  |
|  | Users can add a new pet (see ME07-EP01. Add Pet) by tapping on the corresponding button. |  |  |
|  | After the collar is successfully added the app displays the screen from which the device was added (list of collars, TBD) |  |  |
