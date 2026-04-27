---
title: "[Outdated] ME02-US09. Choose a 'Giver' who should receive the referral program bonus"
sidebar_label: "[Outdated] ME02-US09. Choose a 'Giver' who should receive the referral program bonus"
sidebar_position: 127
last_modified: "Feb 16, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X], Zakhar Makarevich (BE), Anastasia Brechko (QA), Pavel Leonenko (MOB) |
| HALO-5922 - BE [SMRGP II]: 'Choosing a 'giver' who should receive referral program bonus' (optional) Closed HALO-6688 - MOB [SMRGP II]: 'Choosing a 'giver' who should receive referral program bonus' Closed |
| 16 Feb 2022 Maria Shikareva [X] Marked the story as "outdated" after new Referral Program release (see actual requirements here: EC03 Referral program). |# Possible options discussed

Click here to expand...| Option | Decision | Flow description | Pros | Cons | Ballpark estimation | BE | MOB | Via e-mail | Via mobile app |
|---|---|---|---|---|---|---|---|---|---|
|  | The Receiver binds a collar within the account.BE sends an e-mail to the Receiver with the list of all Givers who has invited the Receiver (and meet the requirements of the Referral program).The Receiver select one Giver by clicking the link with their name within e-mail. | Mobile work is not required → cheaper to implement. | E-mails may fail to be sent.Receivers may not read the e-mails. | X | - |
|  | The Receiver binds a collar within the account.The Receiver sees a dialog with the list of all Givers who has invited the Receiver (and meet the requirements of the Referral program).The Receiver select one Giver by tapping on the Giver's name. | It's a better solution from UX perspective. | Mobile work is required.The logic may be complex:E.g. the user kills the app when the dialog is shown: what to do in this case: show in some time, skip at all or smth else?)E.g. can we skip this step? and return later? | X minus (1-2 SP) | 3 SP |User story

\> As a Receiver (a Referral) I want to be able to select a Giver (a Referrer) so that the Referral program bonuses will be granted only for the most preferable one.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation notes | Android screen design/ implementation notes |
|---|---|---|---|
| ME02-US09-AC01 | When the user taps the 'Select' button on the 'Referrals' screen, then:the request is sent to the back-end;the app displays the screen with the spinner on the screen (see the screen designs).After getting the response from BE the app displays the corresponding pop-up message (depending on the response) in ME02-US09-AC02.Tech note: the app behavior when the user kills the app while spinner is running is described here: ME14-F02 General system implementation constraints. | Pic ME02-US09-P01 'Referrers + spinner' screenLink to Zeplin | Link to Zeplin |
| ME02-US09-AC02 | Precondition: BE has successfully responded.The 'Congratulations' pop-up should be displayed: M169 Bonuses granted to Receiver (see the screen designs). | Pic ME02-US09-P02 'Congratulations' pop-upLink to Zeplin | Link to Zeplin |
| ME02-US09-AC03 | All the errors should be handled in accordance with ME14-F01 Unified errors handling. | - | - |
| ME02-US09-AC04 | When the user taps the 'OK' button, then:the pop-up should be closed;the 'Referrals' screen should be opened with the updated information. | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME02-US09-IN01 | The 'You have free month(s) waiting' banner should be hidden from UI before displaying M169 Bonuses granted to Receiver.Note: pull-to-refresh action is not required here. |
