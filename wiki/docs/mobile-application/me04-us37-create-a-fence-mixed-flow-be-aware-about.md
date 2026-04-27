---
title: "ME04-US37. Create a fence (mixed flow): be aware about inaccurate/invalid collar location"
sidebar_label: "ME04-US37. Create a fence (mixed flow): be aware about inaccurate/invalid collar location"
sidebar_position: 24
last_modified: "Nov 05, 2020"
author: "Galina Lonskaya"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| APPROVED |
| Galina Lonskaya |
| HALO-2095 - [ME04. Create Fence with a collar] : ME04-US37: Be aware about inaccurate/invalid collar location Closed |# User story

\> As an owner, I want to view the warning so that I can be aware of the incorrect/invalid collar location.

# Acceptance criteria

| AC | Description |
|---|---|
| AC01 | Precondition: The user got at least one accurate and valid collar location during the current connection session. If the got collar location accuracy is \> 1000 or the coordinates are invalid, then the latest location should be ignored and the collar pin should be displayed in "Weak GPS" status. |
| AC02 | Precondition: GPS is enabled on the phoneIf the first got coordinate during the session is invalid/inaccurate, then the collar pin should be placed at the user location and the collar pin should be displayed in "Weak GPS" status. |
| AC03 | Precondition: GPS is disabled on the phoneIf the first got coordinate during the session is invalid/inaccurate, then the collar pin should start in the middle of the screen. and the collar pin should be displayed in "Weak GPS" status. |
| AC04 | If I tap on the "Add via GPS"/"Move" button and the location accuracy is \> 1000 or the coordinates are invalid, then:the following toast message should be displayed: "GPS satellites provide a poor signal. Please try again"; the dot location isn't updated. |
