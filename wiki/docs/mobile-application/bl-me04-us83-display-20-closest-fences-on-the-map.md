---
title: "[BL] ME04-US83. Display 20 closest fences on the map"
sidebar_label: "[BL] ME04-US83. Display 20 closest fences on the map"
sidebar_position: 380
author: "Kiryl Trafimau"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| BASELINED in ME04-EP05. Baseline: Unlimited fences by Ekaterina Dupanova on 04 Oct 2024 |
| Kiryl Trafimau |
| HALO-18968 - BE, MOB: Display 20 fences on My Map Closed |
|  |User Story ME04-US83-AC01 ME04-US83-AC02 ME04-US83-AC03 ME04-US83-AC04 Implementation notes ME04-US83-IN01 ME04-US83-IN02

# User Story

\> As a USER I want to be able to create unlimited fences so that I have more flexibility in walking with the dog IDAcceptance criteriaME04-US83-AC01IF there are less than 20 fences in the user account THEN all fences should be send to the mob appNote for QA: Fences could be visible on My map and carousel on Find card.ME04-US83-AC02IF there are more than 20 fences in the user account THEN 20 fences, which are closer to the center of the visible map area should be send to the mob appNote for QA: Fences could be visible on My map and carousel on Find card.ME04-US83-AC03Edge casePre-condition: there are more than 20 fences in the user accountIF MOB did not push coordinates to BETHEN 10 oldest and 10 most recent fences should be send to the mob appNote for QA: Fences could be visible on My map and carousel on Find card.ME04-US83-AC04Mob app should update list of fences each 15 secondsImplementation notesIDDescriptionME04-US83-IN01Visible map area see Sync user fences with collar#APIchangesME04-US83-IN02


