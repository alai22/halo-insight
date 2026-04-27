---
title: "ME04-US41. Add error for fence validation"
sidebar_label: "ME04-US41. Add error for fence validation"
sidebar_position: 663
last_modified: "Jun 05, 2020"
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|
| Owner |
| ME01 Enter the system |
| APPROVED |
| Galina Lonskaya |
| HALO-2863 - MOB:The user gets 'Response Error' if he tries to create fence with small safe zone area Closed |# User story

\> As owner, I want to view errors about incorrect fence so that I can understand how I should adjust fence.

# Acceptance criteria

| AC | Text |
|---|---|
| ME04-US41-AC01 | If during BE fence square validation is identified that the fence has more then 1 save zone, then M128 Fence has more than 1 safe zone (BE validation) should be displayed. |
| ME04-US41-AC02 | If during BE fence square validation is identified that the fence is too small, then M127 Fence is too small (BE validation) should be displayed. |
| US is relevant for both Fence creation / Fence editing flow. |
