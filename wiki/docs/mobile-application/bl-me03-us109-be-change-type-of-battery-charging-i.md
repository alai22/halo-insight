---
title: "(BL) ME03-US109 BE: Change type of Battery charging issue 1 to Non-catastrophic"
sidebar_label: "(BL) ME03-US109 BE: Change type of Battery charging issue 1 to Non-catastrophic"
sidebar_position: 308
last_modified: "May 03, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Estimates | Related pages | Change history |
|---|---|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-16035 - BE: ME03-US109 Change type of Battery charging issue 1 to Non-catastrophic Closed |
| create requirementsrefinementget final approval from the Halo LT finalised, ready for devadded final designsadd to the baseline |
| BE: 0.5QA: 0.5 |
| The affected requirements:(BL) ME03-US101 BE+MOB: Catastrophic issues: calculation and displaying of the issue in appRelated issues: |
| 03 May 2024 Kiryl Trafimau Baselined to Appendix 14 - List of catastrophic and non-catastrophic issues |User Story Catastrophic and non-catastrophic issues of the collar Acceptance Criteria BE scope ME03-US109-AC01 ME03-US109-AC02 MOB scope ME03-US109-AC03 ME03-US109-AC04

# User Story

\> As a USER I want to get notified when battery charging issue 1 happened so that I can take actions to fix it

# Catastrophic and non-catastrophic issues of the collar

|  | Section name---------------Error name | Error validations | Catastrophic issue? | Grey text in the diagnostics screen |
|---|---|---|---|---|
| 1 | Battery charging issue 1 | at least 1 of 3 days 0\<ChargeCurr\<100ANDother days in a 3-days range could be ChargeCurr == 0___________________________________Battery discharge charge amperage range is from 0 to 500. | NON-CATASTROPHIC | An issue was detected with the battery. Tap here to review our warranty and Protection Plans or contact support for further instructions.tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103contact support = Dog Park |# Acceptance Criteria

| ID | Acceptance criteria |
|---|---|
|  | BE scope |
| ME03-US109-AC01 | Based on Daily Diagnostic Back End should calculate if Battery charging issue 1 issue happened.If issue happened, then send info about the Battery charging issue 1 to the mobile so that it is displayed. |
| ME03-US109-AC02 | Log errors (to AppInsight) each time Battery charging issue 1 happens and save info about Serial number of the collar AND error type (from the table above - column Error name - 2nd column). |
|  | MOB scope |
| ME03-US109-AC03 | In case of Battery charging issue 1 detected the mobile application should display it according to current rules of displaying the daily diagnostics issues. |
| ME03-US109-AC04 | In case of Battery charging issue 1 detected the mobile application:AND there are no any catastrophic issue:Red dot should not be displayed on the Settings menu tab, blue dot should be displayed."My collars" tab should not have the Red dot, blue dot should be displayed.On the "Collars" tab the Red Exclamation mark near the photo of the collar should not appear, the grey one should be displayed.On the Collar diagnostics section Red exclamation mark should not be displayed and text "Critical issues detected" should not be displayed. In the collar diagnostics screen:Red exclamation mark on the proper section should not be displayed, orange exclamation mark should be displayed.The red text with the problem (column "Error text to be displayed on the Diagnostics screen in red") should not be displayed before the regular grey textGrey text description from the from the table above (column "Grey text in the diagnostics screen") should be displayed. |
