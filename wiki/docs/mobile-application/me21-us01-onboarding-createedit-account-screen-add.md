---
title: "ME21-US01. Onboarding: \"Create/edit account\" screen (add note about \"family membership\")"
sidebar_label: "ME21-US01. Onboarding: \"Create/edit account\" screen (add note about \"family membership\")"
sidebar_position: 231
last_modified: "Jul 13, 2022"
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Valeryia Chyrkun [X] |
| HALO-12508 - MOB: Add note about "family membership" on "Create/edit account" screen Closed |
| Click here to expand... |# General description

# User story

\> As an app user, I want to be informed on how to use shared account with members of my family.

# Acceptance criteria

| AC | Description | Links, design |
|---|---|---|
| ME21-US01-AC01 | The following text should be added at the bottom of 'Tell Us Your Name' (see the initial reqs here):Plan to share the Halo app with your family? Tap here to learn how.Where 'Tap here' is a button to show 'Family Membership' card. |  |
| ME21-US01-AC02 | If I tap on 'Tap here', then I see 'Family Membership' card with the following elements:Title: Family MembershipBody: When you create an account in the Halo App and connect to that account, only that specific account can be used to access that collar. Therefore, if there are multiple people in your family who need access to the collar, you must share the same login credentials. We strongly recommend that each individual who is accessing the Halo Collar through the app goes through User Training before taking responsibility for a dog that is using the collar.Button: Close |  |
| ME21-US01-AC03 | If I tap 'Close' button then the 'Family Membership' card is closed. |  |
| ME21-US01-AC04 | 2 events for gathering analytics should be added: View_family_membership_cardCreate_user_account |  |
