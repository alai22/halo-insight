---
title: "ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards"
sidebar_label: "ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards"
sidebar_position: 467
last_modified: "Dec 09, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-21463 - MOB: ME04-US106. Calculate and log minimal distances from hazards to Amplitude Closed |
| As of 09 Oct 2024:Mariya Kolyada created this user story by moving requirements from ME04-US105. Log fence creation, canceled creation, borders edit, name edit and delete events to Amplitude. |# Content

Content User Story Acceptance criteria Main building Road Water Neighboring building Other saved fences

# User Story

\> As a Halo Product Owner I want to view the fence hazards-related analytics in fence Amplitude events so that I can understand how often intersections happen, do they happen with hazards themselved or their buffer zones, how big overlap and etc.

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US106-AC01 | Add the following Amplitude analytics to the fence-related events:Main buildingRoadWaterNeighboring buildingOther saved fences |## Main building

Main building(s):

- 
  - is one building placed on the registered property, when cadastral data is presented for selected location.
  - are all buildings in the area, when there is no cadastral data for selected location.

![](../attachments/232069535/236786589.jpg)

Users are not recommended to place the fence line closer than a buffer zone from a building (currently 5 meters, but it is possible to manage via config).The app displays a warning toast but doesn't forbid saving such fences.

By logging the data bellow we can understand:

- How often fence intersects building
- How often fence intersects buffer of the building → Maybe we need to reconsider 5 meters value.
- Usual distances from fence to building → Maybe our usual user has too small areas around their house.

| Parameter description | Description | Visualization | Fence creation event | Fence failed creation event | Fence borders edit event | Suggested Fence Parameters (auto/simple square) | Saved Edited Fence Parameters | Suggested Fence Parameters (auto/simple square) | Edited Fence Parameters | Updated Fence Parameters |
|---|---|---|---|---|---|---|---|---|---|---|
| Main Building(s) is intersected (boolean) | True - if fence intersects the at least one main building.False - if fence doesn't intersect any main building(s). |  |  | Saved_Fence_Is_Main_Building_Intersected |  | Edited_Fence_Is_Main_Building_Intersected | Updated_Fence_Is_Main_Building_Intersected |
| Minimum distance from Included Main Building(s) | Positive number (meters) - if there is some distance between a fence and building(s) inside it.0 - if fence intersects this building(s). |  | Suggested_Fence_Min_Distance_Included_Main_Building | Saved_Fence_Min_Distance_Included_Main_Building | Suggested_Fence_Min_Distance_Included_Main_Building | Edited_Fence_Min_Distance_Included_Main_Building | Updated_Fence_Min_Distance_Included_Main_Building |
| Buffer of included Main building(s) is intersected (boolean) | True - if fence intersects the buffer of any included main building(s).False - if fence doesn't intersect the buffer of any included main building(s). |  | Saved_Fence_Is_Included_Main_Building_Buffer_Intersected |  | Edited_Fence_Is_Included_Main_Building_Buffer_Intersected | Updated_Fence_Is_Included_Main_Building_Buffer_Intersected |
| Minimum distance from excluded Main Building | Null - if no buildings within 16 zoom map level (~ 1 km from fence).Positive number (meters) - if there is some distance between a fence and building outside it.0 - if fence intersects this building. |  |  | Saved_Fence_Min_Distance_Excluded_Main_Building |  | Edited_Fence_Min_Distance_Excluded_Main_Building | Updated_Fence_Min_Distance_Excluded_Main_Building |
| Buffer of excluded Main building is intersected (boolean) | True - if fence intersects the buffer of any excluded main building.False - if fence doesn't intersect the buffer of any excluded main building. |  | Saved_Fence_Is_Excluded_Main_Building_Buffer_Intersected |  | Edited_Fence_Is_Excluded_Main_Building_Buffer_Intersected | Updated_Fence_Is_Excluded_Main_Building_Buffer_Intersected |## Road

Road is a road line extended to a polygon by adding buffers on both sides of it.

Note

If a road is on the bridge, the app doesn't consider this part of the road as a road.

Buffer = distance till property lines if cadastral is presented for the chosen location. Otherwise, buffer = 5 meters, but it is possible to manage via config.

Road line position is defined by map source data and may be placed anywhere on the real existing physical road.

