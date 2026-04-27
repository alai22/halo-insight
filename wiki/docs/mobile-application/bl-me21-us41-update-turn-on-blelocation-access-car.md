---
title: "[BL] ME21-US41. Update 'Turn On BLE/Location access' cards on 'Enable Permissions' screen (related to Android changes)"
sidebar_label: "[BL] ME21-US41. Update 'Turn On BLE/Location access' cards on 'Enable Permissions' screen (related to Android changes)"
sidebar_position: 278
last_modified: "Dec 08, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA issue | History of changes |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Kirill Akulich [X] Nikita Krisko Katherina Kaplina |
| HALO-14192 - MOB [Android]: ME21-US41. Update 'Turn On BLE/Location access' cards on 'Enable Permissions' screen (related to Android changes) Closed |
| Click here to expand...08 Dec 2022 Maria Shikareva [X] Marked the story as baselined (see ME01-F10. Enable Permissions). |# General description

As of 13 Oct 2022 'Turn On Bluetooth Access' card for Android contains only information about necessity of enabled Bluetooth access. But starting from Android 12 to have access to BLE a user will have to give access also to precise location → only in this case the app will be able to use BLE for scanning devices.

# User story

\> As Halo app account owner I want to see an updated 'Turn On BLE access' card for Android so that to have clear instructions and clarification what is needed from me for the best app performance.

# Acceptance criteria

| AC | Description | Android screen design | AS IS | TO BE | AS IS | TO BE |
|---|---|---|---|---|---|---|
| ME21-US41-AC01 | The changes described below should be applied for Android ≥ 12 only. | - |
| 'Turn On Location Access' card- |
| ME21-US41-AC02 | The text for this card should be changed (changes are highlighted in blue):AS ISTO BEYour phone's current location will be displayed as a blue dot on My Map to improve navigation between you and your pets.You can change permissions in your phone's Halo App settings.Your phone's current location will be displayed as a blue dot on My Map to improve navigation between you and your pets. Please note that in order to use the Halo Collar app and Bluetooth, you must allow access to your phone's precise location.You can change permissions in your phone's Halo App settings. | Your phone's current location will be displayed as a blue dot on My Map to improve navigation between you and your pets.You can change permissions in your phone's Halo App settings. | Your phone's current location will be displayed as a blue dot on My Map to improve navigation between you and your pets. Please note that in order to use the Halo Collar app and Bluetooth, you must allow access to your phone's precise location.You can change permissions in your phone's Halo App settings. | Link to Zeplin |
| Your phone's current location will be displayed as a blue dot on My Map to improve navigation between you and your pets.You can change permissions in your phone's Halo App settings. | Your phone's current location will be displayed as a blue dot on My Map to improve navigation between you and your pets. Please note that in order to use the Halo Collar app and Bluetooth, you must allow access to your phone's precise location.You can change permissions in your phone's Halo App settings. |
| 'Turn On Bluetooth Access' card |
| ME21-US41-AC03 | The text for this card should be changed (changes are highlighted in blue):AS ISTO BEWe need the app to have access to your phone's Bluetooth to communicate to your Halo Collar.You can change permissions in your phone's Halo app settings. But you should not try to 'pair' your phone with your Halo.We need the app to have access to your phone's Bluetooth to communicate to your Halo Collar. You can change permissions in your phone's Halo app settings. But you should not try to 'pair' your phone with your Halo.Please note that in order to use the Halo Collar app and Bluetooth, you must also allow access to your phone's precise location. | We need the app to have access to your phone's Bluetooth to communicate to your Halo Collar.You can change permissions in your phone's Halo app settings. But you should not try to 'pair' your phone with your Halo. | We need the app to have access to your phone's Bluetooth to communicate to your Halo Collar. You can change permissions in your phone's Halo app settings. But you should not try to 'pair' your phone with your Halo.Please note that in order to use the Halo Collar app and Bluetooth, you must also allow access to your phone's precise location. | Link to Zeplin |
| We need the app to have access to your phone's Bluetooth to communicate to your Halo Collar.You can change permissions in your phone's Halo app settings. But you should not try to 'pair' your phone with your Halo. | We need the app to have access to your phone's Bluetooth to communicate to your Halo Collar. You can change permissions in your phone's Halo app settings. But you should not try to 'pair' your phone with your Halo.Please note that in order to use the Halo Collar app and Bluetooth, you must also allow access to your phone's precise location. |
