---
title: "(BL) ME03-US103. Notification about catastrophic and non-catastrophic issues to Braze"
sidebar_label: "(BL) ME03-US103. Notification about catastrophic and non-catastrophic issues to Braze"
sidebar_position: 301
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Estimates | Related pages | Change history |
|---|---|---|---|---|---|---|
| APPROVED |
| Maryia Paklonskaya [X] Kiryl Trafimau |
| HALO-15601 - BE: ME03-US103 Notification about catastrophic and non-catastrophic issues to Braze Closed HALO-15997 - [NT] Review and update communication contract with Braze Closed |
| create requirementsrefinementget final approval from the Halo LT finalised, ready for devadd to the baseline |
| BE: 1spQA: 3sp |
| https://docs.google.com/document/d/1n-HYaKaMsnhYX2yJ15Kx8-FEuzaO1ttKJLZaYG5WAN4/edit |
| 03 May 2024 Kiryl Trafimau Baselined to ME03-F07. Collar Diagnostic |# User Story

\> As a Business Owner I want to get trigger from BE so that I could use Braze to notify users about critical errors

# Acceptance Criteria

| AC | Description |
|---|---|
| ME03-US103-AC01 | Immediately once BE detected catastrophic OR non-catastrophis issue for the collar which is in the user account - the event should be sent to Braze (no matter if firmware feature for action on collar is supported) |
| ME03-US103-AC02 | For catastrophic issuesEvent should be sent:-when the issue is detected on first time OR-after `clear issues` when catastrophic/non-catastrophic issue is detected, the braze catastrophic/non-catastrophic custom event should be sentIf issue is detected for 2nd day in a row and it wasn't reset- event should not be sent.2. `Clear catastrophic issues` can be:a. mob request to clear catastrophic issues (ME03-US103-AC05)b. unbind collar from account (ME03-US103-AC06)c. deletion user account (ME03-US103-AC06)d. deactivation by user replace or return (ME03-US103-AC07)e. admin request to reset catastrophic issues (will not be implemented for this story) (BL) AE03-US123 FE: AAP - An ability to reset cat issue from Admin |
| ME03-US103-AC03 | For non-catastrophic issuesEvent should be sent:-when the issue is detected on first time OR-after `clear issues` when catastrophic/non-catastrophic issue is detected, the braze catastrophic/non-catastrophic custom event should be sentIf issue is detected for 2nd day in a row and it wasn't reset- event should not be sent.2. `Clear non-catastrophic issues` can bea. mob request to clear catastrophic issues (ME03-US103-AC05)b. unbind collar from account (ME03-US103-AC06) c. deletion user account (ME03-US103-AC06)d. deactivation by user replace or return (ME03-US103-AC07)e. admin request to reset catastrophic issues (will not be implemented for this story) (BL) AE03-US123 FE: AAP - An ability to reset cat issue from Adminf. If Daily diagnostics reported that the issue not happened (ME03-US103-AC09)(a-e cases can happen if there was catastrophic issue at the same time) |
| ME03-US103-AC04 | The following data should be sent to Braze: Collar serial numberBinded pet's name (could be empty if collar not assigned to pet).Type of the issue detected (catastrophic or non-catastrophic). |
| ME03-US103-AC05 | Precondition: Daily diagnostics reported that catastrophic or non-catastrophic issue was detectedIF user 'cleared' catastrophic issue by clicking Proceed On popup 'Dismiss the issue' (ME03-US121-AC02)THENClear 'Notification to braze is sent' flags for all catastrophic and non-catastrophic issues (ME03-US103-AC02) (Should be 2 braze flags: for catastrophic and non-catastrophic issues) |
| ME03-US103-AC06 | Precondition: Daily diagnostics reported that catastrophic issue was detectedIF user unbinded (deleted) from account a collar with a catastrophic issueOR user deleted an accountTHENClear 'Notification to braze is sent' flags for all catastrophic and non-catastrophic issues (ME03-US103-AC02) (Should be 2 braze flags: for catastrophic and non-catastrophic issues) |
| ME03-US103-AC07 | Precondition: Daily diagnostics reported that catastrophic issue was detectedIF collar was deactivated THENClear 'Notification to braze is sent' flags for all catastrophic and non-catastrophic issues (ME03-US103-AC02) (Should be 2 braze flags: for catastrophic and non-catastrophic issues)Notes: Deactivation performs automatically when during the warranty replacement process user selected "ship my replacements before I return my unit" and user did not return the old collar within 30 days from the request approvalDeactivation performs automatically during the warranty replacement of the Halo Care or Halo Protection Plan. It happens within 2 weeks after buying new collar. |
| ME03-US103-AC08 | IF collar unbinded (deleted) from account OR collar was deactivatedOR account was deletedWHEN daily diagnostics received that catastrophic issue was detectedTHEN not sent notification to Braze |
| ME03-US103-AC09 | Precondition: Daily diagnostics reported that non-catastrophic issue was detectedWHEN Next Daily diagnostics reported that there is no longer non-catastrophic issues detectedTHEN Clear 'Notification to braze is sent' flags for non-catastrophic issue (ME03-US103-AC02) |
