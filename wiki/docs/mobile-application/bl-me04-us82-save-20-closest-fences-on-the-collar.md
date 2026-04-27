---
title: "[BL] ME04-US82. Save 20 closest fences on the collar"
sidebar_label: "[BL] ME04-US82. Save 20 closest fences on the collar"
sidebar_position: 379
author: "Kiryl Trafimau"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| BASELINED in ME04-EP05. Baseline: Unlimited fences by Ekaterina Dupanova on 04 Oct 2024 |
| Kiryl Trafimau |
| HALO-18967 - BE: Save 20 closest fences on the collar Closed |
|  |User Story ME04-US82-AC01 ME04-US82-AC02 ME04-US82-AC03 Implementation notes ME04-US82-IN01 ME04-US82-IN02 ME04-US82-IN03

# User Story

\> As a USER I want to be able to create unlimited fences so that I have more flexibility in walking with the dog IDAcceptance criteriaME04-US82-AC01IF there are more than 20 fences in the accountWHEN collar position changed significantly comparing with the last synchronized positionTHEN BE should push to the collar 19 closest fences to the collar position and 1 most recent fenceME04-US82-AC02IF there are more than 20 fences in the accountWHEN collar position changed not significantly comparing with the last synchronized positionTHEN BE should not push to the collar any changes to the list of fencesME04-US82-AC03IF there are 20 or less fences in the accountWHEN collar position changed either not significantly or notTHEN BE should not push to the collar any changes to the list of fencesImplementation notesIDDescriptionME04-US82-IN01Position changed significantly is 5000 metresME04-US82-IN02Last synchronized position=collar coordinates received during the last synchronization of fences with the collarME04-US82-IN03Number of fences that pushed to the collar should be configurable:X1: recentX2: closestX1+X2=20


