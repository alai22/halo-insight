---
title: "ME02-F04. View \"Help\" screen (incl. integration with Zendesk and mobile logs)"
sidebar_label: "ME02-F04. View \"Help\" screen (incl. integration with Zendesk and mobile logs)"
sidebar_position: 98
last_modified: "Jul 24, 2024"
author: "Galina Lonskaya"
---

| Document type | Document status | Test cases status | Document owners | Link to JIRA Issue | Change history |
|---|---|---|---|---|---|
| Baseline story |
| Revised |
| NEED UPDATE as of 04/13/2021 (ME02-F04-AC12 is updated with NEW FROM 51 SPRINT info, ME02-F04-AC13 is added). |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko, Maria Shikareva [X] |
| HALO-4821 - Android: ME02-F04. View "Help" screen (incl. integration with Zendesk) Closed HALO-5923 - QA: Add subscription plan level (current + temporary) info to the App Logs Closed |
| Maria Shikareva [X] 13 Apr 2021 Baselined the story: ME02-US13. Add subscription plan level (current + temporary) info to the App LogsMaria Shikareva [X]25 Apr 2022 Baselined [BL] ME02-US25. Update the Settings screen tiled view to list view. |# User story

\> As an account owner, I want to view Help Center articles and manage Zendesk tickets so that I can get a tip of advice from Halo Support about Halo Collar system usage.

### Acceptance criteria

| AC | Description | iOS UI design / impl-n notesIOS DONE | Android UI design / impl-n notesANDROID DONE | App Logs Logic |
|---|---|---|---|---|
| ME02-F04-AC01 | If I tap on the 'Guide and Video Tutorials' button at the Settings screen, then:The screen from Zendesk library with the Help Center articles should be opened. | Pic 1 Help screen (iOS, as of 1/28/21) | Pic 2 Help screen (Android, as of 1/28/21)Note: My tickets icon should be the same as on iOS → Update the screen after impl-n |
| ME02-F04-AC02 | The following functionality should be available within Zendesk web-view:Help Center articles;Tickets management.Note 1: All info provided in web-view depends on a third-party system "Zendesk".Note 2: It's acceptable that Android and iOS screen UI can be different. Note 3: Android bottom navigation bar should be added later in a separate task, since it can require 8+ SP. | Pic 3 My Tickets - Empty (iOS, as of 1/28/21)Pic 4 My Tickets - with tickets (Android, as of 1/28/21) | Pic 3 My Tickets - Empty (iOS, as of 1/28/21) | Pic 4 My Tickets - with tickets (Android, as of 1/28/21) | Pic 5 My Tickets - empty (iOS, as of 1/28/21)Pic 6 My Tickets - with tickets (Android, as of 1/28/21) | Pic 5 My Tickets - empty (iOS, as of 1/28/21) | Pic 6 My Tickets - with tickets (Android, as of 1/28/21) |
| Pic 3 My Tickets - Empty (iOS, as of 1/28/21) | Pic 4 My Tickets - with tickets (Android, as of 1/28/21) |
| Pic 5 My Tickets - empty (iOS, as of 1/28/21) | Pic 6 My Tickets - with tickets (Android, as of 1/28/21) |
| ME02-F04-AC03 | Each message should contain a file with logs. | - | - |
| ME02-F04-AC04 | File with logs could be removed by the user if necessary. | - | - |
| ME02-F04-AC05 | Each file inside the archive shouldn't be more than 1 Mb.Note: There is 1 archive with one or several text files in it. Users can remove the whole archive before sending a message, not a particular file. | - | - |
| ME02-F04-AC06 | The app can save no more than 12 files at a time. | - | - |
| ME02-F04-AC07 | If the available number of files is achieved, then the oldest file should be removed and a new one should be created. | - | - |
| ME02-F04-AC08 | The file's name is \<Do-Not-Delete.ZIP\>. | - | - |
| ME02-F04-AC09 | The files with logs are archived in ZIP. | - | - |
| ME02-F04-AC10 | ZIP can be unpacked with password "2 3 EGG PARK fruit 7 golf sky". | - | - |
| ME02-F04-AC11 | Each logfile event consists of:TimestampClass nameMessage | - | - |
| ME02-F04-AC12 | The following info should be added to the logs:user's ID who is logged in;timestamp when the user is logged in;user's ID who is logged out;timestamp when the user is logged out;device information (device model / OS version);the user's current subscription plan; NEW FROM 51 SPRINTthe user's subscription plan with temporary access.NEW FROM 51 SPRINT.Note1: Logs shouldn't be cleared after logging out.Note 2: information about user's subscription plan is added for the CSA/ SA convenience to check easily what subscription level is currently applied on the mobile app. It may be useful, for example, in case the user has some troubles with their plan, contacts support and CSA has no other opportunity to define the user's current plan (e.g. the user has 'Basic' plan → the user changes it to 'Gold' but doesn't refresh the mobile application → the CSA within AAP sees 'Gold' plan for the user → but the user sees only features relevant for 'Basic' plan). | - | - |
| ME02-F04-AC13 | Information about the user's subscription plans should be logged each time a request is made to the backend. |  |  |
