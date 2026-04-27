---
title: "(NI) ME03-US120 FW: Inform the user that collar has no issues"
sidebar_label: "(NI) ME03-US120 FW: Inform the user that collar has no issues"
sidebar_position: 310
last_modified: "May 15, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages |
|---|---|---|---|
| DRAFT |
| Kiryl Trafimau |
| HALO-16227 - FW: inform the user that collar has no issues Open |
| MQTT Communication implemented on the back-end |# User Story

\> As a get notified that the collar is not broken without checking settings so that I can use it for dog's protection

# Acceptance Criteria

| ID | Acceptance criteria |  | FW | GIVEN | WHEN | THEN |
|---|---|---|---|---|---|---|
| ME03-US120-AC01 | GIVENCollar did not get from the BE trigger (via TWIN) that catastrophic issue happened WHENThe collar is taken off from the chargerTHENActions should start on the collar:short blinking WHITE 5 times once every second on the Logo Light | Collar did not get from the BE trigger (via TWIN) that catastrophic issue happened | The collar is taken off from the charger | Actions should start on the collar:short blinking WHITE 5 times once every second on the Logo Light |
| Collar did not get from the BE trigger (via TWIN) that catastrophic issue happened |
| The collar is taken off from the charger |
| Actions should start on the collar:short blinking WHITE 5 times once every second on the Logo Light |
