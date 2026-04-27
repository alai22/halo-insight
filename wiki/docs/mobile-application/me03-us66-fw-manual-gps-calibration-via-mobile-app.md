---
title: "ME03-US66. FW: Manual GPS calibration via mobile app"
sidebar_label: "ME03-US66. FW: Manual GPS calibration via mobile app"
sidebar_position: 172
last_modified: "Apr 29, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| APPROVED (SQ) |
| Maria Shikareva [X] |
| HALO-9351 - BA: FW requirements for manual GPS calibration Closed |# Contents

Description Acceptance criteria

# Description

As of 30 Jul 2021 current GPS calibration doesn't work precisely at the moment. The users notice that the app show indoors when the collar is outdoors and vice versa. The end users leave these comments on Markets and ask about it in Solvvy. Also there's an email "HALO: Refunds statistics" from Sep 22, 2021 from which it's clear that inaccurate GPS and poor feedback/ fence performance are among of the main reasons for return (for refund) and warranty (for replacement): 17.6% for GPS (accuracy) category and 12.4% for Feedback/ Fence Performance.

Update as of 05 Oct 2021 Auto GPS calibration logic doesn't improve precision of the location determination.

So it was decided to give the users UI for manual indoor/outdoor adjustment for each user to be able to set the best outdoor/indoor threshold positioning on their own (see the related UI story: [Not implemented] ME03-US64. Use slider for outdoor/indoor threshold adjustment.

# Acceptance criteria

| AC | Description | Source requirement |
|---|---|---|
| ME03-US66-AC01 | Only new FW should support "Manual GPS calibration" feature. | - |
| ME03-US66-AC02 | Current automatic calibration procedure should be removed. |  |
| ME03-US66-AC03 | New algorithm with user Boundaries usage should be implemented: new FW version should use Boundaries directly and should allow to save Boundaries received from BE. | HALO-7880 - FW: Manual GPS calibration (improved logic for Indoor/Outdoor determination) Closed |
| ME03-US66-AC04 | Limits should not be removed. Note: FW uses limits to definitely define that the collar is outdoor/ indoor even when the collar is not moving around, i.e. when the collar reaches limits, it's clear that the collar is outdoor/ indoor. | - |
| ME03-US66-AC05 | "Backdoor" section processing should be removed (Backend contract changes). | - |
| ME03-US66-AC06 | The collar should support new C2D message (Backend contract changes).Note: the collar should get the Boundaries from the mobile app via BE (not directly via BLE) as BE must be source of trust. | - |
| ME03-US66-AC07 | The collar should be able to update reported TWIN with new parameters. | - |
| ME03-US66-AC08 | The collar can restore Boundaries values after formatting from the desired TWIN.Note: when a collar needs values to be re-synchronized after resetting, then it should happen via Configuration Session sync with C2D direct method for setting values instead of putting raw numbers to desired TWIN section. | - |
| ME03-US66-AC09 | FW should calculate Limits itself based on the received Boundaries.Note: if the math is changed, then we need to only update FW. We need to have this logic in one place, the collar can now update its own limits, so it's better to have this calculation logic on FW, not BE. If we have a new formula in the future, it'll just depend on what version of FW you're running. | - |
| ME03-US66-AC10 | FW should send all 2 parameters to the reported TWIN:Limits of automatic calibration;Boundaries of manual calibration. | - |
| ME03-US66-AC11 | After getting new values the collar should use new saved boundaries. | - |
| ME03-US66-AC12 | The collar should send it's current GPS level to the mobile app each 1 second (Bluetooth contract changes). | - |
