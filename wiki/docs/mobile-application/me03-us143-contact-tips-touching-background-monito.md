---
title: "ME03-US143. Contact tips touching background monitoring + Daily diagnostic"
sidebar_label: "ME03-US143. Contact tips touching background monitoring + Daily diagnostic"
sidebar_position: 434
last_modified: "Aug 16, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| DRAFT |
| Mariya Kolyada |
| HALO-20892 - FW+BA: ME03-US143. Contact tips touching background monitoring + Daily Diagnostic In Analysis or Clarification |
| Click here to expand...As of 25 Jul 2024 Mariya Kolyadacreated the initial version of US. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo acount owner I want that I want to view in Daily diagnostic report if my pet's collar contact tips did't touch the skin sometime during the day so that I can imrove it next time I wear the collar on my pet.

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-US143-AC01 | PreconditionCollar generation is Halo 4While the pet is moving, the Collar's FW should perform the contact tips touching test every 10 seconds. |
| ME03-US143-AC02 | PreconditionCollar generation is Halo 4While the pet is at rest, the Collar's FW should pause performing the contact tips touching test until the pet begins moving again. |
| ME03-US143-AC03 | Add collar contact tips touching test daily data results to the Daily diagnostic feature. |