Users are not recommended to place the fence line closer than a buffer zone of a road line.The app displays a warning toast but doesn't forbid saving such fences.

When the app generates fence automatically based on cadastral data it even sets fence lines on extra 5 meters from the buffer zone (so the fence is not placed right near the 'road polygon' that the app created by adding buffers to a road line).

By logging the data bellow we can understand:

- How often fence intersects road line.
- How often fence intersects buffer of the road line → Maybe we need to reconsider the 5-meter value and distance to property lines.
- Usual distances from fence to road line → Maybe our usual user has too small areas around their house and they can either intersect the road or main building.

| Parameter description | Description | Visualization | Fence creation event | Fence failed creation event | Fence borders edit event | Suggested Fence Parameters (auto/simple square) | Saved Edited Fence Parameters | Suggested Fence Parameters (auto/simple square) | Edited Fence Parameters | Updated Fence Parameters |
|---|---|---|---|---|---|---|---|---|---|---|
| Road line is intersected (boolean) | True - if fence intersects the road line.False - if fence doesn't intersect the road line. |  | Suggested_Fence_Is_Road_Line_Intersected | Saved_Fence_Is_Road_Line_Intersected | Suggested_Fence_Is_Road_Line_Intersected | Edited_Fence_Is_Road_Line_Intersected | Updated_Fence_Is_Road_Line_Intersected |
| Road buffer is intersected (boolean) | True - if fence intersects the road buffer.False - if fence doesn't intersect the road buffer. |  | Suggested_Fence_Is_Road_Buffer_Intersected | Saved_Fence_Is_Road_Buffer_Intersected | Suggested_Fence_Is_Road_Buffer_Intersected | Edited_Fence_Is_Road_Buffer_Intersected | Updated_Fence_Is_Road_Buffer_Intersected |
| Minimum distance to a Road line | Null - if no roads within 16 zoom map level (~ 1 km from fence).0 - if intersects road line (includes case when road line inside fence).Positive (meters) - if road line is outside fence, no intersection with road line. | - | Suggested_Fence_Min_Distance_Road_Line | Saved_Fence_Min_Distance_Road_Line | Suggested_Fence_Min_Distance_Road_Line | Edited_Fence_Min_Distance_Road_Line | Updated_Fence_Min_Distance_Road_Line |## Water

Water is one of the following objects:

- water polygon (wide rivers, lakes, seas, oceans, etc) with no buffer.
- waterway line extended to a polygon by adding buffers on both sides of it (ditch, canal, drain, etc).

Buffer from waterway line = 5 meters, but it is possible to manage via config.

Waterway line position is defined by map source data and may be placed anywhere on the real existing physical waterway. Quite often there may be no water at all in the physical world, but there still may be some dirt and holes.

Users are notified if they place the fence line closer than the water polygon and a buffer zone of a waterway line.The app displays an info toast but doesn't forbid saving such fences.

By logging the data bellow we can understand:

- How often fence intersects water objects.
- How big the area of water and fence overlap is.
- How often fence intersects buffer of the waterway line → Maybe we need to reconsider 5 meters value or remove the buffer at all.
- Usual distances from fence to waterway line.

Note

Sometimes water objects can be considered as water polygons and waterway lines at the same time based on data from Map Box. Thus both types of analytics will be gathered. However waterway-related analytics cannot be verified because there is no waterway line UI for water polygons even on the Standard Map view.

