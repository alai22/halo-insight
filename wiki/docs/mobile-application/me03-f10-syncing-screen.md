---
title: "ME03-F10. 'Syncing' screen"
sidebar_label: "ME03-F10. 'Syncing' screen"
sidebar_position: 484
last_modified: "Mar 31, 2025"
author: "Galina Lonskaya"
---

| Document owners | Linear/Jira ticket | History of changes |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-273/[ios]-collar-details-syncing-screen |
| 06 Feb 2025 draft user story is created by Galina Lonskaya |User story Acceptance Criteria Table 1 - Syncing screen states Table 2 - BLE section states Table 3 - Wi-Fi section states Table 4 - LTE section states

#### User story

As Halo app account owner, I want to access detailed connectivity information related to my collar so that I can ensure that it works reliably.

#### Acceptance Criteria

| AC | Description | Connectivity percentage | Bottom buttons |
|---|---|---|---|
| ME03-F10-AC01 | If I tap on 'Syncing' section, then 'Syncing Details' screen should be shown. See the table with all screen states below. |
| ME03-F10-AC02 | The connectivity percentage time should be shown on the Syncing Details screen. See BE related task and contract details in HALO-22323 - BE: Fetch connectivity average time for 7 days and send to mob Closed cc Alexei Zhukov |
| ME03-F10-AC03 | If connectivity percentage is equal or lower than 89 %, the the color A should be used as a background, see figma. |
| ME03-F10-AC04 | If connectivity percentage is greater than 89 %, the the color B should be used as a background, see figma. |
| ME03-F10-AC05 | If connectivity percentage is unavailable due to any reason, then the following UI should be shown, see figma. |
| ME03-F10-AC06 | The percentage should be rounded mathematically to whole numbers. |
| ME03-F10-AC07 | 'Allow Bluetooth' button should be shown at the bottom of the screen, if BLE permission is disabled, see figma. |
| ME03-F10-AC08 | 'Enable Bluetooth' button should be shown, in case Bluetooth permission is granted, BUT Bluetooth is disconnected on the smartphone, see figma. |
| ME03-F10-AC08 | If I tap on Allow Bluetooth button and BLE permission is denied, then: M143 popup should be shown, see Figma |
| ME03-F10-AC09 | If I tap on 'Enable Bluetooth' button and BLE permission is provided BUT Bluetooth is disconnected, then: M178 popup should be shown, see iOS Figma;OR M178 popup should be shown, see Android Figma |
| ME03-F10-AC10 | If I tap on 'Add Wi-Fi' button, then the same 'Add Wi-Fi' screen should be opened as within Onboarding with a few UI changes, see Figma. |
| ME03-F10-AC29 | After successfully adding Wi-Fi, the toast should be shown, see Figma plus(Native apps) ME14-F06. Toast notifications (general requirements). |#### Table 1 - Syncing screen states

| AC | BLE connection (or SocketBle - received from another phone) | Wi-Fi connection | LTE connection | Connection Never Established | Last telemetry received in | UI design | Assigned collar to a pet | Not assigned | Assigned collar to a pet | Not assigned | ME03-F10-AC12 | ME03-F10-AC13 | ME03-F10-AC14 | ME03-F10-AC15 | ME03-F10-AC16 | ME03-F10-AC17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Yes | No | No | No | less than 3 sec ago (Assigned collar) | N/A (Unassigned collar) | Figma | the same as for assigned collar |
| Yes | Yes (Wi-Fi is available, but BLE is used as primary) | No | No | less than 3 sec ago (Assigned collar) | N/A (Unassigned collar) | Figma |
| No | Yes | No | No | less than telemetry.secondsToNext + 1s ago (Assigned collar) | less than 20s ago (Unassigned collar) | Figma |
| No | No | Yes | No | less than telemetry.secondsToNext + 1s ago (Assigned collar) | less than 20s ago (Unassigned collar) | Figma |
| No | No | No | Yes | never received | never received | Figma |
| Doesn't matter | Doesn't matter | Doesn't matter | No | more than threshold above | more than threshold above | Figma See the general rule for 'passed time format' (native apps): Non-Functional Requirements#BR-16PassedtimeformatTime changes on the fly |#### Table 2 - BLE section states

| AC | Description | UI design (Figma - source of truth) | ME03-F10-AC18 | ME03-F10-AC19 | ME03-F10-AC20 |
|---|---|---|---|---|---|
| BLE is used |  | Figma |
| BLE permission denied or BLE disconnected |  |
| BLE is out of range |  |#### Table 3 - Wi-Fi section states

| AC | Description | UI design (Figma - source of truth) | ME03-F10-AC21 | ME03-F10-AC22 | ME03-F10-AC23 | ME03-F10-AC24 | ME03-F10-AC25 |
|---|---|---|---|---|---|---|---|
| Both Wi-Fi and BLE are available. BLE is used as primary connection |  | Figma |
| Wi-Fi is connected AND BLE is out of range |  |
| Wi-Fi is not connected, but it has been connected at least once before |  |
| Wi-Fi network hasn't been added, but BLE or LTE is currently in use. |  |
| Wi-Fi network hasn't been added, and neither BLE nor LTE is in use at the moment. |  |#### Table 4 - LTE section states

| AC | Description | UI design (Figma - source of truth) | ME03-F10-AC26 | ME03-F10-AC27 | ME03-F10-AC28 |
|---|---|---|---|---|---|
| LTE is used |  | Figma |
| LTE is not used at the moment, but was connected previously |  |
| LTE has never been connected |  |Implementation details

Real Time Updates logic should be used here in order to receive telemetry from all 3 channels.The last used channel is displayed near the Syncing label.For reference see PetViewModelsManager.OnPetTelemetryUpdate()

The connectivity percentage is a new feature. It will be available only via the Backend APIAll other data is available through telemetry and Backend API.Connection via BLE is displayed if telemetry comes via BLE or SocketBle.We need information about the current adapter type, adapter status and signal strength.The collar always returns the signal strength of the adapter in use via BLE.The checks are taken one by one:

- First, the adapter type. If a WiFi adapter is currently in use, then we assume the Cellular is currently paused and disconnected (the UI will have the text*Last Connected*)
- Then it's status. For WiFi status it must be`SocketConnected`, otherwise, we consider that WiFi has no signal (**in this case we should probably not write Out of range, as it can be a situation when WiFi has no internet access**).

If in real time we receive data not via Bluetooth nor SocketBle, the type of the current adapter received in telemetry is marked.Information about the previously used adapter and status can only be obtained via BE. We also use them to display information about the status of currently unused adapters on the UI. That is, if we get updates via BLE, and the collar uses WiFi, we can only get Cellular adapter data from BE. If there is no information about the adapters, it means that the connection never happened.

For reference see CollarNetworkConnectivity.FromAdapterSettings() (You can ignore the signal strength checks, as they are not necessary to use them here)


