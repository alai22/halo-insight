---
title: "ME04-F17. Add fence with GPS: Inaccurate/invalid collar location"
sidebar_label: "ME04-F17. Add fence with GPS: Inaccurate/invalid collar location"
sidebar_position: 116
author: "Galina Lonskaya"
---

| Document status | Test cases status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 30 May 2022 |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko |
| HALO-5357 - Android GOAL: Add/Edit fence with GPS Closed HALO-11535 - MOB: Change pet pins (related to indoor/ outdoor) Closed |
| Click here to expand...30 May 2022 Maria Shikareva [X] Baselined [BL] ME07-US72. Changes to pet pins (related to indoor/ outdoor). |User story

\> As an owner, I want to view the warning so that I can be aware of the incorrect/invalid collar location.

# Acceptance criteria

| AC | Description | iOS implementation/UI design | Android implementation/UI design |
|---|---|---|---|
| ME04-F17-AC01 | Precondition: The app received at least one accurate and valid collar location within the current connection session.If the accuracy of the received collar location is \> 1000 or the coordinates are invalid, then: the received location should be ignored; the collar pin should be greyed out. | - | - |
| ME04-F17-AC02 | Precondition: GPS is enabled on the phoneIf the first received collar location within the current connection session is invalid/inaccurate, then:the collar pin should be placed at the place of the user location;the collar pin should be greyed out. | - | - |
| ME04-F17-AC03 | Precondition: GPS is disabled on the phoneIf the first received collar location within the current connection session is invalid/inaccurate, then:the collar pin should be displayed in the middle of the viewed screen at the moment;the collar pin should be greyed out. | - | - |
| ME04-F17-AC04 | If I tap on the "Add (GPS)"/"Move" button and the location accuracy is \> 1000 or the coordinates are invalid, then:the following toast message should be displayed: "GPS satellites provide a poor signal. Please try again";a new fence post should not be added (for "Add(GPS)" button) or the fence post location should not be updated (for "Move" button). | - | - |
