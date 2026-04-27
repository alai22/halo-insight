---
title: "[BL] ME03-US43. View the statuses of the collar buttons"
sidebar_label: "[BL] ME03-US43. View the statuses of the collar buttons"
sidebar_position: 80
author: "Galina Lonskaya"
---

| Epic | Document status | BA owner | DEV, QA owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|---|
| ME03 Manage collars |
| APPROVED |
| Galina Lonskaya |
| Eugene Paseka, Pavel Leonenko, Anastasia Brechko |
| HALO-4430 - BE+MOB GOAL: View the statuses of the collar update Closed |
| 07 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As an owner, I want to view the status of the collar update so that I can follow how my collar is updating.

| AC | Description | Source requirement |
|---|---|---|
| See source story: ME03-US26. View Collar details (UI redesign) |
| ME03-US43-AC01 | Precondition: "Collar details" screen is openedIf an FW update has been started at the collar, then:the status of the FW update should be displayed within the "Collar Update" tile.Note 1: see the list of the statuses in table 1.Note 2: if the collar is offline while updating, then some statuses could be skipped or not displayed at all for the end-user. | Pic 1 - Collar details with the status of the FW update |
| ME03-US43-AC02 | No real-time update for FW update status | - |Table 1 - Statuses of the FW update that should be described within the app (as on June 10, 2020)

| Current status title | New status title |
|---|---|
| Unknown | Downloading not started |
| Waiting For Download - Incompatible Network | Downloading paused, no Wi-Fi |
| Waiting For Download - Low battery | Downloading paused, low battery |
| Waiting For Download - Not on a charger | Downloading paused, not charging |
| Downloading | Downloading |
| Download Failed | Downloading failed |
| Verifying | Verifying |
| Verify Failed | Verifying failed |
| Applying Delayed - Not Charging | Applying paused, not charging |
| Applying | Applying |
| Apply Failed | Applying failed |
