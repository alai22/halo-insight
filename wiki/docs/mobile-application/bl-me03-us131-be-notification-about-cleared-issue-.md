---
title: "(BL) ME03-US131 BE: Notification about cleared issue to Braze"
sidebar_label: "(BL) ME03-US131 BE: Notification about cleared issue to Braze"
sidebar_position: 315
last_modified: "May 03, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Related pages | Change history |
|---|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-16464 - BE: Notifications about cleared issues to Braze Closed HALO-16471 - BE: Update Braze contract with new event (Issues cleared) Closed |
| create requirementsrefinementget final approval from the Halo LT finalised, ready for devadd to the baseline |
| Related requirements:(BL) ME03-US121 BE+MOB: Ability to reset catastrophic issue(NI) ME03-US103 BE: Notification about catastrophic and non-catastrophic issues to Braze |
| 03 May 2024 Kiryl Trafimau Baselined to ME03-F07. Collar Diagnostic |User Story Acceptance Criteria ME03-US131-AC01 ME03-US131-AC02 ME03-US131-AC03 ME03-US131-AC04 ME03-US131-AC05 ME03-US131-AC06 ME03-US131-AC07

# User Story

\> As a Braze manager I want to be notified when catastrophic issues cleared so that I can stop displaying the content card

# Acceptance Criteria

| ID | Acceptance criteria | Design |
|---|---|---|
| ME03-US131-AC01 | When all catastrophic issues for ALL collars in the account cleared, BE should sent event to Braze that issues are cleared for certain account |  |
| ME03-US131-AC02 | For catastrophic issues event should be sent:a. mob request to clear catastrophic issues (ME03-US131-AC03)b. unbind collar from account (ME03-US131-AC04)c. deletion user account (ME03-US131-AC05)d. deactivation by user replace or return (ME03-US131-AC06)e. admin request to reset catastrophic issues (will not be implemented for this story) (NI) AE03-US123 FE: AAP - An ability to reset cat issue from AdminAND There is no collars left with catastrophic issues |  |
| ME03-US131-AC03 | Precondition: previously Daily diagnostics reported that catastrophic issue was detectedIF user 'cleared' catastrophic issue AND There is no collars left with catastrophic issuesTHEN BE should send Event to Braze that all issues cleared for account |  |
| ME03-US131-AC04 | Precondition: previously Daily diagnostics reported that catastrophic issue was detectedIF user unbinded (deleted) from account a collar with a catastrophic issueAND There is no collars left with catastrophic issuesTHEN BE should send Event to Braze that all issues cleared for account |  |
| ME03-US131-AC05 | Precondition: previously Daily diagnostics reported that catastrophic issue was detectedIF user deleted accountTHEN BE should send Event to Braze that all issues cleared for account |  |
| ME03-US131-AC06 | Precondition: previously Daily diagnostics reported that catastrophic issue was detectedIF collar was deactivatedAND There is no collars left with catastrophic issuesTHEN BE should send Event to Braze that all issues cleared for accountNotes: Deactivation performs automatically when during the warranty replacement process user selected "ship my replacements before I return my unit" and user did not return the old collar within 30 days from the request approvalDeactivation performs automatically during the warranty replacement of the Halo Care or Halo Protection Plan. It happens within 2 weeks after buying new collar. |  |
| ME03-US131-AC07 | If collar is not in the accountAND catastrophic issues were cleared on itTHEN nothing is send to Braze |  |
