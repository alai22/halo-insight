---
title: "(BL) ME04-US97. PHF. Update distance from building and property boundaries"
sidebar_label: "(BL) ME04-US97. PHF. Update distance from building and property boundaries"
sidebar_position: 409
last_modified: "Oct 07, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| BASELINED in (In progress) ME04-F00. Baseline: Add fence with auto-generation by Mariya Kolyada on 07 Oct 2024 |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Zakhar Makarevich |
| HALO-20178 - MOB+BE: ME04-US97. PHF. Update distance from building and property boundaries Closed |
| As of 01 May 2024 - 03 May 2024 :Mariya Kolyada created the initial version of US. |# User Story

\> As a Halo accout owner I want that my fence border that is not near to the road is far from property lines on the warning zone distance so I my dog recieve the first feedback right on teh property line and not earlier.

# Acceptance criteria

| AC | Description | iOs design | Android design | As is | To be | As is | To be | As is | To be | As is | To be |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-US97-AC01 | Update the fence border generation where there is no road and enough distance to the building inside following the rules:As isTo beGenerate fence boundaries clearly along the property line.Generate fence boundaries by retreating the warning zone distance from the property line. | Generate fence boundaries clearly along the property line. | Generate fence boundaries by retreating the warning zone distance from the property line. | - | - |
| Generate fence boundaries clearly along the property line. | Generate fence boundaries by retreating the warning zone distance from the property line. |
| ME04-US97-AC02 | Update the fence border generation where there is not enough space between the property line and the building inside following the rules:As isTo beGenerate fence boundaries so there are at least 15 feet between the building and the fence border.Generate fence boundaries so there are at least 15 feet + the warning zone distance between the building and the fence border. | Generate fence boundaries so there are at least 15 feet between the building and the fence border. | Generate fence boundaries so there are at least 15 feet + the warning zone distance between the building and the fence border. |  |
| Generate fence boundaries so there are at least 15 feet between the building and the fence border. | Generate fence boundaries so there are at least 15 feet + the warning zone distance between the building and the fence border. |
| ME04-US97-AC03 | Update the validation on the fence intersection with the building following the rules:As isTo beIf user intersects the building itself or an area 15 feet from it, then the app should display the building intersection toast. If user intersects the building itself or an area '15 feet + warning zone distance' from it, then the app should display the building intersection toast. | If user intersects the building itself or an area 15 feet from it, then the app should display the building intersection toast. | If user intersects the building itself or an area '15 feet + warning zone distance' from it, then the app should display the building intersection toast. |
| If user intersects the building itself or an area 15 feet from it, then the app should display the building intersection toast. | If user intersects the building itself or an area '15 feet + warning zone distance' from it, then the app should display the building intersection toast. |
| ME04-US97-AC04 | Update the building purple visualization UI following the rules:As isTo beThe app should hover over the building and rear 15 feet from it with the purple building UI layer.The app should hover over the building and area '15 feet + warning zone distance' from it with the purple building UI layer. | The app should hover over the building and rear 15 feet from it with the purple building UI layer. | The app should hover over the building and area '15 feet + warning zone distance' from it with the purple building UI layer. |
| The app should hover over the building and rear 15 feet from it with the purple building UI layer. | The app should hover over the building and area '15 feet + warning zone distance' from it with the purple building UI layer. |
| ME04-US97-AC05 | Update an image on the Step 5 screen of the Fence Tutorial. |  | TBD |
| ME04-US97-AC06 | The required distance between the fence border and the road should remain the same. | - | - |
| ME04-US97-AC07 | Add the possibility to manage the warning zone distance in meters via config.The current value is 2 meters. | - | - |
| ME04-US97-AC08 | Add the possibility to manage the required distance between road and fence border via config.The current value is 5 meters. | - | - |
| ME04-US97-AC09 | Add the possibility to manage the required distance between the building and fence border excluding the warning zone via config.The current value is 5 meters. | - | - |
| ME04-US97-AC10 | Add the possibility to manage the simple square area size via config.The current value is 1500 m2. | - | - |
| ME04-US97-AC12 | Add the possibility of managing the property registered size threshold that triggers the replacement of the autogenerated fence with the simple square fence.The current value is 50000 m2. | - | - |
| ME04-US97-AC13 | Add the possibility to manage the required distance between the river line and fence border via config.The current value is 5 meters. |  |  |
