---
title: "ME05-US16. Unintentional fence border violation"
sidebar_label: "ME05-US16. Unintentional fence border violation"
sidebar_position: 693
last_modified: "Feb 25, 2020"
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|
| Owner |
| ME05 Manage commands |
| APPROVED |
| Galina Lonskaya |
| HALO-2909 - QA: Test ME05-US16. Unintentional fence border violation Closed |# User story

\> As an owner I want my pet not to be corrected in case of unintentional fence violation so that the pet doesn't be punished unintentionally.

# Acceptance criteria

| AC | Text |
|---|---|
| AC01 | If a pet appears in an unsafe zone, but he/she has come to this zone unintentionally, then:a pet shouldn't be corrected by the commands;notifications about pet geofence should be still sent; |
| AC02 | If a pet appears in an unsafe zone at once after the collar has turned on, then it will be considered as an "unintentional zone violation". |
