---
title: "ME05-US41 [AFFMP]: Showing pets that didn't get the feedback"
sidebar_label: "ME05-US41 [AFFMP]: Showing pets that didn't get the feedback"
sidebar_position: 133
last_modified: "Apr 26, 2021"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| ME05-EP02. Apply feedback for multiple pets |
| APPROVED |
| Nicolay Gavrilov |
| HALO-6577 - iOS [RI]: ME05-US41. Showing pets that didn't get the feedback Reopened HALO-6711 - Android [RI]: ME05-US41. Showing pets that didn't get the feedback Reopened |# User story

\> As a user I want to know which pets didn't get the feedback so that I would be aware that it did not work for some pets and I may need to retry the operation or do something else.

# Acceptance criteria

| AC | Text | iOS design/notes | Android design/notes | iOS/Android implementation status | IOS TO DO | ANDROID TO DO |
|---|---|---|---|---|---|---|
| ME05-US41-AC01 | If at least one pet didn't get the feedback after the user applied it for multiple pets (see ME05-US24 [AFFMP]: 'Apply feedback for multiple pets' action sheet), the app should show the corresponding pop-up that will list all the pets that did not get the feedback. | TBD: wording + remove the retry button | TBD |
| ME05-US41-AC02 | The pop-up is shown right after the app hides the spinner over the button makes all UI elements on the action sheet available again (see ME05-US24 [AFFMP]: 'Apply feedback for multiple pets' action sheet). | - | - |
| ME05-US41-AC03 | The pop-up should have the following UI elements:"Some Pets Didn't Get Feedback" header"Pets list" section"Do you want to retry applying feedback for these pets?" label"Cancel" button | - | - |
| ME05-US41-AC04 | Each pet in the 'Pets list' section should be presented as \<Pet avatar\> + \<Halo ring\> + \<Pet name\> on the pop-up. | - | - |
| ME05-US41-AC05 | Pet names should be abbreviated if they are too long to fit the pet icon width. | - | - |
| ME05-US41-AC07 | Users may close the pop-up by tapping on the corresponding button. At that, the app should show the "Apply feedback for multiple pets" action sheet. | - | - |
