---
title: "(BL) ME04-US95. PHF. Generate simple square fence if cadastral area too big or there are no buildings inside"
sidebar_label: "(BL) ME04-US95. PHF. Generate simple square fence if cadastral area too big or there are no buildings inside"
sidebar_position: 408
last_modified: "Oct 07, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| BASELINED in (In progress) ME04-F00. Baseline: Add fence with auto-generation by Mariya Kolyada on 07 Oct 2024 |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-20048 - MOB: ME04-US95. PHF. Generate simple square fence if cadastral area too big or there are no buildings inside Closed |
| As of 17 Apr 2024 - 18 Apr 2024 :Mariya Kolyada created the initial version of US. |# User Story

\> As a Halo accout owner I want to get simple square fence instead of too big or without buildings inside that based on cadastral data so I can edit it easier.

# Acceptance criteria

| AC | Description | As is | To be |
|---|---|---|---|
| ME04-US95-AC01 | PreconditionI'm in the process of the Fence creation.I chose the location for auto-generation.The chosen location is presented in the cadastral data list.There are NO buildings inside the fence.If I click the 'Create Fence' button on the 'Fence location positioning' screen, then the app should:Open the 'Fence edit mode' screen.Display auto-generated simple square fence, the same as if there is no cadastral data (see details in ME04-US59-AC03).Display the updated 'Simple square' toast over the 'Fence edit mode' screen. |
| ME04-US95-AC02 | PreconditionI'm in the process of the Fence creation.I chose the location for auto-generation.The chosen location is presented in the cadastral data list.The location's (parcel from ReportAll API) registered size is bigger than 50000 m2 (~12.355269 acres).If I click the 'Create Fence' button on the 'Fence location positioning' screen, then the app should:Open the 'Fence edit mode' screen.Display auto-generated simple square fence as if there is no cadastral data (see details in ME04-US59-AC03).Display the 'Simple square' toast over the 'Fence edit mode' screen. |
| ME04-US95-AC03 | PreconditionI'm in the process of the Fence creation.I chose the location for auto-generation.The chosen location is presented in the cadastral data list.BE returns some error.If I click the 'Create Fence' button on the 'Fence location positioning' screen, then the app should:Open the 'Fence edit mode' screen.Display auto-generated simple square fence as if there is no cadastral data (see details in ME04-US59-AC03).Display the 'Simple square' toast over the 'Fence edit mode' screen.Implementation notesBE may return an error in case some of these validations have been failed: BuildZones API endpoint: Safe zones count \<= config.MaxSafeZonesCount Safe zone area \< config.MinSafeArea Max points count for each zone \< config.MaxPointsCount |
| ME04-US95-AC03 | Update the message of the 'Simple square' toast following the rules:As isTo beWe created a square fence because there is limited map data in this areaPlease edit this basic fence | We created a square fence because there is limited map data in this area | Please edit this basic fence |
| We created a square fence because there is limited map data in this area | Please edit this basic fence |
