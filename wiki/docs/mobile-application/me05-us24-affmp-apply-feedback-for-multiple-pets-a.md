---
title: "ME05-US24 [AFFMP]: 'Apply feedback for multiple pets' action sheet"
sidebar_label: "ME05-US24 [AFFMP]: 'Apply feedback for multiple pets' action sheet"
sidebar_position: 10
author: "Olga Bumazhenko [X]"
---

| Epic | Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| ME05-EP02. Apply feedback for multiple pets |
| APPROVED |
| Nicolay Gavrilov |
| HALO-6052 - iOS [RI]: ME05-US24 'Apply feedback for multiple pets' action sheet Closed HALO-6588 - Android [RI]: ME05-US24 'Apply feedback for multiple pets' action sheet Closed |
| 30 Sep 2021 Maria Shikareva [X] Implementation status is marked as "Done" for both iOS and Android. |# Contents

User story Acceptance criteria 'Apply feedback for multiple pets (your pet)' button on the 'Find' card 'Apply feedback for all/your pet' action sheet Select pets "Select All / Unselect All" button Changing the caption of the button and the action sheet

# User story

\> As a user I want to be able to apply feedback to multiple pets with one tap because doing this one by one is uncomfortable, takes too much time and the command may no longer be needed while I run trhough all the pets in my account. Some of the usage scenarios are the following:Call all dogs home with 'Return whistle' buttonEncorage all dogs with 'Good behavior' feedback when everyone is doing goodWarn all dogs with 'Warning' feedback when a car is coming, or another dog shows up and all dogs start going crazy

# Acceptance criteria

