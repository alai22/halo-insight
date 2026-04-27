---
title: "ME05-US56. Fix 'Network congestion' toast message behavior"
sidebar_label: "ME05-US56. Fix 'Network congestion' toast message behavior"
sidebar_position: 302
author: "Ekaterina Dupanova"
---

| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-15574 - MOB: Fix 'Network congestion' toast message behavior Closed |
| 09 Feb 2023 draft story is created |# Contents

Background User story Acceptance criteria Send feedback to one pet

# Background

As of 03 Feb 2023 it was figured out that the logic of displaying 'Network congestion' toast message needs to be revised.

# User story

\> As an account owner, I want to see a toast when the instant feedback is not delivered because of timeout so that I can understand that I need to retry the instant feedback sending one more time. As an account owner, I want to see a toast when the instant feedback is not delivered because the collar is offline so that I can understand that I need to connect the collar.

# Acceptance criteria

| Send feedback to one pet |
|---|
| ME05-US56-AC01 | The acceptance criteria below should be applied for the following scenarios:When the user applies feedback from the pet card → Advanced SettingsWhen the user taps the 'Test on collar' button from:'Emergency feedback' settings screen'Warning feedback' settings screen'Boundary feedback' settings screen'Good behavior feedback' settings screen'Return whistle feedback' settings screen'Heading home feedback' settings screen |
| ME05-US56-AC02 | If the instant feedback is not delivered to my pet because BE has not received response from the collar at a specified the timeout (see ME05-US52-AC01, AC02), the following toast message should be displayed: the error toast icon'Your collar is out of Wi-Fi, cellular and Bluetooth range or powered OFF.' text |
| ME05-US56-AC03 | If the instant feedback is not delivered to my pet because it was too late when command reached the collar, the following toast message should be displayed: the error toast icon'Feedback was not received by your dog due to network congestion. Please try again.' text |
