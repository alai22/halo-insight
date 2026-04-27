---
title: "ME04-US103. Fence edit. Display user's position pin and the button to focus on it"
sidebar_label: "ME04-US103. Fence edit. Display user's position pin and the button to focus on it"
sidebar_position: 444
last_modified: "Sep 05, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-21199 - MOB: ME04-US103. Fence edit. Display user's position pin and the button to focus on it Closed |
| Click here to expand...As of 05 Sep 2024:Mariya Kolyadacreated the initial version of US. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo acount owner I want to view my device location pin and be able move the map on my user's device location so that I could edit a fence borders in place where I am in case the map images are outdates.

# Acceptance criteria

| AC | Description | iOs design | Android design |
|---|---|---|---|
| ME04-US103-AC01 | Add the user's location pin on the Fence Edit screen. |  |  |
| ME04-US103-AC02 | Add the 'My Location' button on the Fence Edit screen. | Figma | Figma |
| ME04-US103-AC03 | The My Location' button should appear only if the user's location pin is not visible on the screen |
| ME04-US103-AC04 | PreconditionApp has the user's device location accessIf I click the 'My Location' button, then the app should:Display the Map part in Fence Edit mode with my location in the center. |
| ME04-US103-AC05 | PreconditionApp has no user's device location accessIf I click the 'My Location' button, then the app should:Display the M55 Disabled Location pop-up. |
