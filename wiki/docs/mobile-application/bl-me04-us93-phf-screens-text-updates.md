---
title: "(BL) ME04-US93. PHF screens' text updates"
sidebar_label: "(BL) ME04-US93. PHF screens' text updates"
sidebar_position: 402
last_modified: "Oct 07, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| BASELINED in (In progress) ME04-F00. Baseline: Add fence with auto-generation by Mariya Kolyada on 07 Oct 2024 |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-19686 - MOB: ME04-US09. PHF screens' text updates Closed |
| As of 19 Mar 2024 :Mariya Kolyada created the initial version of US. |# User Story

\> As a Halo accout owner I want to view more clear, easy to read text and witout grammar mistakes so that I can easily understand the meaning of the screen's text.

# Acceptance criteria

| AC | Description | iOs Design | AndroidDesign | 'No cadastral data' toast | As is | To be | 'Fence preview with water and/or road' screen | Condition | As is | To be | 'Unique Fence' pop-up | As is | To be | 'No building issue confirmation' pop-up | As is | To be |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-US93-AC01 | Update the language following the rules:As isTo beWe created a square fence as there is no data available in the chosen locationWe created a square fence because there is limited map data in this area | We created a square fence as there is no data available in the chosen location | We created a square fence because there is limited map data in this area |  |  |
| We created a square fence as there is no data available in the chosen location | We created a square fence because there is limited map data in this area |
| ME04-US93-AC02 | Update the language following the rules:ConditionAs isTo beIntersection with just waterWe've created a fence for your location, but it does overlap water.We've created a fence for your location, but it overlaps water. Intersection with just roadWe've created a fence for your location, but it does overlap a road.We've created a fence for your location, but it overlaps a road. Intersection with both water and roadWe've created a fence for your location, but it does overlap water and a road.We've created a fence for your location, but it overlaps both water and a road. | Intersection with just water | We've created a fence for your location, but it does overlap water. | We've created a fence for your location, but it overlaps water. | Intersection with just road | We've created a fence for your location, but it does overlap a road. | We've created a fence for your location, but it overlaps a road. | Intersection with both water and road | We've created a fence for your location, but it does overlap water and a road. | We've created a fence for your location, but it overlaps both water and a road. |  |  |
| Intersection with just water | We've created a fence for your location, but it does overlap water. | We've created a fence for your location, but it overlaps water. |
| Intersection with just road | We've created a fence for your location, but it does overlap a road. | We've created a fence for your location, but it overlaps a road. |
| Intersection with both water and road | We've created a fence for your location, but it does overlap water and a road. | We've created a fence for your location, but it overlaps both water and a road. |
| ME04-US93-AC03 | Update the language following the rules:As isTo beDiscover safety tips for your unique fence to protect your dog.Discover safety tips on using your unique fence to protect your dog. | Discover safety tips for your unique fence to protect your dog. | Discover safety tips on using your unique fence to protect your dog. |  | The same as iOS view |
| Discover safety tips for your unique fence to protect your dog. | Discover safety tips on using your unique fence to protect your dog. |
| ME04-US93-AC04 | Update the language following the rules:As isTo beIt seems like your fence is intersecting a building. Please confirm the fence does not actually intersect a building, otherwise the Halo system will not work properly.Your fence seems to intersect a building. Please confirm that it does not actually intersect a building, since this will prevent Halo from working properly. | It seems like your fence is intersecting a building. Please confirm the fence does not actually intersect a building, otherwise the Halo system will not work properly. | Your fence seems to intersect a building. Please confirm that it does not actually intersect a building, since this will prevent Halo from working properly. |  | The same as iOS view |
| It seems like your fence is intersecting a building. Please confirm the fence does not actually intersect a building, otherwise the Halo system will not work properly. | Your fence seems to intersect a building. Please confirm that it does not actually intersect a building, since this will prevent Halo from working properly. |
