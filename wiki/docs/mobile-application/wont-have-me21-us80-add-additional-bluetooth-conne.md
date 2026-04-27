---
title: "(Won't have) ME21-US80. Add additional Bluetooth connection check before 'Link Collar to Account' opening"
sidebar_label: "(Won't have) ME21-US80. Add additional Bluetooth connection check before 'Link Collar to Account' opening"
sidebar_position: 442
last_modified: "Sep 11, 2024"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya Dmitry Kravchuk |
| HALO-21055 - MOB: ME21-US80. Add additional Bluetooth connection check before 'Link Collar to Account' opening Closed |
| the user story draft is created 07 Aug 2024 |Table of Contents

Background User story Acceptance criteria

# Background

The reason why this story is created: the parent screen were previously this check was performed was removed. See the previous behavior.

# User story

\> As Halo app account owner I want to see 'Bluetooth is disabled' before going to 'Link Collar to account' screen so that I can be in advance aware about bluetooth connection necessity.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| ME21-US79-AC01 | Precondition: 'Collar Attach' flow is initiated within FTUE Onboarding or from the app If I tap on Next button on 'Adding Your Halo Collar' screen and Bluetooth is disabled on the smartphone, then: M178 Disabled Bluetooth (Wi-Fi setup, Add Beacon, Update beacon) error popup message should be displayed on 'Adding Your Halo Collar' screen. | n/a |
