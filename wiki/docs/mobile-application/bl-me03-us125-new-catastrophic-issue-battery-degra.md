---
title: "(BL) ME03-US125 New catastrophic issue: battery degradation"
sidebar_label: "(BL) ME03-US125 New catastrophic issue: battery degradation"
sidebar_position: 394
last_modified: "May 03, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages | Change history |
|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-19477 - MOB[+BE]: Add a cat. issue: battery degradation Closed |
| Appendix 14 - List of catastrophic and non-catastrophic issues(BL) ME03-US101 BE+MOB: Catastrophic issues: calculation and displaying of the issue in appMQTT Communication implemented on the back-end |
| 03 May 2024 Kiryl Trafimau Baselined to Appendix 14 - List of catastrophic and non-catastrophic issues |User Story

# User Story

\> As a USER I want to get notified when the there is a catastrophic issue with the collar so that I can replace it

Issues in the battery section

|  | Error name | Error validations | Error text to be displayed on the Diagnostics screen in red | Grey text in the diagnostics screen |
|---|---|---|---|---|
| 20 | Battery degradation | battery_health \<50% && \>2 days in a row (3 Daily Diagnostics in a row)AND battery_health \>0 at least once in these 3 daysImplementation notes:we need the lower byte for battery_health=toint(MsgBody. battery_health) % 256.2. 50% and 3 days are configurable values. | "Battery level issue" | An issue was detected with the battery. Tap here to review our warranty and Protection Plans or contact support for further instructions.tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103contact support = Dog Park |
