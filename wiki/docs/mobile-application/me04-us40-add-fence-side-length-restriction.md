---
title: "ME04-US40. Add fence side length restriction"
sidebar_label: "ME04-US40. Add fence side length restriction"
sidebar_position: 662
last_modified: "Jan 21, 2020"
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| APPROVED |
| Galina Lonskaya |
| HALO-2804 - MOB+BE: ME04-US40. Add fence side length restriction Closed |# User story

\> As owner, I want to view restrictions on fence sides so that I can create only valid fences

# Intro

This US should resolve the following issues:

- [HALO-2189](https://jira.softeq.com/browse/HALO-2189?src=confmacro)-Every dot appears under the previous on Create Fence with Collar flow if the user adds the dot for the same location pointsClosed

# Acceptance criteria

| AC | Text |
|---|---|
| ME04-US40-AC01 | If I try to add a new dot/ move the added dot/ close a fence AND distance between any dots becomes less than 2 m, then:the action shouldn't be performed;the following toast message should be displayed for 4 sec: "Please make sure fence posts are at least 2 meters apart" |
| ME04-US40-AC02 | If I try to add a new dot/ move the added dot/ close a fence AND distance between any dots becomes more than 10000 m, then:the action shouldn't be performed;the following toast message should be displayed for 4 sec: "Please make sure fence posts are less than 10000 meters apart." |
| ME04-US40-AC03 | MIN and MAX side length should be configurable on the BE. |
| ME04-US40-AC04 | If during BE fence square validation was identified that the fence is too small, then M127 Fence is too small (BE validation) should be displayed. |
| US is relevant for both Fence creation / Fence editing flow. |
