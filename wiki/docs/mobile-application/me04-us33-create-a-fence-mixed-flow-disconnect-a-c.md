---
title: "ME04-US33. Create a fence (mixed flow): \"disconnect a collar\" card"
sidebar_label: "ME04-US33. Create a fence (mixed flow): \"disconnect a collar\" card"
sidebar_position: 17
author: "Galina Lonskaya"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| UNDER REVISION |
| Galina Lonskaya |
| HALO-2038 - [ME04. Create Fence with a collar] ME04-US33: "disconnect a collar" card Closed |# User story

\> As owner, I want to disconnect collar so that I stop using it for dots addition or choose the other collar.

# Acceptance criteria

| AC | Text |
|---|---|
| AC01 | The first entry point to the "Disconnect a collar" card:If I tap on the "Select a collar" icon and there is a paired collar, then the "disconnect a collar" card should be displayed.Pic 1 Disconnect a collarThe screen consists of:"Using \<Pet's name or Collar type\> collar" textHALO collar icon with HALO ring"disconnect" button | Pic 1 Disconnect a collar | The screen consists of:"Using \<Pet's name or Collar type\> collar" textHALO collar icon with HALO ring"disconnect" button |
| Pic 1 Disconnect a collar | The screen consists of:"Using \<Pet's name or Collar type\> collar" textHALO collar icon with HALO ring"disconnect" button |
| AC02 | The second entry point to the "Disconnect a collar" card:If I tap on the collar pin, then the "disconnect a collar" card should be displayed. |
| AC03 | If I tap on the "disconnect" button, then the collar should be disconnected. |
| AC04 | If I tap on the "disconnect" button and the collar is successfully disconnected, then:the "\<Device name\> has been successfully disconnected" toast message should be displayed;the "Disconnect a collar" card should be closed |
| AC05 | After the successful disconnection, then toolbar should be updated. See the details in ME04-US29. Create a fence (mixed flow): toolbar behavior updates. |
| AC06 | After the successful disconnection, then the collar pin shouldn't be displayed on the map and the user's location pin should be displayed again. |
| AC07 | If I tap on the "swap collar" button, then:the collar should be disconnected;the collars list should be displayed, see a continuation in ME04-US25. Create a fence (mixed flow): collars list. |
