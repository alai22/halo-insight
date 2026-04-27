---
title: "ME21-US36. Onboarding: Updates for 'GPS Initialization' flow"
sidebar_label: "ME21-US36. Onboarding: Updates for 'GPS Initialization' flow"
sidebar_position: 273
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Dmitry Kravchuk Timofey Burak [X] Yekaterina Hovin |
| Click here to expand... HALO-14144 - MOB: ME21-US36. Onboarding: Updates for 'GPS Initialization' flow Closed |
| Click here to expand... |# Contents

User story Acceptance criteria 'Halo Collar GPS' screen 'Initialize Your Collar's GPS' screen 'Initialize Collar's GPS' screen Add a question mark icon

# User story

\> As a Halo business owner I want to have the screens for the 'GPS Initialization' flow updated so that they are ready to be included into the Onboarding flow.

# Acceptance criteria

| AC | Description | iOS screens designs | Android screens designs | Main flow | Onboarding flow | Main flow | Onboarding flow |
|---|---|---|---|---|---|---|---|
| 'Halo Collar GPS' screen |
| ME21-US36-AC01 | Entry points:a user taps on the 'Next' button on the 'Automatic Halo Collar Updates' screenORa user taps a 'Update Collar Later' button on M259 Continue Without Update. | Link to Zeplin | Link to Zeplin |
| ME21-US36-AC02 | When a user taps a 'Initialize Collar's GPS' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should navigate a user to the 'Initialize Your Collar's GPS' screen. |
| 'Initialize Your Collar's GPS' screen |
| ME21-US36-AC03 | Main flowOnboarding flowNo button should be displayed (leave as is).BA note: we don't want to add this button to the main flow because we don't allow a user to skip this flow.A '\<' button should be added to the screen only for Onboarding flow, which navigates a user to the "Halo Collar GPS" screen with video. | No button should be displayed (leave as is).BA note: we don't want to add this button to the main flow because we don't allow a user to skip this flow. | A '\<' button should be added to the screen only for Onboarding flow, which navigates a user to the "Halo Collar GPS" screen with video. | Link to Zeplin | - |
| No button should be displayed (leave as is).BA note: we don't want to add this button to the main flow because we don't allow a user to skip this flow. | A '\<' button should be added to the screen only for Onboarding flow, which navigates a user to the "Halo Collar GPS" screen with video. |
| 'Initialize Collar's GPS' screen |
| ME21-US36-AC04 | Main flowOnboarding flow'Done' button should remain as is.'Done' button should be renamed to the 'Next' button. | 'Done' button should remain as is. | 'Done' button should be renamed to the 'Next' button. |  | - |
| 'Done' button should remain as is. | 'Done' button should be renamed to the 'Next' button. |
| ME21-US36-AC05 | When a user taps 'Next' button OR 'Skip Initialization for now', then the app should navigate a user to the 'Beacons' screen.Note: on tapping 'Done' the logic shouldn't be changed. |
| Add a question mark icon |
| ME21-US36-AC06 | A question mark tappable icon should be displayed at the left upper corner on the following screens (both opened within the main flow and Onboarding):'Halo Collar GPS' screen;'Initialize Your Collar's GPS' screen;'GPS Light Signals' screen;'Initialize Collar's GPS' screen. | - | - |
| ME21-US36-AC07 | When a user taps on a question mark icon, then the app should open the 'Need Help?' screen. | - | - |
