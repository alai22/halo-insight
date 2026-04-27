---
title: "(NA) ME04-US?. Propose Name Options to the user"
sidebar_label: "(NA) ME04-US?. Propose Name Options to the user"
sidebar_position: 524
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| iOS:Android: |
| 26 Mar 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to manage my fence name so I can name as I want.

# Acceptance criteria

| AC | Description | Design | Name candidates list |
|---|---|---|---|
|  | Before opening the Name Your Fence pop-up, the app should:Form the list of possible name candidates. | Figma |
|  | If the app does NOT know if the location is private ('Residential' in ReportAll) or public (other than 'Residential' in ReportAll'), then the app should take the list of most popular names for both private and public places saved in config. |
| ME04-F03-AC01 | If the Fence location is private, then the app should take the list of the most popular names for private places saved in confi. |
|  | If the Fence location is public, then the app should form the list based on public place keywords from Mapbox. |  |
|  | If Mapbox has no keywords, then the app should take the list of the most popular names for public places saved in the config. |  |
|  | The app should display the first 3 unused names from the config lists. |  |
|  | If all the names from the config list has been used, then the app should TBD |  |
|  | Open question:Should the app display candidates both for Add and Edit flows? |  |
| Alternative 2 |
|  | The app displays no Name candidates. |  |
| Alternative 3 |
|  | The app displays the same list in any situation. |  |
