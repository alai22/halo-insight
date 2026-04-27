---
title: "ME06-US14. Testing feedback on collar via BLE"
sidebar_label: "ME06-US14. Testing feedback on collar via BLE"
sidebar_position: 711
last_modified: "Jun 02, 2020"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owners | Link to JIRA Issue |
|---|---|---|---|
| ME06. Trainings |
| APPROVED (SQ) |
| Nicolay Gavrilov |
| HALO-3813 - MOB+ FW: ME06-US14. Testing feedback on collar via BLE Open |# User story

\> As an owner I want to send 'Test on collar' commands to the device via Bluetooth so that I could easily find the right feedback intensity for my dog during the training. During 'Finding the right feedback' training course I need to set the feedback intensity to the minimal value and tap on the 'Test on collar' button when the dog approaches the forbidden zone. If the dog does not respond, I need to increase the feedback intensity and repeat the whole process until the dog reacts. Given that, if there will be a delay between tapping on the 'Test on collar' button and applying the feedback on the collar, the dog will not understand why he or she receives the correction or encouragement.

# Acceptance criteria

| AC | Text | Notes/Links/Wireframes |
|---|---|---|
| ME05-US14-AC01 | 'Test on collar' commands are sent via BLE and via the internet. BLE is used as the primary channel while the internet is used if:Bluetooth is disabled on the smartphoneThe collar was not found during the background scanningThe app failed to unlock the collar | See the sequence diagram below |
| ME05-US14-AC02 | The app connects and pairs with the collar when the user opens (and disconnects it when the user leaves) one of the following screens:Warning Feedback settings screenBoundary Feedback settings screenEmergency Feedback settings screenGood Behaviour Feedback settings screenReturn Whistle Feedback settings screenHeading Home Feedback settings screen | N/A |
| ME05-US14-AC03 | In case the collar is not connected via BLE by the time the user taps on 'Test on collar', the BT channel is ignored and the command is sent via the Internet. | N/A |
| ME05-US14-AC04 | When the command is sent, the mobile app displays the spinner until a success confirmation is received either via Bluetooth or via the Internet. | N/A |
| ME05-US14-AC05 | In case both BLE is disabled and the internet is unavailable on the smartphone, the app displays the "Collar is out of Wi-Fi, cellular and Bluetooth range” toast message. | N/A |
| ME05-US14-AC06 | If the Bluetooth permission is not granted (e.g. after the user re-installed the app) the app will ask for it on the first attempt to test feedback on the collar. | N/A |# Dependencies

| # | Text | Notes/Links/Wireframes |
|---|---|---|
| ME05-US14-DE-01 | Collar FW has a characteristic to notify the mobile app about the result for instant commands that are sent via BLE. | See the sequence diagram below |
| ME05-US14-DE-02 | Collar registers all incoming commands in the logs. | N/A |# Sending instant commands via BLE (success flow) sequence diagram


