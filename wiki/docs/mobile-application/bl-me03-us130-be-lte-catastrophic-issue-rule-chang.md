---
title: "(BL) ME03-US130 BE: LTE catastrophic issue rule change"
sidebar_label: "(BL) ME03-US130 BE: LTE catastrophic issue rule change"
sidebar_position: 314
last_modified: "May 03, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Related pages | Changes history |
|---|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-16444 - BE: LTE catastrophic issue rule change Closed |
| create requirementsrefinementfinalised, ready for devadd to the baseline |
| The affected requirements:(BL) ME03-US101 BE+MOB: Catastrophic issues: calculation and displaying of the issue in appAppendix 14 - List of catastrophic and non-catastrophic issues |
| 03 May 2024 Kiryl Trafimau Baselined to Appendix 14 - List of catastrophic and non-catastrophic issues |User Story BE scope ME03-US130-AC01 ME03-US130-AC02

# User Story

\> As a USER I want to get notified when the LTE modem failure happened so that I do not use it for dog's protection

|  | Section name---------------Error name | Error validations | Catastrophic issue? | Error text to be displayed on the Diagnostics screen in red | Grey text in the diagnostics screen |  | LTE |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | LTE modem failure | LTE_Init_Fails \>= 255 && \>2 days in a row (3 DailyDiagnostics in a row) | CATASTROPHIC(No changes in issue type) | (No changes in UI messages)"LTE chip issue" | (No changes in UI messages)LTE module is not working properly and the collar needs to be replaced. Tap here to review our warranty and Protection Plans or contact support for further instructions.tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103.contact support = Dog Park || ID | Acceptance criteria |
|---|---|
|  | BE scope |
| ME03-US130-AC01 | Trigger for issue LTE modem failure should be: LTE_Init_Fails \>= 255 && \>2 days in a row (3 DailyDiagnostics in a row) |
| ME03-US130-AC02 | Clear existing issue for users who have it by old rule.2 approaches:Change errors in DB and it will be updated for user when next DD receivedClear issues in DB AND cache. Push command to users to clear it. |
