---
title: "ME01-F06. Set a new password (web)"
sidebar_label: "ME01-F06. Set a new password (web)"
sidebar_position: 93
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issue |
|---|---|---|---|
| Baseline story (checked by dev team) |
| APPROVED |
| Galina Lonskaya, Anastasia Brechko |
| HALO-2866 - MOB+BE: ME01-US14. Forgot password (new UI design) Closed |# User story

\> As an account owner, I want to set a new password so that I can log into my account using the new password.

| AC | Description | UI design / impl-n status |
|---|---|---|
| ME01-F06-AC01 | Precondition: EM002 Reset Your Halo Password (initiated by app user) or EM005 Reset Your Halo Password (initiated by admin) is opened.I press the Reset Password button and the recovery link is expired, then:web screen with the "Resend recovery link" button should be opened. See Pic 1. | Pic 1 Web screen with the expired recovery linkIOS DONE ANDROID TO DOLink to Zeplin |
| ME01-F06-AC02 | Precondition: Web screen with the "Resend recovery link" button is opened. See Pic 1.If I press the Resend recovery link button and the email is sent, then:EM002 Reset Your Halo Password (initiated by app user) with a new link should be sent;A web screen with a success message should be displayed. See Pic 2. | Pic 2 Web screen with the info that new recovery link has been sentIOS DONE ANDROID TO DOLink to Zeplin |
| ME01-F06-AC03 | Precondition: EM002 Password reset initiated by app user is opened.I tap on the Reset Password button and the recovery link isn't expired, then:web screen new password setting should be displayed. See Pic 3.Note: See the screen functionality description below in the table ME01-F06-1 "Reset Your Halo Password" web screen: functionality description. | Pic 3 Web screen with the fields to create a new passwordIOS DONE ANDROID TO DOLink to Zeplin |
| ME01-F06-AC04 | Precondition: "Reset Your Halo Password" web screen is displayed. The system should allow me to hide and show the typed password by pressing an eye icon.By default, the crossed icon should be displayed. | IOS DONE ANDROID TO DO |
| ME01-F06-AC05 | Precondition: "Reset Your Halo Password" web screen is displayed. If I tap on the Submit button and the entered passwords match, but they don't correspond to BR-5, then:"Please enter a strong password" should be displayed. | IOS DONE ANDROID TO DOSee the similar error displaying as below. |
| ME01-F06-AC06 | Precondition: "Reset Your Halo Password" web screen is displayed. If I tap on the Submit button and the entered passwords don't match (BR-5 isn't taken into account), then:"Passwords don't match" error should be displayed. See Pic 4. | Pic 4 Web screen with the fields to create a new password and errorIOS DONE ANDROID TO DOLink to Zeplin |
| ME01-F06-AC07 | Precondition: "Reset Your Halo Password" web screen is displayed. If both password fields are empty and I press the "Submit" button, then "Please enter a new password" should be displayed. | IOS DONE ANDROID TO DO |
| ME01-F06-AC08 | Precondition: "Reset Your Halo Password" web screen is displayed. If I tap on the Submit button and the entered passwords match and correspond to BR-5, then:the old password cannot be used for login further;web screen with a success message should be displayed;The system should log me out of my account on all devices once the Access token expires (as of 1/24/2023 expiration period = 2 h).I can log into the Halo app with a new password. | Pic 5 Web screen with the success message about the new password savingIOS DONE ANDROID TO DOLink to Zeplin |
| ME01-F06-AC09 | I can change a password in both statuses: active and inactive. | - |
| ME01-F06-AC10 | If the link was used successfully for the password set, then:the link should get "expired" status. | - |Table ME01-F06-1 "Reset Your Halo Password" web screen: functionality description

| ID | Title | Validation | Description |
|---|---|---|---|
| ME01-F06-1-1 | "Reset Your Halo Password" title | - | - |
| ME01-F06-1-2 | "Password must include 1 uppercase letter, number or special symbol, and be at least 8 characters long." text | - | - |
| ME01-F06-1-3 | "New password" field with "eye" icon | Mandatory. Should have up to 20 symbols. The system forbids us to enter the 21st character. | The field is empty by default. |
| ME01-F06-1-4 | "Confirm password" field with "eye" icon | Mandatory. Should have up to 20 symbols. The system forbids us to enter the 21st character. | The field is empty by default. |
| ME01-F06-1-5 | "Submit" button | See ME01-F06-AC05,06,07,08. | - |
