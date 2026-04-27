---
title: "ME05-FE11. Feedback and notification logic"
sidebar_label: "ME05-FE11. Feedback and notification logic"
sidebar_position: 691
last_modified: "Oct 07, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story (checked by dev team) |
| IN PROGRESS |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| TBD |### Content

Content Table ME05-FE11-1 Feedback and Notifications logic description for Fence Zone Event 1 - Warning (case 1) Event 2 - Warning (case 2) Event 3 - Boundary Event 4 - Emergency Feedback (case 1) Event 5- Emergency Feedback (case 2) Event 8 - Pet left fence 30 min ago Event 6 - Pet returns in the fence

### Table ME05-FE11-1 Feedback and Notifications logic description for Fence Zone

| Event # | Possible events (conditions should be performed simultaneously) | FENCES ON |  | FENCES OFF | Feedback | Notifications about feedback | Notifications about pet geofence |  | Feedback | Notifications about feedbacks | Notifications about pet geofence |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Event 1 - Warning (case 1) | Condition 1. A pet is in a fence warning zone (warning zone = about 2 meters or less to the unsafe zone border).Condition 2. The previous time a pet was determined in a safe area. (it means that a pet was not in a fence warning zone, see ME04-US03-AC06). | Warning Feedback is applied once (collar). | NT1. Applied warning feedback - fenceis displayed (app). | No pet geofence notifications | No feedbacks | No feedback notifications | NT4. Pet is near to the unsafe zoneis displayed. (app) |
| Event 2 - Warning (case 2) | Condition 1. A pet stays in a fence warning zone more than 2 secCondition 2. A pet was in a fence warning zone previous time. | Apply warning feedback every 2 sec until a pet is more than 2 meters from an unsafe zone (collar) | No notifications | No pet geofence notifications | No feedbacks | No feedback notifications | No pet geofence notifications |
| Event 3 - Boundary | Condition 1 A pet is determined in an unsafe zone.Condition 2. A pet was determined in a fence warning zone or in beacon zone previous time. | Apply boundary feedback once (collar) | NT2. Applied first-time correction - unsafe zoneis displayed (app). | No pet geofence notifications | No feedbacks | No feedback notifications | NT5. Pet crosses the boundaries of an unsafe zone at first or againis displayed. (app) |
| Event 4 - Emergency Feedback (case 1) | Condition 1. A pet is determined in an unsafe zone.Condition 2. Event 3, 2 or 1 has just happened. (For MVP: Event 1 or 2 just has happened) | Apply Emergency Feedback once (collar) | NT3. Applied Emergency Feedback - unsafe zoneis displayed (app). | No pet geofence notifications | No feedbacks | No feedback notifications | NT6. Pet is in the unsafe zoneis displayed. (app) |
| Event 5- Emergency Feedback (case 2) | Condition 1. A pet is determined in an unsafe zone and moves:Warning1 to Danger towards border-cross point with angle \> 90°Lost to Danger towards border-cross point with angle \> 90°Condition 2. Event 4 has just happened and a pet is still in an unsafe zone.Condition 3. A pet was in a fence less than 30 min ago. | Apply Emergency Feedback while a pet is in an unsafe zone every 2 seconds during 5 min after last time presence in a fence in case a pet is walking farther away from the nearest fence.Apply Emergency Feedback while a pet is in an unsafe zone every 30 seconds (collar) during 5-30 min after last time presence in a fence in case a pet is walking farther away from the nearest fence. | No feedback notifications | No pet geofence notifications | No feedbacks | No feedback notifications | No pet geofence notifications |
| Event 8 - Pet left fence 30 min ago | Condition 1. A pet is determined in an unsafe zone.Condition 2. A pet was in a fence more than 30 min ago. | No feedbacks | No feedback notifications | NT15. Pet left fence 30 min ago | No feedbacks | No feedback notifications | NT15. Pet left fence 30 min ago is displayed. (app) |
| Event 6 - Pet returns in the fence | Condition 1. A pet is determined in a fenceCondition 2. A pet was determined in an unsafe zone or in the warning area of a fence previous time. | No feedbacks | No feedback notifications | NT7. Pet returns in the fenceis displayed. (app) | No feedbacks | No feedback notifications | NT7. Pet returns in the fenceis displayed. (app) |
