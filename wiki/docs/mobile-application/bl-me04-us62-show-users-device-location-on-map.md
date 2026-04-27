---
title: "[BL] ME04-US62. Show user's device location on map"
sidebar_label: "[BL] ME04-US62. Show user's device location on map"
sidebar_position: 347
last_modified: "Mar 04, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes | Estimates |
|---|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-18048 - MOB: ME04-US62. Show user's device location on map Closed |
| Click here to expand...As of 08 Oct 2023:Mariya Kolyadacreated the initial version of US.As of 18 Oct 2023 Added Jira ticket and added criterions with links to screens when this button should be added. |
| MOB: 0.25 per screenQA: 0.5 per screen |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo acount owner I want to be able move the map on my user's device location so that I could easily open the place where I want to create a fence.

# Acceptance criteria

| AC | Description | iOs design | Android design |
|---|---|---|---|
| ME04-US62-AC01 | Add the 'My Location' button on the (BL) ME04-US58. Fence location positioning step. |  |  |
| ME04-US62-AC02 | Add the 'My Location' button on the [Outdated] ME04-US61. Fence preview with warning area step. |
| ME04-US62-AC03 | PreconditionApp has the user's device location accessIf I click the 'My Location' button, then the app should:Display the Map part with my location in the center and hovered by the 'Fence Location Position' pin. |
| ME04-US62-AC04 | PreconditionApp has no user's device location accessIf I click the 'My Location' button, then the app should:Display the M55 Disabled Location pop-up. | - | - |
