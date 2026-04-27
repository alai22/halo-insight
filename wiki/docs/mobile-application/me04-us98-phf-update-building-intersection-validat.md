---
title: "ME04-US98. PHF. Update building intersection validation"
sidebar_label: "ME04-US98. PHF. Update building intersection validation"
sidebar_position: 672
last_modified: "May 28, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-20278 - MOB: ME04-US98. PHF. Update building intersection validation Closed |
| As of 15 May 2024:Mariya Kolyada created the initial version of US. |# User Story

\> As a Halo accout owner I want that I have bigger area required from the building inside my fence so my dog does NOT recieve wrong feedback.

# Acceptance criteria

| AC | Description | iOs design | Android design | As is | To be | As is | To be | As is | To be | As is | To be | As is | To be |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-US98-AC01 | Update the validation on the fence intersection with the building following the rules:As isTo beIf user intersects the building itself or an area 15 feet from it, then the app should display the building intersection toast. If user intersects the building itself or an area '4.1 meters + warning zone distance' from it, then the app should display the building intersection toast. | If user intersects the building itself or an area 15 feet from it, then the app should display the building intersection toast. | If user intersects the building itself or an area '4.1 meters + warning zone distance' from it, then the app should display the building intersection toast. |  |
| If user intersects the building itself or an area 15 feet from it, then the app should display the building intersection toast. | If user intersects the building itself or an area '4.1 meters + warning zone distance' from it, then the app should display the building intersection toast. |
| ME04-US98-AC02 | Update the building purple visualization UI following the rules:As isTo beThe app should hover over the building and rear 15 feet from it with the purple building UI layer.The app should hover over the building and area '4.1 meters + warning zone distance' from it with the purple building UI layer. | The app should hover over the building and rear 15 feet from it with the purple building UI layer. | The app should hover over the building and area '4.1 meters + warning zone distance' from it with the purple building UI layer. |
| The app should hover over the building and rear 15 feet from it with the purple building UI layer. | The app should hover over the building and area '4.1 meters + warning zone distance' from it with the purple building UI layer. |
| ME04-US98-AC03 | Update the language of the building intersection toast:As isTo beYour fence appears to be closer than 15 feet from a house/building.Your fence appears to be closer than 20 feet from a house/building. | Your fence appears to be closer than 15 feet from a house/building. | Your fence appears to be closer than 20 feet from a house/building. |
| Your fence appears to be closer than 15 feet from a house/building. | Your fence appears to be closer than 20 feet from a house/building. |
| ME04-US98-AC04 | Update an image on the Step 5 screen of the Fence Tutorial. | www.figma.com | TBD |
| ME04-US98-AC05 | Update the language on the Step 5 screen of the Fence Tutorial:As isTo beAt least 15ft outside your entire homeAt least 15ft from public roadsAligned with existing barriers (like fences or hedges)At least 15ft from public roadsAt least 20ft outside your entire homeAligned with existing barriers (like fences or hedges) | At least 15ft outside your entire homeAt least 15ft from public roadsAligned with existing barriers (like fences or hedges) | At least 15ft from public roadsAt least 20ft outside your entire homeAligned with existing barriers (like fences or hedges) |
| At least 15ft outside your entire homeAt least 15ft from public roadsAligned with existing barriers (like fences or hedges) | At least 15ft from public roadsAt least 20ft outside your entire homeAligned with existing barriers (like fences or hedges) |
| ME04-US98-AC06 | Update the current config value of the required distance between the building and fence border excluding the warning zone:As isTo be5 meters4.1 meters | 5 meters | 4.1 meters | - | - |
| 5 meters | 4.1 meters |
