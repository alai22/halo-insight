---
title: "(BL) ME21-US78. Redesign Splash/'Screen with Log in/Sign up options' prior H4 launch"
sidebar_label: "(BL) ME21-US78. Redesign Splash/'Screen with Log in/Sign up options' prior H4 launch"
sidebar_position: 437
last_modified: "Oct 04, 2024"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| BASELINED by Galina Lonskaya on 10/04/2024, see the baseline: ME01-F00. App Launch (Splash Screen, Start Screen, Error Screen) |
| Galina Lonskaya Dmitry Kravchuk |
| HALO-20818 - MOB: Splash screen redesign required for Sept 2024 release Closed |
| the user story draft is created on 08 Aug 2024 UI design is added on 10 Sep 2024 |Table of Contents

User story Acceptance criteria Implementation Notes

# User story

\> As Halo Collar app account owner, I want to view photo of the dog owner and the dog with Halo as Splash and Start screen so that I can imagine how Halo Collar system might change our life being with the dog.

# Acceptance criteria

| AC | Description | AS IS: iOSSee the screen recording | AS IS: Android See the screen recording | TO BE: iOS | TO BE: Android |
|---|---|---|---|---|---|
| ME01-US78-AC01 | "Splash Screen" should have updated UI: see TO BE columns.See the initial requirements in ME01-F00-AC01. | Figma | Android ≤ 11Android ≥ 12The system splash screen should be displayed. This is an automatically generated screen that appears when an app is launched on Android devices starting from version 12. The following elements only are under mob dev control: (1) App Icon, (2) Background Color, (3) Icon AnimationFigmaFigma link is not found, a screenshot from the app | Android ≤ 11 | Android ≥ 12The system splash screen should be displayed. This is an automatically generated screen that appears when an app is launched on Android devices starting from version 12. The following elements only are under mob dev control: (1) App Icon, (2) Background Color, (3) Icon Animation | Figma | Figma link is not found, a screenshot from the app | Figma | Android ≤ 11Figma Android ≥ 12Same logo animation but yellow instead of blue. Figma |
| Android ≤ 11 | Android ≥ 12The system splash screen should be displayed. This is an automatically generated screen that appears when an app is launched on Android devices starting from version 12. The following elements only are under mob dev control: (1) App Icon, (2) Background Color, (3) Icon Animation |
| Figma | Figma link is not found, a screenshot from the app |
| ME01-US78-AC02 | "Splash Screen with Loading Spinner" should have updated UI: see TO BE columns.See the initial requirements in ME01-F00-AC01. | Figma | Figma | FigmaNote "™" added to tagline | FigmaNote "™" added to tagline |
| ME01-US78-AC03 | "Start screen with Log in/Sign up options" have updated UI: TBD See the initial requirements in ME01-F00-AC05. | FigmaiPhone SE | Figma | Figma Note "™" added to tagline | FigmaNote "™" added to tagline |
| ME01-US78-AC04 | iOS specific "Start screen with Сancel Option" should have updated UI: see TO BE columns.See the initial requirements in ME01-F00-AC05. Note: this screen is displayed after the user taps on Log in/Sign Up button. This behavior is valid only for iOS 11/12/13 and 14.0 + 14.1. in order to prevent some situations when endless spinner displaying (known issue) | Figma | n/a | FigmaNote "™" added to tagline | FigmaNote "™" added to tagline |
| ME01-US78-AC05 | Android specific "Start screen with Log in/Sign up options for foldable devices" should have updated UI:see TO BE columns.Note: As of 8/9/24 1973 users who opened the app at least once used foldable devices (1.03% from all users). Samples of the most popular foldable devices among our users: SM-F946U, SM-F731U. The source: Firebase | n/a | Zeplin (Figma link is not found) | n/a | Foldable Device FigmaNote "™" added to tagline |# Implementation Notes

| IN | Description |
|---|---|
| ME01-US78-IN01 | n/a |
