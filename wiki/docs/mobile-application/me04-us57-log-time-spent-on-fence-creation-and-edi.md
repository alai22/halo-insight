---
title: "ME04-US57. Log time spent on fence creation and edit + tutorials analytics"
sidebar_label: "ME04-US57. Log time spent on fence creation and edit + tutorials analytics"
sidebar_position: 338
last_modified: "Oct 19, 2023"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Ilona Borsuk [X] |
| HALO-17515 - [NT] MOB+Firebase: ME04-US57. Log time spent on fence creation and edit + tutorials analytics Closed |
| Click here to expand...As of 29 Aug 2023:Mariya Kolyadacreated the initial version of US. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo Product Owner I want to be able to have in Firebase the data related the time spent on fence creation so that I could see if future fence creation improves decrease the time spent on fence creation.

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US57-AC01 | Count and log to the create_fence_success Firebase event:Time spent on fence creation. |
| ME04-US57-AC02 | Time spent on fence creation =from the moment the user triggered the fence creation by clicking the 'Add Fence' button.to the moment the user finishes creation after adding the fence name by clicking the 'Done' button. |
| ME04-US57-AC03 | Count and log to the edit_fence_success Firebase event:Time spent on fence edit. |
| ME04-US57-AC04 | Time spent on fence edit=from the moment the user triggered the fence edit by clicking the 'Edit Fence' button from the 'Fence Details' screen.to the moment the user finishes editing after adding clicking the 'Done' button on the 'Fence Preview with warning area'. |
| ME04-US57-AC05 | Add to create_fence_success Firebase event the fence tutorial parameters defining if the user: saw Fence Tutorial screens automatically displayed for the first fence creation;how much time user spent in the tutorial;on which step user left the tutorial; opened Fence Tutorial screens by clicking on the 'Question mark' button:how much time user spent in the tutorial;on which step user left the tutorial. |
| ME04-US57-AC06 | Add to edit_fence_success Firebase event the fence tutorial parameters defining if the user: saw Fence Tutorial screens automatically displayed for the first fence creation;how much time user spent in the tutorial;on which step user left the tutorial; opened Fence Tutorial screens by clicking on the 'Question mark' button:how much time user spent in the tutorial; |
