---
title: "ME21-US12. Onboarding: general requirements (for exceptional and alternative cases)"
sidebar_label: "ME21-US12. Onboarding: general requirements (for exceptional and alternative cases)"
sidebar_position: 242
last_modified: "Jun 25, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Timofey Burak [X] Maria Shikareva [X] Nikita Krisko Dmitry Kravchuk Katherina Kaplina |
| HALO-12562 - MOB: ME21-US12. Onboarding: general requirements (for exceptional and alternative cases) Closed |
| Click here to expand...01 Jul 2022 draft story is created by Galina Lonskaya14 Jul 2022 Maria Shikareva [X] Crossed out criteria about a stepper as they will be described separately within [NI] ME21-US11. Onboarding: parent screens (with video and stepper). |# Contents

General description Acceptance criteria No Internet Connection Session expiration Notifications

# General description

This story is intended for describing general requirements for the Onboarding flow, so that any alternative/exceptional scenarios are handled consistently within the whole flow.

Note: it seems that all criteria are already implemented within separate tasks. Therefore the following is required:

1. BA should describe all cases;
2. a mobile dev should check whether everything is implemented;
3. QA should test described cases.

# Acceptance criteria

| AC | Description | iOS UI design/ implementation status | Android UI design/ implementation status |
|---|---|---|---|
| No Internet Connection |
| ME21-US12-AC01 | If there is no Internet connection during Onboarding, then the app should display a Blue Bar on every screen (see the behavior description in ME12-F01-AC01) with the exception for Log In screen (ME01-F00. Run the app (Splash/ Start/ App startup failed screens)). | IMPLEMENTED | IMPLEMENTED |
| Session expiration |
| ME21-US12-AC02 | Session expiration happened during Onboarding flow should be handled as described in ME14-F01-AC03, ME14-F01 Unified errors handling. | IMPLEMENTED | IMPLEMENTED |
| Notifications |
| ME21-US12-AC03 | In-app notifications should not be shown during Onboarding flow. | TO DO | TO DO |
| ME21-US12-AC04 | In-app notification should be shown after Onboarding is completed (we should not miss this notification).From technical perspective it means that next time this in-app notification will be shown under the following conditions: the app is launched again (this condition remains as is: as described in ME08-US26. Receive in-app notification);Onboarding is completed. | TO DO | TO DO |
| ME21-US12-AC05 | Push-notifications should not be displayed during Onboarding flow.Implementation note: as of 25 Oct 2022 the app signs up for push-notifications on any screen when the tab bar is visible. It means that during Onboarding flow the app won't sign up for push-notifications - this is an existing logic and there's no need in changing it. | IMPLEMENTED | IMPLEMENTED |
| Notifications from Braze should be discussed and handled separately within another task: HALO-14427 - MOB: Braze notifications for Onboarding events Closed . |
