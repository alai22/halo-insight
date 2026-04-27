---
title: "ME04-US101. Update building, road and water overlays"
sidebar_label: "ME04-US101. Update building, road and water overlays"
sidebar_position: 424
last_modified: "Jun 14, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-20446 - MOB: ME04-US101. Update building, road and water overlays Closed |
| Click here to expand...As of 10 Jun 2024:Mariya Kolyadacreated the initial version of US.As of 14 Jun 2024 Mariya Kolyada added ACs about Overlays card. |# Contents

User Stories Acceptance criteria

# User Stories

\> As a Halo acount owner I want to view the highlited road/building/water with transparent area of intersection so that I can easily view what is under overlay.

# Acceptance criteria

| AC | Description | iOs design | Android design | Icon | Label |  | Icon | Header | Main text |
|---|---|---|---|---|---|---|---|---|---|
| ME04-US101-AC01 | Hide the default water overlay from My Map on the Fence Preview and Edit screens. | - | - |
| ME04-US101-AC02 | Display the intersection legend above the bottom actions menu that consists of the following elements:IconLabelBuildingRoadWaterCaution |  | Building |  | Road |  | Water |  | Caution | Figma Link(Icon & Pattern assets) | - |
|  | Building |
|  | Road |
|  | Water |
|  | Caution |
| ME04-US101-AC03 | If I click on any legend element, then the app should:Open Overlays description card. | Figma Link | Figma Link |
| ME04-US101-AC04 | Overlays description card should consist of the following elements:DescriptionIconHeaderMain textBuilding overlay descriptionBuildingIndicates a building structure plus 20ft buffer.Road overlay descriptionRoadIndicates a public road plus 15ft buffer.Water overlay descriptionWaterIndicates an area with water. No buffer added.Caution overlay descriptionCautionIndicates areas to avoid for safety. Use discretion when creating a fence that intersects these areas.'Close' / 'X' button - closes 'Overlays card' on click. | Building overlay description |  | Building | Indicates a building structure plus 20ft buffer. | Road overlay description |  | Road | Indicates a public road plus 15ft buffer. | Water overlay description |  | Water | Indicates an area with water. No buffer added. | Caution overlay description |  | Caution | Indicates areas to avoid for safety. Use discretion when creating a fence that intersects these areas. |
| Building overlay description |  | Building | Indicates a building structure plus 20ft buffer. |
| Road overlay description |  | Road | Indicates a public road plus 15ft buffer. |
| Water overlay description |  | Water | Indicates an area with water. No buffer added. |
| Caution overlay description |  | Caution | Indicates areas to avoid for safety. Use discretion when creating a fence that intersects these areas. |
| ME04-US101-AC05 | PreconditionsFence Edit screen is opened.If the app or I put fence post(s) on another existing fence in my account, then the app should:Fill the overlapping area of the editing fence with a red cross pattern.Color in red the borders of another existing fence:Fence preview - whole fence border.Fence edit screen - only the inner part of the existing overlapping fence inside the editing fence (as already implemented) | Figma Link | Figma Link |
| ME04-US101-AC06 | PreconditionsFence Edit screen is opened.ORFence Preview with road or water overlapping is opened.If the app or I put fence post(s) on the road, then the app should:Hover the visible part of the road with an orange transparent overlay and dashed border.Fill the area of fence and road overlapping with a red cross pattern. | Figma Link | Figma Link |
| ME04-US101-AC07 | PreconditionsFence Edit screen is opened.ORFence Preview with road or water overlapping is opened.If the app or I put fence post(s) on the water, then the app should:Hover the visible part of the water with a blue transparent overlay and dotted border.Fill the area of fence and road overlapping with a red cross pattern.NoteThe app should apply the water overlay to waterways that are not covered with an overlay on My Map. |
| ME04-US101-AC08 | PreconditionsFence Edit screen is opened.ORFence Preview screen is opened.The app should always hover over the buildings inside the fence with a transparent pattern of blue diagonal lines. |
| ME04-US101-AC09 | PreconditionsFence Edit screen is opened.If the app or I fully or partially exclude the building from the fence, then the app should:Fill the excluded area of the building with a red cross pattern. |
| ME04-US101-AC10 | PreconditionsFence Edit screen is opened.ORFence Preview screen is opened.If I zoom out, then the app should:Hover the new displaying parts of road and water with a required pattern.But only if this is part of the same piece of a road and water that is intersected. | - | - |
