---
title: "ME21-US20. Onboarding: stepper on the parent screens"
sidebar_label: "ME21-US20. Onboarding: stepper on the parent screens"
sidebar_position: 253
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Links to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] Maria Shikareva [X] Nikita Krisko Kirill Akulich Dmitry Kravchuk |
| Click here to expand... HALO-12994 - MOB [NT]: ME21-US20. Onboarding: stepper on the parent screens Closed HALO-13035 - QA: ME21-US20. Onboarding: stepper on the parent screens Closed |
| Click here to expand...20 Jul 2022 Maria Shikareva [X] Updated screens with the correct existing player.05 Aug 2022 Maria Shikareva [X] Updated ME21-US20-AC02 based on changes for GPS calibration flow. |# Contents

User story Acceptance criteria Implementation notes

# User story

\> As a Halo app user I want to be able to see a stepper on the parent screens within the Onboarding flow so that to understand how many steps are left.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | Step value | Step name | Screen name |
|---|---|---|---|---|---|---|
| ME21-US20-AC01 | The app should display a stepper on the top of the parent screens with the following elements:text "#/5:", where # is the order number of the step a user is currently on (see ME21-US20-AC02 below);a horizontal intermittent line colored in blue for the current step and for the passed steps.Note: see an implementation note ME21-US20-IN01 below. | Link to Zeplin | Link to Zeplin |
| ME21-US20-AC02 | The app should display a stepper according to the following table:Step valueStep nameScreen name1Add CollarPrepare Your Halo Collar2Add PetAssign Your Halo to Your Dog3Wi-Fi SetupAbout the Halo Collar Connections4Collar UpdateHalo Collar and Satellite Data Updates Overview5GPS CalibrationHow Halo Locates Your DogNote: the screens will be implemented separately within [NI] ME21-US11. Onboarding: parent screens (with video and stepper). | 1 | Add Collar | Prepare Your Halo Collar | 2 | Add Pet | Assign Your Halo to Your Dog | 3 | Wi-Fi Setup | About the Halo Collar Connections | 4 | Collar Update | Halo Collar and Satellite Data Updates Overview | 5 | GPS Calibration | How Halo Locates Your Dog | - | - |
| 1 | Add Collar | Prepare Your Halo Collar |
| 2 | Add Pet | Assign Your Halo to Your Dog |
| 3 | Wi-Fi Setup | About the Halo Collar Connections |
| 4 | Collar Update | Halo Collar and Satellite Data Updates Overview |
| 5 | GPS Calibration | How Halo Locates Your Dog |
| ME21-US20-AC03 | The stepper should not be tappable. | - | - |
| ME21-US20-AC04 | When a user adds the second collar (see [Not impl.] ME21-US14. Onboarding: add the 2nd collar), then the app should not display a stepper at each of the steps. | - | - |# Implementation notes

| ID | Description |
|---|---|
| ME21-US20-IN01 | It's required to implement a stepper extendable and reusable. Maybe even as container for child screens (pager). |
