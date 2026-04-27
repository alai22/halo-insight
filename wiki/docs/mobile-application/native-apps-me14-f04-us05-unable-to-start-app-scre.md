---
title: "(Native apps) ME14-F04-US05. 'Unable to start app' screen error handling"
sidebar_label: "(Native apps) ME14-F04-US05. 'Unable to start app' screen error handling"
sidebar_position: 486
last_modified: "Feb 26, 2025"
author: "Galina Lonskaya"
---

| Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-392/[ios]-unable-to-start-app-screen-error-handling |
| 21 Feb 2025 the draft story is created by Galina Lonskaya |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to get clear errors so that I can understand that the something goes wrong

# Acceptance criteria

| AC | Description |  |
|---|---|---|
| ME14-F04-US05-AC01 | Precondition: 'Unable to start app' screen is shown, see FigmaIf after tapping on the "Retry" button a connection error occurs, then:the app should display M125 popup Figma (see the old reference in Confluence M125 Connection error) |  |
| ME14-F04-US05-AC02 | If the user taps "Retry" on the M125 pop-up and ConfigurationInitializationError happens, then:first 4 times: the app should display M125 popup Figma should be shown5+ time: the app should show M113 popup Figma (see the old reference in Confluence M113 Network error). |  |
| ME14-F04-US05-AC03 | If the user taps on CTA (Report Issue) on M113, then: the system should behave according to requirements described in (Native apps) ME14-F07. Send email to Halo from the mob app (universal flow)the following data should be applied by default:Recipient: support@halocollar.comSubject: [HALO-APP] Login issueBody: empty;Attachments: App logs, as of 2/24/2025 'app logs' functionality is not implemented in Project R, will be done within a separate user story: Logging and log file handling in mobile app |  |
| ME14-F04-US05-AC04 | Precondition: 'Unable to start app' screen is shown, see FigmaIf after tapping on the "Retry" button and communication error occurs, then: M126 popup Figma (see the old reference in Confluence M126 Communication error) popup should be shownAfter the pop-up is closed the user should remain logged in and should stay on the 'Unable to start app' screen, see Figma |  |Tech notes:

Implementation details:

See implementation in NoInternetConnectionViewModel.cs.

ConfigurationInitializationError is thrown in case we couldn't fetch Configuration due to Connection error (thrown after the first attempt) or due to any other error except IncompatibleClient error (thrown after the second attempt). See the logic in StartScreenManager.TryNavigateToProperScreenAsync().

The logic of logging in and opening the proper screen should be implemented in a shared class, and reused here and in two more places. Please see StartScreenManager.TryNavigateToProperScreenAsync().


