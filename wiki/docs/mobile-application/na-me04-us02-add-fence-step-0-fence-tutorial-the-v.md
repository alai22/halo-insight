---
title: "(NA) ME04-US02. Add Fence: Step 0. Fence Tutorial (the very first adding only)"
sidebar_label: "(NA) ME04-US02. Add Fence: Step 0. Fence Tutorial (the very first adding only)"
sidebar_position: 526
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-648/[ios]-add-fence-step-0-fence-tutorial-the-very-first-adding-onlyAndroid: https://linear.app/fueled/issue/HALO-649/[android]-add-fence-step-0-fence-tutorial-the-very-first-adding-only |
| 27 Mar 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be proposed to view the fence tutorial if it is my very fist time adding fence, so I spend no time investigating how it works myself.

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US02-AC01 | If I create a fence for the first time in the same user account, then the spp should:Display (NA) ME04-F05. Fence tutorial. |
| ME04-US02-AC02 | If I tap one of the following buttons:either the 'Skip' button on any of tutorial steps,or the 'I'm Ready!' on the last stepthen the app should:Navigate to (NA) ME04-US03. Add Fence: Step 1. Set Fence Location. |
| ME04-US02-AC03 | The app should store the Tutorial viewed status for my account locally on the mobile device.This means that if I open my app account using another device, then the app will present the Fence Tutorial again. Because it will be the very first time on another device. |
| ME04-US02-AC05 | Tutorial viewed status values can be cleared for the account used on the specific mobile device in the following cases only after I:Removed the app from the mobile device;Logged out and logged into a different account using the same mobile device. |Tech details

If the tutorial was viewed for the first time during editing (clicking on the button) before creating the fence - we remember it and do not show it during creation


