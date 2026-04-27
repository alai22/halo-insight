---
title: "[BL] ME02-US34. Add 'last name' to the 'edit' user account screen"
sidebar_label: "[BL] ME02-US34. Add 'last name' to the 'edit' user account screen"
sidebar_position: 202
last_modified: "Mar 21, 2022"
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] |
| HALO-10799 - BE+MOB: Add "last name" to the user account + update some related texts Closed |# User story

\> As a business owner, I want app users to add their real (or just not abusive) names in the user profile so that CSA can use it while addressing to the app user in emails or during live Dog park sessions.

| AC | Description | iOS UI design / impl-n status | Android UI design / impl-n status | AS-IS | To-Be |
|---|---|---|---|---|---|
| ME01-US34-AC01 | The list of the UI elements on "Edit Account" screen should be changed:AS-ISTo-BeThe screen consists of:Сross icon for Android (Cancel button for iOS)"Edit Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update Photo" button\<User email\>"Name" label + \<User Name\>"Delete Account" buttonThe screen consists of:Сross icon for Android (Cancel button for iOS)"Edit Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update Photo" button\<User email\>"First Name" label + \<User First name\>"Last Name" label + \<User Last name\>"Delete Account" buttonThe 'Name' field should be renamed to 'First Name'.The 'Last Name' field should be added. | The screen consists of:Сross icon for Android (Cancel button for iOS)"Edit Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update Photo" button\<User email\>"Name" label + \<User Name\>"Delete Account" button | The screen consists of:Сross icon for Android (Cancel button for iOS)"Edit Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update Photo" button\<User email\>"First Name" label + \<User First name\>"Last Name" label + \<User Last name\>"Delete Account" button | Link to Zeplin | Link to Zeplin |
| The screen consists of:Сross icon for Android (Cancel button for iOS)"Edit Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update Photo" button\<User email\>"Name" label + \<User Name\>"Delete Account" button | The screen consists of:Сross icon for Android (Cancel button for iOS)"Edit Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update Photo" button\<User email\>"First Name" label + \<User First name\>"Last Name" label + \<User Last name\>"Delete Account" button |
| ME01-US34-AC02 | The 'Last Name' field should not be required. | - | - |
| ME01-US34-AC03 | The length of the 'Last Name' field should not exceed 20 characters. | - | - |
