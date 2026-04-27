---
title: "(NA) ME05-FE02-US01. Manual Feedback: Manual Feedback Icon on My Fences tab"
sidebar_label: "(NA) ME05-FE02-US01. Manual Feedback: Manual Feedback Icon on My Fences tab"
sidebar_position: 548
author: "Galina Lonskaya"
---

| Document owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-804/[ios]-manual-feedback-mf-icon-on-my-fences-tab HALO-23070 - [iOS] Manual Feedback: MF Icon on My Fences tab Open HALO-23071 - [Android] Manual Feedback: MF Icon on My Fences tab Open |
| 16 Apr 2024 draft story is created |# User story

\> See the parent page

Contents

User story Acceptance criteria

### Acceptance criteria

| AC | Text | UI design |
|---|---|---|
| AC01 | Manual Feedback (MF) icon should always be displayed in the top navigation bar on My Fences tab. |  |
| AC02 | MF icon can have 2 states:disabledenabled | FigmaFigma |
| AC03 | If there is 0 pet(s) with linked collar in the account, then:MF icon should be disabled. | - |
| AC04 | If all collars in the account have:dead battery OR/AND assumed powered offOR/AND have not received telemetry then:MF icon should be disabled. | - |
| AC05 | If last sync was with all collars more than 30 sec ago, then:MF icon should be disabled. | - |
| AC06 | If I tap on the disabled MF button, then:the toast message should be shown. | Figma |Implementation details

To detect "dead battery"/"assumed powered off" statuses, Reachability System should be used. "30 sec ago" status could be added to Reachability System as well.

In .NET, we use IPetCollarReachabilityObserver to create an observable which provides statuses for a certain pet in real time. We planned to create a shared observable per each PetViewModel (those are shared wrappers around PetModels which can be used to notify UI everywhere simultaneously) - perhaps something similar could be done in the native apps.


