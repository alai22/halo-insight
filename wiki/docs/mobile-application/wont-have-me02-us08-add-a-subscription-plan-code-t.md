---
title: "[Won't have] ME02-US08. Add a subscription plan code to the User Account screen"
sidebar_label: "[Won't have] ME02-US08. Add a subscription plan code to the User Account screen"
sidebar_position: 124
last_modified: "Feb 01, 2021"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue |
|---|---|---|
| TEAM REVIEW |
| Maria Shikareva [X], Anastasia Brechko (QA), Pavel Leonenko (MOB), Eugene Paseka (BE) |
|  |# User story

\> As a user, I want to see a subscription plan code within my 'Account' screen so that CSA will be able to check easily what subscription level is currently applied on the mobile app. It may be useful, for example, in case the user has some troubles with their plan, contacts support and CSA has no other opportunity to define the user's current plan (AAP failed to synchronize with back-end). On the other hand App store reviewers will have no clue what does this code mean (for more details see the assumption here).

# Acceptance criteria

| # | Acceptance Criteria | iOS screen design/ implementation status | Android screen design/ implementation status | Precondition: the user tapped on the 'Account' button within 'Settings' screen. |
|---|---|---|---|---|
| ME02-US08-AC01 | The following Account screen should be displayed with the new current subscription plan code.The Account screen consists of:elements described in ME02-F01-AC01 of ME02-F01. View "Account" screen;subscription plan code (a new element next to the \<User name\> as shown on the design screen). |  |  |
| ME02-US08-AC02 | The following subscription plan codes should be used:NP - for No Plan;B1 - for Basic 1 month plan;B12 - for Basic 12 months plan;TBD with Heather Gode and Michael Ehrman:do we need separate codes for monthly/ yearly subscriptions?S1 - for Silver 1 month plan;S12 - for Silver 12 months plan;G1 - for Gold 1 month plan;G12 - for Gold 12 months plan.TBD with Heather Gode and Michael Ehrman:maybe it's better to make these codes less informative, e.g. X1, X2, X3, X4, etc.;do we need separate codes for temporary granted plans or current subscription plan only? | - | - |
