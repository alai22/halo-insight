---
title: "(Native Apps) ME01-F04-US02. Log-in Error Handling"
sidebar_label: "(Native Apps) ME01-F04-US02. Log-in Error Handling"
sidebar_position: 490
last_modified: "Apr 17, 2025"
author: "Galina Lonskaya"
---

| Document owners | Link to JIRA/Linear Issue | History of changes |
|---|---|---|
| Galina Lonskaya, Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-412/[ios]-log-in-error-handling |
| 26 Feb 2025 draft story is created by Galina Lonskaya |# Contents

User story Acceptance criteria Login Error: Pending User Account Login Error: Unknown Email or Password Login Error: Deactivated User Account Login Error: Incorrect Device Time Login Error: Connection Issue Login Error: Communication Issue or any other issue not mentioned above

# User story

\> As Halo App account owner, I want to receive clear and actionable error messages when I enter incorrect login credentials, so that I can easily understand what went wrong and take the necessary steps to log in successfully.

# Acceptance criteria

| AC | Description | Login Error: Pending User Account | Login Error: Unknown Email or Password | Login Error: Deactivated User Account | Login Error: Incorrect Device Time | Login Error: Connection Issue | Login Error: Communication Issue or any other issue not mentioned above |
|---|---|---|---|---|---|---|---|
| ME01-F04-US01-AC01 | If the user taps on the "Log In" button, the app should disable the screen and show the loading spinner until it receives the response from BE. |
| ME01-F04-US01-AC03 | If I tap the "Log In" button and the entered email and password are found in DB and have "Pending" status, then:"Enter the Code from the Email" screen should be opened (web UI). |
| ME01-F04-US01-AC04 | If I tap the "Log In" button and the email and/or password you entered is incorrect, thenthe сorrespodning screen error should be shown on web UI. Screen error: The email and/or password you entered is incorrect. |
| ME01-F04-US01-AC05 | If I tap the "Log In" button but the account is deactivated, thenthe сorrespodning screen error should be shown on web UI. Note: In the future, the "Deactivated user" screen should be opened in this case. (this will be handled in a separate US:ME10-US01. "Deactivated user" screen |
| ME01-F04-US01-AC06 | Precondition:user tries to Log inANDtime on the user's mobile phone is incorrect (i.e. it differs from the system time for more than 5 minutes).The mobile app should display the following error message: M224 popup see Figma (see the old reference in Figma M224. Check Your Device Time). |
| ME01-F04-US01-AC07 | If the user taps on Report Issue CTA on M224, then:the system should behave according to requirements described in (Native apps) ME14-F07. Send email to Halo from the mob app (universal flow)the following data should be applied by default:Recipient: support@halocollar.com; Subject: [HALO-APP] Login issueBody: empty;Attachments: App logs, as of 2/24/2025 'app logs' functionality is not implemented in Project R, will be done within a separate user story: Logging and log file handling in mobile app |
| ME01-F04-US01-AC08 | If I tap the "Log In" button and connection issue happens, thenM125 popup Figma with 'Retry' button ( see old reference in Confluence: M125 Connection error) should be shown. |
| ME01-F04-US01-AC09 | If I tap the "Log In" button and communication issue happens or any other issue not mentioned above, thenthe app should show M113 popup Figma (see the old reference in Confluence M113 Network error). |
| ME01-F04-US01-AC10 | If the user taps on CTA (Report Issue) on M113, then: the system should behave according to requirements described in (Native apps) ME14-F07. Send email to Halo from the mob app (universal flow)the following data should be applied by default:Recipient: support@halocollar.comSubject: [HALO-APP] Login issueBody: empty;Attachments: App logs, as of 2/24/2025 'app logs' functionality is not implemented in Project R, will be done within a separate user story: Logging and log file handling in mobile app |Implementation details:

The logic of logging in and opening the proper screen should be implemented in a shared class, and reused here and in two more places. Please see StartScreenManager.TryNavigateToProperScreenAsync().


