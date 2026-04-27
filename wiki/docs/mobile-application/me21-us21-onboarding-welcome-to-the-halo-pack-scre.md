---
title: "ME21-US21. Onboarding: 'Welcome to the Halo Pack!' screen with video"
sidebar_label: "ME21-US21. Onboarding: 'Welcome to the Halo Pack!' screen with video"
sidebar_position: 254
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Links to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] Maria Shikareva [X] Nikita Krisko Kirill Akulich Dmitry Kravchuk Valeria Malets Timofey Burak [X] Yekaterina Hovin |
| Click here to expand... HALO-12368 - iOS [Investigation]: Solution choice/check for video displaying within Onboarding Closed HALO-12439 - Android [Investigation]: Solution choice/check for video displaying within Onboarding Closed HALO-12996 - MOB: ME21-US21. Onboarding: 'Welcome to the Halo App' screen with video Closed HALO-13861 - BE: Add 'fake' links to the videos and thumbnails Closed |
| Click here to expand...23 Sep 2022 Maria Shikareva [X] Added several notes to ME21-US21-AC01, ME21-US21-AC05, ME21-US21-IN02, ME21-US21-IN03 for more clarity based on discussion with Dmitry Kravchuk during implementation.26 Sep 2022 Maria Shikareva [X] Updated designs based on new description provided within https://docs.google.com/document/d/16DOWa1CeR5cMOcFvRvYUVATa8Lqv4v4Bj3PtTbAOcsA/edit).27 Sep 2022 Maria Shikareva [X] Added ME21-US21-AC19 (missed requirement) + added link to Zeplin. |# Contents

User story Acceptance criteria 'Welcome to the Halo Pack!' screen Video: general requirements Error handling Google Analytics Implementation notes

# User story

\> As a Halo app user I want to be able to watch Onboarding videos so that to learn more about app functionality before making some settings and not to search info by myself.

# Acceptance criteria

See the link to the Miro board.

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| 'Welcome to the Halo Pack!' screen |
| ME21-US21-AC01 | Entry point: a user taps a 'Next' button on the 'Tell Us Your Name' screen.The app should display a 'Welcome to the Halo Pack!' screen with the following UI elements:'Back' button;'Welcome to the Halo Pack!' title;'Are you ready to change you and your dog's lives?' text;a video preview image in the video rectangle (if the video is not playing) with a 'Play' button;See details in the 'Video: general requirements' section below.See implementation details: ME21-US21-IN03.'Skip' button. | Link to Zeplin | Link to Zeplin |
| ME21-US21-AC19 | If a video preview image isn't available (cannot be retrieved from BE), then the app should display a placeholder image. | Link to Zeplin | Link to Zeplin |
| ME21-US21-AC02 | The link to video: TBDNote: see an implementation note ME21-US21-IN01 below. | - | - |
| ME21-US21-AC03 | When a user taps on the 'Back' button, then the app should display a 'Tell Us Your Name' screen. | - | - |
| ME21-US21-AC04 | When a user taps on the area with the video, then the app should start playing the video in a full-screen mode.Note: see ME21-US21-IN01 below. | Native iOS player | Native Android player |
| ME21-US21-AC05 | The app should track whether the user watched the video till the end.BA note: if a user just scrolled the video till the end, the app will also consider this case as watching till the end.Note: if a user watched till the end, then on next opening the app should show the video from the beginning. But the progress should be tracked as 100% completed (because previously a user watched till the end) | - | - |
| ME21-US21-AC06 | Precondition: a user watched the video till the end.When a user taps a 'Close' button on the video OR enters 'Welcome to the Halo Pack!' screen again, then the app should display 'Next' button visible and enabled.BA note: we're hiding the button first to force the user to see an important video.For future improvement if required: the app can automatically close the video when it ends. | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US21-AC07 | When a user taps on the 'Next' button, then the app should display a 'Support explanation' screen. | - | - |
| ME21-US21-AC08 | Precondition: a user didn't watch the video till the end.When a user taps a 'Skip' button, then the app should display a M262 Please Watch the Video! message.BA: Update in Appendix 3 – Error, Success, Warning Messages (if required) | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US21-AC09 | Precondition: M262 Please Watch the Video! is displayed.When a user taps 'Watch the Video' button, then the app should:close the pop-up;open a full-screen video with the progress saved.Note: see an implementation note ME21-US21-IN02 below. | - | - |
| ME21-US21-AC10 | Precondition: M262 Please Watch the Video! is displayed.When a user taps 'Watch Later' button, then the app should:close the pop-up;display the next 'Support explanation' screen. | - | - |
| Video: general requirements |
| ME21-US21-AC10 | The system should use a standard player that is now used in the Halo app. | - | - |
| ME21-US21-AC11 | A user should be able to view the video in the album or portrait orientation. | - | - |
| ME21-US21-AC12 | A user should be able to pause and resume the video. | - | - |
| ME21-US21-AC13 | A user should be able to drag the slider to navigate to a specific moment in the video. | - | - |
| ME21-US21-AC14 | A user should be able to mute/ unmute the video. | - | - |
| ME21-US21-AC15 | The size of the video displaying should be customized so that all content should fit the screen.BA note: it's required because of devices with different width. | - | - |
| ME21-US21-AC16 | If the Internet connection is lost during video playing and then appear again, then the app should continue to play the video from where is stopped. | - | - |
| Error handling |
| ME21-US21-AC17 | ME14-F01 Unified errors handling mechanism should be applied. | - | - |
| Google Analytics |
| ME21-US21-AC18 | The app should track:user's progress for watching the video (in seconds and %);number of times user watched this video before reaching 100%;the platform.BA note: we've also discussed an option to add link to watched video and agreed that for the first iteration it's not necessary → we don't expect the video will be changed soon. Otherwise it's needed to check restrictions (e.g. number of symbols). | - | - |# Implementation notes

| ID | Description |
|---|---|
| ME21-US21-IN01 | The link should be stored on BE side.For implementation purposes we can start with a video for prompting screens without a real link. |
| ME21-US21-IN02 | The app will save the user's progress within the current session; if user kills the app, then the progress will be reset.Example: if another user logs in their own account on this device, the progress for previous user will be reset, the app should save the progress of the current user. |
| ME21-US21-IN03 | The picture should not be stretched, need to show it in the original size. |
