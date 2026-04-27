---
title: "(Native Apps) ME01-F00. App Launch (Splash Screen, Start Screen, Error Screen)"
sidebar_label: "(Native Apps) ME01-F00. App Launch (Splash Screen, Start Screen, Error Screen)"
sidebar_position: 491
author: "Galina Lonskaya"
---

Page info| Task owners | Link to JIRA Issue | Changes history |
|---|---|---|
|  |
| Click here to expand... |
|  |# Contents

User Story Acceptance criteria 'Application Startup Failed' screen Start screen with 'Sign Up' / 'Log In' buttons

# User Story

\> As Halo App Account Owner, I want the app to launch smoothly with clear feedback during the startup process, so that I understand that the app is loading and can be informed if something goes wrong.

# Acceptance criteria

| AC | Precondition | iOS UI design | Android UI design | Error handling during App Launch process |  | Preconditions |  | UI for the user | n/a | Displayed screen | IC (internet connection) | Communication with server | Cashed app configuration data | Logged out | 'Your Phone Has No Internet Connection' bar | 'Application Startup Failed' screen | 'Start' screen with 'Log In' / 'Sign Up' buttons | 'Application Startup Failed' screen | Start screen with 'Sign Up' / 'Log In' buttons |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME01-F00-AC01 | If I launch the app, then:the Splash screen without a spinner should be displayed first. | Figma | Android ≤ 11Android ≥ 12The system splash screen should be displayed. This is an automatically generated screen that appears when an app is launched on Android devices starting from version 12. The following elements only are under mob dev control: (1) App Icon, (2) Background Color, (3) Icon AnimationFigma Figma | Android ≤ 11 | Android ≥ 12The system splash screen should be displayed. This is an automatically generated screen that appears when an app is launched on Android devices starting from version 12. The following elements only are under mob dev control: (1) App Icon, (2) Background Color, (3) Icon Animation | Figma | Figma |
| Android ≤ 11 | Android ≥ 12The system splash screen should be displayed. This is an automatically generated screen that appears when an app is launched on Android devices starting from version 12. The following elements only are under mob dev control: (1) App Icon, (2) Background Color, (3) Icon Animation |
| Figma | Figma |
| ME01-F00-AC02 | A loading white spinner and 'Your backyard, now everywhere™' text should be displayed on the Splash screen when the time required to load and transition to the next screen exceeds 0.5 seconds. | Figma | Figma |
| ME01-F00-AC20 | If I launch the app and a mandatory update is required, then: 'Update is required' screen should be opened, see the details in ME14-F00 Mandatory app updates. | - | - |
| If the mandatory update is not required and an error happens during Halo app launch process, then see how the different errors should be handled in the following table: PreconditionsUI for the usern/aDisplayed screenIC (internet connection)Communication with serverCashed app configuration dataLogged out'Your Phone Has No Internet Connection' bar'Application Startup Failed' screen'Start' screen with 'Log In' / 'Sign Up' buttonsME01-F00-AC14n/aME01-F00-AC15n/anoME01-F00-AC16n/ayesME01-F00-AC17n/a | ME01-F00-AC14 |  |  |  | n/a |  |  |  | ME01-F00-AC15 |  | n/a |  | no |  |  |  | ME01-F00-AC16 |  | n/a |  | yes |  |  |  | ME01-F00-AC17 |  |  |  | n/a |  |  |  |
| ME01-F00-AC14 |  |  |  | n/a |  |  |  |
| ME01-F00-AC15 |  | n/a |  | no |  |  |  |
| ME01-F00-AC16 |  | n/a |  | yes |  |  |  |
| ME01-F00-AC17 |  |  |  | n/a |  |  |  |
| ME01-F00-AC03 | 'Application Startup Failed' screen should consist of:Image 'Application Startup Failed' screen title 'Your phone has no Internet access - please check your network settings. Halo is still protecting your pets!' text'Retry' button | Figma | Figma |
| ME01-F00-AC04 | Precondition: The App Startup Failed screen is displayed.If I tap on the Retry button and there is a connection error, then: M113 Network error standard message without 'Report Issue' button should be displayed. |
| ME01-F00-AC18 | Precondition: The App Startup Failed screen is displayed.If I tap on the Retry button and there is a communication error, then: M113 Network error standard message with 'Report Issue' button should be displayed.Note: See more details about the error in ME01-US24. Create a Zendesk ticket with logs when the user is unable to launch the app / log in. |
| ME01-F00-AC05 | Precondition: The App Startup Failed screen is displayed.If I tap on the Retry button and Internet connection is set, then:in accordance with the access rights 'Start' screen, 'Tell us About Yourself' or 'My Map' screen or other should be displayed. |
| ME01-F00-AC19 | Precondition: The App Startup Failed screen is displayed.If Internet connection is disappeared during I am staying on 'Application Startup Failed' screen, then: "Your Phone Has No Internet Connection" bar should be displayed on the screen. |
| ME01-US78-AC06 | Precondition: The Splash screen just has been displayed OR I tap on 'Retry' button on 'Application Startup Failed' screen and there is no connection/communication issue.If I haven't logged into the app using the downloaded/re-installed app at least once, then:the Start screen with the highlighted Sign Up button should be displayed. | Figma | Figma |
| ME01-F00-AC07 | Precondition: The Splash screen just has been displayed OR I tap on 'Retry' button on 'Application Startup Failed' screen and there is no connection/communication issue.If I have logged into the app using the downloaded app at least onceOR I have just re-installed the Halo collar app and at the moment of the app removal I was logged into the app, then:the Start screen with the highlighted Log In button should be displayed (i.e. auto-login should not be performed). | Figma | Figma |
| ME01-F00-AC08 | The "highlighted" Sign Up/Log In button should be displayed with white background. | - | - |
| ME01-F00-AC09 | The "not highlighted" Sign Up/Log In button should be displayed as a link without an underline and with bold text. | - | - |
| ME01-F00-AC13 | Android specific: "Start screen with Log in/Sign up options for foldable devices" should have specific 'Start' screen. Note: As of 8/9/24 1973 users who opened the app at least once used foldable devices (1.03% from all users). Samples of the most popular foldable devices among our users: SM-F946U, SM-F731U. The source: Firebase | n/a | Figma |
| ME01-F00-AC10 | When I tap 'Sign Up'/ 'Log In' button on the Start screen, the app should:iOS specific: display a Start screen with "Cancel" button but without buttonsThis behavior is valid only for iOS 11/12/13 и 14.0 + 14.1;perform actions described in ME01-F01. Sign Up (Create an account) → in case a user taps 'Sign Up' button;perform actions described in ME01-F04. Login → in case a user taps 'Log In' button. | Figma | n/a |
| ME01-F00-AC11 | iOS specifiс: If I tap 'Cancel' button, the app should:cancel log in/ sign up process;display the Start screen with Sign Up/Log In button. |
| ME01-F00-AC12 | IfI have logged into the app using the downloaded app at least onceAND I wasn't logged out previous timeANDthere is cashed app configuration data, THEN:The app should perform auto-login (see the cases in ME15-F00. View my map). | - | - |
