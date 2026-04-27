---
title: "(BL) ME03-US108 MOB: Create external and deeplinks for catastrophic issues"
sidebar_label: "(BL) ME03-US108 MOB: Create external and deeplinks for catastrophic issues"
sidebar_position: 306
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Estimates | Related pages |
|---|---|---|---|---|---|
| APPROVED |
| Maryia Paklonskaya [X] Kiryl Trafimau |
| HALO-15923 - MOB: Create deeplink (for pushes \ content cards) and external link (for emails) for catastrophic issues Closed |
| create requirementsrefinementget final approval from the Halo LT finalised, ready for devadd to the baseline |
| MOB: 2spQA: 2sp |
| Appendix 13 - Universal and iOS Deep links |# User Story

\> As a Halo Marketing team I want to have deeplinks and external links to the app so that I could insert them to the push notifications and emails

# Acceptance Criteria

https://miro.com/app/board/uXjVPuBWSYM=/?moveToWidget=3458764545768397437&cot=14

| AC # | Acceptance Criteria Description |
|---|---|
| ME03-US104-AC01 | The push notification about catastrophic issue should contain deep link to the collar list. |
| ME03-US104-AC02 | The email message about catastrophic issue should contain deep link to the collar list. |
| ME03-US104-AC03 | If several push-notifications are sent to the end user (one for one collar and one for another collar)THEN-iOS - both push-notifications should be displayed-Android - the latest notification should be displayed. |
# Implementation notes

| N | Description |
|---|---|
| 1 | The deep links should be created on all Halo App environments.The ending of the link should be: /open-halo-app-collar-list |
| 2 | Once deep links will be implemented please add them to the Appendix 13 - Universal and iOs Deep links |

