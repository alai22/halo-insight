---
title: "(NA) ME04-US19. View Active Fence on the Map"
sidebar_label: "(NA) ME04-US19. View Active Fence on the Map"
sidebar_position: 543
last_modified: "Apr 24, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada , Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-725/[ios]-view-active-fence-on-the-mapAndroid: https://linear.app/fueled/issue/HALO-726/[android]-view-active-fence-on-the-map |
| 08 Apr 2025 Mariya Kolyada created the initial version of a user story.10 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to view my fence on the map so I can view whether my pet is safe or not.

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-US19-AC01 | The app should display the 20 closest fences to the center of the map camera on the My Fences screen. | Figma |
| ME04-US19-AC02 | If I pan the map, then the app should display another 20 closest fences to the map camera. |
| ME04-US19-AC03 | The app should update the list of 20 closest fences each 15 sec.TBD: HALO-19377 - MOB: Refresh fences when map moves for 1+ km Ready for Development |
| ME04-US19-AC04 | Precondition: There are more than 20 fences in the user accountIf I move the map for 1 km or more, the app should:Display 20 fences, which are closer to the center of the visible map area.Refresh schedule of data update (app should start count 15 seconds from beginning). |
| ME04-US19-AC05 | Precondition: There are more than 20 fences in the user accountIf I move the map for less than 1 km, the app should:Display 20 fences, which are closer to the center of the visible map area.Update data with usual schedule, NO refresh is needed. |
| ME04-US19-AC06 | The app should display the fence border with highlighted warning zone.NoteThe calculation logic for both the Protection zone and Warning Area is implemented on the BE side, see technical description in Geofence Zone Calculation. |
| ME04-US19-AC07 | Until the following user stories are implemented, the app should always display the fences in Active state:(NA) ME04-F11. Fence Feedback Settings(NA) ME04-F12. Fence Feedback Status(NA) ME04-US20. Change fence UI depending on Feedback Status |Tech details

Information about fences can be retrieved from GET /account/my/map. The zones array contains the zone type and coordinates of the shape. We are interested in three types of zones

- Safe - Safe Fence Area. On the design, this is the part of the fence that is transparent
- Warning - On the design, this part appears translucent yellow. In the response, we get coordinates, by which we can draw the fence border (yellow line). To draw a yellow translucent zone, we need to cut the Safe zone from the Warning zone polygon
- Danger - We don't currently display this area on the design, but it will come in the response

To get the nearest 20 fences to the current map camera position, we pass the coordinate to the query (query parameters viewport.center.latitude and viewport.center.longitude)On initial load, we may not know the coordinates (e.g., they are not saved locally in the cache). In this case, we can skip the query parameters

The data update is invisible to the user, no indicators are needed.If, in the process of updating the data, we are unable to retrieve it due to some error, these errors are ignored and not displayed to the user in any way

This comment should be resolved in scope of this task: https://github.com/Fueled/halo-collar-android/pull/200#discussion_r2050417253


