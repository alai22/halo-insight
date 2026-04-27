---
title: "ME05-US40. Display the tab bar at the Warning Feedback settings (and other feedback settings screens)"
sidebar_label: "ME05-US40. Display the tab bar at the Warning Feedback settings (and other feedback settings screens)"
sidebar_position: 91
author: "Galina Lonskaya"
---

| Epic | Document status | BA story owner | DEV, QA story owner | Link to JIRA Issue |
|---|---|---|---|---|
| ME05. Manage feedbacks |
| APPROVED |
| Galina Lonskaya |
| Pavel Leonenko, Anastasia Brechko |
| HALO-4275 - MOB: Display tab bar at the Warning Feedback settings screen (and other feedback settings screen) Closed |# User story

\> As an owner, I want to have access to the tab bar at the Warning feedback screen (and other feedback screens) so that I can easily switch between the Warning Feedback (and other feedback screens) and Training tab.

# Acceptance criteria

| AC | Description | Source requirement |
|---|---|---|
| The following ACs are relevant for the followings screens:Warning Feedback screenBoundary Feedback screenEmergency Feedback screenGood Behavior screenReturn Whistle screenHeading Home screenBut within the ACs as a sample "Warning Feedback" will be used. |
| ME05-US40-US01 | The tab bar should be displayed at the Warning Feedback screen. |  |
| ME05-US40-US02 | Precondition: Warning Feedback screen is opened.The Bluetooth connection should be interrupted while navigating to other tabs. | - |
| ME05-US40-US03 | Precondition: At the moment the user is on one of the following tabs: Training, Notifications, or Settings, but the Warning Feedback screen is opened on My Map.The Bluetooth connection should be restored after getting back to the Warning Feedback screen. | - |
| ME05-US40-US04 | Precondition: the Warning feedback screen is opened, the settings are updated (but not saved).If I tap on My Map tab, then:the following popup is displayed: M50 Unsaved Changes. | - |
| ME05-US40-US05 | Precondition: the Warning feedback screen is opened, the settings are updated (but not saved).If I go to the Settings screen and log out, then:Feedback setting updates should not be saved;I should be logged out of the app.Note: the simplest approach is described. | - |
