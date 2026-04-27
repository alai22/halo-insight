---
title: "[BL] ME03-US90. Update map centering logic for GPS calibration flow"
sidebar_label: "[BL] ME03-US90. Update map centering logic for GPS calibration flow"
sidebar_position: 265
last_modified: "Oct 14, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Siarhei Leushunou [X] Timofey Burak [X] Katherina Kaplina |
| HALO-13869 - MOB: Update map centering logic for GPS calibration flow Closed |
| Click here to expand...26 Sep 2022 Maria Shikareva [X] Replaced 'pet' word within 'collar' as on this step pets could not be assigned yet and the app display only the location of the collar, not the pet.14 Oct 2022 Maria Shikareva [X] Baselined the story (see ME03-F08. Collar GPS initialization). |# Contents

General description User story Acceptance criteria

# General description

As of 14 Sep 2022 (see "Bug - New GPS Calibration flow" email, Sep 12, 2022): the ‘collar pin’ on the map needs to be in ‘auto-tracking mode’ during new GPS calibration flow. Case: the last position (before calibration) was in Taiwan. As it was calibrating, the pin moved to Texas (as it should), but the map did not follow. The user had to manually pan/zoom to Texas.

# User story

\> As a Halo app user I want to have auto-tracking mode for the map during the calibration flow so that to have map centered on the app after getting updated location.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| ME03-US90-US01 | The app should display a 'Compass' button when a user adjusts the map angle. |  |  |
| ME03-US90-US02 | When a user taps on the 'Compass' button, the app should:re-orient the screen and revert the map view back to its original direction;hide the 'Compass' icon. |  |  |
| ME03-US90-US03 | The app should center the map on the collar always (not only on the first showing of the map) based on logic described in ME03-US85-AC09.I.e. if afterwards collar changes position on the map, the app should automatically center the map by its new position. |  |  |
| ME03-US90-US04 | "Center on the collar's location" button should be added to the map on the 'Calibrate Collar's GPS' screen. |  |  |
| ME03-US90-US05 | Precondition: 'Calibrate Collar's GPS' screen is displayed; my map area is centered on the collar's location.If a user drags the map, then the app should:stop centering the map on the collar's pin;display the "Center on the collar's pin" button |  |  |
| ME03-US90-US06 | Precondition: 'Calibrate Collar's GPS' screen is displayed; my map area isn't centered on the collar's location.If a user taps on the "Center on the collar's pin" button, then the app should:center the map on the collar's pin;hide the "Center on the collar's pin" button. | - | - |
| ME03-US90-US07 | The app should display the "Center on the collar's pin" button above the "Compass" button (in case they both are displayed together). |  |  |
