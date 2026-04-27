---
title: "[BL] ME02-US12. View \"Help\" screen (incl. Zendesk int-n and mobile logs)"
sidebar_label: "[BL] ME02-US12. View \"Help\" screen (incl. Zendesk int-n and mobile logs)"
sidebar_position: 53
author: "Galina Lonskaya"
---

| Role | Epic | Document status | BA story owner | DEV story owner | QA story owner | Link to JIRA Issue |
|---|---|---|---|---|---|---|
| Owner |
| ME02 Settings |
| APPROVED |
| Galina Lonskaya |
| Pavel Leonenko |
| Anastasia Brechko |
| Part 1: HALO-2990 - MOB: Zendesk integration investigation Closed Part 2: HALO-3238 - MOB: ME02-US12. Support: help center, tickets man-t, logs sending Closed |# User story

\> As a user, I want to view Help Center articles and report ticket so that I can get a tip of advice on HALO app usage

| AC | Description | App Logs Logic (All AC below are already implemented, except ME02-US12-AC15) |
|---|---|---|
| ME02-US12-AC01(added on 2/19/2020) | "Support" icon should be updated on the "Question" icon. See the screen below: |
| ME02-US12-AC02 | The following screen should be removed: |
| ME02-US12-AC03 | If I tap on the Support icon at Settings, then:ZenDesk web-view should be opened. |
| ME02-US12-AC04 | All info provided in web-view depends on a third-party system "Zendesk".The following functionality should be available:Help CenterTickets managementNote: All behavior depends on Zendesk |
| ME02-US12-AC05 | Each message should contain a file with logs. |
| ME02-US12-AC06 | File with logs could be removed by the user if necessary. |
| ME02-US12-AC08 | Each file shouldn't be more than 1 Mb. |
| ME02-US12-AC09 | The app can save no more than 12 files at a time. |
| ME02-US12-AC10 | If the available number of files is achieved, then the oldest file should be removed and a new one should be created. |
| ME02-US12-AC11 | The file's name is \<Do-Not-Delete.ZIP\>. |
| ME02-US12-AC12 | The file with logs is archived in ZIP. |
| ME02-US12-AC13 | ZIP can be unpacked with password "2 3 EGG PARK fruit 7 golf sky". |
| ME02-US12-AC14 | Each logfile event consists of:TimestampClass nameMessage |
| ME02-US12-AC15 | The following info should be added to the logs:user's ID who is logged in;timestamp when the user is logged in;user's ID who is logged out;timestamp when the user is logged out.Note: Logs shouldn't be cleared after logging out. |
