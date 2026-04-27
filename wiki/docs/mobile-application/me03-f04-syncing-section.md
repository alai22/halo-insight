---
title: "ME03-F04. Syncing section"
sidebar_label: "ME03-F04. Syncing section"
sidebar_position: 624
author: "Mariya Kolyada"
---

| Document owners | Linear/Jira ticket | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-182/[ios]-collar-details-syncing-sectionhttps://linear.app/fueled/issue/HALO-283/[android]-collar-details-syncing-section |
| 04 Feb 2025 draft user story is created by Galina Lonskaya |User story: As Halo app account owner, I want to access connectivity information related to my collar so that I can ensure that it works reliably.

Acceptance Criteria:

See the possible statuses of 'Syncing' section / LTE/Wi-Fi icons in the tables below.

Table 1 - Syncing section statuses

|  | BLE connection (or SocketBle - received from another phone) | Wi-Fi connection | LTE connection | Connection Never Established | Last telemetry received in | UI design | Figma(Source of truth) | AC01 | AC02 | AC03 | AC04 | AC05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Yes | No | No | No | less than 3 sec ago (Assigned collar)N/A (Unassigned collar) |  | Figma |
| No | Yes | No | No | less than telemetry.secondsToNext + 1s ago (Assigned collar)less than 20s ago (Unassigned collar) |  |
| No | No | Yes | No | less than telemetry.secondsToNext + 1s ago (Assigned collar)less than 20s ago (Unassigned collar) |  |
| No | No | No | Yes | never received |  |
| Doesn't matter | Doesn't matter | Doesn't matter | No | more than threshold above | See the general rule for 'passed time format' (native apps): Non-Functional Requirements#BR-16Passedtimeformat |Table 2 - Wi-Fi icon states

|  | Signal strength | Level | UI | Figma | AC05 | AC06 | AC07 | AC08 |
|---|---|---|---|---|---|---|---|---|
| Strong signal | All thresholds are in /configuration endpoint response in telemetry.signalStrength Current values (Feb 2025):\> - 50 dBm- 50 to - 60 dBm- 60 to -70 dBm\< -70 dB |  | Figma |
| Good signal |  |
| Fair signal |  |
| Poor signal |  |Table 3 - LTE icon states

|  | Signal strength | Level | UI | Figma | AC09 | AC10 | AC11 | AC12 |
|---|---|---|---|---|---|---|---|---|
| Strong signal | All thresholds are in /configuration endpoint response in telemetry.signalStrength Current values (Feb 2025):\> - 65 dBm- 65 to - 75 dBm-75 to - 85 dBm\< - 85 dBm |  | Figma |
| Good signal |  |
| Fair signal |  |
| Poor signal |  |Implementation details

Real Time Updates logic should be used here in order to receive telemetry from all 3 channels.

The last used channel is displayed near the Syncing label.

For reference see `PetViewModelsManager.OnPetTelemetryUpdate()` .


