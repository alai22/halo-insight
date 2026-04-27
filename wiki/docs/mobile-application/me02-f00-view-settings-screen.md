---
title: "ME02-F00. View \"Settings\" screen"
sidebar_label: "ME02-F00. View \"Settings\" screen"
sidebar_position: 64
last_modified: "Aug 14, 2024"
author: "Galina Lonskaya"
---

| Document status | Test cases status | Document owners | Link to JIRA Issues | Changes history |
|---|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 24 Dec 2021 |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko, Mariya Kolyada, Maria Shikareva [X] |
| Click here to expand... HALO-3391 - MOB: ME02-US13. View Settings screen (improved UI/UX) Closed HALO-4477 - Android: ME02-F00. View "Settings" screen Closed HALO-7435 - MOB [NT]: [Investigation] Solvvy integration Closed HALO-7786 - BE: [Investigation] Solvvy integration Closed HALO-9321 - MOB+BE: ME02-US16. Solvvy integration Closed HALO-9457 - MOB: "Smart Help" should open Zendesk web-view with the Help Center articles Closed HALO-9782 - MOB: "Settings" screen updates Closed HALO-10741 - [RI] BE+MOB: Add "Collar Diagnostic" section to the "Collars list" Closed HALO-11032 - MOB: Update Solvvy before Dog Park release (it should lead to the correct screen in the app) Closed |
| Click here to expand...25 Apr 2022 Maria Shikareva [X] Baselined [BL] ME02-US16. Solvvy integration, [BL] ME02-US27. Zoom opening from Solvvy, [BL] ME02-US35. Update Solvvy before Dog Park release (it should lead to the correct screen in the app)).30 May 2022 Maria Shikareva [X] Baselined [BL] ME03-US71. Add "Collar Diagnostic" section to the "Collars list".30 Aug 2022 Maria Shikareva [X] Baselined EC03-US04. Refer friends from the "Account" screen.03 May 2024 Kiryl Trafimau Baselined (NI) ME03-US101 BE+MOB: Catastrophic issues: calculation and displaying of the issue in app |# Contents

