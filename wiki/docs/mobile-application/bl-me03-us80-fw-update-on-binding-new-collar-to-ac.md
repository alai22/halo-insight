---
title: "[BL] ME03-US80. FW update on binding new collar to account"
sidebar_label: "[BL] ME03-US80. FW update on binding new collar to account"
sidebar_position: 215
author: "Nicolay Gavrilov"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED (SQ) |
| Nicolay Gavrilov |
| HALO-11474 - BE: ME03-US80. FW update on binding new collar to account Closed |
| Click here to expand... |User story

\> As a user I want my new collar to have the latest FW version so that I have no problems with using the device

# Acceptance criteria

| AC | Text | Links / |
|---|---|---|
| ME03-US80-AC01 | Preconditions:no over-the-air FW updates were installed to the collar previouslyIf the collar is added to the account the BE should trigger an FW update for this device. The collar should be updated with the FW that is marked as "Current production FW version" in the AAP.Note: the collar will start the FW update process after it is connected to a charger | AE05-US35. "Beta/ Production" versions |
| ME03-US80-AC02 | If a collar does not support the "Current production FW version", then it should not install it and log a separate error, and create the corresponding allert in Azure for L2 engineer. |
