---
title: "ME04-US107. Log more fence analytical data to Operational DBs"
sidebar_label: "ME04-US107. Log more fence analytical data to Operational DBs"
sidebar_position: 656
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-21462 - MOB+BE: ME04-US107. Log more fence analytical data to Operational DBs Closed |
| As of 09 Oct 2024 Mariya Kolyada created this user story by moving requirements from ME04-US105. Log fence creation, canceled creation, borders edit, name edit and delete events to Amplitide and updating them after discussion with Meg and Adrian.As of 03 Dec 2024 Mariya Kolyada added parameters related to hazards. |# User Story

\> As a Halo Product Owner I want To be able to have Fence creation, canceled creation, borders edit, Name edit, delete events in Amplitude and Operational DBs so that I can have the access to all Fence event historical data and not just 3 months as Azure AppInsights allows right now.

# Acceptance criteria

Important note

If there is no value for the parameter - MOB should send 'Null' to BE.

| Event parameter | As is | Operational DBs | To be| Operational DBs | Operational DB tech details (field name + notes) | Created Saved Fence Parameters |  | Last Updated Fence Parameters |  |
|---|---|---|---|---|---|---|---|
| User Id |  | User_Id | UserIdAvailable only for the most recent change of a fence |
| Fence Id |  | Fence_Id | FenceIdAvailable only for the most recent change of a fence |
| Fence center location |  |  | GeoFence → Centroid |
| Country |  | Country | LocationFacts_Country |
| State |  | State | LocationFacts_State |
| City |  | City | LocationFacts_City |
| Postal code |  | Postal_Code | LocationFacts_PostalCode |
| Public place type (beach, park, etc) |  | Public_Place_Type | LocationFacts_PublicPlaceName |
| Number of edits after creation |  | Edits_Made | MadeEditsCount |
| Created Timestamp |  | Created_Timestamp | Created |
| Is Auto Fence Suggested (boolean) |  | Is_Auto_Fence_Suggested | IsAutoFenceSuggested |
| Simple square reason (none, no data, no buildings, too big, tech error) |  | Simple_Square_Reason | SimpleSquareReason |
| Is Auto Fence Adopted (boolean)* Only for auto fences, if simple square this parameter should be null. |  | Is_Auto_Fence_Adopted | IsAutoFenceAdopted |
| Saving type (auto, preview, edit) |  | Saving_Type | SavingType |
| Qty of warnings during the creation |  |  |  |
| Qty of warnings on saving |  |  |  |
| Viewed warnings during creation (array of warning types) |  | Created_Fence_Warnings | OriginalFacts_Warnings |
| Area |  | Created_Fence_Area | OriginalFacts_AreaInSquareMeters |
| Fence Posts (array of lat-lon coordinates) |  | Created_Fence_Posts | GeoFence → InitialZonesJson |
| Intersection after saving (None/Water/Road/Main Building/Neighboring Buildings) |  |  |  |
| Zero buildings in a Fence in meters (boolean) |  | Created_Fence_Fully_Enclosed_Buildings | OriginalFacts_FenceFullyEnclosedBuildings |
| Main building parameters (see value details here: ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards#Mainbuilding) |  |
| Main Building(s) is intersected (boolean) |  | Created_Fence_Is_Main_Building_Intersected | OriginalFacts_BuildingFacts_IsIntersected |
| Minimum distance from Included Main Building(s) |  | Created_Fence_Min_Distance_Included_Main_Building | OriginalFacts_BuildingFacts_MinDistanceIncludedInMeters |
| Buffer of included Main building(s) is intersected (boolean) |  | Created_Fence_Is_Included_Main_Building_Buffer_Intersected | OriginalFacts_BuildingFacts_IsIncludedBufferIntersected |
| Minimum distance from excluded Main Building |  | Created_Fence_Min_Distance_Excluded_Main_Building | OriginalFacts_BuildingFacts_ExcludedBufferIntersectedMinDistanceInMeters |
| Buffer of excluded Main building is intersected (boolean) |  | Created_Fence_Is_Excluded_Main_Building_Buffer_Intersected | OriginalFacts_BuildingFacts_IsExcludedBufferIntersected |
| Road (see value details here: ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards#Road) |  |
| Road line is intersected (boolean) |  | Created_Fence_Is_Road_Line_Intersected | OriginalFacts_RoadFacts_IsLineIntersected |
| Road buffer is intersected (boolean) |  | Created_Fence_Is_Road_Buffer_Intersected | OriginalFacts_RoadFacts_IsBufferIntersected |
| Minimum distance to a Road line |  | Created_Fence_Min_Distance_Road_Line | OriginalFacts_RoadFacts_MinDistanceLineInMeters |
| Water (see value details here: ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards#Water) |  |
| Water polygon overlapping area |  | Created_Fence_Water_Overlapping_Area | OriginalFacts_WaterFacts_OverlappingAreaInSquareMeters |
| Waterway line is intersected (boolean) |  | Created_Fence_Is_waterway_Line_Intersected | OriginalFacts_WaterFacts_IsLineIntersected |
| Waterway buffer is intersected (boolean) |  | Created_Fence_Is_waterway_Buffer_Intersected | OriginalFacts_WaterFacts_IsBufferIntersected |
| Minimum distance to a waterway line |  | Created_Fence_Min_Distance_Waterway_Line | OriginalFacts_WaterFacts_MinDistanceLineInMeters |
| Neighboring building (see value details here: ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards#Neighboringbuilding) |  |
| Neighboring building(s) intersection area |  | Created_Fence_Neighboring_Buildings_Overlapping_Area | OriginalFacts_NeighbourFacts_BuildingIntersectionAreaInSquareMeters |
| Last updated timestamp |  | Updated_Timestamp | Updated |
| Qty of warnings during the creation |  |  |  |
| Qty of warnings on saving |  |  |  |
| Viewed warnings during creation (array of warning types) |  | Updated_Fence_Warnings | UpdatedFacts_Warnings |
| Area |  | Updated_Fence_Area | UpdatedFacts_AreaInSquareMeters |
| Fence Posts (array of lat-lon coordinates) |  | Updated_Fence_Posts | GeoFence → ZonesJson |
| Intersection after update (None/Water/Road/Main Building/Neighboring buildings) |  |  |  |
| Zero buildings in a Fence (boolean) |  | Updated_Fence_Fully_Enclosed_Buildings | UpdatedFacts_FenceFullyEnclosedBuildings |
| Main building parameters (see value details here: ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards#Mainbuilding) |  |
| Main Building(s) is intersected (boolean) |  | Updated_Fence_Is_Main_Building_Intersected | UpdatedFacts_BuildingFacts_IsIntersected |
| Minimum distance from Included Main Building(s) |  | Updated_Fence_Min_Distance_Included_Main_Building | UpdatedFacts_BuildingFacts_MinDistanceIncludedInMeters |
| Buffer of included Main building(s) is intersected (boolean) |  | Updated_Fence_Is_Included_Main_Building_Buffer_Intersected | UpdatedFacts_BuildingFacts_IsIncludedBufferIntersected |
| Minimum distance from excluded Main Building with intersected buffer |  | Updated_Fence_Min_Distance_Excluded_Main_Building | UpdatedFacts_BuildingFacts_ExcludedBufferIntersectedMinDistanceInMeters |
| Buffer of excluded Main building is intersected (boolean) |  | Updated_Fence_Is_Excluded_Main_Building_Buffer_Intersected | UpdatedFacts_BuildingFacts_IsExcludedBufferIntersected |
| Road (see value details here: ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards#Road) |  |
| Road line is intersected (boolean) |  | Updated_Fence_Is_Road_Line_Intersected | UpdatedFacts_RoadFacts_IsLineIntersected |
| Road buffer is intersected (boolean) |  | Updated_Fence_Is_Road_Buffer_Intersected | UpdatedFacts_RoadFacts_IsBufferIntersected |
| Minimum distance to a Road line |  | Updated_Fence_Min_Distance_Road_Line | UpdatedFacts_RoadFacts_MinDistanceLineInMeters |
| Water (see value details here: ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards#Water) |  |
| Water polygon overlapping area |  | Updated_Fence_Water_Overlapping_Area | UpdatedFacts_WaterFacts_OverlappingAreaInSquareMeters |
| Waterway line is intersected (boolean) |  | Updated_Fence_Is_waterway_Line_Intersected | UpdatedFacts_WaterFacts_IsLineIntersected |
| Waterway buffer is intersected (boolean) |  | Updated_Fence_Is_waterway_Buffer_Intersected | UpdatedFacts_WaterFacts_IsBufferIntersected |
| Minimum distance to a waterway line |  | Updated_Fence_Min_Distance_Waterway_Line | UpdatedFacts_WaterFacts_MinDistanceLineInMeters |
| Neighboring building (see value details here: ME04-US106. Amplitude. Calculate and log minimal distances/areas of intersection with hazards#Neighboringbuilding) |  |
| Neighboring building(s) intersection area |  | Updated_Fence_Neighboring_Buildings_Overlapping_Area | UpdatedFacts_NeighbourFacts_BuildingIntersectionAreaInSquareMeters |