User story Role = Halo App user Solvvy 'Blue dot' on the 'Settings' tab and on "My Collars" option Role = Super Admin (Note: it's relevant for one-time Super Admin access, see ME01-F08. SA/CSA logs into the app user account) Implementation notes

# User story

\> As an Halo app user, I would like to view settings list with explanation of UI elements so that I can clearly understand what every element means, can quickly navigate and choose what it need to be configured.

Acceptance criteria

| AC | Description | iOS UI design | Android UI design | Role = Halo App user | Role = Super Admin (Note: it's relevant for one-time Super Admin access, see ME01-F08. SA/CSA logs into the app user account) |
|---|---|---|---|---|---|
| ME02-F00-AC01 | If I tap on the "Settings" button at the tab bar, then:The previously displayed screen at the Settings tab should be displayed;The settings button should be selected. | - | - |
| ME02-F00-AC02 | The "Settings" screen should consist of the following UI elements:'My Devises' group of options:'My Collars' option:Icon;'My Collars' title;Right arrow icon.'My Beacons' option:Icon;'My Beacons' title;Right arrow icon.'Support' group of options:'Halo Help' option:Icon;'Halo Help' title;'The easiest and quickest way to get answers to your Halo Collar questions is our interactive Halo Help - available 24/7.' subtitle;Right arrow icon.'Halo Dog Park' option:Icon;'Live Support' title;'Join a live video session with a member of the Halo Support Team.' subtitle;Right arrow icon. 'My Tickets' option:Icon;'My Tickets' title;'Create and view Support tickets.' subtitle;Right arrow icon.'Guide and Video Tutorials' option:Icon;'Guide and Video Tutorials' title;Right arrow icon.'General' group of options:'Refer a Friend' option:Icon;'Refer a Friend' title;Right arrow icon.'Submit Video Testimonial' option: Icon;'Submit Video Testimonial' title;Right arrow icon.'My Account' option:Icon;'My Account' title;Right arrow icon.'Push Notifications' option: Icon;'Push Notifications' title;Right arrow icon.'About' option:Icon;'About' title;Right arrow icon.'Log Out' button | Figma | Figma |
| ME02-F00-AC03 | If I tap on the 'My Collars', then the app should:display the 'My Collars' screen (see ME03-F01. Collars list). | - | - |
| ME02-F00-AC04 | If I tap on the 'My Beacons', then the app should:display the 'My Beacons' screen (see ME09-F01 Beacon list). | - | - |
| ME02-F00-AC22 | If Catastrophic issue detected in DDRed dot should be displayed on the 'My collars'Red dot should be displayed on the 'Settings' tab in the tab bar |  | - |
| Solvvy |
| ME02-F00-AC05 | When the user taps on the "Halo Help" button on the "Settings" screen, then a Solvvy WebView should be opened with the "Back" icon (see screen designs).The URL from the e-Commerce team is used.All info provided in the web-view depends on a third-party system "Solvvy".It's acceptable that Android and iOS screen UI can be different. |  | The same as for iOS. |
| ME02-F00-AC06 | The link should be the following: https://cdn.solvvy.com/deflect/customization/halocollar/support.html | - | - |
| ME02-F00-AC07 | Precondition: Solvvy WebView is opened.When the user taps on the "Back" icon, then:the previous "Settings' screen should be opened;all stored data should be cleared (i.e. the history should not be saved; is the user taps "Halo Help" again, then they will not see their previous questions).See the investigation results in HALO-8568 - [GOAL] MOB [NT]: [Investigation] Solvvy: Clearing the stored data on iOS the same as on Android Closed . | - | - |
| ME02-F00-AC08 | Precondition: a user opened 'Solvvy' in the mobile app.When the user taps any "Dog Park" option in Solvvy, the mobile app should display the "Dog Park areas list" screen as described in ME20-US01. View dog Park areas list and replace Live support with Dog Park on Settings screen. | - | - |
| ME02-F00-AC09 | Precondition: the 'Dog Park areas list" is opened from Solvvy.If the user taps "Back" icon, then the app should open Solvvy WebView again.Need to check it during implementation. If it's impossible to return the user to Solvvy due to some technical restrictions, it's OK to open the 'Settings' screen. | - | - |
|  |
| ME02-F00-AC10 | If I tap on the 'Halo Dog Park Support', then the app should:start joining of Customer Support Zoom Meetings (see ME02-US24. Dog park MVP). | - | - |
| ME02-F00-AC11 | If I tap on the 'My Tickets', then the app should:display the 'My Tickets' screen (see ME02-F04. View "Help" screen (incl. integration with Zendesk and mobile logs)) | - | - |
| ME02-F00-AC12 | If I tap on the 'Guide and Video Tutorials', then the app should:initiate Help Center Webview (see ME02-F04. View "Help" screen (incl. integration with Zendesk and mobile logs)) | - | - |
| ME02-F00-AC13 | "Refer A Friend" menu option should be visible only if there's a generated code for this user (based on info from BE) regardless of whether the user has a collar in the account or not.Note 1: see ME02-F00-IN01 below.Note 2: the code should not be expired. If for some reason the code is expired and a new one is not generated yet, then this option should not be visible. | - | - |
| ME02-F00-AC14 | If I tap on the 'Refer a Friend' option, then the app should:display 'Refer a Friend' screen (see ME02-F08. View "Refer a Friend" screen). | - | - |
| ME02-F00-AC15 | If I tap on the 'My Account', then the app should:display the 'Account' screen (see ME02-F01. View "Account" screen). | - | - |
| ME02-F00-AC16 | If I tap on the 'About', then the app should:Display the 'About' screen (see ME02-F04. View "About" screen) | - | - |
| ME02-F00-AC17 | If I tap on the 'Log Out' button, then the app should:perform actions as described in ME01-F07. Log out. | - | - |
| 'Blue dot' on the 'Settings' tab and on "My Collars" option |
| ME02-F00-AC18 | When an 'Issues detected' label is displayed on the 'Collars list', then a 'Blue dot' indicator should be displayed:on the 'Settings' tab;next to "My Collars" section. | Link to Zeplin (should be updated) | The same as for iOS. |
| ME02-F00-AC19 | Precondition: 'Blue dot' indicator is displayed on the 'Settings' tab/ next to "My Collars' option.A 'Blue dot' indicator should disappear from both places when: a new DailyDiagnostics is sent ANDno issues are detected.QA Note: the blue dot should stay in place for another notifications (if applicable). | - | - |
| ME02-F00-AC20 | Super Admin should see the same Settings screen with all functionality as a Halo app user. Additionally a "Log Out (Admin)" button should be displayed. | Link to Zeplin | The same as for iOS. |
| ME02-F00-AC21 | When Super Admin taps on the Account icon, then the system should display the following error message: M116 Super Admin doesn't have access to the app user's personal data.Note: the app user's personal info shouldn't be available for the Super Admin. | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME02-F00-IN01 | The mobile app will retrieve the code from BE:on opening the app in the user_profileANDon restoring the app to the foregroundANDafter the user adds a collar to the account. |
