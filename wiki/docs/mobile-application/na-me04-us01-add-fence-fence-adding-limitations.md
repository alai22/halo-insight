---
title: "(NA) ME04-US01. Add Fence: Fence adding limitations"
sidebar_label: "(NA) ME04-US01. Add Fence: Fence adding limitations"
sidebar_position: 511
last_modified: "Apr 16, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-644/[ios]-add-fence-fence-adding-limitationsAndroid: https://linear.app/fueled/issue/HALO-645/[android]-add-fence-fence-adding-limitations |
| 26 Mar 2025 Mariya Kolyada created the initial version of a user story.10 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to view explanation why I cannot add the fence, so I can fix it and proceed with fence adding.

# Acceptance criteria

| AC | Description |
|---|---|
| If I tap the 'Add Fence' button, the app should first check if a user is allowed to add a fence.Then proceed with the following conditions defined below. |
| - | Current fences qty \ Plan | No plan (lost a plan) | No plan (never had a plan) | Bronze | Silver | Gold |
| ME04-US01-AC01 | \< 5 | (NA) ME19-F01-US02. Prompting for users with lost access | (NA) ME04-US03. Add Fence: Step 1. Set Fence Location |
| ME04-US01-AC02 | 5-19 | M288 Fence restrictionThis is needed for users who added more than 5 without a plan before we restricted fence number depending on plan | (NA) ME19-F01-US01. Prompting for users who allowed to use the app | (NA) ME04-US03. Add Fence: Step 1. Set Fence Location |
| ME04-US01-AC03 | 20-1000 | (NA) ME19-F01-US01. Prompting for users who allowed to use the app | (NA) ME04-US03. Add Fence: Step 1. Set Fence Location |Tech details

The number of current fences comes in GET /account/my/map - field geoFencesInfo.geoFencesTotalCountThe number of maximum fences comes in GET /subscription/my or POST /subscription/my/refresh - field maxGeoFencesCount. It can be null in cases when the user can add an unlimited number of fences

Before opening the Add Fence screen, you need to make a check that geoFencesTotalCount \< maxGeoFencesCount and that the user has the ManagedFences feature in the subscription (NA) ME19-FE00-US03. Subscription сheck for potentially restricted features.

Also here (NA) ME19-FE00-US03. Subscription сheck for potentially restricted features describes the details of how to determine what to show in case a feature is unavailable


