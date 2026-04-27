---
title: "(Outdated) ME21-US67. Do not show the pet pin on the my map screen after adding collar for the first time"
sidebar_label: "(Outdated) ME21-US67. Do not show the pet pin on the my map screen after adding collar for the first time"
sidebar_position: 450
author: "Ekaterina Dupanova"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-21330 - [Critical] QA: Do not show the pet pin on the my map screen after adding collar for the first time Closed |
| the user story draft is created 10 Sep 2024 |Table of Contents

Background User story Acceptance criteria Implementation notes

# Background

The reason why this story is created: When the map first loads with a collar that was just attached and not initialized it will not be able to show the pet pin on the map. We explored a way to show a ghosted pet pin showing the pet at the same location as the user. This was technically doable though with some considerations that needed to be developed. We could also take the collar's location that gets picked up during attach (if there is one, which could also be the wrong location - cached - if it's a refurb). Forcing a fake pet pin location felt like bad UX. It also created the false expectation that they should be able to see their pet pin while in the house. And with the HC4 and the gps chip updates made, the collars will be even more precise when it's in a building or not. We also plan to shortly introduce indoor mode which would not show the pet pin and instead show a house icon.

Ultimately the goal is to get them outside to experience tracking. Not showing them the pet pin should serve as more motivation to go see my collar show up. Once it goes outside the pin will show up almost immediately.

# User story

\> As Halo app account owner I want see the Pet Pin on my map with an accurate location so that I am sure that my collar is working and showing the correct location.As Halo app account owner I do not want see the Pet Pin on my map if my collar was not initialized so that I do initialization and make sure my collar is working properly and showing the correct location.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| ME21-US67-AC01 | Preconditionthe collar was added for the first timeGPS initialization is requiredThe pet pin should not be displayed on My Map. | n/a |# Implementation notes

| IN | Description |
|---|---|
| ME21-US67-IN01 | FW: After the collar is linked to an account, it clears location data by overwriting coordinates (changes to 200 200) |
