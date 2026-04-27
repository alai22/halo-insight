---
title: "ME04-US73. Fence Edit + Preview. Highlight roads, water and building zones when fence intersects them"
sidebar_label: "ME04-US73. Fence Edit + Preview. Highlight roads, water and building zones when fence intersects them"
sidebar_position: 372
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Kirill Akulich |
| HALO-17713 - MOB: ME04-US73. Fence Edit + Preview. Highlight roads, water and building zones when fence intersects them Closed |
| Click here to expand...As of 08 Dec 2023:Mariya Kolyadacreated the initial version of US with links to draft designs in Figma.As of 13 Dec 2023 Mariya Kolyada updated US after approval on BA call. |# Contents

User Stories Acceptance criteria

# User Stories

\> As a Halo acount owner I want to view the highlited road/building/water and area of overlapping with my fence so that I can easily understand what should I do to avoid intersection.

# Acceptance criteria

| AC | Description | iOs design | Android design |
|---|---|---|---|
| ME04-US73-AC01 | PreconditionsFence Edit screen is opened.If the app or I put fence post(s) on another existing fence in my account, then the app should:Fill the overlapping area of the editing fence with another existing fence in a transparent red color.Color in dark red the borders of another existing fence inside the editing fence.NoteThe app should stop returning the moved post to the previous state. There is no need anymore because we now have visualization of intersections. |  |  |
| ME04-US73-AC02 | PreconditionsFence Edit screen is opened.ORFence Preview with road or water overlapping is opened.If the app or I put fence post(s) on the road, then the app should:Hover the visible part of the road with an orange transparent pattern of diagonal lines.Fill the area of fence and road overlapping with a solid orange color. |  |  |
| ME04-US73-AC03 | PreconditionsFence Edit screen is opened.ORFence Preview with road or water overlapping is opened.If the app or I put fence post(s) on the water, then the app should:Hover the visible part of the water with a blue transparent pattern of wave lines.Fill the area of fence and road overlapping with a solid blue color. |  |  |
| ME04-US73-AC04 | PreconditionsFence Edit screen is opened.ORFence Preview screen is opened.The app should always hover over the buildings inside the fence with a purple transparent pattern of circles. |
| ME04-US73-AC05 | PreconditionsFence Edit screen is opened.If the app or I fully or partially exclude the building from the fence, then the app should:Fill the excluded area of the building with a solid purple color. |  |  |
| ME04-US73-AC06 | PreconditionsFence Edit screen is opened.ORFence Preview screen is opened.If I zoom out, then the app should:Hover the new displaying parts of road and water with a required pattern. | - | - |
