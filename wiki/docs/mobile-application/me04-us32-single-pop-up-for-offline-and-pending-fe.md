---
title: "ME04-US32. Single pop-up for offline and pending fence updates"
sidebar_label: "ME04-US32. Single pop-up for offline and pending fence updates"
sidebar_position: 661
author: "Nicolay Gavrilov"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| DRAFT |
| Nicolay Gavrilov |
| HALO-6134 - ME04-US32. Single pop-up for offline and pending fence updates Open |# User story

\> As an owner, I want to get a single pop-up message instead of two separate messages in case I deactivate/edit/delete a fence and there are both online collars that are affected by this change and offline collars in my account so that I would not be confused with two separate messages.

# Acceptance criteria

| AC | Text | Links / Comments |
|---|---|---|
| ME04-US32-AC01 | There are ONLINE collars and OFFLINE collars using this fence (i.e. yes/yes)→the user sees pop-up stating "Changes are pending for some pets. \<pet name(s)\> will receive the update after they exit the fence or you turn fences off. \<pet name(s)\> has/have offline collars and will receive this update when collar(s) are online again." | Affects the flow described in the following stories:ME04-US11. Deactivate a fence with pets inside the polygonME04-US12. Delete a fence with pets inside the polygonME04-US13. Edit a fence with pets inside the polygon |