| AC | Text | iOS designs/notes | Android designs/notes | 'Apply feedback for multiple pets (your pet)' button on the 'Find' card | 'Apply feedback for all/your pet' action sheet | Select pets | "Select All / Unselect All" button | Changing the caption of the button and the action sheet |
|---|---|---|---|---|---|---|---|---|
| iOS / Android implementation status | IOS DONE | ANDROID DONE |
| ME05-US24-AC01 | The 'Apply feedback for multiple pets (your pet)' button should be available on the 'Find' action sheet only if there is at least one pet with a collar in the user account. |  | TBD |
| ME05-US24-AC02 | If the user taps on the 'Apply feedback for multiple pets (your pet)' button, the app should show the 'Apply feedback for multiple pets (your pet)' action sheet. Note: the fonr size of the caption on the button may be reduced to fit on iPhone SE screens OR, we can remove "Apply" (whichever is easier to implement). | - | - |
| ME05-US24-AC03 | 'Apply feedback for multiple pets' action sheet should have the following UI elements:Header'Select all / Unselect all' button'X pets selected' field'Pets selection' section'Prevention' section'Encouragement' section'Close' button |  | TBD |
| ME05-US24-AC04 | To apply feedback for multiple pets users should tap on a button from the preventions or encouragements section. | - | - |
| ME05-US24-AC11 | When the user applies feedback for all pets, the app displays the spinner over the corresponding button. At that, all UI elements on the action sheet should become unavailable until the app gets the results (either success or errors) from all pets. |  | The design is similar to iOS |
| ME05-US24-AC05 | If the app fails to send a feedback command via BLE because:Bluetooth is disabled on the smartphoneThe collar was not found during the background scanningThe app failed to unlock the collarthe app should send the command via the internet. | - | - |
| ME05-US24-AC06 | The action sheet should be closed by tapping on any other area of the screen outside it or by tapping on the 'Close' button. | - | - |
| ME05-US24-AC08 | If the Bluetooth permission is not granted (e.g. after the user re-installed the app) the app will ask for it on the first attempt to apply feedback for multiple pets.And in case the user denies the Bluetooth permission the app should only use the internet channel until permission is granted. At that, the app should not request Bluetooth permission on sending instant feedback. | - | - |
| ME05-US24-AC07 | If the feedback was successfully applied for all pets, the app should show the 'success' icon on the feedback button. |  | The design is similar to iOS |
| ME05-US24-AC12 | If more than one pet didn't get the feedback, the app should show the following pop-up:Header: Feedback to Some Pets Could Not Be ConfirmedBody: \<pet_name1\>, \<pet_name2\>, ... \<pet_nameX\> collars are out of Wi-Fi, Bluetooth and Cellular range. Buttons: OKTo close the pop-up users should tap on the 'OK' button. | - | - |
| ME05-US24-AC35 | If one pet only didn't get the feedback, the app should show the following pop-up:Header: Feedback to the Pet Could Not Be ConfirmedBody: \<pet_nameX\> collar is out of Wi-Fi, Bluetooth and Cellular range.Buttons: OKTo close the pop-up users should tap on the 'OK' button. | - | - |
| ME05-US24-AC34 | If the text of the 'Feedback to Some Pets Could Not Be Confirmed' pop-up is too long, then:the popup frame is stretched.users should be able to scroll the text to read it all. (this functionality is not implemented as of 4/22/21, might be done later within the general task: HALO-6964 - MOB: Automatically add scroll to custom popup messages, in case the text doesn't fit into the popup frame Open ). | - | - |
| ME05-US24-18 | Each pet in the 'Pets selection' section should be presented with a button that has:\<Pet avatar\> + \<Halo ring\> + \<Pet name\>;checkbox. | - | - |
| ME05-US24-19 | Only those pets who are assigned with collars should be displayed on the action sheet. | - | - |
| ME05-US24-20 | If there are at least 3 pet buttons on the action sheet, they should be displayed in two rows |  | The design is similar to iOs |
| ME05-US24-21 | If there are too many pet buttons to fit on the screen, users should be able to swipe to the left or to the right to view all of them. | - | - |
| ME05-US24-22 | To select (unselect) a pet users should tap on the button with it's icon. At that the checkmark should appear in (disappear from) the checkbox on the button. | - | - |
| ME05-US24-23 | The number of selected pets should be displayed in the top right area of the action sheet. | - | - |
| ME05-US24-24 | When users taps on a feedback button the command should be sent only to those pets, that are selected. | - | - |
| ME05-US24-25 | Pet names should be abbreviated if they are too long to fit into their buttons. | - | - |
| ME05-US24-AC26 | All pets should be selected by default when the user opens the 'Apply feedback for multiple pets' action sheet after logging in. | - | - |
| ME05-US24-27 | The app should remember the selection state of the pets on the action sheet and the user should see the same pets selected when the action sheet is reopened within one session. | - | - |
| ME05-US24-AC36 | If the new pet(s) is(are) added within the current session, this(these) pet(s) should be displayed unselected. |  |  |
| ME05-US24-28 | Users should not be able to select or unselect pets as well as tap the feedback buttons while the feedback command is being sent to the pets. | - | - |
| ME05-US24-29 | When none of the pets are selected and the user taps on a feedback button the following toast message should be displayed:Please select at least one pet to apply feedback | - | - |
| ME05-US24-30 | Users should be able to select all pets by tapping on the 'Select All' button. | - | - |
| ME05-US24-31 | If all pets are selected the 'Select All' button should be replaced with the 'Unselect All' button. | - | - |
| ME05-US24-32 | Users should be able to unselect all pets by tapping on the 'Unselect All' button. | - | - |
| ME05-US24-33 | If at least one pet is unselected, the 'Unselect All' button should be replaced with the 'Select All' button. | - | - |
| ME05-US24-AC09 | The button on the 'Find card' should have 'Apply feedback for your pet' caption if there is only 1 pet with a collar in the user account. | - | - |
| ME05-US24-AC10 | The button on the 'Find card' should have 'Apply feedback for multiple pets' caption if there is more than 1 pet with a collar in the user account. | - | - |Feedback to Some Pets Could Not Be Confirmed


