---
title: "[Outdated] ME02-US14. Banner as a reminder for the Referral Program actions"
sidebar_label: "[Outdated] ME02-US14. Banner as a reminder for the Referral Program actions"
sidebar_position: 147
last_modified: "Feb 16, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X], Anastasia Brechko (QA), Pavel Leonenko (MOB), Timofey Burak [X] (MOB), Aleksandra Mashenkova (MOB) - the requirements are reviewed while the US review meeting on 04/13/2021. |
| HALO-6759 - MOB [SMRGP II]: ME02-US14. Banner as a reminder for the Referral Program actions Closed HALO-6974 - BE [SMRGP II]: ME02-US14. Banner as a reminder for the Referral Program actions Closed |
| 16 Feb 2022 Maria Shikareva [X] Marked the story as "outdated" after new Referral Program release (see actual requirements here: EC03 Referral program). |# User story

\> As a user I would like to see a reminder while I'm using the HALO app if some actions are required for the Referral Program from my side so that to be notified about it and not miss my bonuses.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation notes | Android screen design/ implementation notes |
|---|---|---|---|
| Precondition: the user logs in the app/ opens the minimized app AND the mobile app gets a response from BE that the user has bonuses to accept and/ or several referrers to select (the whole logic for the referral program check is described in preconditions for the [Outdated] ME02-US11. Add 'Referrals' menu option to the Account screen). |
| ME02-US14-AC01 | The app should display the corresponding banner when the user opens either 'My map' or 'Training' tab. | Pic ME02-US14-P01 'Referral banner' Link to Zeplin | The design is similar to iOS. |
| ME02-US14-AC02 | The banner should say the following:You have Free Months of Gold waiting!To accept, go to Settings→Account→Referrals. | - | - |
| ME02-US14-AC03 | The banner should be enabled for the first time when the app gets the info from BE that the user has bonuses to accept/ givers to select. | - | - |
| ME02-US14-AC04 | The user should be able to close the banner by tapping on the cross icon. | - | - |
| ME02-US14-AC05 | Precondition: the banner was closed but the user still hasn't accepted the bonuses/ selected the giver OR the user has accepted the bonuses partially.The banner should be re-enabled again in 7 days after the user closes the banner (i.e. MOB will remember the time of closing the banner).Note: next banner will be shown in 7 days even if the amount of bonuses was changed (e.g. new bonuses appeared/ user got No Plan and then re-activate the plan within these 7 days). | - | - |
| ME02-US14-AC06 | If the banner is closed on 'My Map' screen, it also should not be shown on the 'Training' screen, and vice versa. | - | - |
| ME02-US14-AC07 | When the user pulls-to-refresh the content on the Training screen, the banner should remain on the same place and the spinner should be displayed below it. | - | - |
| ME02-US14-AC08 | Precondition: the banner was not closed.When the user has accepted all the bonuses and selected the giver (i.e. no actions are required from them within the 'Referrals' screen), the banner should disappear both on 'My Map' and 'Training' screens. | - | - |
| ME02-US14-AC09 | The banner should not be tappable. | - | - |
| ME02-US14-AC10 | The banner should be displayed below the toast messages.Note: the reason is that in this case the users can read toast messages before they disappear. | - | - |
| ME02-US14-AC11 | The banner should be displayed under the 'No internet connection' blue panel.Note: the reason is that 'No internet connection' panel contains more valuable information for the user. | - | - |
| ME02-US14-AC12 | If the Banner with temporary privileges is shown, then the banner for the Referral Program should not be displayed until the Banner with temporary privileges disappears.Note 1: in this case next time the banner should be shown on opening the app, not on closing the Banner with temporary privileges.Note 2: if the 'Referral banner' is displayed and MOB gets info that the Banner with temporary privileges should be also displayed, the 'Referral banner' should be hidden, as Banner with temporary privileges has higher priority. | - | - |
| ME02-US14-AC13 | The banner should not be visible on:'Edit pet profile' screen;'Feedback settings' screen;any of the 'Create fence' flow screens;any of the training course screens. | - | - |
