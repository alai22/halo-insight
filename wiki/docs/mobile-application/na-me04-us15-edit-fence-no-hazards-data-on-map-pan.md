---
title: "(NA) ME04-US15. Edit Fence: No hazards data on map pan"
sidebar_label: "(NA) ME04-US15. Edit Fence: No hazards data on map pan"
sidebar_position: 555
last_modified: "Apr 28, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-774/[ios]-edit-fence-no-hazards-data-on-map-pan#comment-3b79c164Android: https://linear.app/fueled/issue/HALO-775/[android]-edit-fence-no-hazards-data-on-map-pan |
| 14 Apr 2025 Mariya Kolyada created the initial version of a user story.15 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to view spinner while the app is waiting for the hazards data from teh backend.

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-US15-AC01 | If I pan the map so the hazards data update is needed, then the app should:Display the GUI-7 Full-screen loader on the map. | Figma |
| ME04-US15-AC02 | If some error happens or NO response from BE, the app should:Display NO errors and behave as if NO hazards in displayed area.Request data on the next pan again. |Tech details

If during editing we went outside these boundaries (see Retrieving map objects#Loadingadditionaldata), we call GET /geo-fence/location-zone-info and pass the coordinate of the new point in the fence. This scenario is possible when moving and adding a point.Accordingly, this request should be made before validating the fence


