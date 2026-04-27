---
title: "ME04-US108. Add fence centroid, user location and distance between them to fence-related Amplitude events"
sidebar_label: "ME04-US108. Add fence centroid, user location and distance between them to fence-related Amplitude events"
sidebar_position: 474
last_modified: "Dec 16, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-22106 - MOB: ME04-US108. Add fence centroid, user location and distance between them to fence-related Amplitude events Closed |
| As of 10 Dec 2024:Mariya Kolyada Created the initial version of US. |# User Story

\> As a Halo Product Owner I want to view the fence center and user location and the distance between them in fence creation, canceled creation, and edit Amplitude events so that I can understand how often users create fences for the future VS at the moment and in the place they are now.

# Acceptance criteria

| AC | Description | Event parameter | To be | Amplitude |
|---|---|---|---|
| ME04-US108-AC01 | Add the following parameters:Event parameterTo be | AmplitudeFence center location (lat, lang) Fence_CentroidUser location (lat, lang)User_LocationDistance between user location and fence center locationDistance_User_Location_To_Fence_Centroidto the following fence events in Amplitude: Fence Created EventFence Creation Canceled Event Fence Edited EventNoteLog the User location at the moment edit or creation is triggered.No further value updates are needed if the user changes location during the fence edit. | Fence center location (lat, lang) | Fence_Centroid | User location (lat, lang) | User_Location | Distance between user location and fence center location | Distance_User_Location_To_Fence_Centroid |
| Fence center location (lat, lang) | Fence_Centroid |
| User location (lat, lang) | User_Location |
| Distance between user location and fence center location | Distance_User_Location_To_Fence_Centroid |
