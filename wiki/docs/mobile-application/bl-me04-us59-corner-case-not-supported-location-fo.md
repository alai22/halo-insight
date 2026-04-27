---
title: "[BL] ME04-US59. Corner case. Not supported location for fence auto-generation"
sidebar_label: "[BL] ME04-US59. Corner case. Not supported location for fence auto-generation"
sidebar_position: 342
last_modified: "Apr 18, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-17717 - MOB: ME04-US59. Corner case. Not supported location for fence auto-generation Closed |
| Click here to expand...As of 05 Oct 2023:Mariya Kolyadacreated the initial version of US.As of 17 Oct 2023 Updated to the final version after refinement and text updates.As of 16 Jan 2024 - 17 Jan 2024 Updated existing ACs to the final version after refinement and text updates.Added ME04-US59-AC04. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo acount owner I want to be notified if my location is not supported for fence auto-generation so that I could understand the reason and not worry that I can use it in supported locations.

# Acceptance criteria

| AC | Description | iOs design | Android design | Icon | Displaying time | Message |
|---|---|---|---|---|---|---|
| ME04-US59-AC01 | PreconditionI'm in the process of the Fence creation.I chose the location for auto-generation.The chosen location is absent in the cadastral data list.If I click the 'Confirm Location' button on the 'Fence location positioning' screen, then the app should:Open the 'Fence edit mode' screen.Display auto-generated simple square fence (see details in ME04-US59-AC03).Display the 'Not supported location' toast over the 'Fence edit mode' screen. |  |  |
| ME04-US59-AC02 | The app should display the 'Not supported location' toast in the following format:IconDisplaying timeMessageTemporarily toast (4 seconds)We created a square fence as there is no data available in the chosen location |  | Temporarily toast (4 seconds) | We created a square fence as there is no data available in the chosen location |
|  | Temporarily toast (4 seconds) | We created a square fence as there is no data available in the chosen location |
| ME04-US59-AC03 | The app should display the simple square fence following requirements:Fence shape: Square;Area: 1500 m2;Center of the fence: In the place where user placed the 'Fence Location Positioning' pin on the 'Fence Location Positioning' step;Default zoom level: See design. |
| ME04-US59-AC04 | The app should check the fence on intersections as with usual Edit mode following requirements from: ME04-US64. Fence edit. Add roads, buildings and water intersection validation |
