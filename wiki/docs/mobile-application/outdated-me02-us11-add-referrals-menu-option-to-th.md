---
title: "[Outdated] ME02-US11. Add 'Referrals' menu option to the Account screen"
sidebar_label: "[Outdated] ME02-US11. Add 'Referrals' menu option to the Account screen"
sidebar_position: 140
last_modified: "Feb 16, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X], Zakhar Makarevich (BE), Aleksandra Mashenkova (MOB), Maria Levko [X] (QA) |
| HALO-6691 - BE [SMRGP II]: ME02-US11. Add 'Referrals' menu option to the Account screen Closed HALO-6716 - MOB [SMRGP II]: ME02-US11. Add 'Referrals' menu option to the Account screen Closed |
| Maria Shikareva [X] 05 Apr 2021, 06 Apr 2021, 07 Apr 2021 Update the wording + the screen designs based on the comments from Michael Ehrman and Heather Gode.Maria Shikareva [X] 08 Apr 2021 Added a note for the link to the referral page for more clarity. Updated ME02-US11-AC02 (different plans can be granted within the Referral Program for possible future improvements).Maria Shikareva [X] 09 Apr 2021 Updated the precondition: a 'You Have X Referrals' banner will be shown if there is at least 1 Referrer for the user (it seems to be more user friendly: the user will see who has invited them and can accept bonuses or wait till the required Referrer appears in the list).Updated ME02-US11-AC02: only givers who has ever had a collar in the account should be visible in the list of givers (it's hard to 'remember' on BE if the user has never had a collar in the account but was selected as a Giver → it was discussed while estimating the ME02-US09. Choose a 'Giver' who should receive the referral program bonus).Maria Shikareva [X] 16 Feb 2022 Marked the story as "outdated" after new Referral Program release (see actual requirements here: EC03 Referral program). |# User story

\> As a user I want to see a separate menu option for the Referral program within the Account so that to see all the available options and information in one place.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation notes | Android screen design/ implementation notes |
|---|---|---|---|
| Precondition 1: The user has met all the conditions and can get bonuses for referring someone within the Referral program (for more details see EC03-US01-AC01, EC03-US01. Referral program: grant bonuses to the participants):both the Giver and Receiver has ever had collars in the account;the user has any subscription plan.Note: we want to restrict Givers and Receivers based on whether they have an 'active' subscription so that to motivate them buying a plan. If a giver has ended their plan, they will not receive their free 30 days until they re-activate their plan (i.e. the giver's benefit is on 'hold' until they re-activate).Precondition 2:The user (Receiver, Referral) has met all the conditions and has to select a Giver (Referrer):the user has already bounded a collar to the account;the user has any subscription plan;there is at least 1 Referrer for them.https://app.diagrams.net/#G13_uSerXkeDqLtFfd7noIV0Gx-UZoa9LU |
| ME02-US11-AC01 | When the user taps on the 'Account' button, then the Account screen should be displayed with the following UI elements:the elements described in ME02-F01-AC01 (ME02-F01. View "Account" screen);a 'Referrals' menu option with a 'Right arrow' tile:Should be always visible even if the preconditions above are not applied - i.e. anybody can see this menu option). | Pic ME02-US11-P01 'Account' screenLink to Zeplin | Link to Zeplin |
| ME02-US11-AC02 | Precondition: the mobile app has information that the user has bonuses to accept AND/ OR givers to select.When the user taps a 'Referrals' menu, then the 'Referrals' screen should be opened with the following UI elements (see the screen designs):a 'Back' icon;a 'Referrals' label;a 'Refer Your Friends' banner (always displayed):'Go to our website referral-program page to refer your friends.' text;a 'Go' button.a 'You Have Free Month(s) Waiting' banner (if precondition 1 is applied):a 'Someone accepted your referral! Please tap to accept your free Halo \<Subscription plan\> service.' text,where \<Subscription plan\> is the plan which is granted for the user within the Referral Program.Note: currently (as of 04/08/2021) only Gold plan is given within the Referral Program.an 'Accept' button.a 'You Have X Referrals' banner (if precondition 2 is applied), where X is the amount of Referrers for this user:a 'Choose a referral to accept, and you'll both receive one FREE Month of Halo \<Subscription plan\> Plan.' text;where \<Subscription plan\> is the plan which is granted for the user within the Referral Program.Note: currently (as of 04/08/2021) only Gold plan is given within the Referral Program.a down arrow tile;the list of givers who has ever had a collar in the account.Expanded by default. | Pic ME02-US11-P02 'Referrals' screenLink to Zeplin | Link to Zeplin |
| ME02-US11-AC03 | When the user taps a 'Go' button, then a https://www.halocollar.com/referral-program/ web page should be opened in the default mobile browser.Note: in order to access the Referral page the user must be logged in. If they try to access the referral page and are not logged in, then they must first get through the SSO login process. |  |  |
| ME02-US11-AC04 | When the user taps an 'Accept' button, then the app performs the actions as described in [Outdated] ME02-US10. Accept bonuses for the referral program. | - | - |
| ME02-US11-AC05 | When the user taps a 'You Have X Referrals' banner, then the list of givers should be collapsed. | Link to Zeplin | Link to Zeplin |
| ME02-US11-AC06 | The list of givers should contain the following:a Giver name (First + Last);If there's no data about the giver's name, then only a giver's email should be displayed.a giver's email;a 'Select' button. | - | - |
| ME02-US11-AC07 | When the user taps a 'Select' button, then the app performs the actions as described in [Outdated] ME02-US09. Choose a 'Giver' who should receive the referral program bonus. | - | - |
| ME02-US11-AC08 | The user should be able to choose only one Giver. |  |  |
| ME02-US11-AC09 | If the user pulls down the screen, the info should not be refreshed. | - | - |# Implementation notes

|  | Description |
|---|---|
| ME02-US11-IN01 | The mobile app will request the info about the referral bonuses/ givers on opening the app (the same as for the info about the subscription plans). |
