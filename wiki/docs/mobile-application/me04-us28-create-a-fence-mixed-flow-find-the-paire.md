---
title: "ME04-US28. Create a fence (mixed flow): find the paired collar"
sidebar_label: "ME04-US28. Create a fence (mixed flow): find the paired collar"
sidebar_position: 19
author: "Galina Lonskaya"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| REVISED |
| Galina Lonskaya |
| HALO-2017 - [ME04-US28]: Create a fence (mixed flow): find the paired collar Closed |# User story

\> As owner, I want to view the collar blinking and hear collar sound so that I can be sure the correct collar is paired.

# Acceptance criteria

| AC | Text |
|---|---|
| AC01 | If the "Find the collar" flow is initiated via BLE, then the collar should blink/beep for about 10 seconds per request. |
| AC02 | If the "Find the collar" flow is initiated and the collar doesn't respond, the "M70. No answer from the collar" error should be displayed. |
