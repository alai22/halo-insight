---
title: "[Postponed] ME05-US37. Receive \"Excessive feedback\" warning"
sidebar_label: "[Postponed] ME05-US37. Receive \"Excessive feedback\" warning"
sidebar_position: 75
last_modified: "Sep 07, 2023"
author: "Galina Lonskaya"
---

| Epic | Document status | BA story owner | DEV story owner | QA story owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| ME05. Manage feedbacks |
| APPROVED BY SQ |
| Galina Lonskaya |
| Konstantin Smolyakov, Pavel Leonenko |
| Anastasia Brechko |
| HALO-3937 - MOB: ME05-US37. Receive "Too many feedback" warning Ready for Development |# Intro

It was agreed to remove push- notification about too many feedback, as the prevention calculation isn't correct to perform on BE side anymore. At the moment instant preventions can be sent via BLE and BE isn't aware of it. So, ME05-US18. Notify the user about too frequent feedbacks isn't relevant anymore.

# User story

\> As an owner, I want to be notified about too many feedback so that I can be sure that I don't abuse my dog.

# Acceptance criteria

| AC | Description | Note/Link/Wireframe |
|---|---|---|
| ME05-US36-US01 | "Too many feedback" counter should be set on the mobile side.The counter should add "+1" in the following cases:Feedback is initiated from the "Instant command" card and successfully performed on the collar;Test feedback is initiated from the prevention settings and successfully performed on the collar. | This logic is important for QA so that they can test this functionality within the whole system.Note 1: After "Log out", the counter will be cleared.Note 2: Mention the case about 2 devicesNote 3: No conf-n on BE |
| ME05-US36-US02 | If I initiate the instant/test feedback for the specific pet and within the last 5 min 10 or more instant/test feedback were performed, then:the standard iOS message M140 Excessive Feedback should be displayed. | Note 1: "Feedback" functionality isn't blocked after M140 message receiving.Note 2: New "Instant prevention" response status should be received from the collar (MQTT and BLE contract update) |
