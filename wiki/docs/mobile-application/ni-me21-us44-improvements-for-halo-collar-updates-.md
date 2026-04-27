---
title: "[NI] ME21-US44. Improvements for 'Halo Collar Updates' flow (no Wi-Fi and LTE)"
sidebar_label: "[NI] ME21-US44. Improvements for 'Halo Collar Updates' flow (no Wi-Fi and LTE)"
sidebar_position: 282
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Maria Shikareva [X] |
| HALO-14261 - MOB+BE: ME21-US44. Improvements for 'Halo Collar Updates' flow (no Wi-Fi and LTE) Closed |
| Click here to expand... |# Contents

User story Acceptance criteria Error handling Google Analytics

# User story

\> As a Halo app user I want to see a notification that the collar isn't connected to Internet so that to understand the importance of it and have an option to setup Wi-Fi if it was skipped previously.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
|  | Preconditions: a user skipped configuring Wi-Fi and tapped 'Continue Without Wi-Fi' buttonANDthere's no LTE on the collar.When a user taps 'Check Updates' button, then the app should display a pop-up:Change buttons to 'Setup Wi-Fi'; Update Collar LaterWe need to change one of 2 flow (add a collar OR setup wi-fi) to get more info from the collar (e.g. read telemetry about LTE configuration).We need to double check with FW how we can exactly understand that there's no LTE/ Wi-Fi on the collar (maybe the user skipped in the app but Wi-Fi was setup earlier).This can be tricky from restoring progress perspective:user skipped wi-fi setup;mobile app send this info to BE;in some time this info on BE side isn't actualmobile app:saved it locally w/o sending to BEBE won't save this progress and show the screen again later.Good idea: check this info only of Onboarding goes continuously. If it was restored, than don't show this pop-up at all. → in this case we can do it as an improvement.If we want to show this pop-up always, we need to think of it right now within Restoring task → if not, users might have issues with compatibility (it will affect users who already started Onboarding but didn't finalize it yet). | Link to Zeplin | Link to Zeplin |
|  | When a user taps the 'Setup Wi-Fi' button, then the app should:close the pop-up;open 'Connect Your Halo to Wi-Fi' screen.Note: it was confirmed that we can do that because of screens modality. |  |  |
|  | When a user taps the 'Update Collar Later' button, then the app should:close the pop-up;close 'Halo Collar Updates' screen; → if opened from Onboardingopen the next step as described in ME03-US85. Add Collar: GPS calibration screens. |  |  |
|  | Precondition: 'Connect Your Halo to Wi-Fi' screen is opened.If a user taps 'Setup Wi-Fi Later', then the app should:TBD how can we avoid opening the same screens in circle |  |  |
| Error handling |
| ME21-US44-AC15 |  |
| Google Analytics |
| ME21-US44-AC17 |  | - |  |
