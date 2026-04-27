---
title: "[BL] ME02-US27. Zoom opening from Solvvy"
sidebar_label: "[BL] ME02-US27. Zoom opening from Solvvy"
sidebar_position: 177
last_modified: "Apr 25, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED (SQ) |
| Maria Shikareva [X] Vadim Pylsky [X] Pavel Leonenko |
| HALO-9426 - MOB: Zoom opening from Solvvy Closed Ballpark estimation:MOB: 3SP |
| Click here to expand...25 Apr 2022 Maria Shikareva [X] Marked the story as baselined (ME02-F00. View "Settings" screen). |# User Story

\> As a Halo app user I want to be able get live video support from Halo via Zoom when I select a corresponding option within Solvvy so that I can get support anywhere I am and show anything I need.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| ME02-US27-AC01 | Precondition: Solvvy WebView is opened.When the user taps on the corresponding option within Solvvy, then the app should initiate Zoom opening (using ZoomSDK):"Live support 9am-6pm EST" buttons;visit our virtual "Dog Park" link;"Visit our Dog Park to chat with a customer representative" buttons.Note: Zoom opening should be initiated in all places as it implemented on halocollar.com. | - | - |
| ME02-US27-AC02 | The requirements for further app behavior should be the same as described in ME02-US24-AC02 - ME02-US24-AC04, ME02-US24-AC06 and ME02-US24-AC08). | - | - |
| ME02-US27-AC03 | If Zoom meeting host declines User to join the meeting, then the app should:display the Solvvy screen from which Zoom opening was initiated (Halo app);display the pop-up notifying that the user was removed from the Zoom meeting.NoteIf it's not possible to display the "Solvvy" screen (and it becomes clear during implementation), then the app can display the "Settings" screen instead. | The pop-up UI is managed by ZoomSDK | The pop-up UI is managed by ZoomSDK |
| ME02-US27-AC04 | When the user taps on the 'Leave' button on the Zoom meeting screens (Waiting Room and Zoom Meeting) and on the next screen with confirmation, then the app should:close Zoom meeting;display the Solvvy screen from which Zoom opening was initiated (Halo app).NoteIf it's not possible to display the "Solvvy" screen (and it becomes clear during implementation), then the app can display the "Settings" screen instead. | - | - |
