---
title: "(BL) ME03-US188 BE+MOB: Display average battery lifetime instead last reported"
sidebar_label: "(BL) ME03-US188 BE+MOB: Display average battery lifetime instead last reported"
sidebar_position: 364
last_modified: "Jun 04, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-18488 - MOB, BE: Display battery average for 7 days Closed |
| Kiryl Trafimau Baselined to ME03-F07. Collar Diagnostic |User Story

# User Story

\> As a USER I want to see average of the collar battery lifetime so that I understand that the battery is in a good state

Acceptance Criteria| AC# | Description | Comments, designs |
|---|---|---|
| ME21-US188-AC01 | IF I am on the 'Collar Diagnostic' screenTHEN I should see 'Battery life (7 days average)' row AND I should not see 'Last reported battery life' row | Zeplin |
| ME21-US188-AC02 | Pre-condition: All DD which received over the last 7 days before the last DD received contains either invalid battery life data (IN02) OR no battery life data (IN01)IF I am on the 'Collar Diagnostic' screenTHEN I should see 'No data'AND I should not see 'Battery life (7 days average)' rowAND There is no 'check' icon near the 'Battery' titleNote: if we don't have any DD for the collar then the whole Collar Diagnostic is not displayed for this collar. | Zeplin |Implementation notes

| AC# | Description |
|---|---|
| ME21-US188-IN01 | If no battery life in DD-we ignore this DD in calculation. |
| ME21-US188-IN02 | Ignore invalid values (less than 6 hours and more than 30 42 hours).(30 hours will be changed in config to 42 in task HALO-20437 - BE: Update rules of Average battery life calculation (July 2024) Closed ). |
| ME21-US188-IN03 | Count independently on how many DDs we have, even if we have only 1 DD with battery life over this period. |
| ME21-US188-IN04 | Period for calculation is the last 7 days prior to the last received DD |
| ME21-US188-IN05 | 7 days is configurable |
