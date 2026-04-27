---
title: "[BL] ME02-US35. Update Solvvy before Dog Park release (it should lead to the correct screen in the app)"
sidebar_label: "[BL] ME02-US35. Update Solvvy before Dog Park release (it should lead to the correct screen in the app)"
sidebar_position: 206
last_modified: "Apr 25, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED (SQ) |
| Maria Shikareva [X] |
| Click here to expand... HALO-11032 - MOB: Update Solvvy before Dog Park release (it should lead to the correct screen in the app) Closed |
| Click here to expand...25 Apr 2022 Maria Shikareva [X] Marked the story as baselined (ME02-F00. View "Settings" screen). |# General information

As of 17 Mar 2022 when a user opens Dog park using Solvvy, the mobile app initiates a Zoom conference (the same as from 'Live Support' option on the Settings list). After new Dog Park release (presumably in early April) the app should initiate opening the 'Dog Park areas list' (as described in ME20-US01. View dog Park areas list and replace Live support with Dog Park on Settings screen).

# User story

\> As a Halo account owner I want to have access to a smart tool to answer my questions so that not to search for the Help articles by myself.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME02-US35-AC01 | Precondition: a user opened 'Solvvy' in the mobile app.When the user taps any "Dog Park" option in Solvvy, the mobile app should display the "Dog Park areas list" screen as described in ME20-US01. View dog Park areas list and replace Live support with Dog Park on Settings screen. | - | - |
| ME02-US35-AC02 | Precondition: the 'Dog Park areas list" is opened from Solvvy.If the user taps "Back" icon, then the app should open Solvvy WebView again.Need to check it during implementation. If it's impossible to return the user to Solvvy due to some technical restrictions, it's OK to open the 'Settings' screen. | - | - |
