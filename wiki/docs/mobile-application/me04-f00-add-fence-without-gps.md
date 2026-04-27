---
title: "ME04-F00. Add fence without GPS"
sidebar_label: "ME04-F00. Add fence without GPS"
sidebar_position: 647
last_modified: "Jan 09, 2024"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| No JIRA links |# User story

\> As an account owner, I would like to create a new fence so that I can mark safe area for my pet.

Contents

User story As an account owner, I would like to create a new fence so that I can mark safe area for my pet. Acceptance criteria The entry point to the Add Fence flow "Create New Fence - Fence Drawing step" screen: buttons "Create New Fence - Fence Drawing step" screen: toast messages "Create New Fence - Fence Drawing step" screen: drawing process "Create New Fence - Fence Drawing step" screen: a tip on how to close a fence "Create New Fence - Fence Drawing step" screen: fence form validation "Create New Fence - Fence Name step" screen Fence operating description Table ME04 -1 Draw a fence errors/warnings

### Acceptance criteria

| AC | Text | iOS | Android | The entry point to the Add Fence flow | "Create New Fence - Fence Drawing step" screen: buttons | "Create New Fence - Fence Drawing step" screen: toast messages | "Create New Fence - Fence Drawing step" screen: drawing process | "Create New Fence - Fence Drawing step" screen: a tip on how to close a fence | "Create New Fence - Fence Drawing step" screen: fence form validation | "Create New Fence - Fence Name step" screen | Fence operating description |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-FE00-AC01 | Precondition: Find card is opened, see the card description in ME15-F02. Find card.If I tap on the Add Fence button and there are 20 fences in my account, then:M58 Fence restriction error message should be displayed. | - | - |
| ME04-FE00-AC02 | Precondition: Find card is opened, see the card description in ME15-F02. Find card.If I tap on the Add Fence button and there are less than 20 fences, then:the "Create New Fence - Fence Drawing" screen should be opened;zoom 16 (minimum acceptable zoom to place a post with finger) should be applied for My Map;my map should be centered on my location.Note: if the access to the user location isn't provided, then see BR-11 Map view settings. | - | - |
| ME04-FE00-AC03 | If I tap on the Cancel button and at least one fence post is added, then:M63. Cancel Fence warning message should be displayed.Toast text for AndroidPlease tap on the map to create your first fence post | Pic 1 - Create New Fence - Fence Drawing | Pic 1 - Create New Fence - Fence Drawing |
| ME04-FE00-AC04 | If I tap on the Questionmark icon, then see a continuation in ME04-FE05. Fence Tutorials. | - | - |
| ME04-FE00-AC05 | If I tap on the Collars icon, then see a continuation in ME04-EP03 Create a fence with a collar. | - | - |
| ME04-FE00-AC06 | If I tap on the Map Settings icon, the see a continuation in ME15-F01. Map settings card. | - | - |
| ME04-FE00-AC07 | The Compass button can be displayed on the "Create New Fence" screen under certain circumstances. See the button functionality description within ME15-F00. View my map. | - | - |
| ME04-FE00-AC08 | See the list of error/warning toasts (+triggers) that can appear while the fence creating or editing in Table ME04 -1 Draw a fence errors/warnings below. | - | - |
| ME04-FE00-AC09 | If I tap on My Map while a new fence creation, then:the fence post should be added;the added fence post should be connected with the last added fence post;the fence side length should meet the rules, described in ME04-FE00-AC10 and AC11. | - | - |
| ME04-FE00-AC10 | If I try to add a new fence post/ move the added post/ close a fence AND distance between any posts become less than 6 feet, then:the action shouldn't be performed;the following toast message should be displayed for 4 sec: "Please make sure fence posts are at least 6 feet apart"Note: MIN and MAX side length should be configurable on the BE. | - | - |
| ME04-FE00-AC11 | If I try to add a new post/ move the added post/ close a fence AND distance between any posts become more than 6 miles, then:the action shouldn't be performed;the following toast message should be displayed for 4 sec: "Please make sure fence posts are less than 6 miles apart". | - | - |
| ME04-FE00-AC12 | If at least one fence post is added, then:the toolbar should be displayed at the bottom of the screen.Note: the bar doesn't disappear, even if all fence posts are removed.The toolbar consists of:"Undo" button;"Redo" button;"Delete" button. |  | - |
| ME04-FE00-AC13 | If I tap on the Undo button, then:the previous action with a fence should be reverted. | - | - |
| ME04-FE00-AC14 | If I tap on the Redo button, then:the last undone action with a fence should be restored. | - | - |
| ME04-FE00-AC15 | Precondition: the fence is closed.If I tap on the Delete button, then:the selected fence post should be removed;the fence should auto-fill without an old deleted post. | - | - |
| ME04-FE00-AC16 | Precondition: the fence is open.If I tap on the Delete button, then:the selected fence post should be removed;the adjacent fence posts should be connected (if they exist). | - | - |
| ME04-FE00-AC17 | If there are no posts to undo/redo/delete and I initiate these actions, nothing happens. | - | - |
| ME04-FE00-AC18 | I can move fence posts using a long tap across the map anytime. | - | - |
| ME04-FE00-AC19 | I can pinch in/out the map, swipe to any side while creating a fence. | - | - |
| ME04-FE00-AC20 | If I tap on the first post and there are 3 fence posts at least, then:the fence should be closed;the Next button should become available. | - | - |
| ME04-FE00-AC21 | If at least 3 fence posts are added and the fence still hasn't been closed, then:the first fence post should be animated, see animation.the animation continues till I close a fence or less than 3 fence posts are left on My Map. | - | - |
| ME04-FE00-AC22 | If I add a fence post, the number of dots becomes 3 and the fence hasn't been closed, then:the standard iOS popup message M139 Great job with the fence creation should be displayed. | - | - |
| ME04-FE00-AC23 | If I remove fence posts, only 1 or 2 fence posts left and I add the 3rd fence post, then:the popup M139 Great job with the fence creation should be displayed again. | - | - |
| ME04-FE00-AC24 | If the 3rd point is added via a tap on Undo/Redo, then:the popup M139 Great job with the fence creation should not be displayed again. | - | - |
| ME04-FE00-AC25 | If I tap on the Next button and during BE fence square validation it is identified that the fence has more then 1 safe area, then:the M128 Fence has more than 1 safe zone (BE validation) error should be displayed. | - | - |
| ME04-FE00-AC26 | If I tap on the Next button and during BE fence square validation it is identified that the fence is less than 250 square feet, then:the M127 Fence is too small (BE validation) error should be displayed. | - | - |
| ME04-FE00-AC27 | If I tap on the Next button and some other error happens, then:ME14-F01 Unified errors handling mechanism should be applied. | - | - |
| ME04-FE00-AC28 | If I tap on the Next button and all validations are passed successfully, then:"Create New Fence - Fence Name step" screen with the open keyboard should be opened. | - | - |
| ME04-FE00-AC29 | If I tap on the Back button, then:"Create New Fence - Fence Drawing step" screen should be displayed and I can edit the fence outline.Note: the entered fence name isn't saved. | - | - |
| ME04-FE00-AC30 | If I enter not unique fence name (for this account), then:the following field error should be displayed: "You currently have a fence with the same name".Triggers:A user confirms value on the keyboard by tapping a buttonWhen the keyboard is open, a user taps out of it, initiating closing the keyboardA user taps "Done" in the navigation bar |  |  |
| ME04-FE00-AC31 | If I don't enter at least one character, then:the following field error should be displayed: "Сannot be blank".Triggers:A user confirms value on the keyboard by tapping a buttonWhen the keyboard is open, a user taps out of it, initiating closing the keyboard | - | - |
| ME04-FE00-AC32 | The app should not allow entering more than 20 characters. | - | - |
| ME04-FE00-AC33 | If I entered at least one character, then:the Done button should become available. | - | - |
| ME04-FE00-AC34 | Cross icon should be displayed in the Fence name field while editing.If I tap on the Cross icon the field should be cleared. | - | - |
| ME04-FE00-AC35 | If I tap on the Done and an error happens, then:ME14-F01 Unified errors handling mechanism should be applied. | - | - |
| ME04-FE00-AC36 | If I tap on the Done and a fence is successfully saved, then:my map should be opened centering on the just created fence;the fence card in the default view should be displayed.the fence should be sent to the collars with the assigned pets. | - | - |
| ME04-FE00-AC37 | A fence is a safe area for all pets. If a pet has 1 or more active safe areas, all other territories should be considered as an unsafe area. | - | - |
| ME04-FE00-AC38 | If a pet has zero fences, then the pet cannot engage Fences On mode, Fences Off is the only available. | - | - |
| NoteThe logic of the fence area calculation is presented there: Geofence Zone Calculation#FunctionalRequirementsFormalizationSuggestion |### Table ME04 -1 Draw a fence errors/warnings

