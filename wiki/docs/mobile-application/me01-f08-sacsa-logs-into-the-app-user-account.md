---
title: "ME01-F08. SA/CSA logs into the app user account"
sidebar_label: "ME01-F08. SA/CSA logs into the app user account"
sidebar_position: 25
last_modified: "Oct 11, 2024"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| Baseline story (checked by dev team) |
| APPROVED |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko |
| HALO-2482 - [ME01. Enter the system] [ME01-US08. Super Admin logs into the app user account] Closed HALO-4698 - Android: ME01-F08. SA/CSA logs into the app user account Closed |
| 14 Dec 2022 Maria Shikareva [X] Updated ME01-F08-AC02 (added a note about Onboarding).11 Oct 2024 ME01-F08-AC05 is added by Galina Lonskaya (discussed internally in QA chat) |# User story

\> As SA (Super Admin) or CSA (Customer Support Agent), I want to log into the app user's account so that I can help the app user with app usage.

| AC | Description | iOS design | Android design |
|---|---|---|---|
| ME01-F08-AC01 | SA/CSA should be able to log into the app user's account with the following credentials:SA (CSA)'s emailAccess code in PENDING status from the emailSee the code creation details in AE03-US06. Request one-time user account access via the app. | - | - |
| ME01-F08-AC02 | The app user's personal info shouldn't be available for the Super Admin.If the Super Admin tries to enter to the Account, then the M116 Super Admin doesn't have access to the app user's personal data error should be displayed.Note: onboarding will NOT be visible for SA/ CSA and will be skipped on the mobile side without checking a flag on BE side. | - | - |
| ME01-F08-AC03 | For now, the app users don't get any push-notifications related to the "log in"/ "log out" of SA/CSA to their account. | - | - |
| ME01-F08-AC04 | SA/CSA should see the "Log out" button at the Settings screen.Note: This is required as Super Admin can't see the Profile screen, but he/she should be able to log out from the app. | - | - |
| ME01-F08-AC05 | SA/CSA should not see 'Refer a Friend' option on Settings screen. | - | - |
