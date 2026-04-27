---
title: "ME01-F01. Sign Up (Create an account)"
sidebar_label: "ME01-F01. Sign Up (Create an account)"
sidebar_position: 92
author: "Galina Lonskaya"
---

| Document status | Test cases status | Document owners | JIRA links | Changes history |
|---|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 02 Sep 2022 |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| Click here to expand... HALO-2857 - MOB: ME01-US10. Create an account (new UI design) Closed |
|  |# Contents

User story Acceptance criteria "Sign Up" screen 'Email' section 'Password' section 'Sign Up' flow "Check Your Email" screen

# User story

\> As an account owner, I want to create account so that I can log into the Halo account and start using of the Halo app.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | "Sign Up" screen | "Check Your Email" screen |  |
|---|---|---|---|---|---|---|
| Entry points to Sign Up screen:Halo start screen, see ME01-FI00. Run the app (splash, start, "app startup failed" screen).Log In screen, see ME01-FI04. Log in. |
| ME01-F01-AC01 | When the Sign Up screen view is initiated, then the app should display a "Sign Up screen" with the following UI elements:Halo logo + Halo title;“Sign up for Your Account” title;"Already have an account?" text;"Log In" link.On tapping the app should redirect the user to the "Log in" screen. See continuation in ME01-FI04. Log in.an input field "Email";Password section:an input field "Password";"Password must include 1 uppercase letter, number or special symbol and be at least 8 characters long" text;'Sign Up' button;other Sign Up options:'Continue with Apple';'Continue with Google';'Continue with Facebook'."By signing up, you accept the Terms of Service and Privacy Policy." text. | Link to Zeplin | Link to Zeplin |
| ME01-F01-AC02 | Input fields should contain tips on what information the user should enter. | - | - |
| ME01-F01-AC03 | Text of a tip in the input field must disappear when a user starts typing any available symbol in the field. | - | - |
| ME01-F01-AC04 | 'Terms of Service' should be a link to https://app.termly.io/document/terms-of-use-for-ecommerce/02d81772-7c46-4ce0-9149-aca6a49fba8e. | - | - |
| ME01-F01-AC05 | 'Privacy Policy' should be a link to https://app.termly.io/document/privacy-policy/2fc6550d-2a1c-4858-8a2f-bd3cd3b2021a. | - | - |
| 'Email' section |
| ME01-F01-AC06 | Precondition: a user starts populating the field.If the user changes the focus to another field and leaves the 'email' field blank, then the app should display a M246 Enter email error. |  | - |
| ME01-F01-AC07 | Precondition: a user starts populating the field.If the user changes the focus to another field, the app should validate whether the field contains the "@" and "." symbols and displays an M247 Enter valid email error if not. | Link to Zeplin | - |
| ME01-F01-AC08 | Precondition: a user starts populating the field.If the user changes the focus to another field and the entered email belongs to the already registered user, the app should display a M257 Email is used error. | - | - |
| ME01-F01-AC09 | Precondition: a user starts populating the field.The app should display a 'cross' icon in the field. | - | - |
| ME01-F01-AC10 | Precondition: a 'cross' icon is displayed.When the user taps on the 'Cross' icon, the app should clear the field. | - |  |
| ME01-F01-AC11 | The app should not allow to enter more than 50 symbols. | - | - |
| 'Password' section |
| ME01-F01-AC12 | Precondition: a user starts populating the field.If the user changes the focus to another field and leaves the 'password' field blank, then the app should display a M255 Enter password error. |  | - |
| ME01-F01-AC13 | Precondition: a user starts populating the field.If the user changes the focus to another field, the app should perform validations as described in BR-5 and display a M256 Enter stronger password error if the validation fails. |  | - |
| ME01-F01-AC14 | The app should not allow to enter more than 20 symbols. | - | - |
| ME01-F01-AC15 | The 'password' field should contain an eye icon to allow the user to show/hide the typed password:'uncrossed eye' state means that the user could see password symbols;a crossed eye state means that the user could NOT see password symbols. | - | - |
| ME01-F01-AC16 | Precondition: the app displays an 'Uncrossed eye'. When a user is typing a password, the system should mask it (show dot symbols instead of typed symbols). | - | - |
| ME01-F01-AC17 | Switching between states should not reset already populated characters. | - | - |
| 'Sign Up' flow |
| ME01-F01-AC18 | Precondition: the user taps on an 'Sign Up' button.If the validation described in TBD passes successfully, then the system should :send the email EM001 Confirm Your Halo Account with a confirmation link to the provided address;open a "Check Your Email" screen should be opened. | - | - |
| ME01-F01-AC19 | Precondition: the user taps on an 'Sign Up' button.If there's no internet connection or the server is unavailable due to any reason, then the app should display a M113 Network error. | - | - |
| ME01-F01-AC20 | When the user taps on the 'Resend Confirmation' button and the email isn't confirmed, then:email EM001 Confirm Your Halo Account with a NEW confirmation link should be sent to the provided email address. | IOS DONELink to Zeplin | ANDROID TO DOLink to Zeplin |
| ME01-F01-AC21 | If I tap on the Resend Confirmation button and the email is confirmed, then I should be logged in the app automatically. | IOS DONE | ANDROID TO DO |
| ME01-F01-AC22 | If I tap on the Return to Login button, then the "Log In" screen should be opened. See continuation in ME01-FI04. Log in. | IOS DONE | ANDROID TO DO |
| ME01-F01-AC23 | In order to confirm my email, I need to open EM001 Confirm Your Halo Account email. See the continuation in ME01-F02. Confirm email (web). | IOS DONE | ANDROID TO DO |
