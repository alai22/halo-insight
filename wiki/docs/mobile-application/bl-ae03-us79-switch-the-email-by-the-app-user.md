---
title: "[BL] AE03-US79. Switch the email by the app user"
sidebar_label: "[BL] AE03-US79. Switch the email by the app user"
sidebar_position: 204
last_modified: "Jun 02, 2022"
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owners | Link to JIRA issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] Dmitriy Morozov [X] Siarhei Leushunou [X] |
| HALO-11127 - BE+MOB: Switch the email by the app user Closed HALO-11706 - [MOB]: The 'App Error'popup appears in the app when user taps on 'Change email' on the second device Ready for Development |
| Click here to expand...As of 04/05/2022 updated AE03-US79-AC09As of 04/06/2022 updated AE03-US79-AC03, added AE03-US79-AC10 and AE03-US79-AC11, edited AE03-US79-AC06As of 04/11/2022 added AE03-US79-AC12As of 04/13/2022 edited precondition on AE03-US79-AC09As of 04/14/2022 added AE03-US79-AC13As of 04/19/2022 added AE03-US79-AC14As of 05/24/2022 added AE03-US79-AC15As of 06/02/2022 added AE03-US79-AC16 |# General description

We need a self-service email change feature for the cases when user changes his email and would like to update it on our Halo app. Currently, the process of email change needs active CSA's involvement which is not convenient for both sides. It would be great to allow users to change the email themselves to one that is not assigned to activated account. If it is assigned we will not allow the email change.

The process should include request to email change, confirmation on new email and replacement of old email to new email.

# User story

\> As an app user I want to be able to change the email assigned to my account, so that I am able to update it on my account in case I no longer use the current email address.

# Acceptance criteria

| AC | Description | Notes, links, wire frames |
|---|---|---|
| AE03-US79-AC01 | The 'Email' field should be added on Edit Account screen with the button 'Change'. | iOS Android |
| AE03-US79-AC02 | If I click the 'Change' button then 'Enter your New Email' page is displayed with the following elements:'Change email' title'Enter Your New Email' subtitle'You will need to confirm your new address with the 6-digit code we have emailed to your new mail address.' text'New Email Address' input field'Change Email' button | iOS Android |
| AE03-US79-AC03 | The email can be changed only if:newly entered email has correct format (see AE03-US79-US04)newly entered email is not assigned to any account in the system (see AE03-US79-US05)newly entered email is assigned to the account with status 'inactive' or 'pending' (see AE03-US79-US07)If the newly entered email is assigned to any account with 'active' status, then user is not allowed to make email change. (see AE03-US79-US08) |
| AE03-US79-AC13 | In case the email is too long to fit the frame, it should be abbreviated with "..." |
| AE03-US79-AC04 | Precondition: User enters incorrect email on 'Email' fieldIf user clicks 'Change email' button then system validates entered email value and follows the next rules:Number of characters : User is allowed to enter no more than 50 characters. The system doesn't allow to enter more symbols.Email format. The system should check the email format for “@” and “.” presence. If the format is incorrect, then the "Invalid email address." inline error should be displayed after user clicks 'Change email' button. Blank field. If the email is not entered (empty field), then the "Сan not be blank" inline error should be displayed after user clicks 'Change email' button. |  |
| AE03-US79-AC05 | Precondition: User enters valid email (not assigned to any account) If I click 'Change email' button then the new mobile screen 'Verify Your Email' is displayed with the elements:'Change Email' title'Verify Your Email' subtitle'Please enter the code that was emailed to \<newly entered email\> to verify your account' text'Code' input area'Didn't receive a code?' text + 'Resend email' link'Done' button (inactive until user enters code). If I click 'Continue' button then the system displays the Edit Account screen with newly entered email.'Cancel' button. If I click Cancel then I navigate to to the Edit Account screen (with 'Verify' button) .User is allowed to enter only 6 characters (see EE01-US02-AC04).If user enters the expired or incorrect code and clicks 'Done', then the 'Invalid or expired code' field error should be displayed.If I click 'Resend code' link, then see the description on EE01-US02-AC13 | iOS Android |
| AE03-US79-AC06 | Precondition: user enters valid email for change and closes the app without entering the code or user clicks 'Cancel' button on 'Verify Your Email' screenIf I navigate to Edit Account screen, then I see:the newly entered email and Verify button on Email row'Changed your mind?' text'Restore previous email address' buttonIf I click Verify button, then I navigate to the 'Verify Your Email' screen. |  |
| AE03-US79-AC12 | If I click 'Restore previous email' button then the request for email change is cancelled and user is navigated to 'Edit Account' screen with the button 'Change' and the previously used email address. |  |
| AE03-US79-AC07 | Precondition: User enters the existing email and this email is assigned to inactive account If there's an account assigned to the new email, but this account is not activated (has 'pending' or 'inactive' status), then after clicking 'Change Email' button user will see the pop-up screen (see M229).If user successfully verifies the email, then the old email is deleted |  |
| AE03-US79-AC08 | Precondition: User enters the existing email and this email is assigned to another active account If there's an account assigned to the new email and this account is activated, then after clicking 'Change Email' button on 'Enter your New Email' page user will see the pop-up screen M232. |  |
| AE03-US79-AC09 | Precondition: User enters valid email (not assigned to active account) and the following email is sent to the newly entered email addressText of email see on EM034.where \<XXXXXX\> is a one time code randomly generated by BE. The detailed description on code generation see on EE01-US02. SSO: Sign Up process improvement: use a code instead of the confirmation link. The code have the expiration time - 24 hours. |  |
| AE03-US79-AC10 | Precondition: First user enters new email for change, doesn't not verify it and closes the app at the step of verification (see AE03-US79-AC05). At the same time another user activates the email that was in status 'pending' at the moment the first user requested email change. If user navigates the 'Edit Account screen' they will see their new email with the button 'Verify' | iOS Android |
| AE03-US79-AC11 | Precondition: First user enters new email for change, enters valid verification code from the email. At the same time another user activates the email that was in status 'pending' at the moment the first user requested email change. If user enters verification code and clicks 'Done', then user will see AE03-US79-AC08 and user is redirected to Edit Account screen (see AE03-US79-AC01)Note: The request for change is cancelled in the database. | iOS Android |
| AE03-US79-AC14 | Only one request can be associated with the specific email address. When someone creates the request for email change for the address that was already used for another request then the first request is cancelled.E.g. user creates the request for email change to xx@xx.xx in one account and afterwards creates another request for the same address then the first request cancelled and the second can be verified with email |  |
| AE03-US79-AC15 | Precondition: First user enters new email for change, leaves the app without verification. At the same time another user with the same credentials enters the email for change on another device.When I click 'Change email' button on 'Change email - Enter your email' screen then I see the error message 242 pop-up. |  |
| AE03-US79-AC16added as a fix of bug Halo-12126 | Precondition: user buys a collar on e-commerce site using email 1 (details of purchase are stored in our DB) and register on the app with the same email (UserProfileId1).user buys the second collar on e-commerce site using email 2 (details of purchase are stored in our DB) - UserProfileId2.If I change email 1 to email 2 in the app, then email 2 appears in the Admin panel, UserProfileId2 is marked as active in ECommerceUser, UserProfileId1 becomes inactive. All the purchase details assigned to UserProfileId1 should be transferred to UserProfileId2. |  |
