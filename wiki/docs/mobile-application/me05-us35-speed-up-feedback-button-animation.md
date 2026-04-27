---
title: "ME05-US35 Speed up feedback button animation"
sidebar_label: "ME05-US35 Speed up feedback button animation"
sidebar_position: 700
last_modified: "Apr 12, 2020"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Story owners | Link to JIRA Issue |
|---|---|---|---|
| ME05. Feedback |
| APPROVED |
| Nicolay Gavrilov, Pavel Leonenko, Vadim Pylsky [X], Anastasia Brechko |
| HALO-3567 - MOB: ME05-US35 Speed up feedback button animation Closed |# User story

\> As an owner, I want animation on the feedback button to disappear quickly so that I could immediately apply another feedback for my pet.

# Design

| Current design | New design |
|---|---|
| Current feedback button animation (error).MP4 | New feedback animation (success)New feedback animation (error) |# Acceptance criteria

| AC | Text | Notes/Links/Screens |
|---|---|---|
| ME05-US35-AC01 | The app no longer completes the full turn of the spinner to show the result of sending feedback on the button. The feedback sending result is shown immediately after it is received. | N/A |
| ME05-US35-AC02 | Animation of success and error icons on the feedback buttons is changed according to the new design. |
| ME05-US35-AC03 | M97 'Unable to connect to \<pet name\> collar' pop up is replaced with the “Collar is out of Wi-Fi, cellular and Bluetooth range” toast message. |
