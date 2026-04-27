---
title: "[BL] ME02-US25. Update the Settings screen tiled view to list view"
sidebar_label: "[BL] ME02-US25. Update the Settings screen tiled view to list view"
sidebar_position: 169
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Kirill Akulich [X], Valeria Malets |
| HALO-9130 - [GOAL] MOB: ME02-US25. Update the Settings screen tiled view to list view Closed |
| As of 12 Oct 2021 Mariya Kolyada created the initial version of the US.As of 14 Oct 2021 Mariya Kolyadaupdated the US after client's review.As of 19 Oct 2021 Mariya Kolyadaupdated ME02-US25-AC01 and ME02-US25-AC06.As of 02 Nov 2021 Mariya Kolyadaadded a mention about 'Log Out (Admin)' button and added designs and links of updated screens.As of 03 Nov 2021 Mariya Kolyada updated requirements regarding Log Out of Super Admin.As of 24 Dec 2021 Maria Shikareva [X] marked the story as "baselined". |# User Story

\> As Halo Collar app account owner I want to view explanation of Settings screen UI elements so that I can clearly understand what every element means.

# Acceptance criteria

| AC | Description | iOS UI design | Android UI design | See the initial requirements for the Settings Screen here: ME02-F00. View "Settings" screen | As is | To be | As is | To be | As is | To be |
|---|---|---|---|---|---|---|---|---|---|---|
| ME02-US25-AC01 | The Settings screen should consist of the following UI elements instead of tiles:'My Devises' group of options:'My Collars' option:Icon;'My Collars' title;Right arrow icon.'My Beacons' option:Icon;'My Beacons' title;Right arrow icon.'Support' group of options:'Smart Help' option:Icon;'Smart Help' title;'The easiest and quickest way to get answers to your Halo product questions.' subtitle;Right arrow icon.'Live Support' option:Icon;'Live Support' title;'Access live customer support via video conference during open hours: Mon - Fri: 9 am - 6 pm (EST).' subtitle;Right arrow icon. 'My Tickets' option:Icon;'My Tickets' title;'Create and view Halo Support tickets status.' subtitle;Right arrow icon.'Guide and Video Tutorials' option:Icon;'Guide and Video Tutorials' title;Right arrow icon.'General' group of options:'My Account' option:Icon;'My Account' title;'Blue dot alert icon' (See details in [Outdated] ME02-US12. Blue dot indicator for the Referral program)Right arrow icon.'About' option:Icon;'About' title;Right arrow icon.'Log Out' button | Pic 1 Settings screen: list view | Same as iOsAndroid |
| ME02-US25-AC02 | If I click on the 'My Collars', then the app should:Display the 'Collars list' screen (see ME03-EP04 Collars List and ME02-US25-AC03 below) | - | - |
| ME02-US25-AC03 | Update the 'Collars list' screen title:As isTo beCollarsMy Collars | Collars | My Collars | Pic 2 'Collars list' screen | Same as iOs |
| Collars | My Collars |
| ME02-US25-AC04 | If I click on the 'My Beacons', then the app should:Display the 'Beacons list' screen (see ME09-EP02. Beacon list and ME02-US25-AC05 below) | - | - |
| ME02-US25-AC05 | Update the 'Beacons list' screen title:As isTo beBeacons My Beacons | Beacons | My Beacons | Pic 3 'Beacons list' screen | Same as iOs |
| Beacons | My Beacons |
| ME02-US25-AC06 | If I click on the 'Smart Help', then the app should:Display the Solvvy WebView (see [BL] ME02-US16. Solvvy integration)NoteIf the current US is implemented before [BL] ME02-US16. Solvvy integration, then the app should hide this option | - | - |
| ME02-US25-AC07 | If I click on the 'Live Support', then the app should:Start joining of Customer Support Zoom Meetings (see ME02-US24. Dog park MVP)NoteIf the current US is implemented before ME02-US24. Dog park MVP, then the app should hide this option | - | - |
| ME02-US25-AC08 | If I click on the 'My Tickets', then the app should:Display the 'My Tickets' screen (see ME02-F05. View "Feedback" screen) | - | - |
| ME02-US25-AC09 | If I click on the 'Guide and Video Tutorials', then the app should:Help Center Webview (see ME02-F04. View "Help" screen (incl. integration with Zendesk and mobile logs)) | - | - |
| ME02-US25-AC10 | If I click on the 'My Account', then the app should:Display the 'Account' screen (see ME02-F01. View "Account" screen and ME02-US25-AC11, ME02-US25-AC12 below) | - | - |
| ME02-US25-AC11 | Update the 'Account' screen title:As isTo beAccountMy Account | Account | My Account | Pic 5 'Account' screen | Same as iOs |
| Account | My Account |
| ME02-US25-AC12 | Remove the 'Log Out' button on the 'Account' screen. | - | - |
| ME02-US25-AC13 | If I click on the 'About', then the app should:Display the 'About' screen (see ME02-F04. View "About" screen) | - | - |
| ME02-US25-AC14 | If I click on the 'Log Out' button, then the app should:See details in ME01-F07. Log out and ME02-F00. View "Settings" screen. | - | - |
