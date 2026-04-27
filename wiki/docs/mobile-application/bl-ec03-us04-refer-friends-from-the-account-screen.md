---
title: "[BL] EC03-US04. Refer friends from the \"Account\" screen"
sidebar_label: "[BL] EC03-US04. Refer friends from the \"Account\" screen"
sidebar_position: 166
last_modified: "Aug 30, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Yuri Zhdanovich [X] Pavel Leonenko Valeria Malets |
| HALO-9174 - MOB [+BE]: Refer friends from the "Account" screen Closed HALO-9228 - BE [+MOB]: Refer friends from the "Account" screen Closed HALO-9398 - BE+MOB: Refer friends from the "Account" screen Closed Ballpark:MOB: 2 SPBE: 1SPQA MOB: 2SPQA BE: 1SP |
| Click here to expand...27 Oct 2021 Maria Shikareva [X] EC03-US04-AC07 is updated (a picture name is added).15 Nov 2021 Maria Shikareva [X] Added Jira links.19 Nov 2021, 23 Nov 2021 Maria Shikareva [X] The texts and designs are updated based on Michael's comment from 18 Nov 2021 .EC03-US04-AC04 is crossed out because of changes in the text.06 Dec 2021 Maria Shikareva [X] Marked the story as "implemented".30 Aug 2022 Maria Shikareva [X] Marked the story as baselined (see ME02-F00. View "Settings" screen, ME02-F08. View "Refer a Friend" screen). |# Contents

User story Acceptance criteria Implementation notes

# User story

\> As a Halo app user I want to see a separate menu option for the Referral program within the Account so that to refer my friends easily.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation notes | Android screen design/ implementation notes |
|---|---|---|---|
| EC03-US04-AC01 | A new "Refer a friend" menu option with a 'Right arrow' tile should be displayed on the "Account" screen instead of the "Referrals" menu option. Note 1: all other elements should remain the same as described in ME02-F01-AC01 (ME02-F01. View "Account" screen).Note for QAs: ME02-US11-AC01 criterion is no more valid. | Pic EC03-US04-P01 'Account' screenLink to Zeplin | The same as for iOS.Link to Zeplin |
| EC03-US04-AC02 | "Refer A Friend" menu option should be visible only if there's a generated code for this user (based on info from BE) regardless of whether the user has a collar in the account or not.Note 1: see EC03-US04-IN01 below.Note 2: the code should not be expired. I.e. if the usage_limit reaches 5, then BE will generate a new code (for more details see [Not implemented] EC03-US02. Generate a coupon code to refer someone). If for some reason the code is expired and a new one is not generated yet, then this option should not be visible. | - | - |
| EC03-US04-AC03 | When the user taps the "Refer a friend" menu, then the app should open the 'Refer a Friend' screen with the following UI elements (see the screen designs):a "Back" icon;a 'Refer a Friend' title;an image;"Give $50. Get $50" title;a Referral Program explanation with the following text:Refer a Friend Today and Get RewardedShare your love for Halo with a friend — you get a $50 gift card and they get $50 offtheir new Halo!a 'Code' section:\<Coupon code\>;For more details see the main requirements to the coupon code here: [Not implemented] EC03-US02. Generate a coupon code to refer someone'Tap to copy" button. | Pic EC03-US04-P02 'Refer a friend' screenLink to Zeplin | Link to Zeplin |
| EC03-US04-AC04 | Halocollar.com should not be a link. | - | - |
| EC03-US04-AC05 | The following parameters should be configurable on BE side:"50$" discount for a receiver (a coupon amount parameter);"5 times usage" (a coupon usage_limit parameter);60 days (ReferralRewardDuration parameter);"50$" reward for the giver (ReferralRewardAmount parameter).Note1: see the details in [Not implemented] EC03-US02. Generate a coupon code to refer someone.Note 2: see EC03-US04-IN02 below. | - | - |
| EC03-US04-AC06 | When the user taps a "Back" icon, the system should open the "Account" screen. | - | - |
| EC03-US04-AC07 | When the user taps a "Tap to copy" button, then the app should:copy the code to the clipboard;keep the "Refer A Friend" screen opened;display the following toast:Link copied to clipboard!Note: after copying the code the user will be able to send it in any available way to any person they want (email, text message, post somewhere, etc.). | Pic EC03-US04-P03 'Refer a friend' screen with a toastLink to Zeplin | The same as for iOS.Link to Zeplin |# Implementation notes

| IN | Description |
|---|---|
| EC03-US04-IN01 | The mobile app will retrieve the code from BE: on opening the app in the user_profileANDon restoring the app to the foregroundANDafter the user adds a collar to the account. |
| EC03-US04-IN02 | The mobile app will retrieve the parameters from config. |
