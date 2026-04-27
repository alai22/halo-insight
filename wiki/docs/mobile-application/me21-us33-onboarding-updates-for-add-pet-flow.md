---
title: "ME21-US33. Onboarding: Updates for 'Add Pet' flow"
sidebar_label: "ME21-US33. Onboarding: Updates for 'Add Pet' flow"
sidebar_position: 270
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Timofey Burak [X] Dmitry Kravchuk Yekaterina Hovin |
| Click here to expand... HALO-14141 - MOB: ME21-US33. Onboarding: Updates for 'Add Pet' flow Closed |
| Click here to expand... |# Contents

User story Acceptance criteria 'Assign Your Halo Collar to Your Pet' screen 'Add Pet' screen Add a question mark icon

# User story

\> As a Halo business owner I want to have the screens for the 'Add Pet' flow updated so that they are ready to be included into the Onboarding flow.

# Acceptance criteria

| AC | Description | iOS screens designs | Android screens designs | AS IS | TO BE | Main flow | Onboarding flow | Main flow | Onboarding flow |
|---|---|---|---|---|---|---|---|---|---|
| 'Assign Your Halo Collar to Your Pet' screen |
| ME21-US33-AC01 | The title should be changed (changes are highlighted in blue):AS ISTO BEAssign Your Halo Collar to Your DogAssign Your Halo Collar to Your Pet | Assign Your Halo Collar to Your Dog | Assign Your Halo Collar to Your Pet | Link to Zeplin | Link to Zeplin |
| Assign Your Halo Collar to Your Dog | Assign Your Halo Collar to Your Pet |
| ME21-US33-AC02 | Entry points:a user tapped 'Next' on the 'Halo Collar Has Been Securely Added to Your Account' screen. |
| ME21-US33-AC03 | When a user taps on the 'Add Pet' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app navigates them to the 'Add Pet' screen. |
| 'Add Pet' screen |
| ME21-US33-AC04 | Main flowOnboarding flowWhen 'Add Pet' screen is opened from the app not within Onboarding flow (e.g. when a user adds a second pet), the app should display a 'Cancel' button (leave as is).'Cancel' button should be renamed to '\<' when 'Add Pet' screen is opened within Onboarding flow, which navigates a user to the "Assign Your Halo Collar to Your Pet" screen with video. | When 'Add Pet' screen is opened from the app not within Onboarding flow (e.g. when a user adds a second pet), the app should display a 'Cancel' button (leave as is). | 'Cancel' button should be renamed to '\<' when 'Add Pet' screen is opened within Onboarding flow, which navigates a user to the "Assign Your Halo Collar to Your Pet" screen with video. | Link to Zeplin | Link to Zeplin |
| When 'Add Pet' screen is opened from the app not within Onboarding flow (e.g. when a user adds a second pet), the app should display a 'Cancel' button (leave as is). | 'Cancel' button should be renamed to '\<' when 'Add Pet' screen is opened within Onboarding flow, which navigates a user to the "Assign Your Halo Collar to Your Pet" screen with video. |
| ME21-US33-AC05 | Main flowOnboarding flow'Done' button should remain as is.'Done' button should be renamed to the 'Next' button. | 'Done' button should remain as is. | 'Done' button should be renamed to the 'Next' button. |
| 'Done' button should remain as is. | 'Done' button should be renamed to the 'Next' button. |
| ME21-US33-AC06 | 'Next'/ 'Done' buttons should be moved to the bottom. |
| ME21-US33-AC07 | Content of this screen should be scrollable except the bottom part with the 'Next'/ 'Done' buttons. |
| ME21-US33-AC08 | When a user taps 'Next' button, then the app should:automatically assign previously added collar to the created pet (w/o/ displaying separate screens);navigate a user to the 'Connect Your Halo Collar' screen.Note 1: on tapping 'Done' the logic shouldn't be changed.Note 2: error handling will be implemented within a separate task [NI] ME21-US12. Onboarding: general requirements for exceptional and alternative cases. |
| Add a question mark icon |
| ME21-US33-AC09 | A question mark tappable icon should be displayed at the left upper corner on the following screens (both opened within the main flow and Onboarding):'Assign Your Halo Collar to Your Dog' screen;'Add Pet' screen. | - | - |
| ME21-US33-AC10 | When a user taps on a question mark icon, then the app should open the 'Need Help?' screen. | - | - |
