---
title: "[BL] ME03-US25. View Collars List (UI redesign)"
sidebar_label: "[BL] ME03-US25. View Collars List (UI redesign)"
sidebar_position: 57
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Document owner | Link to JIRA Issue | Revision History |
|---|---|---|---|---|---|
| Owner |
| ME03 Manage collars |
| REVISED |
| Galina Lonskaya |
| HALO-3104 - MOB+BE: ME03-US25. View Collars List (UI redesign) Closed |
| 25 Feb 2020 ME03-US22-AC12 is updated07 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As an owner, I want to view the collars list with the improved UI/UX design so that I can get better UX out of the interaction with the collars list app functionality.

| AC | Description | The collars list - empty state | The collars list - filled state. | Collar photo | Collar FW update | Collar Battery | General requirements for Collars list both in empty and filled states | Battery charging |
|---|---|---|---|---|---|---|---|---|
| ME03-US22-AC01 | Precondition: I don't have collars yet.If I tap on the Collars icon at the Settings screen, then:the Collars list screen in an empty state should be opened. See the pic below.The screen consists of:Back iconCollars titleCollars icon"No collars added yet." text"Add Collar" button |  | The screen consists of:Back iconCollars titleCollars icon"No collars added yet." text"Add Collar" button |
|  | The screen consists of:Back iconCollars titleCollars icon"No collars added yet." text"Add Collar" button |
| ME03-US22-AC02 | If I tap on the "Add Collar" button screen, then:the Add Collar screen should be opened. See description in ME03-US01. Add a collar. |
| ME03-US22-AC03 | Precondition: I have one collar at least.If I tap on the Settings icon, then:all collars are linked to this account should be displayed. See the pic Collars list below.The screen consists of:Back iconCollars title"Add New Collar" buttonEach collar tile with the linked pet consists of:HALO collar photo + HALO ringBattery icon + \<Battery charge persents\>, see ME03-US22-AC14"\<Pet Name\>'s Collar" text\<Collar Type\>\<Collar SN\> See BR-12 Product NameEach collar tile without the linked pet consists of: HALO collar photo + Default HALO ring (grey)Battery icon + \<Battery persents\>, see ME03-US22-AC14"Available Collar" text\<Collar Type\>\<Collar SN\> See BR-12 Product NameNote: Collar type should be updated on the following format "HALO v1" |  | The screen consists of:Back iconCollars title"Add New Collar" buttonEach collar tile with the linked pet consists of:HALO collar photo + HALO ringBattery icon + \<Battery charge persents\>, see ME03-US22-AC14"\<Pet Name\>'s Collar" text\<Collar Type\>\<Collar SN\> See BR-12 Product NameEach collar tile without the linked pet consists of: HALO collar photo + Default HALO ring (grey)Battery icon + \<Battery persents\>, see ME03-US22-AC14"Available Collar" text\<Collar Type\>\<Collar SN\> See BR-12 Product Name |
|  | The screen consists of:Back iconCollars title"Add New Collar" buttonEach collar tile with the linked pet consists of:HALO collar photo + HALO ringBattery icon + \<Battery charge persents\>, see ME03-US22-AC14"\<Pet Name\>'s Collar" text\<Collar Type\>\<Collar SN\> See BR-12 Product NameEach collar tile without the linked pet consists of: HALO collar photo + Default HALO ring (grey)Battery icon + \<Battery persents\>, see ME03-US22-AC14"Available Collar" text\<Collar Type\>\<Collar SN\> See BR-12 Product Name |
| ME03-US22-AC04 | If I open the Collars list, then:all collar tiles should be displayed as minimized by default. |
| ME03-US22-AC05 | If I tap on the minimized collar tile, then see the continuation in ME03-US26. View Collar details (UI redesign). |
| ME03-US22-AC06 | The collars list should be sorted as the last provisioned collar at the top. |
| ME03-US22-AC07 | The collars list can be scrollable if all collar tiles don't fit into the frame. |
| ME03-US22-AC08 | Pet name can be cut, if it doesn't fit into the tile. |
| ME03-US22-AC09 | Collar photos should be pulled from BE.Note: Ask Heather to provide relevant photos |
| ME03-US22-AC10 | While the collar photo is loading the placeholder should be displayed. |
| ME03-US22-AC11 | If the collar has not applied collar FW update, then exclamation mark should be displayed near the collar icon |
| ME03-US22-AC12 | Battery icon can have the following statuses: Note: Charging should be delivered within the other story as it requires BE. |
|  | "Unknown" battery charge state is displayed when no telemetry was ever received from the collar or the collar is not assigned to the pet. |
| ME03-US22-AC13 | If I tap on the Back button, the previous screen should be opened. |
| ME03-US22-AC14 | I can pull-to-refresh the Collars list in both states: empty and with the collars tiles. |
| ME03-US22-AC15 | "Charging" status should be displayed at the Collars list, if the "charging" status is got. |
