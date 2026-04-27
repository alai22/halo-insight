---
title: "(Native apps) ME03-F12-US07. Edit Tracking Thresholds: Revert to Previous state"
sidebar_label: "(Native apps) ME03-F12-US07. Edit Tracking Thresholds: Revert to Previous state"
sidebar_position: 503
last_modified: "Mar 13, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links to Jira/Linear tickets | Changes history |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-408/[ios]-edit-tracking-thresholds-revert-to-previous-state |
| 28 Feb 2025 draft user story is created by Galina Lonskaya |# Contents

User story Acceptance criteria

# User story

\> As a Halo app account owner I want to revert back thresholds to the previous state so that I can use previously saved GPS settings

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-F12-US07-AC01 | By default the 'Revert to Previous State' buttons should not be displayed on the 'Edit Tracking Thresholds' screen. |
| ME03-F12-US07-AC02 | If the user drags and releases 'Low OR High GPS' slider AND the chosen value differs from the last saved values, then:the corresponding 'Revert to Previous State' button(s) with the previously last saved value should be shown, see Figma |
| ME03-F12-US07-AC03 | If the user taps on the 'Revert to Previous State' button, then:the current corresponding thumb should be "automatically" moved to the previously saved value;the 'Revert to Previous State' button should be hidden. |Tech note

The initial values here are the values we got from the collar the first time we went to this screen


