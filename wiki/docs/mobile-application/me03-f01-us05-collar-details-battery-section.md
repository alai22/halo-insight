---
title: "ME03-F01-US05. Collar Details: Battery section"
sidebar_label: "ME03-F01-US05. Collar Details: Battery section"
sidebar_position: 485
last_modified: "Mar 19, 2025"
author: "Mariya Kolyada"
---

| Document owners | Linear/Jira ticket | History of changes |
|---|---|---|
| Mariya Kolyada Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-168/[ios]-collar-details-battery-section |
| 06 Feb 2025 draft user story is created by Mariya Kolyada 10 Feb 2025 Mariya Kolyada updated story by adding new designs / text description.18 Feb 2025 Mariya Kolyada final updates after added tech details and designs. |User story: As Halo app account owner, I want to access Collar Battery Details so I know how long can I rely on the collar.

Tech details: Battery data can be retrieved from Telemetry field from the GET /collar/my and GET /collar/\{id\} queries. This data can be used as initial data and also if the data cannot be retrieved in another way (BLE or Socket)In case we will receive Relatime Updates, the data should be taken from Collar Telemetry. We need BatteryChargePercent, BatteryStatus and RemainingBatteryLifetimeInSeconds - the detailed contract is described here Telemetry Unified ContractWe can't always use RemainingBatteryLifetimeInSeconds. The value should only be used when BatteryStatus = NotCharged. Also need to check that this value is there and it is valid - the minimum and maximum values come in the config (GET /configuration - Telemetry.MinBatteryLifetimeInSeconds and Telemetry.MaxBatteryLifetimeInSeconds).

If we can use RemainingBatteryLifetimeInSeconds by the conditions above, it is used to determine if the collar is discharged or not. This is done by determining if the current date is greater than the sum of the RemainingBatteryLifetimeInSeconds and the date the last telemetry was received (Timestamp)If we determine by RemainingBatteryLifetimeInSeconds that the collar is discharged, but BatteryChargePercent \> 0, we still consider the collar to be dischargedIn our code, the model is described here - BatteryCharge class

**BatteryCharge**Expand source```
public BatteryCharge(CollarSummaryModel? collarSummaryModel, TelemetryConfigurationModel configuration) \{ RemainingBatteryLife = collarSummaryModel?.Telemetry?.CanUseRemainingBatteryLife ?? false ? collarSummaryModel.Telemetry?.RemainingBatteryLife : null; var isRemainingBatteryLifeValid = RemainingBatteryLife.HasValue && RemainingBatteryLife.Value .IsTimeInRange( configuration.MinBatteryLifetime, configuration.MaxBatteryLifetime); if (collarSummaryModel?.LastConnected != null && isRemainingBatteryLifeValid) \{ _expectedDischargeTime = collarSummaryModel.LastConnected.Value + RemainingBatteryLife.Value; \} ChargePercent = collarSummaryModel?.BatteryChargePercent; IsCharging = collarSummaryModel?.BatteryStatus == BatteryStatus.Charging || collarSummaryModel?.BatteryStatus == BatteryStatus.ChargingDone; IsUsb = false; \}
```

Collar Diagnostics data can be retrieved in Issues.Battery. This information can only be retrieved from the backend API. More details here

Acceptance Criteria:

Collar Details screen: Figma.

| AC | Description | AC | Remaining battery life | Battery charging level | Battery has catastrophic issues | No Collar Diagnostic for more than 30 days | No | Yes |
|---|---|---|---|---|---|---|---|---|
| AC01 | App should display the following elements:ImageTitleRemaining battery data (format BR-23 Battery level in time units)Charging recommendations / Battery Health statusby following the rules:ACRemaining battery lifeBattery charging levelBattery has catastrophic issuesNo Collar Diagnostic for more than 30 daysNoYesAC01-01\> 1.5 h76-100%FigmaReplace:'Green Checkmark' with 'Orange Triangle' on top of the battery with the appropriate charge level (see designs for each battery level in Figma)'Health is Normal' with 'Issue Detected'Everything else remains the same.Replace either 'Green Checkmark' or 'Orange Triangle' with 'Grey Triangle' on top of the battery with the appropriate charge level.Replace either 'Health is Normal' or 'Issues detected' with 'Health data unavailable.'Everything else remains the same.FigmaAC01-0251-75%FigmaAC01-0326-50%FigmaAC01-044-25%FigmaAC01-05\<=1.5 h-FigmaAC01-06battery is discharged (expected discharge time \< current date)* See Tech details aboveFigmaAC01-07chargingFigmaFigmaSame logic as if collar has some battery level (see above)AC01-08unknown* No telemetry has been received yet or BE returned telemetry without battery levelDisable tap on the sectionFigma | AC01-01 | \> 1.5 h | 76-100% | Figma | Replace:'Green Checkmark' with 'Orange Triangle' on top of the battery with the appropriate charge level (see designs for each battery level in Figma)'Health is Normal' with 'Issue Detected'Everything else remains the same. | Replace either 'Green Checkmark' or 'Orange Triangle' with 'Grey Triangle' on top of the battery with the appropriate charge level.Replace either 'Health is Normal' or 'Issues detected' with 'Health data unavailable.'Everything else remains the same.Figma | AC01-02 | 51-75% | Figma | AC01-03 | 26-50% | Figma | AC01-04 | 4-25% | Figma | AC01-05 | \<=1.5 h | - | Figma | AC01-06 | battery is discharged (expected discharge time \< current date)* See Tech details above | Figma | AC01-07 | charging | Figma | Figma | Same logic as if collar has some battery level (see above) | AC01-08 | unknown* No telemetry has been received yet or BE returned telemetry without battery level | Disable tap on the sectionFigma |
| AC01-01 | \> 1.5 h | 76-100% | Figma | Replace:'Green Checkmark' with 'Orange Triangle' on top of the battery with the appropriate charge level (see designs for each battery level in Figma)'Health is Normal' with 'Issue Detected'Everything else remains the same. | Replace either 'Green Checkmark' or 'Orange Triangle' with 'Grey Triangle' on top of the battery with the appropriate charge level.Replace either 'Health is Normal' or 'Issues detected' with 'Health data unavailable.'Everything else remains the same.Figma |
| AC01-02 | 51-75% | Figma |
| AC01-03 | 26-50% | Figma |
| AC01-04 | 4-25% | Figma |
| AC01-05 | \<=1.5 h | - | Figma |
| AC01-06 | battery is discharged (expected discharge time \< current date)* See Tech details above | Figma |
| AC01-07 | charging | Figma | Figma | Same logic as if collar has some battery level (see above) |
| AC01-08 | unknown* No telemetry has been received yet or BE returned telemetry without battery level | Disable tap on the sectionFigma |
| AC02 | If I tap on the Battery section, then the app should open ME03-F05. Battery Details screen. |
| AC03 | If there is NO Remaining battery data in seconds, then the app should replace all time values with percentages. |
