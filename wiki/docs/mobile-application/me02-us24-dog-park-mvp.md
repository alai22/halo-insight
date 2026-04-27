---
title: "ME02-US24. Dog park MVP"
sidebar_label: "ME02-US24. Dog park MVP"
sidebar_position: 608
last_modified: "Oct 25, 2021"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Vadim Pylsky [X], Pavel Leonenko, Zakhar Makarevich, Svyatoslav Luzin, Valeria Malets |
| HALO-8588 - [GOAL] iOS[+BE]: Dog park MVP Closed HALO-9103 - [GOAL] Android [+BE]: Dog park MVP Closed HALO-9104 - [GOAL] BE +MOB: Dog park MVP Closed |
| As of 05 Oct 2021 - 06 Oct 2021 Mariya Kolyada created the initial version of the US.As of 08 Oct 2021 Mariya Kolyadaadded Option 2 requirements.As of 12 Oct 2021 Mariya Kolyadaupdated descriptions according to the PoC results and added implementation notes.As of 25 Oct 2021 Mariya Kolyadaupdated ME02-US24-AC03 with new meeting credentials. |# User Story

\> As Halo Collar app account owner I want to be able get live video support from Halo via Zoom during open hours so that I can get support anywhere I am and show anything I need.

# Acceptance criteria

| AC | Description | iOS UI design | Android UI design |
|---|---|---|---|
| ME02-US24-AC01 | Add the 'Live Support' option on the Settings screen:As the tiled view option if [BL] ME02-US25. Update the Settings screen tiled view to list view is NOT implemented before the current US.As the list view option if [BL] ME02-US25. Update the Settings screen tiled view to list view is implemented before the current US. | Pic 1 Settings screen: tiled viewORPic 2 Settings screen: list view | Same as iOs |
| ME02-US24-AC02 | If I click on the 'Live Support' option on the Settings screen, then the app should:Display inside the app the screen with options whether to join Zoom meeting with video or without it. | The screen UI is managed by ZoomSDK | The screen UI is managed by ZoomSDK |
| ME02-US24-AC03 | After I chose whether to join with or without video, then the app should:Display inside the app the Waiting room screen of the following Zoom meeting:Meeting link: https://us06web.zoom.us/j/2036806419?pwd=WVRhYms5bHBJamxySXdRTDFFdHlQZz09Meeting ID: 203 680 6419Passcode: 796778Send notification to the host with a request to allow the User to join. | The screen UI is managed by ZoomSDK and in the Halo Zoom account | The screen UI is managed by ZoomSDK and in the Halo Zoom account |
| ME02-US24-AC04 | If Zoom meeting host admits User to join the meeting, then the app should:Open Zoom meeting. The User's camera should be switched on or off depending on what the User has chosen on screen with options whether to join Zoom meeting with video or without it. | The screen UI is managed by ZoomSDK | The screen UI is managed by ZoomSDK |
| ME02-US24-AC05 | If Zoom meeting host declines User to join the meeting, then the app should:Display the Settings screen (Halo app).Display the pop-up notifying that the User was removed from the Zoom meeting. | The pop-up UI is managed by ZoomSDK | The pop-up UI is managed by ZoomSDK |
| ME02-US24-AC06 | The app should display in the header of the Zoom meeting screens (Waiting Room and Zoom Meeting) the following elements:'Live Support' title (instead of 'Zoom').'Leave' button.Note'Live Support' title should be displayed instead of the 'Zoom' title only if during implementation we understand that it is possible.Otherwise, the app will display the 'Zoom' title. | - | - |
| ME02-US24-AC07 | If I click on the 'Leave' button on the Zoom meeting screens (Waiting Room and Zoom Meeting) and on the next screen with confirmation, then the app should:Close Zoom.Display the Settings screen (Halo app). | - | - |
| ME02-US24-AC08 | If I join Zoom meeting, then the app should provide to me all usual features available in Zoom Meetings iOS and Android apps. | - | - |# Implementation notes

| ID | Description |
|---|---|
| ME02-US24-IN01 | BE should store and send to MOB Zoom Meeting ID: 351 570 2655.It should be configurable on BE side. |
| ME02-US24-IN02 | Be should store and send to MOB encrypted Zoom app SDK credentials: SDK Key and SDK Secret (see in slack). |
