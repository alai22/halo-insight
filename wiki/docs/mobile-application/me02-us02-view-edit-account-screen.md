---
title: "ME02-US02. View \"Edit Account\" screen"
sidebar_label: "ME02-US02. View \"Edit Account\" screen"
sidebar_position: 33
author: "Kseniya Petkevich [X]"
---

| Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|
| Owner |
| ME02 Settings |
| APPROVED |
| Galina Lonskaya |
| HALO-2557 - [ME02. Settings] ME02-US02. View Edit My Account screen (simplified) Closed |# User story

\> As an owner, I want to delete my app account so that I cannot use this account anymore and my data are erased.

# Acceptance criteria

| # | Acceptance Criteria | Delete account | Update photo | Update name |
|---|---|---|---|---|
| ME02-US02-AC01 | Precondition: Settings screen is displayed.If I tap on the Edit My Account button, then the Edit My Account screen should be displayed.Pic 1 - Edit My AccountThe screen consists of:Cancel icon"Edit My Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update photo" button\<User email\>"Name" label + \<User Name\>"Delete account" buttonTab bar | Pic 1 - Edit My Account | The screen consists of:Cancel icon"Edit My Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update photo" button\<User email\>"Name" label + \<User Name\>"Delete account" buttonTab bar |
| Pic 1 - Edit My Account | The screen consists of:Cancel icon"Edit My Account" title"Done" button (if updates exist)\<User profile picture\> or "User profile placeholder""Update photo" button\<User email\>"Name" label + \<User Name\>"Delete account" buttonTab bar |
| ME02-US02-AC03 | For return on the previous page, I can tap on the "Cancel" button. |
| ME02-US02-AC04 | If I tap on the "Delete Account" link, then the M117 App account deletion confirmation warning message should be displayed. |
| ME02-US02-AC05 | Precondition: M117 App account deletion confirmation is displayedIf I tap on the Cancel button, then the warning message should be closed and Edit My Account screen should be still displayed. |
| ME02-US02-AC06 | Precondition: M117 App account deletion confirmation is displayedIf I tap on the Confirm button, then: all my personal data should be deleted from the systemthe spinner should be displayed during the account deletionNote: It should be a "hard" delete without the opportunity to restore deleted data. This requirement depends on the CCPA rules. Deleted data shouldn't be available in any case. |
| ME02-US02-AC07 | Precondition: My account deletion is initiated, the spinner is displayed.If my account is successfully deleted, then:My account should get Deleted status;The login screen should be opened;The email field should be cleared. |
| ME02-US02-AC08 | Precondition: My account deletion is initiated, the spinner is displayed.If my account deletion is failed for any reason, then:the M118 App account deletion error should be displayed.After the "OK" button tapping, My account screen should be displayed. |
| ME02-US02-AC09 | If I tap on the Change photo button, then the action sheet should be displayed.Pic 2 Profile photo editing- Action sheetSee the same requirements as for Pet Profile Photo Management: ME16-US03. Manage pet avatar. |
| ME02-US02-AC10 | If I change the photo only (and not update the user name), then the Done button shouldn't be displayed. |
| ME02-US02-AC11 | If I tap on the User name, then the following screen should be displayed:Pic 3 - Edit My Account - Name editing |
