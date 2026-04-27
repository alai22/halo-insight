---
title: "ME04-F02. Edit Fence Posts"
sidebar_label: "ME04-F02. Edit Fence Posts"
sidebar_position: 648
last_modified: "Mar 09, 2021"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story (checked by dev team) |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| HALO-5357 - Android GOAL: Add/Edit fence with GPS Closed |### User story

\> As an account owner, I would like to edit fence dots so that I change the size and location of the area.

Contents

User story Acceptance criteria Entry point to the Edit Fence Posts screen Edit Fence Posts screen: functionality description Cancel Fence Posts editing Save Edited Fence Edit fence posts with GPS

### Acceptance criteria

| AC | Text | iOS screens / impl-n status | Android screens / impl-n status | Entry point to the Edit Fence Posts screen | Edit Fence Posts screen: functionality description | Edit Fence Posts screen: toast messages | Cancel Fence Posts editing | Save Edited Fence | Edit fence posts with GPS |
|---|---|---|---|---|---|---|---|---|---|
| ME04-FE02-AC01 | Precondition: Fence card in the default view is displayed.If I tap on the Edit Fence Posts button, then:the Edit Fence Posts screen should be opened. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC02 | The same buttons as while fence creation should be available.See the following criterias in ME04-FE00. Add Fence (without GPS):Questionmark button - ME04-FE00-AC04Collars button - ME04-FE00-AC05Map Settings button - ME04-FE00-AC06Compass button - ME04-FE00-AC07Toolbar (Undo, Redo, Delete) - ME04-FE00-AC12, AC13, AC14, AC15, AC17 | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC03 | I can't add fence posts to the closed fence while fence posts editing. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC04 | I can't open the fence while fence posts editing. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC05 | I can move fence posts, see ME04-FE00-AC18. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC06 | I can interact with my map, in the same way as while the fence creating, see ME04-FE00-AC19 | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC07 | While the fence editing the following toast messages can be displayed.ME04-F00-M1ME04-F00-M6See them in Table ME04 -1 Draw a fence errors/warnings, ME04-FE00. Add Fence (without GPS). | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC08 | If I tap on the Cancel button and the fence was edited, then:the M100 Cancel fence editing error message should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC09 | If I tap on the Cancel button and the fence wasn't changed, then:the Edit Fence Posts screen should be closed. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC10 | Precondition: the Edit Fence Posts screen is displayed with the Done button.If I tap on the Done button and the fence changes are successfully updated, then:the Fence card in the default view and updated fence outline should be displayed;My Map should be centered on the fence. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC11 | Precondition: the Edit Fence Posts screen is displayed with the Done button.If I tap on the Done button and some error happens, then:unified error handling mechanism should be applied, seeME14-F01 Unified errors handling. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC12 | To edit fence posts with GPS, the user should tap the "Select collar" icon. After that the app should show theCollars list. | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC13 | Users should choose and pair the collar for editing fence posts with GPS as it is described in ME04-F10 Add fence with GPS: Confirm Collar Choice | IOS DONE | ANDROID TO DO |
| ME04-FE02-AC14 | After the collar is paired, the app shows the 'Edit fence posts' screen. After that, the user can edit fence posts similarly to how it is done when adding a new fence with GPS. | IOS DONE | Android design is similar to iOsANDROID TO DO |
