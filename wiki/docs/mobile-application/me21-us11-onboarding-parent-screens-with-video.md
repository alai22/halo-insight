---
title: "ME21-US11. Onboarding: parent screens with video"
sidebar_label: "ME21-US11. Onboarding: parent screens with video"
sidebar_position: 241
last_modified: "Jun 25, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owner | Links to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] Maria Shikareva [X] Nikita Krisko Kirill Akulich Dmitry Kravchuk Valeria Malets Timofey Burak [X] |
| Click here to expand... HALO-12368 - iOS [Investigation]: Solution choice/check for video displaying within Onboarding Closed HALO-12439 - Android [Investigation]: Solution choice/check for video displaying within Onboarding Closed HALO-12561 - MOB+BE: ME21-US11. Onboarding: parent screens with video Closed HALO-13035 - QA: ME21-US20. Onboarding: stepper on the parent screens Closed HALO-13037 - MOB [NT]: ME21-US22. Onboarding: Implement video controls Closed HALO-13861 - BE: Add 'fake' links to the videos and thumbnails Closed Ballpark: Adding additional videos will increase the origin estimate on 2 SP. |
| Click here to expand...26 Sep 2022 Maria Shikareva [X] Updated designs based on comments in https://docs.google.com/document/d/16DOWa1CeR5cMOcFvRvYUVATa8Lqv4v4Bj3PtTbAOcsA/edit#. 04 Oct 2022, 05 Oct 2022 Maria Shikareva [X] Corrected texts to match designs.26 Oct 2022 Maria Shikareva [X] Added a Jira link. |# Contents

User story Acceptance criteria General requirements Videos for 'Setup the Collar' flow 'Stepper' changes 'What's in Your Halo Collar Kit' screen 'Power Up & Connect' screen 'Assign Your Halo Collar to Your Dog' screen 'Connect Your Halo Collar' screen 'Halo Collar Updates' screen 'Halo Collar GPS' screen 'Beacons' screen Implementation notes

# User story

