---
title: "[Outdated] ME02-US10. Accept bonuses for the referral program"
sidebar_label: "[Outdated] ME02-US10. Accept bonuses for the referral program"
sidebar_position: 139
last_modified: "Feb 16, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X], Zakhar Makarevich (BE), Pavel Leonenko (MOB), Anastasia Brechko (QA) |
| HALO-6692 - BE [SMRGP II]: ME02-US10. Accept bonuses for the referral program (optional) Closed HALO-6717 - MOB [SMRGP II]: ME02-US10. Accept bonuses for the referral program Closed |
| 16 Feb 2022 Maria Shikareva [X] Marked the story as "outdated" after new Referral Program release (see actual requirements here: EC03 Referral program). |# User story

\> As a user (both a Referrer or a Referral) I want to have an opportunity to accept my bonuses for participating in the Referral program so that they start after my acceptance only.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation notes | Android screen design/ implementation notes |
|---|---|---|---|
| ME02-US10-AC01 | When the user taps the 'Accept' button on the 'Referrals' screen, then:the request is sent to the back-end;the app displays the screen with the spinner on the screen (see the screen designs).After getting the response from BE the app displays the corresponding pop-up message (depending on the response) described in ME02-US10-AC02.Tech note: the app behavior when the user kills the app while spinner is running is described here: ME14-F02 General system implementation constraints. | Pic ME02-US10-P01 'Referrers + spinner' screenLink to Zeplin | Link to Zeplin |
| ME02-US10-AC02 | Precondition: the user is a Giver AND has any plan except 'No plan'.When the user taps an 'Accept' button on the 'You Have Free Month(s) Waiting' banner within the 'Referrals' screen, then the info pop-up message should be displayed: M168 Bonuses granted to Giver. | The pop-up should have the same design as in ME02-US09-AC02 on ME02-US09. Choose a 'Giver' who should receive the referral program bonus. | - |
| ME02-US10-AC03 | All the errors should be handled in accordance with ME14-F01 Unified errors handling. | - | - |
| ME02-US10-AC04 | When the user taps the 'OK' button, then:the pop-up should be closed;the 'Referrals' screen should be opened with the updated information. | - | - |
| ME02-US10-AC05 | If several bonuses are applied for the user (e.g. the Giver has invited several people and they bounded the collars simultaneously), then the info should be consolidated into one pop-up message: M168 Bonuses granted to Giver. | - | - |
| 'Temporary access expiration' banner |
| ME02-US10-AC06 | If the user currently has a temporary access to Gold plan and is granted one more access to the Gold plan that should start right after the first one expires, than the total amount of Gold days should be summed up. The banner should be shown according to the defined rules (ME19-US27-AC07, ME19-US27. Banner with temporary premium privileges expiration countdown)E.g. the user has 7 days of Gold left → sees the banner → at this day gets the 30 days for new Gold → the total amount of days should be 37 → the banner should not be shown until the 30 days remain. | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME02-US10-IN01 | The 'You have free month(s) waiting' banner should be hidden from UI before displaying M168 Bonuses granted to Giver.Note: pull-to-refresh action is not required here. |
