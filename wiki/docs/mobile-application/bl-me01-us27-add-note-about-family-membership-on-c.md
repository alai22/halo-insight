---
title: "[BL] ME01-US27. Add note about \"family membership\" on \"Create/edit account\" screen"
sidebar_label: "[BL] ME01-US27. Add note about \"family membership\" on \"Create/edit account\" screen"
sidebar_position: 245
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] |
| HALO-12508 - MOB: Add note about "family membership" on "Create/edit account" screen Closed |
| 14 Oct 2022 Maria Shikareva [X] Marked the story as baselined (see ME01-F03. Add profile info after Sign Up). |# General description

# User story

\> As an app user, I want to be informed on how to use shared account with members of my family.

# Acceptance criteria

| AC | Description | Links, design |
|---|---|---|
| ME01-US27-AC01 | The following text should be added at the bottom of 'Tell Us Your Name' (see the initial reqs here):Plan to share the Halo app with your family? Tap here to learn how.Where 'Tap here' is a button to show 'Family Membership' card. | iOS Android |
| ME01-US27-AC02 | If I tap on 'Tap here', then I see 'Family Membership' card with the following elements:Title: Family MembershipBody: When you create an account in the Halo App and connect to that account, only that specific account can be used to access that collar. Therefore, if there are multiple people in your family who need access to the collar, you must share the same login credentials. We strongly recommend that each individual who is accessing the Halo Collar through the app goes through User Training before taking responsibility for a dog that is using the collar.Button: Close | iOS Android |
| ME01-US27-AC03 | If I tap 'Close' button then the 'Family Membership' card is closed. |  |
| ME01-US27-AC04 | 2 events for gathering analytics should be added: View_family_membership_cardCreate_user_account |  |
