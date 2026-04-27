---
title: "[BL] ME03-US144. Update 'Collar Attach' flow initiated from the Pet card / Settings / Add Pet"
sidebar_label: "[BL] ME03-US144. Update 'Collar Attach' flow initiated from the Pet card / Settings / Add Pet"
sidebar_position: 426
last_modified: "Aug 13, 2024"
author: "Galina Lonskaya"
---

Click here to expand...| Document status | Document owner | Link to JIRA issue | Changes history |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Timofey Burak [X] Dmitry Kravchuk |
| HALO-20580 - MOB: ME03-US144. Update 'Collar attach' flow initiated from the Pet card / Settings / Find card (Add Pet flow) Closed |
| Click here to expand...19 Jun 2024 the draft user story is created by Galina Lonskaya |# Contents

User story Acceptance criteria Reference info Implementation notes

# User story

\> As a Halo app account owner I want to attach my collar from the app with decreased number of steps and additional not crucial info so that I can add collar with a min amount of time and efforts.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | The criteria below are relevant for adding any number of collars: from the first one and onwards |
|---|---|---|---|---|
| Entry points to 'Attach the collar from the app' flow (note: onboarding flow will be updated separately):Tap on 'Add Collar'/'Add New Collar' button on 'My Collars' screen ('Settings' tab) Tap on 'Add Collar' button on 'Pet card' without the linked collar ('My Map' tab)Flow completion of the pet adding from 'Find card' ('My Map' tab) |
| ME03-US144-AC01 | The following steps should be fully removed from the 'Attach the collar from the app' flow: Let's Get StartedYour Halo Collar KITHalo Collar Updates (FW/SGEE update)Your Collar’s GPS (GPS initialization)Using Halo Beacons (Beacon adding)Note: you can see all these steps in case you add the first collar from any of the entry points mentioned above. See the reference info with AS IS state recording below. | n/a | n/a |
| ME03-US144-AC02 | The following steps should remain in the 'Attach the collar from the app' flow, but the parent screen displaying videos should be removed from them:Powering Up & Connecting (Add Collar)Assigning Your Halo Collar to Your Pet (Add Pet)Connecting Your Halo Collar (Set up Wi-Fi) | See the screen flow in Figma Note 1: ignore Progress bar showingNote 2: ignore 'Wi-Fi' benefits screen (will be added within separate story) |
| ME03-US144-AC03 | The final sequence of the steps of the 'Attach the collar from the app' flow should be the following: Charge and add collar Assign petSet up Wi-FiNote: no logic changes are assumed to be done inside the steps within this user story. |
| ME03-US144-AC04 | When transitioning from one step of 'Attach the collar from the app' flow to another, the parent screen with a spinner on a white background should be displayed. | See the screen in Figma | The same as for iOS |# Reference info

- **Here**you can see a screen recording showing AS IS process of adding**the first**collar from the pet card (as of21 Jun 2024)
- **Here**you can see a screen recording showing AS IS process of adding**the second**collar from the app settings (as of21 Jun 2024)

# Implementation notes

| IN | Description |
|---|---|
| ME03-INXX-AC01 | This user story can be released separately from all other Onboarding tasks. Victor will get back to us later with the answer, but most probably we will not release it separately or it will be included in Pack Walk release → As of 8/7/24 no need to release separately |
