---
title: "ME04-US35. Create a fence (mixed flow): be aware of the collar unintentional disconnection"
sidebar_label: "ME04-US35. Create a fence (mixed flow): be aware of the collar unintentional disconnection"
sidebar_position: 22
last_modified: "Nov 05, 2020"
author: "Galina Lonskaya"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| APPROVED |
| Galina Lonskaya |
| HALO-2031 - [ME04. Create Fence with a collar] : ME04-US35. Be aware of the collar unintentional disconnection Closed |# User story

\> As owner, I want to view collar connection status so that I can be aware of it.

# Acceptance criteria

| AC | Text |
|---|---|
| AC01 | Precondition: The collar is paired, Create New Fence/Fence edition flow is in-progressIf Bluetooth becomes disabled on the smartphone after some action initiation, then the M102 No Bluetooth (fence creation) error should be displayed. |
| AC02 | Precondition: The collar is paired, Create New Fence flow/Fence edition flow is in-progress, Bluetooth is enabled. If a connection with paired collar is lost unintentionally (not via a user's tap on the Disconnect), the app tries to reconnect during 3 sec.Note: Reconnection time is configurable. |
| AC03 | If the app tries to reconnect to the collar, the "Weak GPS collar pin" icon should be displayed. |
| AC04 | Precondition: The collar is paired, Create New Fence /Edit fence flow is in-progress, Bluetooth is enabled. If a connection with paired collar is lost unintentionally (not via a user's tap on the Disconnect) and the connection isn't restored during 3 sec, then:The M109 No paired collar error should be displayed;Collar pin should be hidden from the map;Corresponded tollbar should be displayed, see details in:ME04-US29. Create a fence (mixed flow): toolbar behavior updates. |
| AC05 | If I tap on the Add button or Move button and the collar doesn't respond (while the app is trying to reconnect), then:the following toast should be displayed "Please try again once your phone reconnects with collar";the dot isn't added. |
