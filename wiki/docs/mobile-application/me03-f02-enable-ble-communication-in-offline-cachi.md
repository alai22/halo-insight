---
title: "ME03-F02. Enable BLE communication in offline (caching Rolling Codes)"
sidebar_label: "ME03-F02. Enable BLE communication in offline (caching Rolling Codes)"
sidebar_position: 55
author: "Nicolay Gavrilov"
---

| Document status | Test cases status | Story owners | Link to JIRA Issues |
|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 28 Oct 2021 |
| Nicolay Gavrilov, Pavel Leonenko, Timofey Burak [X], Anastasia Brechko |
| HALO-3402 - MOB: ME03-US22. Enable BLE communication in offline (caching Rolling Codes) Closed HALO-4793 - Android: ME03-F02. Enable BLE communication in offline (caching Rolling Codes) Closed |# Contents

User story Acceptance criteria ME03-F02 Caching rolling codes sequence diagram Implementation notes

# User story

\> As an owner I want my smartphone to store the rolling codes in smartphone memory so that the collar could be always quickly unlocked.

# Acceptance criteria

| AC | Text | iOS screen design / implementation statusIOS DONE | Android screen design / Implementation statusANDROID DONE |
|---|---|---|---|
| ME03-F02-AC01 | The mobile app caches 100 Rolling Codes (RCs) in smartphone memory. | - | - |
| ME03-F02-AC07 | The app requests a new set of rolling codes after 50 rolling codes are used. | - | - |
| ME03-F02-AC02 | The cached RCs are not deleted after the app is closed or updated to the new version. | - | - |
| ME03-F02-AC03 | The cached RCs are deleted when either:the user logs offORthe collar is removed from the accountORthe app is uninstalled. | - | - |
| ME03-F02-AC04 | The cached RCs are deleted upon failing validation on the collar side (see the ME03-F02 sequence diagram below). | - | - |
| ME03-F02-AC05 | If the smartphone is offline when the user tries to connect to the collar via BLE and there are no RC's cached, the app displays the M125 Connection error.Note: for more details see ME14-F01 Unified errors handling. | - | - |
| ME03-F02-AC06 | In case a 'Handling RC error' occurred, then the mobile app:deletes all cached RC's;displays M124 Security error for provisioning. | - | - |
| ME03-F02-AC06 | The M124 Security error for provisioning contains one of the following codes:1 (Wrong payload format)2 (IC on the collar is equal or greater than the provided IC)3 (The provided IC is significantly greater than the IC on the collar)Error code 3 may be received in case the IC from the sent RC differs from collar RC by more than 10000.4 (Invalid serial number)5 (Decryption error)6 (Wrong payload size)Also there are codes which are not related to RC error:10 (Cannot decrypt Wi-Fi password) - this is shown to users when a collar cannot decrypt a Wi-Fi password encrypted by backend during the process of setting up Wi-Fi on a collar.Error messages example:A security error occurred. If this is not the first time you see this message contact us for support. Error code: 1.Note from the QA team: Error Codes: 5 & 6 can not be tested due to impossibility to reproduce them. | - | - |# ME03-F02 Caching rolling codes sequence diagram

# Implementation notes

| IN | Description |
|---|---|
| ME03-F02-IN01 | There's the RC limit on BE side ("RollingCodeRateLimitDuration": "0.01:00:00.00", "RollingCodeRateLimitCount": 500) → 500 RC per day.Note: as of 28 Oct 2021 there's no any error pop-up on the mobile side which reflects this particular error. Actual result: the mobile app shows popup 'App Upgrade Error' |
