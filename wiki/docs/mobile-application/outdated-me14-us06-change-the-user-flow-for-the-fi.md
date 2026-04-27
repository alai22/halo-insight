---
title: "[Outdated] ME14-US06. Change the user flow for the first login"
sidebar_label: "[Outdated] ME14-US06. Change the user flow for the first login"
sidebar_position: 67
author: "Nicolay Gavrilov"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| OUTDATED |
| Nicolay Gavrilov, Pavel Leonenko, Anastasia Brechko |
| HALO-3457 - MOB: ME14-US06. Change the user flow for the first login Closed |# User story

\> As an owner I want to always go trough the same user flow when creating pets and fences so that I could easily learn how to do it once I launch it for the first time

# Current implementation

At the moment users are redirected to the 'Add Collar!' when they launch the app for the first time. Users have to at first add a collar, and after that, they can add a pet. The screen never appears again after that and the users will never add collars and pets using the same flow. We need to make it so users would have to always do the same actions when adding collars and pets to their accounts.

# Acceptance criteria

| AC | Description | Links/Notes |
|---|---|---|
| ME14-US06-AC01 | The 'Add Collar!' screen is no longer displayed on the first user login to the app. Instead, the user is redirected to My Map screen. |  |
| ME14-US06-AC02 | The 'Add Collar' screen is always displayed as the first step of the process of adding a new collar in the following cases:when adding a new collar right after creating a new pet,when adding a new collar from the collars list,when adding a new collar from corrections settings;when adding a new collar from the pet card. |  |
| ME14-US06-AC03 | 'Skip' button is removed from the 'Add a collar!' screen. | Link to Zeplin |
| ME14-US06-AC04 | 'Cancel' button is added to the 'Add a collar!' screen. When the users tap on this button they cancel the process of adding a new collar and are redirected on the previous screen. |  |
| ME14-US06-AC05 | 'Cancel' button on both the 'QR scanning' and 'Manual SN entering' screens is replaced with 'Back' button. | Links to Zeplin:'QR scanning' screen'Manual SN entering' screen |
