---
title: "[Won't have] ME05-US57. Display whether the collar is online or offline on the 'Instant feedback' card"
sidebar_label: "[Won't have] ME05-US57. Display whether the collar is online or offline on the 'Instant feedback' card"
sidebar_position: 317
author: "Ekaterina Dupanova"
---

| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
|  |
| 30 May 2023 draft story is created |# Contents

User story Goal Acceptance criteria AC Description Design Apply feedback to one pet

# User story

\> As an app user I want to see if my collar is online or offline on the instant feedback card so that I understand if I can send Instant feedback or not.

# Goal

\> At the moment, we know that some users are receiving multiple errors stating that the collar is unavailable when attempting to send instant feedback. This is one of the top 5 errors by the number of repetitions. Thus, users are unable to send instant feedback, and the system does not give them precise understanding of what specific problem is preventing them from doing so. Only a general error is displayed 'Your collar is out of Wi-Fi, cellular and Bluetooth range or powered OFF'.With this feature the goal is to: Decrease number of unsuccessful trying to send IF (IF-Instant Feedback)Increase user loyalty (ratings)

# Acceptance criteria

| AC | Description | Design | Apply feedback to one pet |
|---|---|---|---|
| ME05-US57-AC01 | The acceptance criteria below should be applied for the following scenarios:When the user applies feedback from the Pet CardWhen the user applies feedback from the Trainings tab |  |
| ME05-US57-AC02 | The new UI elements of the IF card should be as follows:\<Pet name\>BLE iconWi-Fi/LTE icon'Apply Instant Feedback' text\<Explanation text\> - see detailed requirements below, it depends on the scenario.IF buttons in enabled and disabled state - see detailed requirement below, it depends on the scenario. (Note: 'in progress', 'pressed button', 'success', 'fail' button states remain as is) | Buttons enabled.Buttons disabled. |
| ME05-US57-AC03 | PreconditionBLE disabled/disconnectedPhone and device onlineThe app should:Show 'Bluetooth disabled/disconnected' icon stateShow 'Wi-Fi' or 'LTE' connected icon (depending on the type of connection)Show \<Explanation text\>: 'For best performance enable Bluetooth in your phone settings'Enable IF buttons |  |
| ME05-US57-AC04 | PreconditionBLE disabled/disconnected Phone and device not onlineThe app should:Show 'Bluetooth disconnected/disabled' icon stateShow 'Wi-Fi' or 'LTE' No Signal icon Show \<Explanation text\>: 'Collar is not on the Internet. Try enabling Bluetooth on your phone, if you are near your dog'Disable IF buttons |  |
| ME05-US57-AC05 | PreconditionBLE connectedDevice not connected over BLE and not onlineThe app should:Show 'Bluetooth connected' icon stateShow 'Wi-Fi' or 'LTE' No Signal icon Show \<Explanation text\>: 'Collar is not on the Internet. If you are near your dog, try getting closer to send Instant Feedback'Disable IF buttons |  |
| ME05-US57-AC06 | PreconditionBLE connectedDevice connected over BLE and not onlineThe app should:Show 'Bluetooth connected' icon stateShow 'Wi-Fi' or 'LTE' No Signal icon Show \<Explanation text\>: nothingEnable IF buttons |  |
| ME05-US57-AC07 | Precondition2 devices1 collarBLE connectedDevice not onlineOn the second device the app should:Show Socket iconShow 'Wi-Fi' or 'LTE' No Signal icon Show \<Explanation text\>: 'Collar is currently connected to another phone's Bluetooth'.Disable IF buttons |  |
| ME05-US57-AC08 | Notifications |  |
| ME05-US57-AC09 | Analytics (discuss with the team)Count how many times they click the grey buttons (to evaluate whether its working).How often they go to the IF card and there is no connection and everything is deactivated (to compare how many times they come to this card and they CAN press a button vs how many times they come to this card and they cannot press a button). Log it to AppInsights: how often they come to this card and the collar is connected vs the collar is disconnected. |  |
