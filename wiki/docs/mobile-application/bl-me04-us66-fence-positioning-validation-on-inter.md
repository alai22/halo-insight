---
title: "[BL] ME04-US66. Fence Positioning. Validation on intersection with road and existing fence + zoom out"
sidebar_label: "[BL] ME04-US66. Fence Positioning. Validation on intersection with road and existing fence + zoom out"
sidebar_position: 352
last_modified: "Mar 04, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-18054 - MOB: ME04-US66. Fence Positioning. Validation on intersection with road and existing fence + zoom out Closed |
| Click here to expand...As of 17 Oct 2023:Mariya Kolyadacreated the initial version of US.As of 18 Oct 2023 Mariya Kolyada added the Jira ticket. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo acount owner I want to view error related to intersection with road and existing fence during fence location positioning so that I can understand why I cannont auto-generate the fence and move to the next step..

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US66-AC01 | Precondition'Fence Location Position' is opened.'Fence Location Position' pin is on the existing fence.If I click the 'Confirm' button, then the app should:Display the Fence overlap error toast (see ME04-F00-M7 in ME04-F00. Add fence without GPS#TableME04-1Drawafenceerrors/warnings).NoteThe app should forbid proceeding with fence creation until the user eliminates the intersection with the existing fence. |
| ME04-US66-AC02 | Precondition'Fence Location Position' is opened.'Fence Location Position' pin is on the road or in an area including 15 feet from it.If I click the 'Confirm' button, then the app should:Display the Fence road intersection toast (see ME04-US64-M3 in ME04-US64. Fence edit. Add roads, buildings and water intersection validation#TableME04-US64-T1)NoteThe app should forbid proceeding with fence creation until the user eliminates the intersection with the road. |
| ME04-US66-AC03 | Precondition'Fence Location Position' is opened.If the zoom scale on the map becomes less than 16 and it is hard to put the 'Fence Location Position' pin accurately.If I click the 'Confirm' button, then the app should:Display the Zoom out error toast (see ME04-F00-M1 in ME04-F00. Add fence without GPS#TableME04-1Drawafenceerrors/warnings)NoteThe app should forbid proceeding with fence creation until the user eliminates the intersection with the road. |
