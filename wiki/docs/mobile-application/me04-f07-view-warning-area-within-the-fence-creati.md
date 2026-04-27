---
title: "ME04-F07. View Warning Area within the fence creation/editing flow"
sidebar_label: "ME04-F07. View Warning Area within the fence creation/editing flow"
sidebar_position: 101
last_modified: "Dec 04, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Story owners | Link to JIRA Issue |
|---|---|---|---|
| Baseline story |
| REVISED |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko, Eugene Paseka |
| HALO-3581 - iOS: GOAL: ME04-F07. Display Warning Area within "fence creation"/"fence editing" flow RESOLVEDHALO-5148 - Android: ME04-FE07. Warning area IN CODE REVIEW |# User story

\> As owner, I want to view Warning Area so that I can understand where my pet will get Warning feedback.

# Acceptance criteria

| AC | Text | iOS impl-n status / NotesIOS DONE | Android impl-n status / NotesANDROID TO DO | "Create New Fence" flow | "Edit Fence Posts" flow |
|---|---|---|---|---|---|
| ME04-F07-AC01 | Precondition: "Create New Fence - fence drawing" screen is displayed. The fence is closed, see the description in See continuation ME04-US03. Create a fence.If I tap on the Next button and the fence validations are passed successfully, then:Warning Area screen should be displayed.The Warning Area screen should consist of:Back icon"Warning Area" titleNext buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary Feedback will occur if your dog is inside the area marked with diagonal lines.All fence warning areas use a 7 to 10 ft diameter. The fence line should be at least 15 ft from your house." subtitle | The Warning Area screen should consist of:Back icon"Warning Area" titleNext buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary Feedback will occur if your dog is inside the area marked with diagonal lines.All fence warning areas use a 7 to 10 ft diameter. The fence line should be at least 15 ft from your house." subtitle | Pic 1 Create New Fence - Warning Areahttps://zpl.io/aRpxZ7E | Note: Map Settings isn't available for the Android users as of 11/10/2020See the screen for Android https://zpl.io/bz4YQB3 |
| The Warning Area screen should consist of:Back icon"Warning Area" titleNext buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary Feedback will occur if your dog is inside the area marked with diagonal lines.All fence warning areas use a 7 to 10 ft diameter. The fence line should be at least 15 ft from your house." subtitle |
| ME04-F07-AC02 | Precondition: "Create New Fence - "Warning Area" screen is displayed.The bottom "Warning Area" card is always displayed on this screen state (user can't close it on his own).It disappears, only if "Map settings" are displayed at the moment. | - | Note: Map Settings isn't available for the Android users |
| ME04-F07-AC03 | Precondition: "Create New Fence - Warning Area" screen is displayed.If I tap on the Map Settings icon, then:"Warning Area" bottom card should be closed;"Map settings" bottom card should be opened, see details of "Map Settings" usage in ME07-US04. Use "My Map" tools. | - | Note: Map Settings isn't available for the Android users |
| ME04-F07-AC04 | Precondition: "Create New Fence - Warning Area" screen is displayed, "Map Settings" is displayed.If the "Map Settings" card is closed, then:"Warning Area" card should be opened again. | - | Note: Map Settings isn't available for the Android users |
| ME04-F07-AC05 | Precondition: "Create New Fence - Warning Area" screen is displayed.If I tap on the Next button, then:"Create New Fence - "fence name" adding" screen should be displayed.See continuation in ME04-US03. Create a fence. | - | - |
| ME04-F07-AC06 | Precondition: "Create New Fence - fence name" screen is displayed.If I tap on the Back button, then:"Create New Fence - Warning Area" screen should be displayed. | - | - |
| ME04-F07-AC07 | Precondition: "Edit Fence Posts - fence editing" screen is displayed. See source story for fence editing flow: ME04-US08. Edit dots of the fence.The "Next" button should be displayed instead of the "Done" button. | Pic 2 Edit Fence Posts - fence editing | The same screen as for iOS.Note: Map Settings isn't available for the Android users |
| ME04-F07-AC08 | Precondition: "Edit Fence Posts - fence editing" screen is displayed.If I tap on the Next button, then:the same validations should be performed as for the "Next" button at the "Create New Fence - fence drawing" screen. | - | - |
| ME04-F07-AC09 | Precondition: "Edit Fence Posts - fence editing" screen is displayed.If fence validations are successfully passed, then:"Warning Area" screen should be displayed.The Warning Area screen should consist of:Back icon"Warning Area" titleDone buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary Feedback will occur if your dog is inside the area marked with diagonal lines.All fence warning areas use a 7 to 10 ft diameter. The fence line should be at least 15 ft from your house." subtitle | The Warning Area screen should consist of:Back icon"Warning Area" titleDone buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary Feedback will occur if your dog is inside the area marked with diagonal lines.All fence warning areas use a 7 to 10 ft diameter. The fence line should be at least 15 ft from your house." subtitle | https://zpl.io/aRpxZ7E | The same screen as for iOS. Note: Map Settings isn't available for the Android users |
| The Warning Area screen should consist of:Back icon"Warning Area" titleDone buttonFence with Warning Area"Map Settings" iconBottom "Warning Area" card consists of:"Warning Area" title"Warning and Boundary Feedback will occur if your dog is inside the area marked with diagonal lines.All fence warning areas use a 7 to 10 ft diameter. The fence line should be at least 15 ft from your house." subtitle |
| ME04-F07-AC10 | Precondition: "Edit Fence Posts - Warning Area" screen is displayed.The same AC should be applied as described in ME04-F07-AC02, AC03, AC04. | - | - |
| ME04-F07-AC11 | Precondition: "Edit Fence Posts - Warning Area" screen is displayed.If I tap on the Done button, then:the fence updates should be saved;"Edit Fence Posts" window should be closed;the previous screen should be opened. | - | - |
