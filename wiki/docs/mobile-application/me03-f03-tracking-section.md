---
title: "ME03-F03. Tracking section"
sidebar_label: "ME03-F03. Tracking section"
sidebar_position: 622
author: "Mariya Kolyada"
---

| Document owners | Linear/Jira ticket | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-172/[ios]-collar-details-tracking-section |
| 04 Feb 2025 draft user story is created by Galina Lonskaya |User story: As Halo app account owner, I want to access GPS Tracking info related to my collar so that I can be sure that GPS works correctly for my collar.

Acceptance Criteria:

See the possible statuses of 'Tracking' section in the table below, see Figma list with all statuses.

Table 1 - Tracking section statuses

|  | High GPS | Medium GPS | Low GPS | No GPS / No data | GPS initialization required | SGEE is outdated | UI | Figma(Source of truth) | AC01 | AC02 | AC03 | AC04 | AC05 | AC06 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Yes | No | No | No | No | No |  | Figma |
| No | Yes | No | No | No | No |  |
| No | No | Yes | No | No | No |  |
| No | No | No | Yes | No | No |  |
| Doesn't matter | Doesn't matter | Doesn't matter | Doesn't matter | Yes | Doesn't matter |  |
| Doesn't matter | Doesn't matter | Doesn't matter | Doesn't matter | No | Yes |  |The logic of the current app can be found in CollarGpsViewModel.UpdateState(...):

**Click to expand**Expand source```
public void UpdateState(CollarSummaryModel collarSummaryModel) \{ if (collarSummaryModel.Telemetry is \{ IsGpsCalibrationRequired: true \}) \{ CollarGpsStatus = CollarGpsStatus.GpsCalibrationRequired; GpsDescription = collarSummaryModel.Type == CollarType.Version4 ? _resources.InitializationRequiredVersion4 : _resources.InitializationRequiredVersion1ToVersion3Final; \} else \{ if (collarSummaryModel.DoesSupportFeature(FirmwareFeatures.Sgee)) \{ if (collarSummaryModel.IsSgeeUpToDate()) \{ GpsDescription = _resources.SatellitePositionDataActual; if (collarSummaryModel.PetInfo == null) \{ CollarGpsStatus = CollarGpsStatus.UpToDateNotAssigned; \} else \{ CollarGpsStatus = collarSummaryModel.GpsModel.ToCollarGpsStatus() switch \{ GpsStatus.NoData =\> CollarGpsStatus.NoData, GpsStatus.NoGps =\> CollarGpsStatus.NoSignal, GpsStatus.Low =\> CollarGpsStatus.Low, GpsStatus.Medium =\> CollarGpsStatus.Medium, GpsStatus.High =\> CollarGpsStatus.High, _ =\> CollarGpsStatus.NoData \}; \} \} else \{ GpsDescription = _resources.SatellitePositionDataMissed; CollarGpsStatus = CollarGpsStatus.SgeeDataMissed; \} \} else \{ GpsDescription = _resources.SatellitePositionDataNotSupport; CollarGpsStatus = CollarGpsStatus.SgeeNotSupported; \} \} \}
```


