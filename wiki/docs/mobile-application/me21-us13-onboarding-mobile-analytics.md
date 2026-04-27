---
title: "ME21-US13. Onboarding: mobile analytics"
sidebar_label: "ME21-US13. Onboarding: mobile analytics"
sidebar_position: 243
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to Jira issues | Changes history |
|---|---|---|---|
| APPROVED (SQ) |
| Maria Shikareva [X] Dmitry Kravchuk Siarhei Leushunou [X] Katherina Kaplina |
| HALO-12563 - MOB: ME21-US13. Onboarding: mobile analytics Closed HALO-14603 - MOB [NT]: Finalize solution for Onboarding: mobile analytics Closed Ballpark: MOB: 3-5SPSolution finalization: 1 SPQA: it's better to test this task separately within small parts (to be discussed during refinement) |
| Click here to expand...17 Nov 2022 Maria Shikareva [X]Added one more result for adding a beacon (how many users skipped adding beacon when trial expired) as discussed with Dmitry Komar [X] during implementation phase.Added a new parameter for a general metric "Onboarding_completed": we will track the total time for Onboarding and the time the user was in the app (the app wasn't folded). It'll help us understand how many users are distracted in the onboarding process.26 Dec 2022 Maria Shikareva [X] Marked the story as implemented.Added events name to the table below. |# Contents

General description Restrictions Acceptance criteria Events to be added General metrics Support Steps completing Already added events Steps completing

# General description

We need to have some metrics about Onboarding flow saved so that to be able analyze after feature release whether it helped us to solve business needs and help the company to meet the goals (see more details here: ME21. FTUE (previously 'App User Onboarding')).

# Restrictions

There's a limit of 500 events.

As of 27 Oct 2022 there are 57 events in Firebase (prod).

# Acceptance criteria

The app should track the following events and the platform:

https://analytics.google.com/analytics/web/#/p238385023/reports/explorer?params=_u..nav%3Dmaui%26_u.comparisonOption%3Ddisabled%26_u.date00%3D20220901%26_u.date01%3D20220928%26_r.explorerCard..selmet%3D%5B%22eventCount%22%5D%26_r.explorerCard..seldim%3D%5B%22eventName%22%5D%26_r.explorerCard..startRow%3D0&r=top-events&collectionId=app

| Metrics category | What should be tracked? | Status | Event name | Events to be added | General metrics | Support | Steps completing | Already added events | Steps completing |
|---|---|---|---|---|---|---|---|---|---|
| 1 | How many users completed the Onboarding (=passed the last screen: made some choice on the 'Start Training' screen/ moved next from the 'The Halo Collar App' screen)BA note: the event will be sent only in case Onboarding screen was shown in the app (the event for all existing users with a 'Onboarding completed' flag set on BE side will not be sent).From which user's choice it was done:has_collar ('I have my Halo Collar');waiting ('I am waiting for my Halo Collar');no_collar ('I'm considering joining the Halo Pack');How much time (in seconds) is required for a user to finish Onboarding (time from the first step to the passing the last one):First screen: 'Welcome to the Halo Pack!"For analytics purposes we'd like to count 'Welcome to the Pack!' screen as a first one - because 'Tell Us Your Name' screen already exist in the account and there's no interest in analyzing people's behavior on this screen -Last screen: depending on user's choice ('Start Training'/ 'The Halo Collar App').If a user left the app during Onboarding/ folded the app: this time should not be excluded from the total time (onboarding total);the app should also track the time the app was in the foreground (onboarding live).BA note 1: if a user started Onboarding from one device and then proceeded on another, we will only track analytics on the device on which the Onboarding was completed.BA note 2: if the app is deleted, timestamp of entering the specific screen will also be deleted. | NOT STARTED | ios_onboarding_completedHasCollarWaitingNoCollarandroid_onboarding_completedHasCollarWaitingNoCollar |
| 2 | How many unique users tapped on a question mark on every screen (i.e. one event for 1 user, even if a user taps 10 times on this icon on one screen).Implementation note: this will be one event with a parameter \<screen name\> sent at the moment of tapping. | NOT STARTED | ios_question_mark_tappedandroid_question_mark_tapped |
| 3 | Beacon addinghow many users skipped adding beaconhow many users completed adding beaconhow many users skipped adding beacon because their trial expiredhow much time a user spends on this flow (from 'Activate Your Halo Indoor Beacon' screen to to tapping 'Done' button OR skipping)was beacon adding initiated within Onboarding or not | NOT STARTED | ios_add_beaconCompletedSkippedandroid_add_beaconCompletedSkipped |
| 4 | User traininghow many users skipped starting traininghow many users moved to starting training | NOT STARTED | ios_onboarding_user_trainingNotNowTrainingandroid_onboarding_user_training |
| 5 | How much time is required for a user to successfully complete the following steps:Add Collar (from 'Charge Your Halo Collar' screen to tapping 'Done' button). | NOT STARTED | ios_add_collarandroid_add_collar |
| 6 | GPS initializationhow many users skip initialization stephow many users complete the initializationhow much time a user spends on the flow (from 'Initialize Your Collar's GPS' screen to tapping 'Done' button OR skipping). | PARTIALLY ADDED | ios_collar_calibrationCompletedSkippedandroid_collar_calibrationCompletedSkipped |
| 7 | Collar Update (these events are added but it's better to change their structure, see mobile development notes in the comments below)how many users skipped the flow (by tapping 'Update Collar Later' button)how many users completed the flow (by tapping 'Done' button)how much time a user spends on the flow (from 'Wait for Your...' till 'Done'/ 'Skip') (in seconds) | IN PROGRESS HALO-12560 - MOB [+BE]: ME21-US07. Add FW update screens to 'Add Collar' flow Closed | ios_collar_updateCompletedSkippedandroid_collar_updateCompletedSkipped |
| 8 | Wi-Fi setuphow many users skipped Wi-Fi setup stephow many users completed Wi-Fi setup stephow much time a user spends on this flow (from 'Connect Your Halo to Wi-Fi' screen to leaving this screen) | ADDED | ios_wi_fi_setup_summarySuccessCanceledSkippedandroid_wi_fi_setup_summarySuccessCanceledSkippedTo understand how much time a user spends to successfully setup Wi-Fi, use https://datastudio.google.com/reporting/9ec1b3d7-0f59-4a6e-8ff8-74d1a84ea40f/page/nYD7C |
| 9 | Video watchinguser's progress for watching the video (in seconds and %)number of times user watched this video before reaching 100%BA note: the event is sent when a user leaves the screen. | IN PROGRESS | ios_video_views_statisticsandroid_video_views_statistics |
