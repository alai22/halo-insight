---
title: "ME01-F04. Login"
sidebar_label: "ME01-F04. Login"
sidebar_position: 597
last_modified: "Feb 25, 2025"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issue |
|---|---|---|---|
| Baseline story (checked by the dev team) |
| APPROVED |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko |
| HALO-2883 - MOB: ME01-US13. Log in (new UI design) Closed |# Contents

User story ME01-F04-1 "Log In" screen: functionality description ME01-F04-2 Log in error handling

# User story

\> As an account owner, I want to log into my account so that I can proceed work with my Halo account.

| AC | Description | iOS UI design / impl-n status | Android UI design / impl-n status |
|---|---|---|---|
| Entry points to "Log In" screen:"Sign Up" screen"Forgot Password?" screen"Tell Us About Yourself" screen"Check Your Email" screen"Start" screenM73 Log out message |
| ME01-F04-AC01 | If the "Log In" screen view is initiated, then:"Log Into Your Account" screen should be opened. See Pic 1 and the table ME01-F04-1 "Log In" screen: functionality description. | Pic 1 "Log Into Your Account" (empty)IOS DONE | Pic 1 "Log Into Your Account" (empty)ANDROID TO DO |
| ME01-F04-AC02 | When I am typing a password, the app should mask it (show dot symbols instead of typed symbols). | IOS DONE | ANDROID TO DO |
| ME01-F04-AC03 | The app should allow me to hide and show the typed password by pressing an eye icon. | IOS DONE | ANDROID TO DO |
| ME01-F04-AC04 | Cross icon is displayed in the Email field while editing.If I tap on the Cross icon the field should be cleared. | IOS DONE | ANDROID TO DO |
| ME01-F04-AC05 | Red underlining should be removed from the field if I focus on the field.Red underlining should be restored if the focus on the field is restored. | Pic 2 "Log Into Your Account" (error)IOS DONE | Pic 2 "Log Into Your Account" (error)ANDROID TO DO |
| ME01-F04-AC06 | The errors that can appear while signing the app are presented in the ME01-FI01-2 Log In error handling table (see below). | IOS DONE | ANDROID TO DO |
| ME01-F04-AC10 | If the user taps on the "Log In" button, the app should disable the screen and show the loading spinner until it receives the response from BE. | IOS TO DO | ANDROID TO DO |
| ME01-F04-AC07 | If I tap on the "Log In" button and the entered email and password are found in DB and have "Active" status, then:I should be logged into the app;the app should show the following screens:- Screen "Tell us about yourself" should be displayed, if I don't provide name, see continuation: ME01-F03. Add profile info after Sign Up- "My Map" screen should be provided if I have already provided his/her name. | IOS DONE | ANDROID TO DO |
| ME01-F04-AC07 | If I tap on the "Log In" button and the entered email and password are found in DB and have "Pending" status, then:"Check your email" screen should be opened. See the screen description: ME01-FI01. Create an account | IOS DONE | ANDROID TO DO |
| ME01-F04-AC08 | If I tap on the "Forgot Password?" button, then:"Forgot Password?" screen should be opened. See continuation in ME01-FI05. Forgot password. | IOS DONE | ANDROID TO DO |
| ME01-F04-AC09 | If I tap on the "Sign Up" button, then:"Sign Up" screen should be opened. See continuation in ME01-FI01. Create an account. | IOS DONE | ANDROID TO DO |### ME01-F04-1 "Log In" screen: functionality description

| № | Component | Validation | Description |
|---|---|---|---|
| ME01-F04-1-1 | Halo logo + Halo title | - | - |
| ME01-F04-1-2 | Title “Log In” | - | - |
| ME01-F04-1-3 | Text field “Email” | Email must be in users' DB.The email max length is 50. The app doesn't allow enter 51. | Required field.The field should contain the "Email" field. |
| ME01-F04-1-4 | Text field “Password” | The email max length is 20. The app doesn't allow enter 21.Should not be empty. | Required field.The field should contain the "Password" field. |
| ME01-F04-1-5 | Eye icon in the "Password" field | - | The icon allows the user to show/hide the typed password.Uncrossed eye state means that the user could see password symbols. When a user is typing a password, the system should mask it (show dot symbols instead of typed symbols). A crossed eye state means that the user could NOT see password symbols.Switching between states does not reset already input characters. |
| ME01-F04-1-6 | Button "Log In" | - | See ME01-F04-AC06,7,8 |
| ME01-F04-1-7 | Button "Forgot Password" | - | See ME01-F04-AC08 |
| ME01-F04-1-8 | Text "Don't have an account?" | - | - |
| ME01-F04-1-9 | Link "Sign Up" | - | See ME01-F04-AC09 |### ME01-F04-2 Log in error handling

| Error ID | Reason | Error type | Content | The first check (is performed when the focus is moved from field to field) | The second check (is performed when the user taps on the Log In button) |
|---|---|---|---|---|---|
| ME01-F04-2-1 | Blank email | Blank email | Screen error: Please enter your email |
| ME01-F04-2-2 | Blank password | Blank password | Screen error: Please enter your password |
| ME01-F04-2-3 | The email and password are not found in DB | Unknown email and password | Screen error: The email and/or password you entered is incorrect. |
| ME01-F04-2-4 | The email and password are found, but the email isn't confirmed | The email | See in ME01-F04-AC07. |
| ME01-F04-2-5 | The email and password are found, but the user is deactivated | Deactivated user | Screen error: The email and/or password you entered is incorrect.Note: In the future, the "Deactivated user" screen should be opened in this case. (this will be handled in a separate US -ME10-US01. "Deactivated user" screen) |
| ME01-F04-2-6 | No internet connection or the server is unavailable due to any reason | Network error | Standard iOS message: M113 Network error |
