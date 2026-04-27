---
title: "(NA) ME05-FE01-US06. 'Test on Collar' button: error handling"
sidebar_label: "(NA) ME05-FE01-US06. 'Test on Collar' button: error handling"
sidebar_position: 571
last_modified: "May 05, 2025"
author: "Galina Lonskaya"
---

.

| Document owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-885/ios-test-on-collar-button-error-handling |
| 01 May 2025 draft is created by Galina Lonskaya |# Contents

User Story Acceptance criteria

# User Story

\> As Halo App Account Owner, I want to receive different toasts for each specific case when I can't send a command to my Halo collar so that I can understand what is exactly the problem.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| AC01 | The acceptance criteria below should be applied for the following scenarios:When the user taps the' Test on collar' button from:'Recall' settings screen'Level 1' settings screen'Level 2' settings screen'Level 3' settings screen'Custom 1' settings screen'Custom 2' settings screen | - |Table 1 - 'Test on Collar' error toasts

| AC | PRECONDITIONS | AS IS | TO BE | BLE related | Internet related | Battery | Bluetooth permission is granted | Bluetooth is turned on | Collar is available via BLE | Bluetooth connection/unlocking process is in progress | The Internet is enabled | The Internet is connected, but HALO BE doesn't reply | Collar is available via Internet | The expected time ofbattery dischargehas come |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AC02 | - | doesn't matter | - | n/a | - | - |  | Figma |
| AC03 | - | doesn't matter |  | - | - | - |  | Figma |
| AC04 |  | - | n/a |  | - | - | - |
| AC05 |  |  | - | - | - | n/a | n/a | - |  | Figma |
| AC07 |  |  | - | - |  | - | - |  |  | Figma |
| AC08 |  |  | - | - |  | - | - | - | "Your collar is out of Wi-Fi, cellular and Bluetooth range or powered OFF". | Figma |
| AC09 |  |  | - | - |  |  | n/a | - | 'Collar is out of Bluetooth range and the Halo app cannot reach our server' | Figma |
| AC10 | - | doesn't matter | n/a | n/a |  |  | n/a | - | 'Your phone's Bluetooth is disabled and the Halo app cannot reach our server' | Figma |
| AC11 |  |  | n/a |  | doesn't matter | doesn't matter | - | - | 'Your phone is not connected to the internet and Bluetooth connection is still in progress.' | Figma |
