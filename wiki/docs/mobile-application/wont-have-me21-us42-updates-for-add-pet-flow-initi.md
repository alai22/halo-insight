---
title: "[Won't have] ME21-US42. Updates for 'Add Pet' flow (initiated within main flow)"
sidebar_label: "[Won't have] ME21-US42. Updates for 'Add Pet' flow (initiated within main flow)"
sidebar_position: 280
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Maria Shikareva [X] Timofey Burak [X] Dmitry Kravchuk Yekaterina Hovin |
| Click here to expand... |
| Click here to expand... |# Contents

User story Acceptance criteria 'Assign Your Halo Collar to Your Dog' screen 'Assign a Collar' screen 'Pair Collar With a Pet' screen Add a question mark icon

# User story

\> As a Halo business owner I want to have the screens for the 'Add Pet' flow updated so that they are ready to be included into the Onboarding flow.

# Acceptance criteria

| AC | Description | iOS screens designs | Android screens designs |
|---|---|---|---|
|  | It was agreed to change all parent screens to modal screens. |  |  |
|  | If a user already has a pet:no need in adding a separate button to the parent screen:if a user doesn't have a pet without a collar → show 'Add Pet' screen;if a user has pet(s) without collars assigned → show "Pair a Collar to Pet" screen with an option to add a new pet;pets with assigned collars should NOT be considered and should NOT be visible in the list.HALO-14222 - MOB: Changes to Onboarding if a user already has a pet without assigned collars OPEN |  |  |
| 'Assign Your Halo Collar to Your Dog' screen |
| ME21-US42-AC01 | Entry points:a user tapped 'Next' on the 'Halo Collar Has Been Securely Added to Your Account' screen. | Link to Zeplin | Link to Zeplin |
| ME21-US42-AC02 | When a user taps on the 'Add Pet' button, then the app navigates them to the 'Add Pet' screen. |
|  | When a user taps on the 'I already have a pet' button, then the app navigates them to the |
| 'Assign a Collar' screen |
| ME21-US42-AC04 | 'Done' button should be moved to the bottom. | Link to Zeplin Update +question mark | Link to Zeplin |
| ME21-US42-AC05 | Content of this screen should be scrollable except the bottom part with the 'Done' button. |
| 'Pair Collar With a Pet' screen |
| ME21-US42-AC06 | 'Done' button should be moved to the bottom. | Link to ZeplinUpdate +question mark | Link to Zeplin |
| ME21-US42-AC07 | Content of this screen should be scrollable except the bottom part with the 'Done' button. |
| Add a question mark icon |
| ME21-US42-AC08 | A question mark tappable icon should be displayed at the left upper corner on the following Onboarding screens:'Assign Your Halo Collar to Your Dog' screen;'Add Pet' screen;'Assign a Collar' screen;'Pair Collar With a Pet' screen. | - | - |
| ME21-US42-AC09 | When a user taps on a question mark icon, then the app should open the 'Need Help?' screen. | - | - |
