---
title: "ME04-US105. Log fence creation, canceled creation, borders edit, name edit and delete events to Amplitude"
sidebar_label: "ME04-US105. Log fence creation, canceled creation, borders edit, name edit and delete events to Amplitude"
sidebar_position: 455
last_modified: "Dec 03, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-21115 - MOB: ME04-US105. Log fence creation, canceled creation, borders edit, name edit and delete events to Amplitude Closed |
| As of 16 Sep 2024:Mariya Kolyada Created the initial version of US.As of 20 Sep 2024 Mariya Kolyada after discussion with Adrian, Meg and Dmitry.As of 24 Sep 2024 Mariya Kolyada added Amplitude parameters Names.As of 09 Oct 2024 Mariya Kolyada removed part of the requirements to separate user stories + updated parameter names with capitalization.As of 10 Oct 2024 Mariya Kolyada undone strikethrough of Suggested_Auto_Fence_Posts and Edited_Posts |# User Story

\> As a Halo Product Owner I want To be able to have Fence creation, canceled creation, borders edit, Name edit, delete events in Amplitude and Operational DBs so that I can have the access to all Fence event historical data and not just 3 months as Azure AppInsights allows right now.

# Acceptance criteria

| AC | Description | Event parameter | As is | AppInsights | To be | Amplitude | Suggested Fence Parameters (auto/simple square) | Saved Edited Fence Parameters | Event parameter | As is | AppInsights | To be | Amplitude | Suggested Fence Parameters (auto/simple square) | Edited Fence Parameters | Event parameter | As is | AppInsights | To be | Amplitude | Updated Fence Parameters | Event parameter | As is | AppInsights | To be | Amplitude | Event parameter | As is | AppInsights | To be | Amplitude | Event parameter | As is | AppInsights | To be | Amplitude |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-US105-AC01 | Log the Fence Created Event with the following updates to Amplitude and/or Operational DBs:Event parameterAs is | AppInsightsTo be | AmplitudeTimestampCreated_TimestampUser IdUser_IdFence IdFence_IdFence center location Country CountryState StateCity CityStreet AddressPostal codePublic place type (beach, park, etc)Public_Place_TypeIs Auto Fence Suggested (boolean)Is_Auto_Fence_SuggestedSimple square reason (none, no data, no buildings, too big, tech error)Simple_Square_ReasonIs Auto Fence Adopted (boolean)* Only for auto fences, if simple square this parameter should be null.Is_Auto_Fence_AdoptedTime Spent EditingTime_Spent_EditingSaving type (auto, preview, edit)Saving_TypeSuggested Fence Parameters (auto/simple square)AreaSuggested_Fence_AreaFence Posts (array of lat-lon coordinates) Suggested_Fence_PostsIntersection after autogeneration (None/Water/Road/Other Fences)Saved Edited Fence ParametersWarnings (array of warning types)Saved_WarningsAreaSaved_AreaFence Posts (array of lat-lon coordinates) Saved_PostsIntersection after autogeneration (None/Water/Road/Main Building/Other Fences)Zero buildings in a Fence (boolean)Fully_Enclosed_BuildingsUnique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection)* separate event nowUnique_Fence_Reason | Timestamp |  | Created_Timestamp | User Id |  | User_Id | Fence Id |  | Fence_Id | Fence center location |  |  | Country |  | Country | State |  | State | City |  | City | Street Address |  |  | Postal code |  |  | Public place type (beach, park, etc) |  | Public_Place_Type | Is Auto Fence Suggested (boolean) |  | Is_Auto_Fence_Suggested | Simple square reason (none, no data, no buildings, too big, tech error) |  | Simple_Square_Reason | Is Auto Fence Adopted (boolean)* Only for auto fences, if simple square this parameter should be null. |  | Is_Auto_Fence_Adopted | Time Spent Editing |  | Time_Spent_Editing | Saving type (auto, preview, edit) |  | Saving_Type | Area |  | Suggested_Fence_Area | Fence Posts (array of lat-lon coordinates) |  | Suggested_Fence_Posts | Intersection after autogeneration (None/Water/Road/Other Fences) |  |  | Warnings (array of warning types) |  | Saved_Warnings | Area |  | Saved_Area | Fence Posts (array of lat-lon coordinates) |  | Saved_Posts | Intersection after autogeneration (None/Water/Road/Main Building/Other Fences) |  |  | Zero buildings in a Fence (boolean) |  | Fully_Enclosed_Buildings | Unique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection) | * separate event now | Unique_Fence_Reason |
| Timestamp |  | Created_Timestamp |
| User Id |  | User_Id |
| Fence Id |  | Fence_Id |
| Fence center location |  |  |
| Country |  | Country |
| State |  | State |
| City |  | City |
| Street Address |  |  |
| Postal code |  |  |
| Public place type (beach, park, etc) |  | Public_Place_Type |
| Is Auto Fence Suggested (boolean) |  | Is_Auto_Fence_Suggested |
| Simple square reason (none, no data, no buildings, too big, tech error) |  | Simple_Square_Reason |
| Is Auto Fence Adopted (boolean)* Only for auto fences, if simple square this parameter should be null. |  | Is_Auto_Fence_Adopted |
| Time Spent Editing |  | Time_Spent_Editing |
| Saving type (auto, preview, edit) |  | Saving_Type |
| Area |  | Suggested_Fence_Area |
| Fence Posts (array of lat-lon coordinates) |  | Suggested_Fence_Posts |
| Intersection after autogeneration (None/Water/Road/Other Fences) |  |  |
| Warnings (array of warning types) |  | Saved_Warnings |
| Area |  | Saved_Area |
| Fence Posts (array of lat-lon coordinates) |  | Saved_Posts |
| Intersection after autogeneration (None/Water/Road/Main Building/Other Fences) |  |  |
| Zero buildings in a Fence (boolean) |  | Fully_Enclosed_Buildings |
| Unique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection) | * separate event now | Unique_Fence_Reason |
| ME04-US105-AC02 | Log the Fence Creation Canceled Event with the following updates to Amplitude and/or Operational DBs:Event parameterAs is | AppInsightsTo be | AmplitudeTimestampCreated_TimestampUser IdUser_IdFence center location Country CountryState StateCity CityStreet AddressPostal codePublic place type (beach, park, etc)Public_Place_TypeIs Auto Fence Suggested (boolean)Is_Auto_Fence_SuggestedSimple square reason (none, no data, no buildings, too big, tech error)Simple_Square_ReasonIs Auto Fence Adopted (boolean)* Only for auto fences, if simple square this parameter should be null.Is_Auto_Fence_AdoptedTime Spent EditingTime_Spent_EditingSuggested Fence Parameters (auto/simple square)AreaSuggested_Fence_AreaFence Posts (array of lat-lon coordinates) Suggested_Fence_PostsIntersection after autogeneration (None/Water/Road/Other Fences)Edited Fence ParametersWarnings (array of warning types)Edited_WarningsAreaEdited_AreaFence Posts (array of lat-lon coordinates) Edited_PostsIntersection after autogeneration (None/Water/Road/Main Building/Other Fences)Zero buildings in a Fence (boolean)Fully_Enclosed_BuildingsUnique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection)* separate event nowUnique_Fence_Reason | Timestamp |  | Created_Timestamp | User Id |  | User_Id | Fence center location |  |  | Country |  | Country | State |  | State | City |  | City | Street Address |  |  | Postal code |  |  | Public place type (beach, park, etc) |  | Public_Place_Type | Is Auto Fence Suggested (boolean) |  | Is_Auto_Fence_Suggested | Simple square reason (none, no data, no buildings, too big, tech error) |  | Simple_Square_Reason | Is Auto Fence Adopted (boolean)* Only for auto fences, if simple square this parameter should be null. |  | Is_Auto_Fence_Adopted | Time Spent Editing |  | Time_Spent_Editing | Area |  | Suggested_Fence_Area | Fence Posts (array of lat-lon coordinates) |  | Suggested_Fence_Posts | Intersection after autogeneration (None/Water/Road/Other Fences) |  |  | Warnings (array of warning types) |  | Edited_Warnings | Area |  | Edited_Area | Fence Posts (array of lat-lon coordinates) |  | Edited_Posts | Intersection after autogeneration (None/Water/Road/Main Building/Other Fences) |  |  | Zero buildings in a Fence (boolean) |  | Fully_Enclosed_Buildings | Unique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection) | * separate event now | Unique_Fence_Reason |
| Timestamp |  | Created_Timestamp |
| User Id |  | User_Id |
| Fence center location |  |  |
| Country |  | Country |
| State |  | State |
| City |  | City |
| Street Address |  |  |
| Postal code |  |  |
| Public place type (beach, park, etc) |  | Public_Place_Type |
| Is Auto Fence Suggested (boolean) |  | Is_Auto_Fence_Suggested |
| Simple square reason (none, no data, no buildings, too big, tech error) |  | Simple_Square_Reason |
| Is Auto Fence Adopted (boolean)* Only for auto fences, if simple square this parameter should be null. |  | Is_Auto_Fence_Adopted |
| Time Spent Editing |  | Time_Spent_Editing |
| Area |  | Suggested_Fence_Area |
| Fence Posts (array of lat-lon coordinates) |  | Suggested_Fence_Posts |
| Intersection after autogeneration (None/Water/Road/Other Fences) |  |  |
| Warnings (array of warning types) |  | Edited_Warnings |
| Area |  | Edited_Area |
| Fence Posts (array of lat-lon coordinates) |  | Edited_Posts |
| Intersection after autogeneration (None/Water/Road/Main Building/Other Fences) |  |  |
| Zero buildings in a Fence (boolean) |  | Fully_Enclosed_Buildings |
| Unique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection) | * separate event now | Unique_Fence_Reason |
| ME04-US105-AC03 | Log the Fence Edited Event with the following updates to Amplitude and/or Operational DBs:Event parameterAs is | AppInsightsTo be | AmplitudeTimestampSaved_TimestampUser IdUser_IdFence IdFence_IdFence center location Country CountryState StateCity CityStreet AddressPostal codePublic place type (beach, park, etc)Public_Place_TypeTime Spent EditingTime_Spent_EditingUpdated Fence ParametersWarnings (array of warning types)Updated_WarningsAreaUpdated_AreaFence Posts (array of lat-lon coordinates) Updated_PostsIntersection after autogeneration (None/Water/Road/Main Building/Other Fences)Zero buildings in a Fence (boolean)Fully_Enclosed_BuildingsUnique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection)* separate event nowUnique_Fence_Reason | Timestamp |  | Saved_Timestamp | User Id |  | User_Id | Fence Id |  | Fence_Id | Fence center location |  |  | Country |  | Country | State |  | State | City |  | City | Street Address |  |  | Postal code |  |  | Public place type (beach, park, etc) |  | Public_Place_Type | Time Spent Editing |  | Time_Spent_Editing | Warnings (array of warning types) |  | Updated_Warnings | Area |  | Updated_Area | Fence Posts (array of lat-lon coordinates) |  | Updated_Posts | Intersection after autogeneration (None/Water/Road/Main Building/Other Fences) |  |  | Zero buildings in a Fence (boolean) |  | Fully_Enclosed_Buildings | Unique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection) | * separate event now | Unique_Fence_Reason |
| Timestamp |  | Saved_Timestamp |
| User Id |  | User_Id |
| Fence Id |  | Fence_Id |
| Fence center location |  |  |
| Country |  | Country |
| State |  | State |
| City |  | City |
| Street Address |  |  |
| Postal code |  |  |
| Public place type (beach, park, etc) |  | Public_Place_Type |
| Time Spent Editing |  | Time_Spent_Editing |
| Warnings (array of warning types) |  | Updated_Warnings |
| Area |  | Updated_Area |
| Fence Posts (array of lat-lon coordinates) |  | Updated_Posts |
| Intersection after autogeneration (None/Water/Road/Main Building/Other Fences) |  |  |
| Zero buildings in a Fence (boolean) |  | Fully_Enclosed_Buildings |
| Unique Fence reason (none, Road intersection, all building exclusion, neighboring building intersection) | * separate event now | Unique_Fence_Reason |
| ME04-US105-AC04 | Log the Fence Deleted Event with the following updates to Amplitude and/or Operational DBs:Event parameterAs is | AppInsightsTo be | AmplitudeTimestampDeleted_TimestampUser IdUser_IdFence IdFence_Id | Timestamp |  | Deleted_Timestamp | User Id |  | User_Id | Fence Id |  | Fence_Id |
| Timestamp |  | Deleted_Timestamp |
| User Id |  | User_Id |
| Fence Id |  | Fence_Id |
| ME04-US105-AC05 | Log the Fence Name Edited Event with the following updates to Amplitude and/or Operational DBs:Event parameterAs is | AppInsightsTo be | AmplitudeTimestampEdited_TimestampUser IdUser_IdFence IdFence_IdFence Name BeforeFence_Name_BeforeFence Name AfterFence_Name_After | Timestamp |  | Edited_Timestamp | User Id |  | User_Id | Fence Id |  | Fence_Id | Fence Name Before |  | Fence_Name_Before | Fence Name After |  | Fence_Name_After |
| Timestamp |  | Edited_Timestamp |
| User Id |  | User_Id |
| Fence Id |  | Fence_Id |
| Fence Name Before |  | Fence_Name_Before |
| Fence Name After |  | Fence_Name_After |
| ME04-US105-AC06 | Stop logging the Unique Fence EventEvent parameterAs is | AppInsightsTo be | AmplitudeTimestampRoad intersection (boolean)All buildings exclusion (boolean)Neighbor building intersection (boolean) | Timestamp |  |  | Road intersection (boolean) |  |  | All buildings exclusion (boolean) |  |  | Neighbor building intersection (boolean) |  |  |
| Timestamp |  |  |
| Road intersection (boolean) |  |  |
| All buildings exclusion (boolean) |  |  |
| Neighbor building intersection (boolean) |  |  |
