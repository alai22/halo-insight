---
title: "ME04-F13 Add fence with GPS: Disconnect collar"
sidebar_label: "ME04-F13 Add fence with GPS: Disconnect collar"
sidebar_position: 112
last_modified: "Nov 25, 2020"
author: "Nicolay Gavrilov"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baselined story |
| APPROVED (SQ) |
| Nicolay Gavrilov, Pavel Leonenko, Anastasia Brechko |
| HALO-5357 - Android GOAL: Add/Edit fence with GPS Closed |# Contents

User story Acceptance criteria

# User story

\> As an owner, I want to disconnect my collar when adding a fence with GPS so that I could choose another collar for fence creation.

# Acceptance criteria

| AC | Text | iOS design / implementation status | Android design / implementation status |
|---|---|---|---|
| ME04-F13-AC01 | If I tap on the "Select a collar" icon on "Create new fence" screen when adding a fence with GPS and there is a paired collar, then the "Disconnect collar" card should be displayed. | IOS DONE | The design is similar to iOsANDROID TO DO |
| ME04-F13-AC02 | The "Disconnect collar" card consists of:"Currently Using \<Pet's name or Collar type\> collar" captionHALO collar icon with HALO color ring"disconnect" button"swap collar" button | IOS DONE | ANDROID TO DO |
| ME04-F13-AC04 | If the collar is not assigned to a pet the color ring around the collar icon should be grey. Otherwise, it should have the same color that was assigned to the pet in settings. | IOS DONE | ANDROID TO DO |
| ME04-F13-AC05 | If I tap on the collar pin on the map, then the "Disconnect collar" card should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-F13-AC06 | If I tap on the "disconnect" button on the "Disconnect collar" card, then the collar should be disconnected. | IOS DONE | ANDROID TO DO |
| ME04-F13-AC07 | If I tap on the "disconnect" button on the "Disconnect collar" card, and the collar is successfully disconnected, then:the collar pin should disappear from the map and the user's location pin should be displayed again;the "\<Device name\> has been successfully disconnected" toast message should be displayed;the "Disconnect a collar" card should be closed;the Toolbar should have only the Undo, Redo, Delete buttons (see ME04-F11. Add fence with GPS: Toolbar behavior (Add (GPS), Move buttons)). | IOS DONE | ANDROID TO DO |
| ME04-F13-AC08 | If I tap on the "swap collar" button, then:the collar should be disconnected;the Collars list should be displayed. | IOS DONE | ANDROID TO DO |
| ME04-F13-AC10 | In case the user disables Bluetooth on the smartphone when adding a fence with GPS, the app shows the M102 No Bluetooth (fence creation) message. | IOS DONE | ANDROID TO DO |
