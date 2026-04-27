---
title: "ME21-US28. Onboarding: video screens (User Choice + App Tour)"
sidebar_label: "ME21-US28. Onboarding: video screens (User Choice + App Tour)"
sidebar_position: 264
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Links to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] Maria Shikareva [X] Nikita Krisko Kirill Akulich Dmitry Kravchuk Valeria Malets Timofey Burak [X] Yekaterina Hovin |
| Click here to expand... HALO-13848 - MOB: ME21-US28. Onboarding: video screens (User Choice + App Tour) Closed HALO-13861 - BE: Add 'fake' links to the videos and thumbnails Closed |
| Click here to expand...26 Sep 2022 Maria Shikareva [X] Updated designs based on comments within https://docs.google.com/document/d/16DOWa1CeR5cMOcFvRvYUVATa8Lqv4v4Bj3PtTbAOcsA/edit#heading=h.68945tgskl1e.04 Oct 2022, 05 Oct 2022 Maria Shikareva [X] Corrected incorrect navigation in ME21-US28-AC25, ME21-US28-AC26. |# Contents

User story Acceptance criteria General requirements Videos for setting up expectations Let's Get Started Let's Get a Head Start Why Halo Collar? Video about the app 'Tour of the Halo Collar App' screen Google Analytics Implementation notes

# User story

