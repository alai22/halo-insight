---
title: "[Won't have] ME03-US06. Assigning/unassigning offline collar"
sidebar_label: "[Won't have] ME03-US06. Assigning/unassigning offline collar"
sidebar_position: 7
author: "Nicolay Gavrilov"
---

| Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|
| Owner |
| ME03 As an Owner, I'd like to manage my collars to keep their info up to date. |
| CUSTOMER REVIEW |
| Nicolay Gavrilov |
|  |# User story

\> As an owner want my changes to be automatically applied once the collar is online when I try to assign or remove an offline device so that I don't have to bother with waiting until the collar is online and manually retrying this operation.

# Acceptance criteria

| AC | Text | Links |
|---|---|---|
| ME03-US06-AC01 | When users try to assign a collar to a pet and the collar is offline, the app applies the change and displays M37 Offline Changes notification.This should also apply to the case when a user creates a new pet and assigns a collar to it. | Pop-ups:M37 Offline Changes |
| ME03-US06-AC02 | When users try to remove a collar from a pet and the collar is offline, the app applies the change and displays M37 Offline Changes notification. | Pop-ups:M37 Offline Changes |
|  | TBD: Warning to inform that the device still has not-updated settings? |  |
|  | Any corner cases? E.g.: the collar is reset while it is still offlinethe collar cannot apply the change for some reason (if any)? → revert? |  |
