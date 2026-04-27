---
title: "ME01-US21. Sign on via Facebook"
sidebar_label: "ME01-US21. Sign on via Facebook"
sidebar_position: 601
last_modified: "Jun 10, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| APPROVED (SQ) |
| Maria Shikareva [X] |
| HALO-7470 - [RI] FE+BE: Social sign on (Facebook) Closed |
| 30 Jun 2021 Maria Shikareva [X] Added an implementation note.15 Jul 2021 Maria Shikareva [X]ME01-US21-AC01 is updated (FB native behavior is described).ME01-US21-AC04, ME01-US21-AC11, Designs are updated: "Back" icon is not required anymore as the screens are opened in the mobile browser and have default "Cancel" button on IOS/ "Cross" icon on Android.10 Jun 2022 Maria Shikareva [X]Marked the story as implemented.Added message texts to Appendix 3 – Error, Success, Warning Messages. |# User story

\> As a user I want to have an ability to log in/ sign-on my Halo account using Facebook so that to have a simplified way to authorize.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME01-US21-AC01 | When the user taps "Continue with Facebook" on Log In/ Sign Up screens, then the user is redirected to the external page (https://www.facebook.com/).Note 1: The system should use the standard logic for signing in using Facebook (for more details see https://developers.facebook.com/docs/facebook-login/).Note 2: if the user has previously logged in via Facebook and there are saved cookies, then the user will be logged in without entering their credentials (this is the native Facebook behavior as Facebook saves cookies for quite a long time). But if the user logs out FB account in the browser/ FB mobile app, then the Halo app will initiate an authorization procedure from scratch. | - | - |
| ME01-US21-AC02 | If the authorization is successful (i.e. the token is received), then the following parameters should be returned to BE:user's name associated;user's email (if provided by the user while creating a Facebook account). | - | - |
| ME01-US21-AC03 | If the email is provided, then the flow should be the same as described in ME01-US17-AC08 - ME01-US17-AC28 (ME01-US17. Social sign-in / sign on). | - | - |
| ME01-US21-AC04 | If the email is not provided, then the app should display the 'Add your email' screen (see screen designs) with the following UI elements:'Back' icon;Facebook icon;'Oops! It looks like you haven't provided your email address while creating your Facebook account. Halo will save your email address so we can send you collar firmware updates, provide you with our support and more. Please enter your email address or choose a different sign up option.' text;"Email" field;'Email' placeholder should be displayed till at least one character/ digit is entered."Continue" button.Note: this screen should appear only once when the user provides an email for the first time only (see IN). | Pic ME01-US21-P03 'FB: provide an email' screenLink to Zeplin | A WebView should be used (the same as for iOS). |
| ME01-US21-AC05 | A 'Cross' icon is displayed in the Email field if there is at least one symbol entered in the field.If the user taps on the 'Cross' icon, then the field should be cleared. | - | - |
| ME01-US21-AC06 | The app shouldn't allow to enter more than 50 characters. | - | - |
| ME01-US21-AC07 | If the 'Email' field is blank, than the following error should be displayed: M246 Enter email. | - | - |
| ME01-US21-AC08 | If the email is not valid (see ME01-F01-1-4 in ME01-F01. Sign Up (Create an account)), then the following error should be displayed: M247 Enter valid email. | - | - |
| ME01-US21-AC09 | The email field should be underlined with a red upon failing the validation (see ME01-US21-AC10, ME01-US21-AC11). | - | - |
| ME01-US21-AC10 | Red underlining should be removed from the email field if the user enters a correct email and validation was successfully passed. | - | - |
| ME01-US21-AC11 | If the user taps Cross' icon on Android/ "Cancel" button on iOS in the native mobile browser, then The "Log Into Your Account" screen should be opened (see ME01-US21-AC01). | - | - |
| ME01-US21-AC12 | Preconditions: the valid email is providedANDthe ACTIVE user's account exists in the database with password-based authentication method (i.e. the user has created an account previously using email and password)When the user taps on 'Continue' button, then the system should perform the flow as described in ME01-US17-AC08 (ME01-US17. Social sign-in / sign on). | - | - |
| ME01-US21-AC13 | Preconditions:the valid email is providedANDthe PENDING user's account exists in the database with password-based authentication methodWhen the user taps on 'Continue' button, then the system should perform the flow as described in ME01-US17-AC10 (ME01-US17. Social sign-in / sign on). | - | - |
| ME01-US21-AC14 | Preconditions:the valid email is providedANDthe DEACTIVATED user's account exists in the database.When the user taps on 'Continue' button, then the system should perform the flow as described in ME01-US17-AC20 (ME01-US17. Social sign-in / sign on). | - | - |
| ME01-US21-AC15 | Preconditions: the valid email is providedANDthe user's account doesn't exist in the database.When the user taps on 'Continue' button, then the system should perform the flow as described in ME01-US17-AC21 (ME01-US17. Social sign-in / sign on). | - | - |
| ME01-US21-AC16 | Error handling should be the same as describe in ME01-US17. Social sign-in / sign on. | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME01-US21-IN01 | When the user tries to log in/ sign up with Facebook, it returns a provider key which can be used as a user ID. So the user Halo account can be associated with FB account via this provider key. |
