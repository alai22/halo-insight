---
title: "[BL] ME01-US27. Add 'last name' to the user account and update some related texts"
sidebar_label: "[BL] ME01-US27. Add 'last name' to the user account and update some related texts"
sidebar_position: 201
last_modified: "Mar 21, 2022"
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Valeryia Chyrkun [X] |
| HALO-10799 - BE+MOB: Add "last name" to the user account + update some related texts Closed Ballpark: BE -0.5SP, MOB - 3SP, QA - 2SP |# User story

\> As a business owner, I want app users to add their real (or just not abusive) names in the user profile so that CSA can use it while addressing to the app user in emails or during live Dog park sessions.

| AC | Description | iOS UI design / impl-n status | Android UI design / impl-n status | AS-IS | To-Be |
|---|---|---|---|---|---|
| ME01-US27-AC01 | The list of UI elements on "Tell Us About Yourself!" screen should be changed:AS-ISTo-BeScreen elements:Title "Tell Us About Yourself!"Avatar placeholder + button "Update Photo"Text field “Name”Button "Done""Do you have another account? Back to" text + "Login" buttonScreen elements:Button "Done"Avatar placeholder + button "Update Photo"Title "Tell Us Your Name'Subtitle 'We will use your name for email and other communications"Text field “First Name”Text field “Last Name”The title should be changed to 'Tell Us Your Name'Subtitle 'We will use your name for email and other communications' should be addedThe 'Name' field should be renamed to 'First Name'.The 'Last Name' field should be added."Do you have another account? Back to" text + "Login" text should be removed. | Screen elements:Title "Tell Us About Yourself!"Avatar placeholder + button "Update Photo"Text field “Name”Button "Done""Do you have another account? Back to" text + "Login" button | Screen elements:Button "Done"Avatar placeholder + button "Update Photo"Title "Tell Us Your Name'Subtitle 'We will use your name for email and other communications"Text field “First Name”Text field “Last Name” | Link to Zeplin | Link to Zeplin |
| Screen elements:Title "Tell Us About Yourself!"Avatar placeholder + button "Update Photo"Text field “Name”Button "Done""Do you have another account? Back to" text + "Login" button | Screen elements:Button "Done"Avatar placeholder + button "Update Photo"Title "Tell Us Your Name'Subtitle 'We will use your name for email and other communications"Text field “First Name”Text field “Last Name” |
| ME01-US27-AC02 | Precondition: "Tell Us About Yourself!" screen is opened.If I tap on the Done button, but the First Name field is empty, then:the "Please enter your name" error should be displayed and the field should be underlined. | - | - |
| ME01-US27-AC03 | The 'Last Name' field should not be required. | - | - |
| ME01-US27-AC04 | The length of the 'Last Name' field should not exceed 20 characters. |  |  |
