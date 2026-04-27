---
title: "ME04-US27. Create a fence (mixed flow): confirm the correct collar pairing"
sidebar_label: "ME04-US27. Create a fence (mixed flow): confirm the correct collar pairing"
sidebar_position: 14
author: "Galina Lonskaya"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| REVISED |
| Galina Lonskaya |
| HALO-2016 - [ME04-US27]: Create a fence (mixed flow): confirm the correct collar pairing Closed |# User story

\> As owner, I want to view the confirmation screen so that I can make sure that the correct collar is paired

# Acceptance criteria

| AC | Text |
|---|---|
| ME04-US27-AC01 | If the selected collar is successfully paired via BLE (see previous step description in ME04-US25. Create a fence (mixed flow): collars list, ME04-US26. Create a fence (mixed flow): pair the collar via BLE), then "Select Collar for GPS - Confirmation screen" should be opened. Pic 1 Select Collar for GPS - Confirmation screenThe screen consists of:Back icon"Add Collar for GPS" title"Done" button"Please remove \<Product name\> from any pet. Hold it in your hand and check that light is blinking to ensure you the correct collar"Image | Pic 1 Select Collar for GPS - Confirmation screen | The screen consists of:Back icon"Add Collar for GPS" title"Done" button"Please remove \<Product name\> from any pet. Hold it in your hand and check that light is blinking to ensure you the correct collar"Image |
| Pic 1 Select Collar for GPS - Confirmation screen | The screen consists of:Back icon"Add Collar for GPS" title"Done" button"Please remove \<Product name\> from any pet. Hold it in your hand and check that light is blinking to ensure you the correct collar"Image |
| ME04-US27-AC02 | Right after screen opening, "Find the collar" request should be sent at the collar. Requests should be sent automatically every 10 sec during "Select Collar for GPS - Confirmation screen" displaying. See the request description in ME04-US28. Create a fence (mixed flow): find the connected collar. |
| ME04-US27-AC03 | If I tap on the Back button, then the collars list should be opened.See ME04-US25. Create a fence (mixed flow): collars list |
| ME04-US27-AC04 | If I tap on the Done button, then "Create Fence" screen with the toolbar should be displayed. See the continuation in ME04-US29. Create a fence (mixed flow): toolbar behavior updates. |
