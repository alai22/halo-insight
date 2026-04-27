---
title: "(BL) ME03-US106 BE+MOB: New catastrophic issue - sim_err"
sidebar_label: "(BL) ME03-US106 BE+MOB: New catastrophic issue - sim_err"
sidebar_position: 305
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Estimates | Related pages | Change history |
|---|---|---|---|---|---|---|
| APPROVED |
| Maryia Paklonskaya [X] |
| HALO-15723 - BE + MOB: Add new catastrophic error to calculation and display in app Closed |
| create requirementsrefinementfinalised, ready for devadd to the baseline |
| BE: 1sp ballparkMOB: 0.5spQA: 2sp |
| The affected requirements:(BL) ME03-US101 BE+MOB: Catastrophic issues: calculation and displaying of the issue in app Related user story:[Outdated] AE03-US93 BE+FE: AAP - Add sim_err as new catastrophic issues of the collar in the Admin portal |
| 03 May 2024 Kiryl Trafimau Baselined to Appendix 14 - List of catastrophic and non-catastrophic issues |User Story New catastrophic issue Acceptance Criteria BE scope ME03-US106-AC01 MOB scope ME03-US106-AC02 ME03-US106-AC03

# User Story

\> As a USER I want to get notified when the card could not be initialized so that I do not use such collar for dog's protection

# New catastrophic issue

|  | Section name---------------Error name | Error validations | Catastrophic issue? | Error text to be displayed on the Diagnostics screen in red | Grey text in the diagnostics screen |  | LTE |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | LTE modem failure (as example, already implemented) | LTE_FW == 0 && \>2 days in a row | CATASTROPHIC | "LTE chip issue" | LTE module is not working properly and the collar needs to be replaced. Tap here to review our warranty and Protection Plans or contact support for further instructions.tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103. |
| 2 | SIM card slot failure - new parameter | sim_err \>= 10 && \>2 days in a row(3 DD in a row) | CATASTROPHIC | "SIM card slot issue" | SIM card could not be initialized and the collar needs to be replaced. Tap here to review our warranty and Protection Plans or contact support for further instructions.tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103.contact support = Dog park |# Acceptance Criteria

| ID | Acceptance criteria |
|---|---|
|  | BE scope |
| ME03-US106-AC01 | Add new parameter "sim_err" to DDANDbased on the rule in the table above calculate as catastrophic issue |
|  | MOB scope |
| ME03-US106-AC02 | Display "sim_err" error in the LTE section as catastrophic based on the ME03-US101-AC07. |
| ME03-US106-AC03 | If both LTE modem failure and Sim card slot failure happenedTHENDisplay Grey text in the diagnostics screen for "sim_err" error in the LTE section |
