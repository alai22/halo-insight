---
title: "ME04-EP05. Baseline: Unlimited fences"
sidebar_label: "ME04-EP05. Baseline: Unlimited fences"
sidebar_position: 382
author: "Mariya Kolyada"
---

Click here to expand...| Document type | Document status | Document owners | Link to JIRA Issues | History of changes |
|---|---|---|---|---|
| Baseline story |
| BASELINED on 04 Oct 2024 |
| Ekaterina Dupanova Mariya Kolyada |
| HALO-18967 - BE: Save 20 closest fences on the collar Closed HALO-18968 - BE, MOB: Display 20 fences on My Map Closed HALO-18997 - MOB: ME04-US87. Double-check overlapping during fence saving Closed |
| As of 04 Oct 2024 Ekaterina Dupanova baselined:ME04-EP05. Baseline: Unlimited fences[BL] ME04-US83. Display 20 closest fences on the map |Click here to expand...User story As a Halo account user I want to be able to create unlimited fences so that I have more flexibility walking with the dog. Acceptance criteria Saving 20 closest fences on the collar Displaying 20 closest fences on My Map Overlapping fences Implementation notes

# User story

\> As a Halo account user I want to be able to create unlimited fences so that I have more flexibility walking with the dog.

# Acceptance criteria

| AC | Text | iOS UI design | Android UI design | Saving 20 closest fences on the collar | Displaying 20 closest fences on My Map | Overlapping fences |
|---|---|---|---|---|---|---|
| ME04-EP05-AC01 | IFthere are more than 20 fences in the accountWHEN collar position changed significantly (see ME04-EP05-IN01) comparing with the last synchronized position (see ME04-EP05-IN02)THEN BE should push 19 closest fences to the collar position and 1 most recent fence |  |  |
| ME04-EP05-AC02 | IF there are more than 20 fences in the accountWHEN collar position did not change significantly comparing with the last synchronized positionTHEN BE should not push any changes to the list of fences to the collar |  |  |
| ME04-EP05-AC03 | IF there are 20 or less fences in the accountWHEN collar position changed either significantly or not significantlyTHEN BE should not push to the collar any changes to the list of fences |  |  |
| ME04-EP05-AC04 | IF there are less than 20 fences in the user accountTHEN all fences should be send to the mobFences should be visible on My map and carousel on Find card (see ME15-F02. Find card) |  |  |
| ME04-EP05-AC05 | IF there are more than 20 fences in the user accountTHEN 20 fences, which are closer to the center of the visible map area should be send to the mob app Fences should be visible on My map and carousel on Find card (see ME15-F02. Find card) |  |  |
| ME04-EP05-AC06 | Mob app should update the list of fences each 15 seconds |  |  |
| ME04-EP05-AC07 | Edge casePrecondition: there are more than 20 fences in the user accountIF MOB did not push coordinates to BETHEN 10 oldest and 10 most recent fences should be send to the mob appFences should be visible on My map and carousel on Find card (see ME15-F02. Find card) |  |  |
| ME04-EP05-AC08 | If I trigger fence creation or edit, then the app should:Update the list of fences saved in the app cache (see ME04-EP05-IN05) |  |  |
| ME04-EP05-AC09 | Precondition:user has more than 20 fences.IFI put the 1st point of the fence THEN Update the list of fences saved in the app cacheAND Display a spinner while updatingAND Update the map UIAND Display a fence point if it does not overlap with any other fence on the mapSee ME04-EP05-IN05 |  |  |
| ME04-EP05-AC10 | Preconditions:User has more than 20 fences.I put the 1st point of the fence IFthe point overlaps another fenceTHEN do not display this point ANDDisplay error that fence overlaps existing fences (see ME04-F00- M7 in ME04-F00. Add fence without GPS#TableME04-1Drawafenceerrors/warnings). |  |  |
| ME04-EP05-AC11 | Known issue: it is possible that we have fences not displayed on the map and which will be overlapped (e.g. I have more than 20 fences in the area where new one is created and the new one overlaps some of the not displayed fences) |  |  |# Implementation notes

| ID | Description |
|---|---|
| ME04-EP05-IN01 | 'Position changed significantly' is 5000 meters |
| ME04-EP05-IN02 | Last synchronized position=collar coordinates received during the last synchronization of fences with the collar |
| ME04-EP05-IN03 | Number of fences that pushed to the collar should be configurable:X1: recentX2: closestX1+X2=20 |
| ME04-EP05-IN04 | Visible map area see Sync user fences with collar#APIchanges |
| ME04-EP05-IN05 | FE should request the list of 20 fences from BE.The collars that meet the same rules as those that BE sends every 15 sec on My Map |
