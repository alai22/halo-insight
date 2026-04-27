---
title: "[Won't have] ME05-US42 [AFFMP]: Toast messages"
sidebar_label: "[Won't have] ME05-US42 [AFFMP]: Toast messages"
sidebar_position: 134
last_modified: "Mar 23, 2021"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| ME05-EP02. Apply feedback for multiple pets |
| DRAFT |
| Nicolay Gavrilov |
| HALO-6578 - MOB [RI]: ME05-US42. Toast messages Closed |Contents

User story Acceptance criteria

# User story

\> As a user I want to see the toast messages with the list of pets that did not get the feedback so that it will be easier to tell which pets got the feedback and which did not when I apply feedback for multiple pets.

# Acceptance criteria

| AC | Text | iOS design/notes | Android design/notes |
|---|---|---|---|
|  | If the feedback was not applied for at least one pet because the collar of the pet is not available neither via Bluetooth nor via the Internet, the app should show a toast message with the list of pets that did not receive the command. The text of the toast should be as follows:"\<pet_name1\>'s, \<pet_name2\>'s .... and \<pet_nameN\>'s collars are out of Wi-Fi, cellular and Bluetooth range”Note: we can list all pets in the toast. Big toast message shouldn't be a problem because there should be not so many users with 10 dogs with long names. | - | - |
|  | If the feedback was applied for none of the pets, the app displays the "All collars are out of Wi-Fi, cellular and Bluetooth range” toast message. | - | - |
