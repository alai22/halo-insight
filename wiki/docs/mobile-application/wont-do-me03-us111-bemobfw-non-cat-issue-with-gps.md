---
title: "(Won't do) ME03-US111 BE+MOB+FW: Non-cat issue with GPS"
sidebar_label: "(Won't do) ME03-US111 BE+MOB+FW: Non-cat issue with GPS"
sidebar_position: 309
last_modified: "May 03, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Estimates | Related pages |
|---|---|---|---|---|---|
| CANCELLED because it was decided not to implement non-catastrophic issues on the mobile, but notify users about them via BEAM HALO-18474 - BE+Braze [Part 1]: Weekly health checks via BEAM (incl. non-catastrophic issues) Closed |
| Kiryl Trafimau |
| HALO-16050 - FW: Count amount of whistle preventions overrode real preventions Resolved HALO-16069 - BE: Count amount of whistle preventions overrode real preventions Closed HALO-16049 - BE+MOB+FW: ME03-US111. Non-cat issue with GPS Closed |
| create requirementsrefinementget final approval from the Halo LT finalised, ready for devadded final designsadd to the baseline |
| BE: MOB: QA: |
| The affected requirements:(BL) ME03-US101 BE+MOB: Catastrophic issues: calculation and displaying of the issue in appRelated issues: |User Story Catastrophic and non-catastrophic issues of the collar Acceptance Criteria BE scope ME03-US111-AC01 ME03-US111-AC02 MOB scope ME03-US111-AC03

# User Story

\> As a USER I want to get notified when GPS is inaccurate so that I can take actions to fix it

# Catastrophic and non-catastrophic issues of the collar

|  | Section name---------------Error name | Error validations | Catastrophic issue? | Grey text in the diagnostics screen |
|---|---|---|---|---|
| 1 | GPS accuracy issue | TBDIf amount of whistles \>[some condition] (more than X% of overall? or more than exact number X) AND GPS level is Medium (what about low?) | NON-CATASTROPHIC | some text telling to adjust GPS thresholds(Maybe we can autochange GPS Thresholds?) |# Acceptance Criteria

| ID | Acceptance criteria |
|---|---|
|  | BE scope |
| ME03-US111-AC01 | Based on Daily Diagnostic Back End should calculate if GPS accuracy issue happened.If issue happened, then send info about the GPS accuracy issue to the mobile so that it is displayed. |
| ME03-US111-AC02 | Log errors (to AppInsight) each time GPS accuracy issue happens and save info about Serial number of the collar AND error type (from the table above - column Error name - 2nd column) AND non-catastrophic type. |
|  | MOB scope |
| ME03-US111-AC03 | In case of GPS accuracy issue detected the mobile application should display it according to current rules of displaying the daily diagnostics issues. |
