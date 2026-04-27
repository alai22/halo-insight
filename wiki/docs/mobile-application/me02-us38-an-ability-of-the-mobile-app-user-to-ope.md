---
title: "ME02-US38 An ability of the mobile app user to open eCommerce profile"
sidebar_label: "ME02-US38 An ability of the mobile app user to open eCommerce profile"
sidebar_position: 612
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history | BA processes | Estimates |
|---|---|---|---|---|---|
| FINAL |
| Maryia Paklonskaya [X] |
| HALO-15433 - BE+MOB: Add magic link to the profile in the app Closed |
| 31 Jan 2023 1st version of the requirements |
| create requirementsrefinementget final approve from the Halo LT finalized, ready for devadded final designsadd to the baseline |
| BE: 1spMOB: 2spQA: 2sp |User Story Acceptance criteria ME02-US38-AC01 ME02-US38-AC02 ME02-US38-AC03

# User Story

\> As a mobile app user I want to open My eCommerce Account from mobile app so that I could manage my subscription in any way I want

# Acceptance criteria

| ID | Acceptance criteria | Designs |
|---|---|---|
| ME02-US38-AC01 | Changes on the My Account screen: Delete "Edit Account" tabAdd pencil iconAdd "Manage My Account" tab with arrow | Old design: New design: ==\> Android; iOS |
| ME02-US38-AC02 | By clicking on the pencil icon - the edit page of the profile in the mobile app is shown. And user is able to change its name, surname, email and profile picture. | n/a |
| ME02-US38-AC03 | By clicking on the "Manage My Account" tab: The email EM049 Message with magic link to open profile from mobile app (Appendix 7 - Email messages#EM049) is sent to the userSubject:Manage Your Halo Pack MembershipBody:Dear [First Name or empty (if there is no First Name)],Click here to sign into your account and review your membership options:CTA BUTTON [magic link under the button with words "Sign into My Account"][NOTE: This link will log you in automatically for the next 72 hours. After that, you will need to log in manually. If you log in manually, remember to use the same login credentials that you used to log into the Halo Collar app.]If you believe you received this email in error, please let our support team know by emailing them at support@halocollar.com.Best regards,The Halo TeamAND"Check Your Email" pop over appears, it contains:Halo logo"Check Your Email" title"An email with next steps was sent to username@email.com." text, where username@email.com - is an email of current user"Open mail app \>" buttonby clicking on which - the default email application should open on the deviceClose - once clicked - the pop up closes, the screen is displayed with no changes | iOS |
