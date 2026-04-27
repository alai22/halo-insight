---
title: "[Outdated] ME02-US12. Blue dot indicator for the Referral program"
sidebar_label: "[Outdated] ME02-US12. Blue dot indicator for the Referral program"
sidebar_position: 141
last_modified: "Feb 16, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X], Aleksandra Mashenkova (MOB), Maria Levko [X] (QA) |
| HALO-6693 - MOB: ME02-US12. Blue dot for the Referral Program Closed |
| Maria Shikareva [X] 06 Apr 2021 Added the links to the designs in Zeplin.Maria Shikareva [X] 12 Apr 2021 Added a note to the Android design due to some special system behavior.Maria Shikareva [X] 16 Feb 2022 Marked the story as "outdated" after new Referral Program release (see actual requirements here: EC03 Referral program). |# User story

\> As a user I would like to see the blue dot on the corresponding tabs and screens so that to be aware that some actions are required from my side for the Referral Program.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation notes | Android screen design/ implementation notes |
|---|---|---|---|
| Precondition: the user logs in the app/ opens the minimized app AND the mobile app gets a response from BE that the user has bonuses to accept and/ or several referrers to select (the whole logic for the referral program check is described in preconditions for the [Outdated] ME02-US11. Add 'Referrals' menu option to the Account screen). |
| ME02-US12-AC01 | A 'Blue dot' indicator should be displayed on the 'Settings' tab. | Pic ME02-US12-P01 'Blue dot on Settings + Account'Link to Zeplin | Link to ZeplinNote: when the 'Settings' tab is selected, the title is enlarged a little, so the blue dot design can slightly differ due to Android standard behavior.E.g. |
| ME02-US12-AC02 | Precondition: the user opens the 'Settings' tab.A 'Blue dot' indicator should be displayed on the 'Account' button tab. | - | - |
| ME02-US12-AC03 | Precondition: the user taps the 'Account' button.A 'Blue dot' indicator should be displayed on the 'Referrals'. | Pic ME02-US12-P02 'Blue dot on Referrals'Link to Zeplin | Link to Zeplin |
| ME02-US12-AC04 | A blue dot should disappear from all the described places above only when there are no required actions on the 'referrals' screen (i.e. the user has no bonuses to accept AND has no referrers to select). | - | - |
