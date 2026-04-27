---
title: "[BL] ME03-US78. Add a warning pop-up when the user drags pin a lot"
sidebar_label: "[BL] ME03-US78. Add a warning pop-up when the user drags pin a lot"
sidebar_position: 214
last_modified: "Apr 29, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] |
| Click here to expand... HALO-11436 - MOB: Add a warning pop-up when the user drags pin a lot Closed |
| Click here to expand...29 Apr 2022 Maria Shikareva [X] Marked the story as baselined (see ME03-F05. Edit GPS signal level settings (ex. GPS calibration)). |# Contents

User story Acceptance criteria

# User story

\> As a user I want to see a warning pop-up when I'm restricted to drag pin a lot so that to understand the reason of such restriction.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| ME03-US78-US01 | Precondition: Indoor/ Outdoor Settings screen with active slider is displayedANDthe user drags Indoor/ Outdoor pins.The user should not be allowed to drag pins in a way when the difference between Indoor and Outdoor pin exceeds the maximum calculated by the existing formula: BL\>= 17 + 0.66BU (see [Not implemented] ME03-US64. Use slider for outdoor/indoor threshold adjustment for more details). | - | - |
| ME03-US78-US02 | When the user tries to drag pin more than allowed, the app should display a warning pop-up: M235 Low and High Thresholds.Note: we need this pop-up to prevent the user from moving the pin further without understanding how this will affect another pin. | - | - |
| ME03-US78-US03 | The app should display M235 Low and High Thresholds only once: i.e. when the user configures the values for the very first time. Note: the app should remember showing this pop-up. | - | - |
