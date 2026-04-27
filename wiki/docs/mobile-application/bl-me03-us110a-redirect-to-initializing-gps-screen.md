---
title: "[BL] ME03-US110a. Redirect to Initializing GPS screen from Collar's list, Advanced Settings menu updates"
sidebar_label: "[BL] ME03-US110a. Redirect to Initializing GPS screen from Collar's list, Advanced Settings menu updates"
sidebar_position: 307
author: "Ekaterina Dupanova"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-15526 - MOB: Redirect to Initializing GPS screen from Collar's list, Advanced Settings menu updates Closed |
| Click here to expand...As of: 24 Mar 2023 Ekaterina Dupanova created initial draft of the story23 Aug 2023 Ekaterina Dupanova updated the screen in ME03-US110-AC05. UI design is updated due to the bug, see https://softeq.slack.com/archives/C016JEX414M/p1691653939344959?thread_ts=1691583336.255649&cid=C016JEX414M |# Contents

User story Acceptance criteria

# User story

As a Halo app user I want to be able to View Collar's GPS state at any time so that to make sure the collar is working properly and my pet is safe.

As a Halo app user I want to know when the collar needs calibration and initiate it so as to make sure the collar is working properly.

# Acceptance criteria

| AC | Description | Links, design | As is | To be |
|---|---|---|---|---|
| 'Advanced settings' screen updates |
| ME03-US110-AC01 | Remove menu items from Advanced settings screen:Compass Calibration (with subtext, Learn more link and button)Satellite position data (with subtext) | Zeplin: iOS | Android |
| ME03-US110-AC03 | Rename GPS level settings menu option:As is To be'GPS Signal Level Settings' title'Here you can change Halo's default settings manually.' text'GPS Signal Level' title | 'GPS Signal Level Settings' title'Here you can change Halo's default settings manually.' text | 'GPS Signal Level' title |  |
| 'GPS Signal Level Settings' title'Here you can change Halo's default settings manually.' text | 'GPS Signal Level' title |
| ME03-US110-A10 | Under GPS Signal Level Settings add the following menu options'View GPS signal level settings' 'Edit GPS signal level settings' |  |
| ME03-US110-AC04 | Upon clicking on the 'View GPS signal level settings' the app should show 'GPS signal level settings' screen in View mode (see [NI] ME03-US98. View/Edit GPS level bar (Advanced Settings -\> 'GPS signal level settings' screen)) |  |
| ME03-US110-AC11 | Upon clicking on the 'Edit GPS signal level settings' the app should open Edit GPS signal level settings screen |  |
