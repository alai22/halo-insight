---
title: "ME21-US09. Onboarding: flow completion"
sidebar_label: "ME21-US09. Onboarding: flow completion"
sidebar_position: 238
last_modified: "Jun 25, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] |
| HALO-12520 - MOB: ME21-US09. Onboarding: flow completion ('Almost Ready!' screen) Closed |
| 24 Oct 2022 Maria Shikareva [X]Updated ME21-US09-AC04 (on tapping the button the whole flow of adding a collar/ setting up Wi-Fi/ etc. should be opened) as discussed during development phase.Added ME21-US09-AC05 (standard error handling on communication with BE).28 Oct 2022 Maria Shikareva [X] Added ME21-US09-AC06 based on HALO-14497 - MOB: Spinner is not displayed when user taps 'Add Another Collar' button Closed |# General description

TBD

# User story

\> As an app user, I want to know when Onboarding flow is completed.

# Acceptance criteria

| AC | Description | Links, design |
|---|---|---|
| ME21-US09-AC01 | 'Almost Ready!' will be shown if user type = 'I have my Halo Collar' and one of the following conditions is met: User clicks 'Next' button on the 'Tour of the Halo Collar App' User clicks 'Watch Later' button on the M262 popup |  |
| ME21-US09-AC02 | 'Almost Ready!' screen should have the following elements: icon (see ME21-US04. Onboarding: Support functional screen)Title: Almost Ready!Text: Before you attempt to use your Halo Collar or create a Halo Fence, please proceed through Halo training - beginning with Basic User Training. Essential safety information and guidelines are included in this training content!Button: Start Halo TrainingSubtitle: Do you have another Halo Collar?Text: To add it now, click the link below. You can also add it later from Settings \> My Collars.Button: Add Another Collar | Link to Zeplin iOSAndroid |
| ME21-US09-AC03 | When I tap 'Start Halo Training', then I navigated to 'Begin Your Halo Training Program!' | - |
| ME21-US09-AC04 | When I tap 'Add Another Collar', then I navigated to ''Charge Your Halo Collar' (i.e. the whole flow of adding a collar/ configuring Wi-Fi/ FW update/ GPS initialization/ pet assigning should be initiated).Note: see the link to Miro board. | - |
| ME21-US09-AC06 | Precondition: a user tapped 'Add Another Collar' button.A spinner should be displayed until 'Charge Your Halo Collar' screen is opened (the same behavior as we have on adding a collar from 'My Collars' list). |  |
| ME21-US09-AC05 | ME14-F01 Unified errors handling mechanism should also be applied. | - |
