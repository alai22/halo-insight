---
title: "ME01-US24. Create a Zendesk ticket with logs when the user is unable to launch the app / log in"
sidebar_label: "ME01-US24. Create a Zendesk ticket with logs when the user is unable to launch the app / log in"
sidebar_position: 190
last_modified: "Oct 07, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya, Pavel Leonenko |
| HALO-10114 - MOB: Automatically create Zendesk ticket when the user is unable to log in Closed |
| 12 Jan 2021 ME01-US24-AC05 is added |## User Story

As Halo App Account owner I want to be able to send the email with the mobile logs when I cannot enter the system so that I can report the "entering the system" issue with and then Halo Team can understand the issue reason and try to resolve it.

## Acceptance criteria

| AC | Description | iOS UI Design / impl-n status | Android UI Design / impl-n status |
|---|---|---|---|
| ME01-US24-AC01 | "Report Issue" button should be included into M113 Network error message. Note: this error can happen within "Enter the system" flow, e.g.: "App Startup Failed" screen is opened (see ME01-F00-AC02), "Splash" screen is opened (see ME01-F00-AC01, ME01-F00-AC05, ME01-F00-AC06) | - | - |
| ME01-US24-AC02 | Precondition: M113 Network error message is displayed"Report Issue" button should be displayed next to "Dismiss" button. ("Dismiss" button name will be changed in ME01-US24-AC05) | - | - |
| ME01-US24-AC03 | Precondition: M113 Network error message is displayedIf I tap on "Report Issue" button, then:the default email sender should be opened with the draft "Issue with Log In" email: see ME01-US24-AC04. | - | - |
| ME01-US24-AC04 | The "Issue with Log In" email should consist of: Subject: "[HALO-APP] Login issue"Email recipient: support@halocollar.zendesk.comEmail body: Attachment: file with the mobile logsNote 1 : the sender's email can differ from the email that is used in Halo accountNote 2: email body should be empty | - | - |
| ME01-US24-AC05 | M113 Network error text should be updated to: Title: Error During Login Body: To help us resolve this issue please email us the error details by pressing the button below. Button: Report IssueButton: Not Now |  |  |
| Softeq doesn't control the following AC, but it's assumed to be performed: In case support@halocollar.zendesk.com is chosen as the email recipient, then after the email sending Zendesk request should be created and CSAs should be able to view it in https://halocollar.zendesk.com/agent/dashboard. |
