---
title: "(BL) ME03-US118 BE: New catastrophic issue: gps chip issue"
sidebar_label: "(BL) ME03-US118 BE: New catastrophic issue: gps chip issue"
sidebar_position: 390
last_modified: "May 03, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages | Change history |
|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-19263 - BE, MOB: New catastrophic GPS chip issue Closed HALO-19264 - [NT] FW, BE: MQTT contract update Closed |
| The affected requirements:(BL) ME03-US101 BE+MOB: Catastrophic issues: calculation and displaying of the issue in appAppendix 14 - List of catastrophic and non-catastrophic issues |
| 03 May 2024 Kiryl Trafimau Baselined to Appendix 14 - List of catastrophic and non-catastrophic issues |User Story ME03-US118-AC01

# User Story

\> As a USER I want to get notified when the LTE modem failure happened so that I do not use it for dog's protection

|  | Section name---------------Error name | Error validations | Catastrophic issue? | Error text to be displayed on the Diagnostics screen in red | Grey text in the diagnostics screen |  | LTE |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GPS chip failure 4 | GPS_timeout \> 1000 && \>2 days in a row (3 DailyDiagnostics in a row) | CATASTROPHIC | "GPS chip issue" | Tap here to review our warranty and Protection Plans or contact support for further instructions.tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103 contact support = Dog Park || ID | Acceptance criteria |
|---|---|
| ME03-US118-AC01 | IF Based on Daily Diagnostic catastrophic issue happened according to the rule aboveTHEN I should see the error text on the Collar diagnostic issue according to the rule aboveAND I should see grey text on the Collar diagnostic issue according to the rule above |
