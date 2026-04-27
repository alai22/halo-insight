---
title: "ME16-US27. Move the feedback settings to the pet's card"
sidebar_label: "ME16-US27. Move the feedback settings to the pet's card"
sidebar_position: 88
author: "Galina Lonskaya"
---

| Epic | Document status | Story owners | Link to JIRA Issue |
|---|---|---|---|
| ME16 As an Owner, I'd like to manage my pets to keep their info up to date. |
| DONE |
| Galina Lonskaya, Timofey Burak [X], Eugene Paseka, Anastasia Brechko |
| HALO-4150 - MOB: ME16-US22. Move the feedback settings to the pet's card Closed |# USer story

\> As an owner, I want to navigate to the feedback settings list from the pet's card so that I can adjust the feedback settings not interuppting a training pass. This will be possible, since the pet's card belongs to My Map tab and the training belongs to the Training tab.

# Acceptance criteria

| AC | Text | UI design | Pet's card screen | Feedback settings list screen |  | Feedback setting screen | Training screen | Instant feedback card |
|---|---|---|---|---|---|---|---|---|
| ME16-US27-US01 | The Feedback Settings button should be added to the pet's card.Note: the pet's card will be the only way for the user to navigate to the feedback settings. | Pic 1 - Pet's card |
| ME16-US27-US02 | Precondition: Pet's card is displayed.If I tap on the Feedback Settings button, then:the Feedback Settings screen should be opened;the Bluetooth connection is interrupted if the pet has an assigned collar (the reason for this behavior: development simplification)Note 1: Feedback Settings screen should provide the same functionality as it had at the Training tab. Exception: the title is added, the tab bar isn't displayed due to the pet's card implementation restriction (will be fixed within the next sprints). | Pic 2 - Feedback Settings list |
| ME16-US27-US03 | Precondition: Feedback Settings screen is displayed.If I tap on the Back button, then:Pet's card should be displayed;the Bluetooth connection should be restored if the pet has an assigned collar. | - |
| ME16-US27-US04 | Precondition: Feedback Settings screen is displayed.If I tap on any feedback setting tile, then:the corresponded feedback setting screen (Warning Feedback, etc.) should be displayed;the Bluetooth connection should be set up if the pet has an assigned collar. Note: no functional changes for the following screens:Warning Feedback settings screenBoundary Feedback settings screenEmergency Feedback settings screenGood Behavior Feedback settings screenReturn Whistle Feedback settings screenHeading Home Feedback settings screen | Pic 3 - Warning Feedback settings |
| ME16-US27-US05 | Precondition: the pet has an assigned collar.The app disconnects Bluetooth when the user leaves one of the following screens:Warning Feedback settings screenBoundary Feedback settings screenEmergency Feedback settings screenGood Behaviour Feedback settings screenReturn Whistle Feedback settings screenHeading Home Feedback settings screenThe logic for the Feedback settings screen, described in ME06-US14. Testing feedback on collar via BLE. | - |
| ME16-US27-US06 | Precondition: Warning Feedback screen (or Boundary Feedback, etc.) is opened.If I tap on the Back button, then:Feedback Settings screen should be displayed;the Bluetooth connection is interrupted if the pet has an assigned collar. (the reason for this behavior: development simplification) | - |
| ME16-US27-US07 | Precondition: The Training screen is displayed. The possibility to navigate to the feedback settings and the title describing setting state should be removed from the Training screen. | Pic 4 - Training |
| ME16-US27-US08 | The updated text should be displayed at the "Apply Feedback for \<Pet\>" action sheet: "\<Pet's\> feedback settings are available at the bottom of the pet card on My Map". | Pic 5 - "Apply Feedback for \<Pet's name\>" action sheet |
