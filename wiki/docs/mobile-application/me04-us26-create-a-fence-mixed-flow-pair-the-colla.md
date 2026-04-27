---
title: "ME04-US26. Create a fence (mixed flow): pair the collar via BLE"
sidebar_label: "ME04-US26. Create a fence (mixed flow): pair the collar via BLE"
sidebar_position: 13
author: "Galina Lonskaya"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| REVISED |
| Galina Lonskaya |
| HALO-2015 - [ME04-US26]: Create a fence (mixed flow): pair the collar via BLE Closed |# User story IMPLEMENTED

\> As owner, I want to pair a collar via BLE so that I can use specific collar for the post location determination

# Acceptance criteria

| AC | Text |
|---|---|
| AC01 | If the pairing is performed successfully, then the confirmation screen should be displayed. |
| AC02 | If Bluetooth isn't enabled on the smartphone during the pairing, then the M102 No Bluetooth (fence creation) error should be displayed. |
| AC03 | If the pairing with the selected collar isn't successful, then the M70. No answer from the collar error should be displayed. |
| AC04 | The pairing should be last no more than 10 sec. Time is configurable. |
