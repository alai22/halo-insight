---
title: "[Postponed] ME03-US58. Battery saver mode"
sidebar_label: "[Postponed] ME03-US58. Battery saver mode"
sidebar_position: 153
last_modified: "Jul 06, 2021"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Maria Shikareva [X] |
| HALO-7552 - BE+MOB+FW: Return back Battery Saving mode (new approach) Open HALO-7710 - [FW] Implement logic for battery saver mode turning on/off Open |# Contents

User Story Acceptance criteria

# User Story

\> As a user I want to be able to turn on/ off Battery Saver mode when required so that to have control over power consumption.

# Acceptance criteria

| AC | Description | iOS screen design / implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME03-US58-AC01 | The new toggle/ button should be added to the Collars list for 'Battery Saver' on/ off mode.TBD notes from 2021-07-05 Meeting notes: BA+UX call:Consider of putting the battery saver to the collars list (even it'll be better to implement Advanced settings: e.g. together with indoor/ outdoor calibrating → see HALO-7726 - Advanced collar settings OPEN ).Also it can be useful to have a battery saver schedule: the users might only want to turn it on over night to have a longer battery life (check if there are previous requirements about it).It's a good idea to have a video how the Battery Saver mode works if the user enters Advanced settings for the first time (if it's possible; need to explain that when the battery saver is ON, the collar might have some degraded functionality for a period of time until the collar reports that it's functioning normally again).When implemented, need to display the current status of battery saver on the UI.Additional: it was meant previously that we might send special not-n to the user that he/she can start use battery saving (depends on collar state, if it's ready to enable this mode). |  | The same screen as for iOS |
| ME03-US58-AC02 | The new button should be added to the "Change Mode For All Pets" action sheet. The button behavior on "Change Mode For All Pets" action sheet should be the same as described in ME15-F03. Change mode for all pets.TBD need to discuss if we need this change → maybe it's better to leave this only on the Collars list. | See previous designs:[BL] ME16-US11. Change mode for all pets (updated flow) |  |
| ME03-US58-AC03 | When the user turns the Battery Saver ON, the collar minimizes power consumption (from FW perspective it means that GPS will be turned off).Note: fences will be less accurate; the collar will slow to acquire location → it doesn't have great meaning for the user, but the battery will have a longer life. | - | - |
