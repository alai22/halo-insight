---
title: "(Won't have) ME21-US66. MOB: Remove training beacon steps from the Onboarding flow"
sidebar_label: "(Won't have) ME21-US66. MOB: Remove training beacon steps from the Onboarding flow"
sidebar_position: 410
last_modified: "May 10, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related requirements |
|---|---|---|---|
| DRAFT |
| Kiryl Trafimau |
| HALO-20037 - MOB+BE: Remove training beacon from flow (Sep 2024) Closed |
|  |# Contents

User story Acceptance criteria

# User story

\> As a Halo account owner I want to pass the Onboarding flow quickly so that I can start to use the app to safe my dog as soon as possible.

# Acceptance criteria

| AC | Description | Designs/Notes |
|---|---|---|
| ME21-US66-AC01 | Pre-conditions:I am on the Onboarding flowI am on the 'Initializing GPS' screenI passed the initialization processIF I Click 'Next' buttonTHEN I should be redirected to the 'Using The Halo Collar app' screen | Initializing GPSUsing the Halo Collar app |
| ME21-US66-AC02 | Pre-conditions:I am on the Onboarding flowI am on the GPS initialization screenI did not pass the initialization processIF I Click 'Skip Initialization for Now' buttonTHEN I should be redirected to the 'Using the Halo Collar app' screen | Initializing GPSUsing the Halo Collar app |