\> As a Halo app user I want to be able to watch Onboarding videos so that to learn more about app functionality before making some settings and not to search info by myself.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | Let's Get Started | Let's Get a Head Start | 'Tour of the Halo Collar App' screen | Entry point | Screen to navigate |
|---|---|---|---|---|---|---|---|---|
| General requirements |
| ME21-US28-AC01 | New screens with video should be added to the Onboarding flow:Videos for setting up expectationsLet's Get Started (for members who have Halo Collar);Let's Get a Head Start (for members who are waiting for the collar);Why Halo Collar? (for members who are considering joining).Video about the app:Tour of the Halo Collar App. | - | - |
| ME21-US28-AC02 | ME14-F01 Unified errors handling mechanism should be applied. | - | - |
| ME21-US28-AC03 | When a user taps on the area with the video, then the app should start playing the video in a full-screen mode (see the requirements in Video: general requirements). |  |  |
| ME21-US28-AC04 | The app should track whether the user watched the video till the end.BA note: if a user just scrolled the video till the end, the app will also consider this case as watching till the end.Note: The app will save the user's progress within the current session; if user kills the app, then the progress will be reset. |  |  |
| ME21-US28-AC05 | On every screen with video the app should display a 'Skip' button when the user didn't watch the video till the end. |  |  |
| ME21-US28-AC06 | When a user taps a 'Skip' button, then the app should display a M262 Please Watch the Video! message. |  |  |
| ME21-US28-AC07 | Precondition: M262 Please Watch the Video! is displayed.When a user taps 'Watch the Video' button, then the app should:close the pop-up;open a full-screen video with the progress saved. |  |  |
| ME21-US28-AC08 | Precondition: M262 Please Watch the Video! is displayed.When a user taps 'Watch Later' button, then the app should:close the pop-up;display the screen described in ACs below specific for each video screen. |  |  |
| Videos for setting up expectations |
| ME21-US28-AC09 | Precondition: a user selected an 'I have my Halo Collar' option and tapped 'Next' on the 'Do You Have a Halo Collar?' screen.The app should display a 'Let's Get Started' screen with the following UI elements:'Back' button;an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'Let's Get Started' title;'Review the steps to get your Halo Collar up and running." texta video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Start' button (see ME21-US28-AC06). | Link to Zeplin | - |
| ME21-US28-AC10 | When a user taps a 'Back' button, then the app should navigate user to the 'Do You Have a Halo Collar?' screen. | - | - |
| ME21-US28-AC11 | If a user watched the video till the end, the app should display a 'Let's Get Started' screen with a 'Start' button instead of a 'Skip'. |  |  |
| ME21-US28-AC12 | When a user taps a 'Start' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should navigate user to the 'What's in Your Halo Collar Kit' screen. | - | - |
| ME21-US28-AC13 | The link to video: TBD |  |  |
| ME21-US28-AC14 | Precondition: a user selected an 'I'm waiting for my Halo Collar' and tapped 'Next' on the 'Do You Have a Halo Collar?' screen.The app should display a "Let's Get a Head Start" screen with the following UI elements:'Back' button;an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'Let's Get a Head Start' title;'Learn how you can get started today.' text;a video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Start' button (see ME21-US28-AC06). | Link to Zeplin |  |
| ME21-US28-AC15 | When a user taps a 'Back' button, then the app should navigate user to the 'Do You Have a Halo Collar?' screen. | - |  |
| ME21-US28-AC16 | If a user watched the video till the end, the app should display a 'Let's Get a Head Start' screen with a 'Start' button instead of a 'Skip'. |  |  |
| ME21-US28-AC17 | When a user taps a 'Start' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should navigate user to the 'Tour to the Halo Collar App' screen (see requirements below). | - | - |
| ME21-US28-AC18 | The link to video: TBD | - | - |
| Why Halo Collar? |
| ME21-US28-AC19 | Precondition: a user selected an 'I'm considering joining the Halo Pack' option and tapped 'Next' on the 'Do You Have a Halo Collar?' screen.The app should display a "Why Halo Collar?" screen with the following UI elements:'Back' button;an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'Why Halo Collar?' title;'Give an overview of Halo to people who select that they are just exploring the app.' text;a video preview image in the video rectangle (if the video is not playing);'Join Halo Pack' button;'Skip' OR 'Join Halo Pack' button (see ME21-US28-AC06);'Next' button → visible and enabled only together with the 'Join Halo Pack' button. | Link to Zeplin |  |
| ME21-US28-AC20 | When a user taps a 'Back' button, then the app should navigate user to the 'Do You Have a Halo Collar?' screen. | - | - |
| ME21-US28-AC21 | If a user watched the video till the end OR taps a 'Watch Later' button in the M262 Please Watch the Video!, the app should display a 'Why Halo Collar?' screen with a 'Join Halo Pack' and 'Next' buttons instead of a 'Skip'. |  |  |
| ME21-US28-AC22 | When a user taps a 'Next' button, then the app should navigate user to the 'Tour to the Halo Collar App' screen (see requirements below). | - | - |
| ME21-US28-AC23 | When a user taps a 'Join Halo Pack' button, then the app should navigate the user to halocollar.com. |  |  |
| ME21-US28-AC24 | The link to video: TBD | - | - |
| Video about the app |
| ME21-US28-AC25 | Entry point: a user taps a 'Start' button OR 'Watch Later' button in the M262 Please Watch the Video! on the 'Let's Get a Head Start' screen;ORa user taps a 'Next' button OR 'Watch Later' button in the M262 Please Watch the Video! on the 'Why Halo Collar?' screen;ORa user taps a 'Done' button on the 'Add Beacon' screen.The app should display a 'The Halo Collar App' screen with the following UI elements:an info icon (see the requirements in ME21-US16. Question mark icon requirements (related to Onboarding flow));'The Halo Collar App' title;'Take a tour of the Halo Collar App' text;a video preview image in the video rectangle (if the video is not playing);'Skip' OR 'Next' button (see ME21-US28-AC06). | Link to Zeplin |  |
| ME21-US28-AC26 | When a user taps an 'Next' OR 'Watch Later' button in the M262 Please Watch the Video! button, the the app should perform the following actions depending on the entry point:Entry pointScreen to navigatea user taps a 'Next' button OR 'Watch Later' button in the M262 Please Watch the Video! on the a 'Let's Get a Head Start' screen'Start Halo Training' screena user taps a 'Next' button OR 'Watch Later' button in the M262 Please Watch the Video! on the 'Why Halo Collar?' screen'My Map' screena user taps a 'Done' button on the 'Add Beacon' screen'Almost Ready' screen | a user taps a 'Next' button OR 'Watch Later' button in the M262 Please Watch the Video! on the a 'Let's Get a Head Start' screen | 'Start Halo Training' screen | a user taps a 'Next' button OR 'Watch Later' button in the M262 Please Watch the Video! on the 'Why Halo Collar?' screen | 'My Map' screen | a user taps a 'Done' button on the 'Add Beacon' screen | 'Almost Ready' screen |  |  |
| a user taps a 'Next' button OR 'Watch Later' button in the M262 Please Watch the Video! on the a 'Let's Get a Head Start' screen | 'Start Halo Training' screen |
| a user taps a 'Next' button OR 'Watch Later' button in the M262 Please Watch the Video! on the 'Why Halo Collar?' screen | 'My Map' screen |
| a user taps a 'Done' button on the 'Add Beacon' screen | 'Almost Ready' screen |
| ME21-US28-AC27 | The link to video: TBDNote: see an implementation note ME21-US28-IN01 below. |  |  |
| ME21-US28-AC28 | If the user watched this video during another flow (e.g. after Getting Started Early screen), the video screen should not be shown. |  |  |
| Google Analytics |
| ME21-US28-AC29 | The app should track:user's progress for watching the video (in seconds and %);number of times user watched this video before reaching 100%;the platform.BA note: we've also discussed an option to add link to watched video and agreed that for the first iteration it's not necessary → we don't expect the video will be changed soon. Otherwise it's needed to check restrictions (e.g. number of symbols). |  |  |# Implementation notes

| ID | Description |
|---|---|
| ME21-US28-IN01 | The link should be stored on BE side.For implementation purposes we can start with a video for prompting screens without a real link. |
