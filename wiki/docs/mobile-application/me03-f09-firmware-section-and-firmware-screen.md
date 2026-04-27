---
title: "ME03-F09. 'Firmware' section and 'Firmware' screen"
sidebar_label: "ME03-F09. 'Firmware' section and 'Firmware' screen"
sidebar_position: 483
author: "Galina Lonskaya"
---

| Document owners | Linear/Jira ticket | History of changes |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-170/[ios]-collar-details-fw-updates-section |
| 04 Feb 2025 draft user story is created by Galina Lonskaya |User story: As Halo app account owner, I want to access FW information related to my collar so that I can ensure that the collar has up-to-date FW.

Tech details: Firmware update data can be obtained in the FirmwareUpdate field using GET /collar/my and GET /collar/\{id\} requests. If this field is null, there are no updates and the firmware version is up to date (up-to-date status).The model contains:

- Information about the firmware to which the collar is being updated -`Firmware`field
- Update status -`Update.Status`field

You can find the current logic here: CollarDetailsViewModel.UpdateStatusToString()

Acceptance Criteria:

| AC | Description | AC01 | AC02 |
|---|---|---|---|
| FW section can have different states depending on collar FW status, see 'Figma link on 'FW section' UI' column in Table ME03-F01 Statuses of the FW update that should be shown in the app. |
| Tap on FW section should open 'Firmware' screen, see 'Figma link on 'FW details' screen UI' column in Table ME03-F01 Statuses of the FW update that should be shown in the app. |#### Table ME03-F01 Statuses of the FW update that should be shown in the app.

| AC | Description | Figma link on 'FW section' UI | Figma link on 'FW details' screen UI | AC03 | AC04 | AC05 | AC06 | AC07 | AC08 | AC09 | AC10 | AC11 | AC12 | AC13 | AC14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Downloading not started | Waiting to begin download. Please plug in your collar to charge in Wi-Fi or LTE range. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | FigmaHere and in the next ACs, the user should open the following link https://support.halocollar.com/hc/en-us/articles/360048638273-How-to-Update-the-Firmware-on-My-Halo-CollarSupport.GpsCalibrationArticleUrl from GET /configuration | Figma |
| Downloading paused, no Wi-Fi | Update paused. Internet connection not detected. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | Figma | Figma |
| Downloading paused, low battery | Update paused. Your collar has a low battery. Make sure your collar is plugged in and charging. | Figma | Figma |
| Downloading paused, not charging | Update paused. Please plug in your collar to charge to complete the update. | Figma | Figma |
| Downloading | Updating. Please be patient while your collar updates. If possible, please do not use your collar. | Figma | Figma |
| Downloading failed | Update failed. Please try moving your collar and charger into a better Internet connection location. | Figma | Figma |
| Verifying | Updating. Please be patient while your collar updates. If possible, please do not use your collar. | Figma | Figma |
| Verifying failed | Update failed. Your update will restart automatically. If possible, please do not use your collar. | Figma | Figma |
| Applying paused, not charging | Update paused. Please plug in your collar to charge to complete the update. | Figma | Figma |
| Applying | Updating... | Figma | Figma |
| Applying failed | Update failed. Your update will restart automatically. If possible, please do not use your collar. | Figma | Figma |
| Up-to-date | Up-to-date | Figma | Figma |
