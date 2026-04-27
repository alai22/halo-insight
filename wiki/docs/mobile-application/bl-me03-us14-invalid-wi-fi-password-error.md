---
title: "[BL] ME03-US14 Invalid Wi-Fi password error"
sidebar_label: "[BL] ME03-US14 Invalid Wi-Fi password error"
sidebar_position: 42
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| ME03-EP02 Collar network connection setup |
| REVISED |
| Nicolay Gavrilov |
| HALO-3404 - MOB: ME03-US14 Invalid Wi-Fi password error Closed |
| 22 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As an owner I want the app to tell me if I entered an invalid Wi-Fi password for my AP so that I know why exactly my collar can't connect to it.

# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US14-AC01 | If the user enters an invalid Wi-Fi AP password for a collar, the app at first displays the connection process on the 'Connecting to the \<Wi-Fi ap name\>' pop-up. After the app receives the error from the collar, it closes the 'Connecting to the \<Wi-Fi ap name\>' pop-up and displays the M132 pop-up. | Screen design:Link to ZeplinM132 pop-up |
| ME03-US14-AC02 | The user can enter a new Wi-Fi password in the corresponding field of the M132 pop-up. The app closes the error pop-up, sends the new password the collar and displays 'Connecting to the \<Wi-Fi ap name\>' pop-up upon tapping on the 'Ok' button. | N/A |
| ME03-US14-AC03 | In case the user entered an invalid password to M132 pop-up, the pop-up reappears again. | N/A |
| ME03-US14-AC04 | In case the user taps on the 'Cancel' button, the M132 pop-up is closed and the app displays 'Choose a Network' screen. | N/A |
| ME03-US14-AC05 | The entered password is validated according to validation rules from ME03-US21 Wi-Fi password pop-up redesign and the same error handling logic is applied. | N/A |
