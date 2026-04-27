---
title: "(NI) ME03-US134 New catastrophic issue: Water damage indication"
sidebar_label: "(NI) ME03-US134 New catastrophic issue: Water damage indication"
sidebar_position: 412
last_modified: "May 30, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages |
|---|---|---|---|
| DRAFT |
| Kiryl Trafimau |
| HALO-19479 - MOB, BE: Add a cat.issue: water damage Open |
| Appendix 14 - List of catastrophic and non-catastrophic issuesMQTT Communication implemented on the back-end |User Story Acceptance criteria Rules Implementation notes

## User Story

\> As a USER I want to get notified when the there is a catastrophic issue with the collar so that I can replace it

## Acceptance criteria

| ID | Acceptance criteria |
|---|---|
| ME03-US134-AC01 | IF Based on Daily Diagnostic catastrophic issue happened according to the rule in the tableTHEN I should see the error text on the Collar diagnostic issue according to the rule in the tableAND I should see grey text on the Collar diagnostic issue according to the rule in the table |## Rules

| Section name | Error name | Error validations | Error text to be displayed on the Diagnostics screen in red | Grey text in the diagnostics screen |
|---|---|---|---|---|
| Other | Water damage | Discussed during the BA call that the FW will be updated to be able to detect this issue | 'Water damage'TBR, should be reviewed by Michael | 'Water damage of the collar was detected. Tap here to review our warranty and Protection Plans or contact support for further instructions.'tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103contact support = Dog ParkTBR, should be reviewed by Michael |Note for BA: Add proper row to Appendix 14 when requirements approved

## Implementation notes

| ID | Implementation note |
|---|---|
| ME03-US134-IN01 |  |
