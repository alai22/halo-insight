---
title: "ME21-US70. Update 'progress bar'/top navigation bar displaying logic in FTUE Onboarding flow"
sidebar_label: "ME21-US70. Update 'progress bar'/top navigation bar displaying logic in FTUE Onboarding flow"
sidebar_position: 429
last_modified: "Jan 14, 2025"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Dmitry Kravchuk |
| HALO-20682 - MOB: ME21-US70. Update Progress bar within FTUE Onboarding flow Closed |
| 03 Jul 2024 the draft user story is created |Table of Contents

User story Acceptance criteria Interaction Design for "Info" Icon in Header Implementation notes

# User story

\> As a Halo app account owner I want to view the progress bar in FTUE (onboarding) flow so that I can understand how many steps left to complete the Onboarding.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| Progress bar updates |
| ME21-US70-AC01 | The progress bar should be added to the following FTUE Onboarding steps: Tell Us About YourselfEnable Permissions Add CollarAdd Pet Set up Wi-FiCongratulationsNote 1: modal windows will be shown without progress bar due to tech restrictions, for instance: Pet Color, Pet Breed, etc.Note 2: it's ok if 'Enable Permissions' screen is shown without progress bar, in case the app is opened not first time and no permissions info are available. For instance: I installed the app → go through 3 steps of onboarding → remove the app → install it again → 'Enable Permissions' will be shown without Progress bar | See the new flow in Figma |
| ME21-US70-AC02 | FTUE Onboarding progress bar should consist of 5 segments. Tell Us About Yourself → 1st segmentEnable Permissions → 2nd segment Add Collar → 3rd segmentAdd Pet → 4th segment Set up Wi-Fi → 5th segmentCongratulations → no dedicated segment for this step (all segments should be shown as passed, see ME21-US70-AC04) | - |
| ME21-US70-AC03 | If FTUE Onboarding step is in progress, then the corresponding segment should be displayed in dark grey color. | - |
| ME21-US70-AC04 | If FTUE Onboarding step(s) is(are) passed , then the corresponding segment(s) should be displayed in yellow color. | - |
| ME21-US70-AC05 | If FTUE Onboarding step(s) hasn't been started, then the corresponding segment(s) should be displayed in light grey color. | - |
| 'Back' button updates |
| ME21-US70-AC06 | I should not be able to get back to previous step within the FTUE Onboarding flow except one case: from 'Adding Your Collar' step to 'Enable Permissions' step. | - |
| Questionmark icon UI updates |
| ME21-US70-AC07 | Questionmark icon color in Navigation bar should be changed from Blue to Black. Note: as of 8/7/2024 'tapping' effect color is in clarification with Ryan at the moment, see https://softeq.slack.com/archives/C01654HRD55/p1722696837813889?thread_ts=1721128400.001609&cid=C01654HRD55 | InfoNote for QA: as of 8/12/2024 the interaction is not implemented, the task will be done within. This task for now will be done for iOS only / for Onboarding flow only HALO-21030 - iOS: Add interaction Design for "Question mark" Icon in Navigation bar Closed . Android task added to FTUE Kaizen will be done later HALO-21031 - Android: Add interaction Design for "Question mark" Icon in Navigation bar (Onboarding) Open Interaction Design for "Info" Icon in HeaderDefault State:Color: Tundora #424242On Press:Instantly changes color to: Dodger Blue #2F93F3Opacity: 50%After 800ms Delay:Opacity transitions to: 100%Button Push State.mov |# Implementation notes

| IN | Description |
|---|---|
| ME21-IN70-AC01 | - |
