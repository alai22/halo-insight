---
title: "(NI) ME21-US76. Update 'Let's get a head start' screen within 'Continue w/o collar' flow"
sidebar_label: "(NI) ME21-US76. Update 'Let's get a head start' screen within 'Continue w/o collar' flow"
sidebar_position: 430
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya Dmitry Kravchuk |
| HALO-20587 - MOB: ME21-US76. Update 'Let's get a head start' screen within 'Continue w/o collar' flow Closed |
| the user story draft is created on 01 Aug 2024 |Table of Contents

User story Acceptance criteria

# User story

\> not applicable, UI redesign of the screen

# Acceptance criteria

| AC | Description | UI design | AS IS | TO BE |
|---|---|---|---|---|
| ME21-US76-AC01 | 'Let's get a head start' screen should be changed to 'What would you like to do?' screen. | AS ISTO BEFigma iOSFigma Android |  | Figma iOSFigma Android |
|  | Figma iOSFigma Android |
| ME21-US76-AC02 | There should be 2 entry points to 'What would you like to do?' screen: 'Don't have a collar?' button at 'Adding Your Halo Collar' screen, see the button description in ME21-US55-AC06, (NI) ME21-US55. Remove the video screens from FTUE onboarding, eliminate several unnecessary steps, small updates'Continue using the app without collar' button at 'Join the Pack' screen, see the button description in ME21-US58-AC11, (NI) ME21-US58. Add 'No Pack Membership' handling after 'Enable Permissions' screen. Note 1: 'Why Halo Collar?' screen was fully removed from the app (the removal was done within ME21-US55-AC02). This is the screen that previously was displayed before 'Let's Get a Head Start'Note 2: Previously we have different flows for the users who didn't have both subscription and collar AND for the users who didn't have collar BUT had subscription. Now for both of this user we show 'What would you like to do screen?' screen. | - |
| ME21-US76-AC03 | 'What would you like to do screen?' should consist of: Navigation bar:Back button Empty title Сan be updated after Ryan's answer https://softeq.slack.com/archives/C01654HRD55/p1723729147163959?thread_ts=1723031002.158049&cid=C01654HRD55 'Questionmark' button, see the details in ME21-US76-AC08Page title: 'What would you like to do screen?' title Card #1:Image 'Use App Without a Collar' card title 'No collar yet? No problem. Explore the app and all the great features Halo has to offer.' card subtitle'Enter the App' button, see the details in ME21-US76-AC04Card #2 Icon 'Get Your Halo Collar' card title 'Discover the safest & most accurate GPS fence ever created and order your Halo Collar today. Learn more at halocollar.com' card text, where halocollar.com is a link, see the details in ME21-US76-AC05 | - |
| ME21-US76-AC04 | If I tap on 'Enter the App' button, then: My Map tab should be opened with Find card opened in the default view the corresponding event should be sent to Braze, see the event details in (NI) ME21-US75. Send 'collar_attached_first_use' event to Braze (required for 'Go Outside' IAM)(NI) ME21-US77. Send 'first_map_view' events to Braze | - |
| ME21-US76-AC05 | If I tap on halocollar.com, then: https://www.halocollar.com/ website should be opened via browser. Сan be updated after Ryan's answer https://softeq.slack.com/archives/C01654HRD55/p1723729768662639?thread_ts=1723031002.158049&cid=C01654HRD55 | - |
| ME21-US76-AC06 | If I have Bronze/Silver/Gold subscription and tap on Back button, then: 'Adding Your Halo Collar' screen should be opened. | - |
| ME21-US76-AC07 | If I don't have subscription and tap on Back button, then: 'Join the Pack' screen should be opened. | - |
| ME21-US76-AC08 | If I tap on 'Questionmark' button, then: standard 'Need Help?' screen should be opened, see the details in ME21-US04. Onboarding: 'Questionmark' icon for user support (-\>Need Help screen). | - |
