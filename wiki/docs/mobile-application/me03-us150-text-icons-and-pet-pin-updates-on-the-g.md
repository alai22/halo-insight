---
title: "ME03-US150. Text, icons and Pet pin updates on the 'GPS Signal Level Settings' screen"
sidebar_label: "ME03-US150. Text, icons and Pet pin updates on the 'GPS Signal Level Settings' screen"
sidebar_position: 477
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya KolyadaGalina Lonskaya Vadzim Litvin [X] Valeria Malets |
| HALO-22180 - MOB: ME03-US150. Text, icons and Pet pin updates on the 'GPS Signal Level Settings' screen Closed |
| Click here to expand...As of 06 Jan 2025 Mariya Kolyada created the initial version of US. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo account owner, I want to view text updates, BLE connectivity over Pet Pin icon and removed GPS level icon so that I can ensure the collar is on the dog and connected via BLE.

# Acceptance criteria

| AC | Description | iOS UI design | As is | To be | As is | To be | Condition | As is | To be | As is | To be |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ME03-US150-AC01 | Update the copy of the subtitle on the top of the screen:As isTo beGPS signal level can take up to 5 seconds to adjust. Make sure collar is on dog for accurate readings. GPS signal level can take up to 5 seconds to adjust. | GPS signal level can take up to 5 seconds to adjust. | Make sure collar is on dog for accurate readings. GPS signal level can take up to 5 seconds to adjust. | Figma |
| GPS signal level can take up to 5 seconds to adjust. | Make sure collar is on dog for accurate readings. GPS signal level can take up to 5 seconds to adjust. |
| ME03-US150-AC02 | Update the logic of the 'ghosted' Pet Pin displaying:As isTo beCollar is trying to reconnect over BLE.There was an exception during the telemetry reading, so the collar was disconnected.The current GPS level from Telemetry is lower than the lower boundary on the GPS Level Settings screen.Collar is trying to reconnect over BLE.There was an exception during the telemetry reading, so the collar was disconnected.The collar GPS level from Telemetry is low. | Collar is trying to reconnect over BLE.There was an exception during the telemetry reading, so the collar was disconnected.The current GPS level from Telemetry is lower than the lower boundary on the GPS Level Settings screen. | Collar is trying to reconnect over BLE.There was an exception during the telemetry reading, so the collar was disconnected.The collar GPS level from Telemetry is low. |
| Collar is trying to reconnect over BLE.There was an exception during the telemetry reading, so the collar was disconnected.The current GPS level from Telemetry is lower than the lower boundary on the GPS Level Settings screen. | Collar is trying to reconnect over BLE.There was an exception during the telemetry reading, so the collar was disconnected.The collar GPS level from Telemetry is low. |
| ME03-US150-AC03 | Update the icons over the Pet pin displaying:ConditionAs isTo beHasn't been connected to GPS beforeNo Pet Pin at allAnimated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma)Attempt to connect over BLEAnimated 'connectivity attempt' icon (see ME05-US59-AC18)Connected via BLE + GPS is low or no GPS'Feedback paused' icon (see ME07-F09-AC107)'BLE active' icon (see Figma)Connected via BLE + GPS medium or highNo icons over Pet Pin | Hasn't been connected to GPS before | No Pet Pin at all | Animated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma) | Attempt to connect over BLE | Animated 'connectivity attempt' icon (see ME05-US59-AC18) | Connected via BLE + GPS is low or no GPS | 'Feedback paused' icon (see ME07-F09-AC107) | 'BLE active' icon (see Figma) | Connected via BLE + GPS medium or high | No icons over Pet Pin |
| Hasn't been connected to GPS before | No Pet Pin at all | Animated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma) |
| Attempt to connect over BLE | Animated 'connectivity attempt' icon (see ME05-US59-AC18) |
| Connected via BLE + GPS is low or no GPS | 'Feedback paused' icon (see ME07-F09-AC107) | 'BLE active' icon (see Figma) |
| Connected via BLE + GPS medium or high | No icons over Pet Pin |
| ME03-US150-AC04 | Replace the 'Attempt to connect over BLE' icon on Walk as well:As isTo beAnimated 'connectivity attempt' icon (see ME05-US59-AC18)Animated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma) | Animated 'connectivity attempt' icon (see ME05-US59-AC18) | Animated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma) |
| Animated 'connectivity attempt' icon (see ME05-US59-AC18) | Animated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma) |
| ME03-US150-AC05 | Remove the GPS indicator icon and Spinner before the 'Current GPS Signal Level' title. |
| ME03-US150-AC06 | Reduce the height before the 'GPS levels' scale and the height of the 'Current GPS level' pin (blue lollipop). |
