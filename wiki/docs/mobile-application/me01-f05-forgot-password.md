---
title: "ME01-F05. Forgot password"
sidebar_label: "ME01-F05. Forgot password"
sidebar_position: 598
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issue |
|---|---|---|---|
| Baseline story (checked by dev team) |
| APPROVED |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko |
| HALO-2866 - MOB+BE: ME01-US14. Forgot password (new UI design) CLOSED |# User story

\> As an account owner, I want to send request to recover my passowrd so that I can log into my Halo account again.

| AC | Description | iOS UI design / impl-n status | Android UI design / impl-n status | "Check Your Email" screen |  |
|---|---|---|---|---|---|
| The entry point to the "Forgot Password?":"Log In" screen, see ME01-FI04. Log in. |
| ME01-F05-AC01 | If the "Forgot Password?" screen view is initiated, then:the "Forgot Password?" screen should be displayed. See below the table ME01-F05-2 "Forgot Password?" screen: functionality description. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC02 | Precondition: "Forgot Password?" screen is displayed."Email" field should contain an "Email" tip. Text of a tip must disappear when a user's typed any available symbol in the field. |
| ME01-F05-AC03 | If I enter the email at the "Log In" screen and tap on the "Forgot Password?" button, then:the entered email should be displayed at the Forgot Password screen. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC04 | Precondition: "Forgot Password?" screen is displayed.Cross icon is displayed in the Email field if there is at least one symbol entered in the field.If I tap on the Cross icon the field entry should be cleared. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC05 | Precondition: "Forgot Password?" screen is displayed.The errors that can appear while the recovery link request is presented in the table ME01-F05-1 "Forgot Password" error handling. See the table below. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC06 | Precondition: "Forgot Password?" screen is displayed.If I tap on the "Send Recovery Link" and the account with the entered email is confirmed (both active and inactive) or isn't registered in the DB, then:"Check Your Email" screen should be displayed. See continuation in ME01-F05-AC09. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC07 | Precondition: "Forgot password?" screen is displayed.I can get back to login via the tap on the "Return to Login" link. See continuation in ME01-FI04. Log in. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC08 | Precondition: "Check Your Email" screen is displayed.If I tap on the Resend Recovery Link button, then:EM002 Reset Your Halo Password (initiated by app user) with a new link should be sent on the same email address;the spinner should be displayed, if necessary;the same screen should be still displayed. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC09 | Precondition: "Check Your Email" screen is displayed.The errors that can appear after a tap on the Resend Recovery Link are presented in the table ME01-F05-3 "Resend Recovery Link" error handling. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC10 | Precondition: "Check Your Email" screen is displayed.I can get back to login via the tap on the "Return to Login" link. See continuation in ME01-FI04. Log in. | IOS DONE | ANDROID TO DO |
| ME01-F05-AC11 | In order to open the recovery link, I need to open EM002 Reset Your Halo Password (initiated by app user) email. See the continuation in ME01-F06. Set a new password (web). | IOS DONE | ANDROID TO DO |Table ME01-F05-1 "Forgot password" error handling (mobile app)

| ID | Trigger | Error type | Content | The first-level check (is performed when the field focus is removed) | The second-level check (is performed when the field focus is removed) | The third-level check (is performed when the user taps on the "Send Recovery Link" button) |
|---|---|---|---|---|---|---|
| ME01-F05-1-1 | Blank email | Empty field | Screen error: Please enter your email |
| ME01-F05-1-2 | The entered email doesn't contain “@” and “.” | Wrong email ("@" and/or "." are not entered) | Screen error: Please enter a valid email address |
| ME01-F05-1-3 | Email is not confirmed | Email isn't confirmed. | Screen error: Please confirm your email |
| ME01-F05-1-4 | No internet connection or the server is unavailable due to any reason | Network error | Standard iOS message: M113 Network error |ME01-F05-2 "Forgot Password?" screen: functionality description

| № | Component | Validation | Description |
|---|---|---|---|
| ME01-F05-2-1 | Halo logo + Halo title | - | - |
| ME01-F05-2-2 | The title “Forgot Password?” | - | - |
| ME01-F05-2-3 | The title "We'll send you the recovery link to" | - | - |
| ME01-F05-2-4 | The text field “Email” | The field must contain “@” and “.”Email must not belong to another user.Should have up to 50 symbols. App forbids to enter the 51st character. | Required field.The field "Email" should contain an "Email" placeholder. |
| ME01-F05-2-5 | Button "Send Recovery Link" | - | See the button functionality description in ME01-F05-AC06. |
| ME01-F05-2-6 | Link "Return to Login" | - | See the button functionality description in ME01-F05-AC07. |ME01-F05-3 "Resend Recovery Link" error handling

| ID | Trigger | Error type | Content | The check is performed when the user taps on the "Resend Recovery Link" button |
|---|---|---|---|---|
| ME01-F05-3-1 | No internet connection or the server is unavailable due to any reason | Network error | Standard iOS message: M113 Network error |
