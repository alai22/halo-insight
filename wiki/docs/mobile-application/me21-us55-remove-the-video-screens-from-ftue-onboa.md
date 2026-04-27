---
title: "ME21-US55. Remove the video screens from FTUE onboarding, eliminate several unnecessary steps, small updates"
sidebar_label: "ME21-US55. Remove the video screens from FTUE onboarding, eliminate several unnecessary steps, small updates"
sidebar_position: 367
author: "Kiryl Trafimau"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APROVED |
| Galina Lonskaya |
| HALO-18153 - MOB: ME21-US55. Remove the video screens from the onboarding and eliminate several unnecessary steps Closed |
| 01 Jul 2024 a draft story is created |Table of Contents

User story Acceptance criteria Implementation notes

# User story

\> As a Halo app account owner I want to set up my account and a collar with the decreased number of steps so that I can see the value that the collar can bring me as soon as possible.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| General updates |
| ME21-US55-AC01 | The following steps should be fully removed from FTUE Onboarding flow: Screen with Help options explanationWelcome to Halo Pack Do you have a collar Let's Get StartedYour Halo Collar KITHalo Collar Updates Your Collar’s GPSUsing Halo Beacons | See the new flow in Figma |
| ME21-US55-AC02 | The parent screens with the video should be removed from all the onboarding steps except 'Why Halo Collar' and 'Let's Get a Head Start' (part of the flow 'Continue using the app without the collar', this screen will be redesigned within (NI) ME21-US76. Update 'Let's get a head start' screen within 'Continue w/o collar' flow). |
| ME21-US55-AC03 | The new sequence of the steps of the 'Onboarding' flow should be the following: 'Welcome to the Halo pack!' (~Tell Us About Yourself) screen'Enable Permissions' screen'Adding Your Halo Collar' sub flow'Set Up Your Pet’s Profile' sub flow'Connecting Your Halo to Wi-Fi' sub flow'Congratulations' screen |
| ME21-US55-AC04 | 'Charging Your Collar' should be used as a parent screen for three sub flows mentioned in ME21-US55-AC03. Note for the dev/qa team: Dmitry Kravchuk has found a solution how to show Add Collar / Add Pet / Set up Wi-Fi flow without parent screen. So, ME21-US55-AC04 and AC05 are not necessary and removed | - |
| ME21-US55-AC05 | When transitioning from one sub flow to another described in ME21-US55-AC03, the parent screen with a spinner on a white background should be displayed. | - |
| 'Charging Your Collar' (~ 'Adding Your Halo Collar') screen updates |
| ME21-US55-AC09 | Several text updates for 'Charging Your Collar' screen: 'Charging your halo collar' title should be changed to 'Adding Your Halo Collar''Plug in your collar ..' text should be changed to 'Grab your collar from the box and plug it in at a location with good Wi-Fi and/or cellular signal.' | - |
| ME21-US55-AC06 | If I am adding the first collar, then: 'Don't have a collar?' button should be displayed at the bottom of 'Adding Your Halo Collar' screen. Note: If I add 2nd / next collar, then 'Don't have a collar?' button should not be displayed. For instance: the user can initiate adding of the 2nd collar after tap on 'Add Another Collar' button from 'Congratulations!' screen. | See the screen in FigmaNote 1: switcher will be added within a separate story: (NI) ME21-US74. Add 'Halo 4' vs 'old versions' switcher |
| ME21-US55-AC07 | 'Don't have a collar?' button should be pinned to the bottom of 'Adding Your Halo Collar' screen together with 'Next' button. | - |
| ME21-US55-AC08 | If I tap on 'Don't have a collar' button at 'Adding Your Halo Collar' screen, then: see the screen is described in AC01 (NI) ME21-US76. Update 'Let's get a head start' screen within 'Continue w/o collar' flow should be opened. | - |
| Other updates |
| ME21-US55-AC10 | 'Can't find your network' text should be changed to 'Don't see your network below?' text on 'Connecting Your Halo to Wi-Fi' screen. | - |# Implementation notes

| IN | Description |
|---|---|
| ME21-IN55-AC01 | Initial tech input from Timofey: 'Charging Your Collar' screen should be a separate screen, to be used as a "parent" to start modal "Add Collar" flow from;Current idea is that it should be a copy of the "Charging your collar" screen (first screen in the modal "Add Collar" flow). If this is the case - then "Add Collar" flow started from this screen should be started from the second screen (with BLE scanning);While modal "Add Collar" flow is in progress, we might need to show a special "opaque" version of the BusyView over the screen content;Includes navigation updates to "skip" adding a collar; |
