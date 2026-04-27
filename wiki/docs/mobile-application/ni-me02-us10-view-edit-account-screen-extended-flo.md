---
title: "[NI] ME02-US10. View \"Edit Account\" screen (extended flow)"
sidebar_label: "[NI] ME02-US10. View \"Edit Account\" screen (extended flow)"
sidebar_position: 31
author: "Kseniya Petkevich [X]"
---

| Role | Epic | Document status | Document owners | Link with Jira |
|---|---|---|---|---|
| Owner |
| ME02 Settings |
| TEAM REVIEW |
|  |
| TBD |# User story

\> As a user, I would like to manage my Account so that to have current information into the system.

Preconditions:

1. The user selected "My Account" tab on the user profile.

# Acceptance criteria

| # | Acceptance Criteria | Screen |
|---|---|---|
| AC01 | The user selected "My Account" tab on the user profile. |  |
| AC02 | The user views Account info:AvatarNameAccount StatusEmail (clickable tab)PhoneChange Password (clickable tab)Delete Account (clickable link) |  |
| AC03 | The user has possibility to change next information using the My Account screen:PhotoNamePhone |  |
| AC04 | The user edits Photo |  |
| AC05 | When the user taps on the Avatar image, the form for the photo upload opens. |
| AC06 | For saving changes, the user should press "Save" button. For returning on the previous screen he should tape "Cancel" button |
| AC07 | The user views his current NameWhen the user taps on the field, the qwerty appears and the user can view his name. |
| AC08 | For cleaning the field the user should tape on the "Cross" icon. |
| AC09 | The user saves Name changesFor saving changes, the user should press "Save" button. For returning on the previous screen he should tape "Cancel" button. |
| AC10 | The user views his current Phone.When the user taps on the field "Phone", he can edit his mobile phone that uses for account managing. |
| AC11 | The user saves the Phone changesFor saving changes, the user should press "Save" button. For returning on the previous screen he should tape "Cancel" button. |
| AC12 | The user views his current email. When the user taps on the "Email" tab, the screen with editable field opens. The user enters his email. |  |
| AC13 | The user checks his current email. When the user taps "Save" button, the screen for email checking opens. |  |
| AC14 | The user confirms his emailWhen the user taps "Save" button, the screen for email checking opens. |
| AC15 | After confirming email the email changes. Before confirming email the system should save and use the current email that the user wants to change. |
| AC16 | The user cancels his email editing. For returning to the previous screen, the user should tape on the "Back" icon. |
| AC17 | For stopping email editing the user should tape on the "Cross" icon. |
| AC18 | The user views the password.For password changing the user should select the "Change Password" tab. The screen for password changing opens. |  |
| AC19 | The user edits his passwordIn the opened page the user can see two fields:Current Password (should be entered by the system) - password that the user uses to enter into the systemNew Password. The user types a new password according to the validation rules. |
| AC20 | The user can manage password visibilityPassword visibility. If the user wants to see entered current or new password, he should tape on the "Eye" icon. |
| AC21 | The user saves his passwordFor new password saving the user should tap on the "Save" button. |
| AC22 | The user cancels the password editing. For cancelling the changes the user should tap on the "Back" icon. |
| AC23 | The user initiates Account deleting. See ME02-US02. View "Edit Account" screen |  |Fields

| # | Field Name | Field Type | Symbols Type | Validation Rules | Requirements and Behavior |
|---|---|---|---|---|---|
| See FI-01, FI-02 description here |
| FI-03 | Account status | String | Text | Only one status exists now: Account Owner | The system shows user account status. |
| FI-04 | Email | String | Text, numbers, symbols | No more than 30 symbols\<emailname\>@\<domenname\>.com | The system shows the user email.When the user taps on the email field, the page for email confirmation opens. |
| FI-05 | Phone | String | Numbers, symbols | No more than 16 symbols\<country phone code\>\<local phone code\>\<phone number\> | The system shows the phone number that is used by user for the system usage.When the user taps on the field, the form for the number editing opens. |
| FI-06 | Current Password | String | Any | No more than 20 symbols.Minimum 8 symbols | The system shows the current password. It is hidden by default. |
| FI-07 | New Password | String | Any | No more than 20 symbols.Minimum 8 symbols | The system shows the new password. It is hidden by default. |
