---
title: "(NI) ME03-US117. Display Collar Updates popup for 1 time only"
sidebar_label: "(NI) ME03-US117. Display Collar Updates popup for 1 time only"
sidebar_position: 389
last_modified: "Jun 07, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related requirements |
|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-19156 - MOB: Information about future FW/SGEE updates is displayed too often Ready for Development |
| [NI] ME21-US35. Onboarding: Updates for 'Collar Update' flowME03-F09. Collar Updates |# Contents

Acceptance criteria Implementation notes

User story

\> As a Halo app user I want not to see the same popup twice so that I don't waste time on reading this information again.

# Acceptance criteria

| AC | Description | Design/Notes |
|---|---|---|
| ME03-US117-AC01 | Pre-condition:I had already passed the full flow of Onboarding including adding a collar.I am adding a collar.I am on the 'Automatic Halo Collar Updates' screen (ME03-F09. Collar Updates see ME03-F09-AC02)IF I tap 'Done' buttonTHEN the app:should not open the pop-up M260should open the next step as described in ME03-US85. Add Collar: GPS calibration screens. | - |
| ME03-US117-AC02 | Pre-condition:I passed not the full flow of Onboarding initially-without adding a collar.I completed the full flow of Onboarding including adding a collar later while adding a collar.I am adding a collar.I am on the 'Automatic Halo Collar Updates' screen (ME03-F09. Collar Updates see ME03-F09-AC02)IF I tap 'Done' buttonTHEN the app:should not open the pop-up M260should open the next step as described in ME03-US85. Add Collar: GPS calibration screens. |  |
| ME03-US117-AC03 | Pre-condition:I had never passed the full flow of Onboarding.IF I tap 'Done' buttonTHEN the app:should open the pop-up M260After user clicks 'Ok' the app should close the 'Automatic Halo Collar Updates' screen;open the next step as described in ME03-US85. Add Collar: GPS calibration screens. |  |# Implementation notes

| IN | Description |
|---|---|
| ME03-US117-IN01 |  |
