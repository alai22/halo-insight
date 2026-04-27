---
title: "(BL) ME03-US133 MOB: Ability to reset catastrophic issue-wording updates"
sidebar_label: "(BL) ME03-US133 MOB: Ability to reset catastrophic issue-wording updates"
sidebar_position: 316
last_modified: "May 03, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages | Change history |
|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-16415 - MOB Update wording for Dismiss cat issue section and popup Closed |
| The affected requirements:(BL) ME03-US121 BE+MOB: Ability to reset catastrophic issue |
| 03 May 2024 Kiryl Trafimau Baselined to ME03-F07. Collar Diagnostic |User Story Acceptance Criteria ME03-US133-AC01 ME03-US133-AC02

# User Story

\> As a Halo account USER owner I want to reset catastrophic issue behavior if I think that issue on collar is fixed so that I can use the collar

# Acceptance Criteria

| ID | Acceptance criteria | Design |
|---|---|---|
| ME03-US133-AC01 | If there is catastrophic issue was detected on collar (no matter if firmware feature for action on collar is supported)THENUser should see on the 'Collar diagnostics' screen of the collar that has an issue a section with:a. Title: 'Halo Quality Assurance has detected an issue(s) with your collar.'b. Grey text: 'Log into your Account [hyperlink to magic link] to submit a warranty claim or order a replacement collar. If you would prefer to troubleshoot instead or need further assistance, please visit the Halo Dog Park [Deep link to Halo Dog Park].' [hyperlink to magic link]-blue, should initiate popup ME03-US121-AC16c. Action button 'Dismiss' | Zeplin: iOS | Android |
| ME03-US133-AC02 | Precondition: catastrophic issue detected for a collar.If user clicks the option 'Dismiss' on the collar diagnostics screenTHEN Display a popup Appendix 3 – Error, Success, Warning Messages#M270DismisstheissueTitle: 'Are You Sure?'Body:Text 1: 'If you confirmed with the support team that your issue has been resolved, check the box below and tap ‘Proceed’ to clear the alert signal on your collar.'Text 2: 'If you dismiss this message without resolving the issue, the error indicator will return automatically.'Checkbox with text: 'Halo Support confirmed that my issue has been resolved.' Buttons 'Proceed' and 'Cancel'. | Zeplin: iOS | Android |
