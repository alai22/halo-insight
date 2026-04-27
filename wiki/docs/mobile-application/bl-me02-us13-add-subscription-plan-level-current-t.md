---
title: "[BL] ME02-US13. Add subscription plan level (current + temporary) info to the App Logs"
sidebar_label: "[BL] ME02-US13. Add subscription plan level (current + temporary) info to the App Logs"
sidebar_position: 126
last_modified: "Apr 13, 2021"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] |
| HALO-5923 - QA: Add subscription plan level (current + temporary) info to the App Logs Closed |
| Maria Shikareva [X] 13 Apr 2021 Baselined the user story (see ME02-F04. View "Help" screen (incl. integration with Zendesk and mobile logs)). |# User story

\> As a CSA I want to see information about the user's subscription plan in the App logs so that I am able to check easily what subscription level is currently applied on the mobile app. It may be useful, for example, in case the user has some troubles with their plan, contacts support and CSA has no other opportunity to define the user's current plan (e.g. the user has 'Basic' plan → the user changes it to 'Gold' but doesn't refresh the mobile application → the CSA within AAP sees 'Gold' plan for the user → but the user sees only features relevant for 'Basic' plan).

# Acceptance criteria

| AC | Description |
|---|---|
| ME02-US13-AC01 | The following information should be added to the logs within \<Do-Not-Delete.ZIP\> file:the user's current subscription plan;the user's subscription plan with temporary access. |
| ME02-US13-AC02 | This information should be logged each time a request is made to the backend. |# Useful notes

1. As discussed on the2021-02-01 Meeting notes: BA+UX call.
2. No work from MOB side required: when this info is returned from BE side, it should be logged 'automatically', no need in logging it separately.


