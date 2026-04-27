---
title: "(BL) ME01-US22. Update UI of Splash screen"
sidebar_label: "(BL) ME01-US22. Update UI of Splash screen"
sidebar_position: 174
last_modified: "Oct 04, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya, Timofey Burak [X], Pavel Leonenko, Nikita Krisko, Katherina Kaplina |
| HALO-9231 - MOB: Update UI design of Splash screen Closed |
| 22 Oct 2021 initial requirements were gathered by Nicolay Gavrilov26 Oct 2021 US is created by Galina Lonskaya02 Sep 2022 Maria Shikareva [X] Baselined the story (see ME01-F00. Run the app (splash, start, "app startup failed" screen)). |# User story

\> As Halo Collar app account owner, I want to view photo of the dog owner and the dog with Halo as Splash and Start screen so that I can imagine how Halo Collar system might change our life being with the dog.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME01-US22-AC01 | Splash screen should have updated UI. See the initial requirements in ME01-F00-AC01. | Pic 1 Splash screen | Android UI |
| ME01-US22-AC02 | Start screen with the spinner should have updated UI. See the initial requirements in ME01-F00-AC01. | Pic 2 Start screen + spinner | The same as for iOS |
| ME01-US22-AC03 | Start screen should have updated UI. See the initial requirements in ME01-F00-AC05. | Pic 3 Start screen + Sign Up + Log In buttonsiPhone SEiPhone X | Android UI |
| ME01-US22-AC04 | Start screen with Cancel button but without buttons should have updated UI. See the initial requirements in ME01-F00-AC05. Note: this screen is displayed after the user taps on Log in/Sign Up button. This behavior is valid only for iOS 11/12/13 и 14.0 + 14.1. | Pic 4 Start screen + Cancel button + Spinner | The same as for iOS |
| ME01-US22-AC05 | Assumption for Android: that photo frame can be not same as presented in ZeplinNote: Michael submitted that it is acceptable, see the email "Halo App Updated Splash Screen" (October 27, 2021) | - | - |
| ME01-US22-AC06 | The "selected" button should be displayed with yellow background (e.g.: "Sign Up" button on Pic 4). See the initial AC: ME01-F00-AC05 and ME01-F00-AC06 | - | - |
| ME01-US22-AC07 | The "unselected" button should be displayed with white background (e.g.: "Log In" button on Pic 4). See the initial AC: ME01-F00-AC05 and ME01-F00-AC06 | - | - |# Implementation Notes

| IN | Description |
|---|---|
| ME01-US22-IN01 | Large size of the photo is required for implementation on Android. See the large image: https://drive.google.com/drive/folders/1_1Xd0J3-JMVSFHbasn79EbRgJkL8b7H0 In case of any questions, please contact Margarita Yasinskaya |
