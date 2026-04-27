---
title: "(Won't do) ME03-US81. UX improvements for \"Collar Diagnostic\" screen (in-app link + 'Report issue')"
sidebar_label: "(Won't do) ME03-US81. UX improvements for \"Collar Diagnostic\" screen (in-app link + 'Report issue')"
sidebar_position: 216
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Timofey Burak [X] |
| HALO-11542 - MOB: UX improvements for "Collar Diagnostic" screen: add "Report issue" button and in-app link on compass cal-n) Closed |
| Click here to expand...29 Apr 2022 Maria Shikareva [X] Added ME03-US81-AC08 to track how many users enters this screen and compare with Daily Active Users. |# Contents

Contents User story Acceptance criteria Compass section Battery section 'Report the issue' link Analytics

# User story

\> As a Halo app account owner I want to have an ability to open required in-app links from the 'Collar Diagnostic' screen directly so that not to search for them manually.

# Acceptance criteria

| AC | Description | iOS screen designs/ implementation status | Android screen designs/ implementation status | AS IS | TO BE |
|---|---|---|---|---|---|
| Compass section |
| ME03-US81-AC01 | Precondition: there's an issue with compass displayed.'Advanced Settings' should be an in-app link that should lead to the Advanced settings screen. | - | - |
| ME03-US81-AC02 | Precondition: the Advanced settings screen was initiated from the 'Collar Diagnostic' screen.When the user taps a 'back' button, the app should open the 'Collar Diagnostic' screen again. | - | - |
| Battery section |
| ME03-US81-AC03 | Precondition: there's an issue with battery displayed.The text should be updated:AS ISTO BEYour battery's maximum capacity has fallen below 70%. Contact support about replacing the battery.Your battery's maximum capacity has fallen below 70%. Report the issue for further instructions. | Your battery's maximum capacity has fallen below 70%. Contact support about replacing the battery. | Your battery's maximum capacity has fallen below 70%. Report the issue for further instructions. | - | - |
| Your battery's maximum capacity has fallen below 70%. Contact support about replacing the battery. | Your battery's maximum capacity has fallen below 70%. Report the issue for further instructions. |
| ME03-US81-AC04 | 'Report the issue' should be a clickable link. | - | - |
| 'Report the issue' link |
| ME03-US81-AC05 | When the user taps on the "Report the issue" link, then the app should open the default email sender with the draft "Issue with battery" email. | - | - |
| ME03-US81-AC06 | The "Issue with battery" email should consist of: Subject: [HALO-APP] Collar Diagnostic: Battery issueEmail recipient: support@halocollar.zendesk.comEmail body: Please do not delete information below: it's required for further instructions.Collar SN: \<collar SN\>.Issue: battery's maximum capacity is below 70%.Note 1 : the sender's email can differ from the email that is used in Halo account.Note 2: no attachments.Note 3: \<70\> is added to config (within [Not implemented] ME03-US71. Add "Collar Diagnostic" section to the "Collars list").TBD need to highlight to Michael that CSA should have an ability to check received data (in Qlik?). | - | - |
| ME03-US81-AC07 | When the user sends an email, the app should open a 'Collar Diagnostic' screen. | - | - |
| Note: Softeq doesn't control the following behavior, but it's assumed to be performed: In case support@halocollar.zendesk.com is chosen as the email recipient, then after the email sending Zendesk request should be created and CSAs should be able to view it in https://halocollar.zendesk.com/agent/dashboard. |
| Analytics |
| ME03-US81-AC08 | The app should track and sent to Google Analytics:the following event → a user enters a "Collar Diagnostic" screen;the platform. | - | - |
