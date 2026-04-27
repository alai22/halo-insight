---
title: "(NI) ME04-US92. Refresh 20 fences on the map when it moved"
sidebar_label: "(NI) ME04-US92. Refresh 20 fences on the map when it moved"
sidebar_position: 392
last_modified: "Jun 07, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-19377 - MOB: Refresh fences when map moves for 1+ km Ready for Development |
|  |User Story ME04-US92-AC01 ME04-US92-AC02 Implementation notes ME04-US92-IN01

# User Story

\> As a USER I want to be able to create unlimited fences so that I have more flexibility in walking with the dog IDAcceptance criteriaME04-US92-AC01Pre-condition: There are more than 20 fences in the user account IF I move the map for 1 km or moreTHEN 20 fences, which are closer to the center of the visible map area should be send to the mob app immediately after I let off the map AND Refresh schedule restarted (app start count 15 seconds from beginning)Notes for QA: Fences could be visible on My map and carousel on Find card.Usual schedule: Mob app should update list of fences each 15 seconds.ME04-US92-AC02Pre-condition: There are more than 20 fences in the user account IF I move the map for less than 1kmTHEN 20 fences, which are closer to the center of the visible map area should be send to the mob app according to usual refresh schedule Notes for QA: Fences could be visible on My map and carousel on Find card.Usual schedule: Mob app should update list of fences each 15 seconds.Implementation notesIDDescriptionME04-US92-IN01


