---
title: "ME21-US14. Show Onboarding when a user adds a collar later"
sidebar_label: "ME21-US14. Show Onboarding when a user adds a collar later"
sidebar_position: 726
last_modified: "Jun 25, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| FINAL |
| Maria Shikareva [X] Dmitry Kravchuk Alina Sharshun [X] Zakhar Makarevich Anton Zimin [X]Maryia Paklonskaya [X] |
| HALO-12969 - MOB+BE: ME21-US14. Show Onboarding when a user adds a collar later Closed |
| 08 Feb 2023 changes in magenta |# Contents

User story Acceptance criteria General requirements Mobile analytics Adding the first collar from the Settings tab → My Collars

# User story

\> As a Halo app user I want to see an onboarding flow when I add a collar and haven't seen an onboarding flow before so that to not miss important information about collar setup.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | Existing event | Change required |
|---|---|---|---|---|---|
| General requirements |
| ME21-US14-AC01 | User's onboarding progress should have 3 states:not completed → when a user didn't complete any part of Onboarding;partially completed → when a user completed 2nd or 3rd flow of onboarding (i.e. selected "I’m waiting for my Halo Collar" or "I’m thinking about joining the Halo Pack" options on the "User type choice" screen) without adding a collar;fully completed → when a user added a collar (passed 7 steps) during onboarding. | - | - |
| ME21-US14-AC02 | Existing users should be updated according to the following logic:existing users who started onboarding but didn't complete any of the flow → should be marked as not completed;existing users with completed onboarding AND who didn't see "3/7 Adding Your Pet" step should be marked as partially completed.Note: these are all existing users who passed the 2nd or 3rd onboarding flows.existing users with completed onboarding AND who didn't see any step should be marked as fully completed partially completed;Note:these are all existing users with collars at the moment of Onboarding release. They marked as completed so that they won't see onboarding from the beginning but they will see it next time when they want to add another collarexisting users with completed onboarding AND who saw "3/7 Adding Your Pet" step should be marked as fully completed;Note: these are all new users who passed Onboarding themselves and added a collar during it (within 1st flow). | - | - |
| ME21-US14-AC03 | When onboarding is not completed, then when a user enters the app next time, the app should:check if it needs to restore user's progressopen the screen based on the existing logic ('My Map' tab/ previously opened screen/ restored progress/ etc.).The app should restore user's progress only if it's in not completed state.Dev note: if a progress is in partially completed state AND a user successfully adds the collar to the account, then the system should change it's progress state to not completed. It's need to correctly restore user's progress if they leave the app during adding a collar.Example: a user completed 2 or 3 flow;a user started adding a collar, stopped somewhere (e.g. stopped on FW update) and left the app;in some time a user enters the app → the app should restore Onboarding from FW update step. | - | - |
| ME21-US14-AC04 | When onboarding is partially completed, then when a user enters the app next time, the app should:not show first screens of Onboarding at all;open the screen based on the existing logic ('My Map' tab/ previously opened screen/ etc.);start showing Onboarding when a user taps 'Add Collar' button (see more details in ME21-US14-AC below). | - | - |
| ME21-US14-AC05 | When onboarding is fully completed, then when a user enters the app next time, the app should:not show first screens of Onboarding at all;open the screen based on the existing logic ('My Map' tab/ previously opened screen/ etc.). | - | - |
| Mobile analytics |
| ME21-US14-AC06 | The following events should be changed:Existing eventChange requiredios_onboarding_completedandroid_onboarding_completedOne more parameter should be added to highlight that onboarding was fully completed after adding a collar from the Collars list.ios_video_views_statisticsandroid_video_views_statisticsAdd 2 parameters to show how many users skip watching the video. Example:CompletedSkipped | ios_onboarding_completedandroid_onboarding_completed | One more parameter should be added to highlight that onboarding was fully completed after adding a collar from the Collars list. | ios_video_views_statisticsandroid_video_views_statistics | Add 2 parameters to show how many users skip watching the video. Example:CompletedSkipped | - | - |
| ios_onboarding_completedandroid_onboarding_completed | One more parameter should be added to highlight that onboarding was fully completed after adding a collar from the Collars list. |
| ios_video_views_statisticsandroid_video_views_statistics | Add 2 parameters to show how many users skip watching the video. Example:CompletedSkipped |
| Adding the first collar from the Settings tab → My Collars |
| ME21-US14-AC07 | Precondition: a user has never seen "3/7 Adding Your Pet' step of Onboarding.Note: it means that a user has never seen Onboarding during adding a collar flow.When a user taps 'Add Collar' button on the 'My Collars' list, then the app should start Onboarding flow from displaying the 'Let's Get Started' screen. | - | - |
| ME21-US14-AC08 | Precondition: Onboarding started from the Settings tab.When a user taps the 'Back' button, the app should open "My Collars" list. |  |  |
| ME21-US14-AC09 | Tab bar should be hidden during Onboarding.BA note: we need to hide it so that a user can't swap to another tab and interfere into the Onboarding process. | - | - |
| ME21-US14-AC10 | 'Using Halo Collar App'/ 'Start Halo Training' screens should be shown in any flow (even if a user saw it already).BA note: for 'Using Halo Collar App' - it's easier from implementation/ support perspective; for 'Start Halo Training' - it's OK to show the screen twice because first time a user could pass only the Basic User Training; after adding a collar - it's high time to pass the Basic Pet Training. | - | - |
| ME21-US14-AC11 | Precondition: 'Powering Up & Connecting' screen is opened.When a user taps 'Return to start' button, the app should open:to 'My Collars' list → when started from Settings;to the 'User type choice' screen → when started from User Choice. | - | - |
| ME21-US14-AC12 | Precondition: a collar is successfully added to the accountANDlimit of pets is maximum in the account (see ME07-F00-AC02 for more details).The app should show a MTBD pop-up:Title: "Unable to Add Pet"Body: "You can have up to 10 pets per account. Please assign this collar to a pet later in Settings → My Collars."Button "OK"This criterion isn't required because we agreed to release this task together with HALO-14222 - MOB: ME21-US50. Changes to Onboarding if a user already has a pet without assigned collars Closed . And this case will be handled separately. | - | - |
| ME21-US14-AC13 | Precondition: MTBD is displayed.When a user taps the "OK' button, then the app should:close the error pop-up;open "Connecting Your Halo Collar" onboarding screen. | - | - |
| ME21-US14-AC14 | Precondition: a user tapped the 'Not Now' button on the 'Start Halo Training' screen.After fully completing the Onboarding the app should open:'My Collars' list (ideally)/ the Settings tab (if it's not possible to open 'My Collars' screen) → if a user passes collar onboarding at once (w/o restoring);My Map screen → if a user passes collar onboarding after restoring the progress. | - | - |
| ME21-US14-AC15 | M200 Suggestion to add Halo Beacon after the first collar addition should be deleted. |  |  |
