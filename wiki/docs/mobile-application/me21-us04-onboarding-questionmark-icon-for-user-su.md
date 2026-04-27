---
title: "ME21-US04. Onboarding: 'Questionmark' icon for user support (->Need Help screen)"
sidebar_label: "ME21-US04. Onboarding: 'Questionmark' icon for user support (->Need Help screen)"
sidebar_position: 240
last_modified: "Aug 14, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | History of changes | Is changed by |
|---|---|---|---|---|
| APPROVED BY SQ |
| Valeryia Chyrkun [X] Timofey Burak [X] Nikita Krisko Siarhei Leushunou [X] |
| HALO-12517 - MOB: ME21-US04. Support page 'Need Help?' Closed HALO-13248 - MOB: Add questionmark icon to Enable Permission screen for showing 'Need help?' screen Closed |
| Click here to expand...28 Jul 2022 Valeryia Chyrkun [X]added ME21-US04-AC07 |
| ME21-US47. Onboarding: pre-release changes (Test Flight feedback) |# General description

Initially it was agreed to show the clickable questionmark icon on the [Not impl.] ME21-US02. Onboarding: 'Questionmark' explanation screen. After BA meeting it was decided not to allow users to click on icon. So the first time when questionmark icon appears on the Onboarding flow will be the Permissions screen.

# User story

\> As an app user, I want to be able to click icon to call the page which Support options, so I'm able to choose the preferable Support method at any time I need it without going to Settings.

# Acceptance criteria

| AC | Description | Links, design |
|---|---|---|
| ME21-US04-AC01 | When I tap on icon at any screen where it's added in the app, then I see 'Need Help?' modal window with the following elements:Image: see on the screen Title: Need Help?Text: In order to get an immediate response, please select one of the preferred options below:Subtitle: Halo HelpHalo Help iconText: The easiest and quickest way to get answers to your Halo product questions.Arrow buttonSubtitle: Halo Dog Park TMHalo Dog Park iconText: Join a live video session with a member of the Halo Support Team.Arrow buttonSubtitle: My ticketsMy Tickets iconText: Create and view Support tickets.Arrow buttonButton: Close | Figma iOSFigma Android |
| ME21-US04-AC07 | The text related to 'My tickets' on the Settings should be updated and contain the following verbiage:'Create and view Support tickets.' |  |
| ME21-US04-AC02 | 'Need Help? screen should not have stepper and '?' icon at the top of the page. | - |
| ME21-US04-AC03 | When I tap on 'Halo Help', then I navigated to 'Halo Help'. |  |
| ME21-US04-AC04 | When I tap on 'Halo Dog Park TM', then I navigated to 'Welcome to Dog Park!' screen | Zeplin |
| ME21-US04-AC05 | When I tap on 'My tickets', then I navigated to the 'My Tickets' screen (see ME02-F04. View "Help" screen (incl. integration with Zendesk and mobile logs)) | - |
| ME21-US04-AC06 | When I tap on 'Close', then 'Need Help?' screen closes and I am navigated to the previous page. | - |-