| Parameter description | Description | Visualization | Fence creation event | Fence failed creation event | Fence borders edit event | Suggested Fence Parameters (auto/simple square) | Saved Edited Fence Parameters | Suggested Fence Parameters (auto/simple square) | Edited Fence Parameters | Updated Fence Parameters |
|---|---|---|---|---|---|---|---|---|---|---|
| Water polygon overlapping area | Null - if no water polygons within 16 zoom map level (~ 1 km from fence).0 - if there is no intersection between fence and water polygons.Area (square meters) of fence and water polygon overlap (sum of areas if fence intersects more than one water polygon). |  | Suggested_Fence_Water_Overlapping_Area | Saved_Fence_Water_Overlapping_Area | Suggested_Fence_Water_Overlapping_Area | Edited_Fence_Water_Overlapping_Area | Updated_Fence_Water_Overlapping_Area |
| Waterway line is intersected (boolean) | True - if fence intersects the waterway line.False - if fence doesn't intersect the waterway line. |  | Suggested_Fence_Is_Waterway_Line_Intersected | Saved_Fence_Is_Waterway_Line_Intersected | Suggested_Fence_Is_Waterway_Line_Intersected | Edited_Fence_Is_Waterway_Line_Intersected | Updated_Fence_Is_Waterway_Line_Intersected |
| Waterway buffer is intersected (boolean) | True - if fence intersects the waterway buffer.False - if fence doesn't intersect the waterway buffer. |  | Suggested_Fence_Is_Waterway_Buffer_Intersected | Saved_Fence_Is_Waterway_Buffer_Intersected | Suggested_Fence_Is_Waterway_Buffer_Intersected | Edited_Fence_Is_Waterway_Buffer_Intersected | Updated_Fence_Is_Waterway_Buffer_Intersected |
| Minimum distance to a waterway line | Null - if no waterways within 16 zoom map level (~ 1 km from fence).0 - if intersects waterway line (includes case when waterway line inside fence).Positive (meters)- if waterway line is outside fence, no intersection with waterway line. | - | Suggested_Fence_Min_Distance_Waterway_Line | Saved_Fence_Min_Distance_Waterway_Line | Suggested_Fence_Min_Distance_Waterway_Line | Edited_Fence_Min_Distance_Waterway_Line | Updated_Fence_Min_Distance_Waterway_Line |## Neighboring building

Neighboring building is a building outside a selected registered property based on cadastral data.

The app allows user to intersect neighboring buildings by the fence because we don't expect that pets are allowed to enter that building.

The app doesn't highlight such intersections with some warning toast during edit but it triggers the unique fence pop-up on saving that navigates to the article.

By logging the data bellow we can understand:

- How often fence intersects neighboring buildings.
- How big the area of neighbor building and fence overlap is.

| Parameter description | Description | Visualization | Fence creation event | Fence failed creation event | Fence borders edit event | Suggested Fence Parameters (auto/simple square) | Saved Edited Fence Parameters | Suggested Fence Parameters (auto/simple square) | Edited Fence Parameters | Updated Fence Parameters |
|---|---|---|---|---|---|---|---|---|---|---|
| Neighboring building(s) intersection area | Null - if there is no cadastral data for selected location (because the app consider all buildings as main ones).ORif no neighboring building(s) within 16 zoom map level (~ 1 km from fence).0 - if there is no intersection between fence and any neighboring building.Area (square meters) of fence and neighboring building overlap (sum of areas if fence intersects more than one neighboring building). |  | Suggested_Fence_Neighboring_Buildings_Overlapping_Area | Saved_Fence_Neighboring_Buildings_Overlapping_Area | Suggested_Fence_Neighboring_Buildings_Overlapping_Area | Edited_Fence_Neighboring_Buildings_Overlapping_Area | Updated_Fence_Neighboring_Buildings_Overlapping_Area |## Other saved fences

Other saved fences are fences that have already been saved in the user's account before they triggered the creation of a new fence or edit of one of these fences.

The app doesn't allow to save overlapping fences. All fences saved in account should have some space between them.The app displays an error toast and forbids saving such fences.

The app may generate an auto fence that intersects other existing fences because the user selected a property that already has a fence. User may move a border of a fence during edit so it overlaps other existing fences.

By logging the data bellow we can understand:

- How often fence intersects with other saved fences.
- How big the area of other saved fences and fence overlap is.

| Parameter description | Description | Visualization | Fence creation event | Fence failed creation event | Fence borders edit event | Suggested Fence Parameters (auto/simple square) | Saved Edited Fence Parameters | Suggested Fence Parameters (auto/simple square) | Edited Fence Parameters | Updated Fence Parameters |
|---|---|---|---|---|---|---|---|---|---|---|
| Other saved fence intersection area | 0 - if there is no intersection for the fence being created or edited with other saved fencesArea (square meters) of overlap for the fence being created or edited with other saved fence (sum of areas if fence intersects more than one other saved fence). |  | Suggested_Fence_Other_Fences_Overlapping_Area |  | Suggested_Fence_Other_Fences_Overlapping_Area | Edited_Fence_Other_Fences_Overlapping_Area |  |
