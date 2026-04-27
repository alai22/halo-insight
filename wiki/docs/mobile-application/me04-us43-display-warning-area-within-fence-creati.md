---
title: "ME04-US43. Display Warning Area within \"fence creation\"/\"fence editing\" flow"
sidebar_label: "ME04-US43. Display Warning Area within \"fence creation\"/\"fence editing\" flow"
sidebar_position: 68
last_modified: "Jan 13, 2021"
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Story owners | Link to JIRA Issue |
|---|---|---|---|---|
| Owner |
| ME04 Create fence |
| APPROVED |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko, Eugene Paseka |
| HALO-3581 - iOS: GOAL: ME04-US43. Display Warning Area within "fence creation"/"fence editing" flow Closed HALO-5148 - Android: View warning area in fence creation flow Closed |# User story

\> As owner, I want to view Warning Area so that I can understand where my pet will get Warning feedback.

# Acceptance criteria

| AC | Text | "Create New Fence" flow | "Edit Fence Posts" flow |
|---|---|---|---|
| ME04-US43-AC01 | M127 Fence is too small (BE validation) wording should be updated. Note: Click on the link to check new wording. |
| ME04-US43-AC02 | Precondition: "Create New Fence - fence drawing" screen is displayed. The fence is closed.If I tap on the Next button and the fence validations are passed successfully, then:Warning Area screen should be displayed.The screen should consist of:Back icon"Warning Area" titleNext buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary feedback will occur if your dog is inside the area marked with diagonal lines. All fence warning areas use a 6ft diameter." subtitle |  | The screen should consist of:Back icon"Warning Area" titleNext buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary feedback will occur if your dog is inside the area marked with diagonal lines. All fence warning areas use a 6ft diameter." subtitle |
|  | The screen should consist of:Back icon"Warning Area" titleNext buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary feedback will occur if your dog is inside the area marked with diagonal lines. All fence warning areas use a 6ft diameter." subtitle |
| ME04-US43-AC03 | Precondition: "Create New Fence - "Warning Area" screen is displayed. The bottom "Warning Area" card is always displayed on this screen state (user can't close it on his own).It disappears, only if "Map settings" are displayed at the moment. |
| ME04-US43-AC04 | Precondition: "Create New Fence - "Warning Area" screen is displayed. If I tap on My Map settings icon, then:"Warning Area" bottom card should be closed;"Map settings" bottom card should be opened, see details of "Map Settings" usage in ME15-F01. Map settings card. |
| ME04-US43-AC05 | Precondition: "Create New Fence - "Warning Area" screen is displayed, "Map Settings" is displayed. If the "Map Settings" card is closed, then:"Warning Area" card should be opened again. |
| ME04-US43-AC06 | Precondition: "Create New Fence - "Warning Area" screen is displayed. If I tap on the Next button, then:"Create New Fence - "fence name" adding" screen should be displayed.See continuation in ME04-US03. Create a fence. |
| ME04-US43-AC07 | Precondition: "Create New Fence - "fence name" adding" screen is displayed. If I tap on the Back button, then:"Create New Fence - "Warning Area" view" screen should be displayed. |
| ME04-US43-AC08 | Precondition: "Edit Fence Posts - fence editing" screen is displayed."Next" button should be displayed instead of the "Done" button.See source story for fence editing flow: ME04-US08. Edit dots of the fence. |
| ME04-US43-AC09 | Precondition: "Edit Fence Posts - fence editing" screen is displayed. If I tap on the Next button, then:the same validations should be performed as for the "Next" button at the "Create New Fence - fence drawing" screen. |
| ME04-US43-AC10 | Precondition: "Edit Fence Posts - fence editing" screen is displayed. If fence validations are successfully passed, then:"Warning Area" screen should be displayed.The screen should consist of:Back icon"Warning Area" titleDone buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary feedback will occur if your dog is inside the area marked with diagonal lines. All fence warning areas use a 6ft diameter." subtitle |  | The screen should consist of:Back icon"Warning Area" titleDone buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary feedback will occur if your dog is inside the area marked with diagonal lines. All fence warning areas use a 6ft diameter." subtitle |
|  | The screen should consist of:Back icon"Warning Area" titleDone buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary feedback will occur if your dog is inside the area marked with diagonal lines. All fence warning areas use a 6ft diameter." subtitle |
| ME04-US43-AC11 | Precondition: "Edit Fence Posts - "Warning Area" screen is displayed. The same AC should be applied as described in ME04-US43-AC03, AC04, AC05. |
| ME04-US43-AC12 | Precondition: "Edit Fence Posts - "Warning Area screen is displayed. If I tap on the Done button, then: the fence updates should be saved;"Edit Fence Posts" window should be closed;the previous screen should be opened. |