\> As a Halo app user I want to be able to watch Onboarding videos so that to learn more about app functionality before making some settings and not to search info by myself.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | Step | Step name | Screen name | 'What's in Your Halo Collar Kit' screen |
|---|---|---|---|---|---|---|---|
| General requirements |
| ME21-US11-AC01 | New screens with video for 'Setup the Collar' flow should be added to the Onboarding flow:What's in Your Halo Collar Kit;Power Up & Connect;Assign Your Halo Collar to Your Dog;Connect Your Halo Collar;Halo Collar Updates;Halo Collar GPS;Beacons. | - | - |
| ME21-US11-AC02 | ME14-F01 Unified errors handling mechanism should be applied. | - | - |
| ME21-US11-AC03 | When a user taps on the area with the video, then the app should start playing the video in a full-screen mode (see the requirements in Video: general requirements). | - | - |
| ME21-US11-AC04 | The app should track whether the user watched the video till the end.BA note: if a user just scrolled the video till the end, the app will also consider this case as watching till the end.Note: The app will save the user's progress within the current session; if user kills the app, then the progress will be reset. | - | - |
| ME21-US11-AC05 | On every screen with video the app should display a 'Skip' button when the user didn't watch the video till the end. | - | - |
| ME21-US11-AC06 | When a user taps a 'Skip' button, then the app should display a M262 Please Watch the Video! message. | - | - |
| ME21-US11-AC07 | Precondition: M262 Please Watch the Video! is displayed.When a user taps 'Watch the Video' button, then the app should:close the pop-up;open a full-screen video with the progress saved. | - | - |
| ME21-US11-AC08 | Precondition: M262 Please Watch the Video! is displayed.When a user taps 'Watch Later' button, then the app should:close the pop-up;display the screen described in ACs below specific for each video screen. | - | - |
| Videos for 'Setup the Collar' flow |
| 'Stepper' changes |
| ME21-US11-AC09 | The stepper should be changed to the following (see stepper requirements here: ME21-US20. Onboarding: stepper on the parent screens):StepStep nameScreen name1Collar UnboxingWhat's in Your Halo Collar Kit2Add CollarPower Up & Connect3Add PetAssign Your Halo Collar to Your Dog4Wi-Fi SetupConnect Your Halo Collar5Collar UpdateHalo Collar Updates6GPS InitializationHalo Collar GPS7Add BeaconBeacons | 1 | Collar Unboxing | What's in Your Halo Collar Kit | 2 | Add Collar | Power Up & Connect | 3 | Add Pet | Assign Your Halo Collar to Your Dog | 4 | Wi-Fi Setup | Connect Your Halo Collar | 5 | Collar Update | Halo Collar Updates | 6 | GPS Initialization | Halo Collar GPS | 7 | Add Beacon | Beacons | - | - |
| 1 | Collar Unboxing | What's in Your Halo Collar Kit |
| 2 | Add Collar | Power Up & Connect |
| 3 | Add Pet | Assign Your Halo Collar to Your Dog |
| 4 | Wi-Fi Setup | Connect Your Halo Collar |
| 5 | Collar Update | Halo Collar Updates |
| 6 | GPS Initialization | Halo Collar GPS |
| 7 | Add Beacon | Beacons |
| ME21-US11-AC10 | Preconditions: a user tapped 'Next' on the 'Let's Get Started' screenORa user tapped 'Watch Later' button in the M262 Please Watch the Video! on the 'Let's Get Started' screen.The app should display a 'What's in Your Halo Collar Kit' screen with the following UI elements:a stepper (see the requirements in [NI] ME21-US20. Onboarding: stepper on the parent screens and ME21-US11-AC09 above);an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'What's in Your Halo Collar Kit' title;'Let’s open up your Halo Collar kits and see what’s inside.' text;a video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Next' button (see ME21-US11-AC05). | Link to Zeplin | Link to Zeplin |
| ME21-US11-AC11 | When a user taps a 'Next' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should navigate user to the 'Power Up & Connect' screen (see requirements below). | - | - |
| ME21-US11-AC12 | The link to video: TBD | - | - |
| 'Power Up & Connect' screen |
| ME21-US11-AC13 | Entry point: a user taps 'Next' on the 'What's in Your Halo Collar Kit' screenORa user tapped 'Watch Later' button in the M262 Please Watch the Video! on the 'What's in Your Halo Collar Kit' screen.The app should display a 'Power Up & Connect' screen with the following UI elements:a stepper (see the requirements in [NI] ME21-US20. Onboarding: stepper on the parent screens and ME21-US11-AC09 above);an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'Power Up & Connect' title;'Learn how to charge your Halo Collar and connect to your Halo Account. Please DO NOT assemble your Halo Collar or put the collar on your dog yet.' text;a video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Add Collar' button (see ME21-US11-AC05). | Link to Zeplin | Link to Zeplin |
| ME21-US11-AC14 | When a user taps a 'Add Collar' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should perform actions as described in [NI] ME21-US25. Onboarding: Charge Your Halo Collar. | - | - |
| ME21-US11-AC15 | The link to video: TBD | - | - |
| 'Assign Your Halo Collar to Your Dog' screen |
| ME21-US11-AC16 | Entry point: a user taps an 'Ok' button in M180 SIM card activation time warning on the 'Halo Collar Has Been Securely Added to Your Account' screen.The app should display a 'Assign Your Halo Collar to Your Dog' screen with the following UI elements:a stepper (see the requirements in [NI] ME21-US20. Onboarding: stepper on the parent screens and ME21-US11-AC above);an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'Assign Your Halo Collar to Your Dog' title;'Create your dog’s profile.' text;a video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Add Pet' button (see ME21-US11-AC05). | Link to Zeplin | Link to Zeplin |
| ME21-US11-AC17 | When a user taps an 'Add Pet' OR 'Watch Later' button in the M262 Please Watch the Video!, the the app should perform actions as described in ME21-US15. Assign pet. | - | - |
| ME21-US11-AC18 | The link to video: TBD | - | - |
| 'Connect Your Halo Collar' screen |
| ME21-US11-AC19 | Entry point: a user taps a 'Done' button on the 'Add Pet' screen.The app should display a 'Connect Your Halo Collar' screen with the following UI elements:a stepper (see the requirements in [NI] ME21-US20. Onboarding: stepper on the parent screens and ME21-US11-AC09 above);an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'Connect Your Halo Collar' title;'Understand Bluetooth, Wi-Fi and Cellular Connections.' text;a video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Setup Wi-Fi' button (see ME21-US11-AC05). | Link to Zeplin | Link to Zeplin |
| ME21-US11-AC20 | When a user taps a 'Setup Wi-Fi' button OR 'Watch Later' button in the M262 Please Watch the Video!, the the app should perform actions as described in ME03-F03. Collar Wi-Fi setup. | - | - |
| ME21-US11-AC21 | The link to video: TBD | - | - |
| 'Halo Collar Updates' screen |
| ME21-US11-AC22 | Entry point: a collar is successfully connected to Wi-Fi on the 'Connect Your Halo to Wi-Fi' screenORa user taps a 'Continue Without Wi-Fi' button on the 'Connect Your Halo to Wi-Fi' pop-up.The app should display a 'Halo Collar Updates' screen with the following UI elements:a stepper (see the requirements in [NI] ME21-US20. Onboarding: stepper on the parent screens and ME21-US11-AC09 above);an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'Halo Collar Updates' title;'Your collar will stay up to date with a few simple steps.' text;a video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Check Updates' button (see ME21-US11-AC05). | Link to Zeplin | Link to Zeplin |
| ME21-US11-AC23 | When a user taps a 'Check Updates' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should perform actions as described in [NI] ME21-US07. Add FW update screens to 'Add Collar' flow. | - | - |
| ME21-US11-AC24 | The link to video: TBD | - | - |
| 'Halo Collar GPS' screen |
| ME21-US11-AC25 | Entry point: a user taps on the 'Done' button on the 'Halo Collar Updates' screenORa user taps a 'Update Collar Later' button on the 'Continue Without Update' pop-up.The app should display a 'Halo Collar GPS' screen with the following UI elements:a stepper (see the requirements in [NI] ME21-US20. Onboarding: stepper on the parent screens and ME21-US11-AC09 above);an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'Halo Collar GPS' title;'Learn very important information about your Halo Collar’s GPS.' texta video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Initialize Collar's GPS' button (see ME21-US11-AC05). | Link to Zeplin | Link to Zeplin |
| ME21-US11-AC26 | When a user taps a 'Initialize Collar's GPS' button OR 'Watch Later' button in the M262 Please Watch the Video!, the the app should perform actions as described in [BL] ME03-US85. Collar Details: GPS Signal Level Settings. | - | - |
| ME21-US11-AC27 | The link to video: TBD | - | - |
| 'Beacons' screen |
| ME21-US11-AC28 | Precondition: a user tapped 'Done' or 'Skip Initialization for Now' buttons on the 'Initialize Collar's GPS' screenThe app should display a 'Beacons' screen with the following UI elements:an info icon (see the requirements in [Not impl.] ME21-US16. Onboarding: Questionmark icon requirements);'Beacons' title;'What is a Halo Beacon?' text;a video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Add Beacon' button (see ME21-US28-AC04 — ME21-US28-AC07). | Link to Zeplin | Link to Zeplin |
| ME21-US11-AC29 | If a user watched the video till the end, the app should display a 'Beacons' screen with an 'Add Beacon' button instead of a 'Skip'. |
| ME21-US11-AC30 | When a user taps a 'Add Beacon' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should navigate user to the 'Make Sure The Halo Beacon Is Turned On' screen for the Halo Indoor Beacon model.Note: in an existing flow the app shows a 'Select Beacon Model...' screen, where a user can select one of 3 options. But in Halo Kit only Halo indoor Beacon is included and only this beacon model is required for Trainings, therefor the app should skip that screen and select 'Halo Indoor Beacon' model for the user automatically. |
| ME21-US11-AC31 | The link to video: TBD |  |  |# Implementation notes

| ID | Description |
|---|---|
| ME21-US11-IN01 | The link should be stored on BE side.For implementation purposes we can start with a video for prompting screens without a real link. |