| № | Messages/errors on the screen | Trigger | Displaying time | iOS impl-n status | Android impl-n status |
|---|---|---|---|---|---|
| ME04-F00-M1 | Please zoom in to place a fence post accurately | If the zoom scale on the map becomes less than 16 after a closer zoom.* So it is hard to see the fence position accurately. | Temporarily toast (4 seconds) | IOS DONE | ANDROID TO DO |
| ME04-F00-M2 | Your fence can include up to \{0\} fence posts. You can adjust existing fence posts with your finger or using toolbar. | A user tries to tap more than max number of posts, see R-13. | IOS DONE | ANDROID TO DO |
| ME04-F00-M3 | Your fence must have at least \{0\} fence posts | A user taps on the first post but has made just 1-2 posts → nothing will happen with the polygon | IOS DONE | ANDROID TO DO |
| ME04-F00-M4 | Tap on your first fence post to complete your fence | A user taps on an existing post, other than first post → nothing will happen with the fencePrecondition: a user has at least 3 posts | IOS DONE | ANDROID TO DO |
| ME04-F00- M5 | iOS: Please tap on the map or select a collar to create your first fence postAndroid: Please tap on the map to create your first fence post | A user has 0 posts placed on the map | Permanent, disappears when a user taps the first post. | IOS DONE | ANDROID TO DO |
| ME04-F00- M6 | Fence lines cannot cross each other | New post causes intersection between another side of the fence and new line | Temporarily toast (4 seconds) | IOS DONE | ANDROID TO DO |
| ME04-F00- M7 | Fences cannot overlap | New post causes intersection with other existing fence in user's account | Temporarily toast (4 seconds) | IOS DONE | IOS DONE |
