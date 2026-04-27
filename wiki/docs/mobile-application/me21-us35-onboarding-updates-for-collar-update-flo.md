---
title: "ME21-US35. Onboarding: Updates for 'Collar Update' flow"
sidebar_label: "ME21-US35. Onboarding: Updates for 'Collar Update' flow"
sidebar_position: 272
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Dmitry Kravchuk Timofey Burak [X] Yekaterina Hovin |
| Click here to expand... HALO-14143 - MOB: ME21-US35. Onboarding: Updates for 'Collar Update' flow Closed |
| Click here to expand... |# Contents

User story Acceptance criteria 'Halo Collar Updates' screen Wait for Your Collar to Update' screen 'Automatic Halo Collar Updates' screen Add a question mark icon

# User story

\> As a Halo business owner I want to have the screens for the 'Collar Update' flow updated so that they are ready to be included into the Onboarding flow.

# Acceptance criteria

| AC | Description | iOS screens designs | Android screens designs | Main flow | Onboarding flow | AS IS | TO BE | Main flow | Onboarding flow |
|---|---|---|---|---|---|---|---|---|---|
| 'Halo Collar Updates' screen |
| ME21-US35-AC01 | Entry points:a collar is successfully connected to Wi-Fi on the 'Connect Your Halo to Wi-Fi' screenORa user taps a 'Continue Without Wi-Fi' button on the 'Connect Your Halo to Wi-Fi' pop-up. | - | - |
| ME21-US35-AC02 | When a user taps a 'Check Updates' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should navigate a user to the Wait for Your Collar to Update' screen. | - | - |
| Wait for Your Collar to Update' screen |
| ME21-US35-AC03 | Main flowOnboarding flowNo button should be displayed (leave as is).BA note: we don't want to add this button to the main flow because we don't allow a user to skip this flow.A '\<' button should be added to the screen only for Onboarding flow, which navigates a user to the "Halo Collar Updates" screen with video. | No button should be displayed (leave as is).BA note: we don't want to add this button to the main flow because we don't allow a user to skip this flow. | A '\<' button should be added to the screen only for Onboarding flow, which navigates a user to the "Halo Collar Updates" screen with video. | - | - |
| No button should be displayed (leave as is).BA note: we don't want to add this button to the main flow because we don't allow a user to skip this flow. | A '\<' button should be added to the screen only for Onboarding flow, which navigates a user to the "Halo Collar Updates" screen with video. |
| 'Automatic Halo Collar Updates' screen |
| ME21-US35-AC04 | The text on the screen should be changed (updates are highlighted in blue):AS ISTO BEAutomatic Collar Updates usually occur at night and take several minutes to complete. Once the Satellite Position Data and Collar Updates are 'Up-To-Date', tap 'Done'.Automatic Collar Updates usually occur at night and take several minutes to complete. Once the Satellite Position Data and Collar Updates are 'Up-To-Date', tap 'Next'. | Automatic Collar Updates usually occur at night and take several minutes to complete. Once the Satellite Position Data and Collar Updates are 'Up-To-Date', tap 'Done'. | Automatic Collar Updates usually occur at night and take several minutes to complete. Once the Satellite Position Data and Collar Updates are 'Up-To-Date', tap 'Next'. | - | - |
| Automatic Collar Updates usually occur at night and take several minutes to complete. Once the Satellite Position Data and Collar Updates are 'Up-To-Date', tap 'Done'. | Automatic Collar Updates usually occur at night and take several minutes to complete. Once the Satellite Position Data and Collar Updates are 'Up-To-Date', tap 'Next'. |
| ME21-US35-AC05 | Main flowOnboarding flow'Done' button should remain as is.'Done' button should be renamed to the 'Next' button. | 'Done' button should remain as is. | 'Done' button should be renamed to the 'Next' button. |
| 'Done' button should remain as is. | 'Done' button should be renamed to the 'Next' button. |
| ME21-US35-AC06 | Precondition: a user tapped 'Next'/ 'Skip' button.When a user taps 'Ok' in the pop-up M260 OR 'Update Collar Later' in M259 Continue Without Update, then the app should navigate a user to the 'Halo Collar GPS' screen.Note: on tapping 'Done' the logic shouldn't be changed. |
| Add a question mark icon |
| ME21-US35-AC07 | A question mark tappable icon should be displayed at the left upper corner on the following Onboarding screens:'Halo Collar Updates' screen;'Wait For Your Collar to Update' screen;'Automatic Halo Collar Updates' screen. | - | - |
| ME21-US35-AC08 | When a user taps on a question mark icon, then the app should open the 'Need Help?' screen. | - | - |
