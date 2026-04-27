---
title: "ME21-US90. Hide Pet Pin until Pet Collar first changes the GPS Level to Outdoor/High in the current user account"
sidebar_label: "ME21-US90. Hide Pet Pin until Pet Collar first changes the GPS Level to Outdoor/High in the current user account"
sidebar_position: 469
last_modified: "Nov 06, 2024"
author: "Mariya Kolyada"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| HALO-21789 - MOB: ME21-US90. Hide Pet Pin until Pet Collar first changes the GPS Level to Outdoor/High in the current user account Closed |
| 05 Nov 2024 Mariya Kolyada created the initial user story. |Table of Contents

User story Acceptance criteria

# User story

\> As a Halo Account owner I want to view my pet's pin only after the collar location is up-to-date so that I can make sure that the collar works correctly and display my location other than the Halo Collars manufacturing or Previous collar owner's location.

# Acceptance criteria

| AC | Description |
|---|---|
| ME21-US90-AC01 | When user adds the collar to their account each time, the app should:Remember this collar as a collar that has NOT had an Outdoor/High GPS Level in the current user account yet. |
| ME21-US90-AC02 | The app should stop storing such a collar in the list only after its first change of the GPS Level to Outdoor/High in the current user account. |
| ME21-US90-AC03 | Before displaying the Pet Pin on the map, the app should:Check if the Pet Collar is presented on the list of collars that have NOT had an Outdoor/High GPS Level in the current user account yet. |
| ME21-US90-AC04 | If the Pet Collar is presented on this list - then the app should:Hide Pet Pin on My Map until the collar gets an Outdoor/High GPS Level for the first time in the current user account. |
| ME21-US90-AC05 | If the Pet Collar is absent from the list - then the app should:Display Pet Pin as usual. |
