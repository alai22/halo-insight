---
title: "[BL] ME03-US48. [MOB] Change text of FW update statuses in collar details"
sidebar_label: "[BL] ME03-US48. [MOB] Change text of FW update statuses in collar details"
sidebar_position: 119
author: "Nicolay Gavrilov"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Nicolay Gavrilov |
| HALO-5529 - ME03-US48. [MOB] Change text of FW update statuses in collar details Closed |
| 07 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As a user I want the FW update statuses to be more clear because now I don't know what actions I should take on my firmware updates.

# Acceptance criteria

| AC | Description | iOS impl-n | Android impl-n | Current FW update status text | New FW update status text |
|---|---|---|---|---|---|
| ME04-US48-AC01 | The FW update statuses that are shown in FW update status section in collar details on the 'Collars list' screen should be updated as follows:Current FW update status textNew FW update status textNew status (unexpected status), Unknown status-Downloading not startedCollar is offline. Charge collar in Wi-Fi range. If needed, connect collar to phone hot-spot. Downloading paused, no Wi-FiDownloading paused, needs Wi-Fi connection. If needed, connect collar to phone hot-spot.Downloading paused, low batteryDownloading paused, low battery. Make sure collar is charging.Downloading paused, not chargingDownloading paused, not charging. Plug collar into charger.DownloadingDownloading. Please be patient while firmware file downloads. If possible, avoid using collar.Downloading failedDownloading failed. Consider moving collar and charger into better Wi-Fi location. VerifyingVerification in progress. This will take a few seconds. Verifying failedVerification failed. File will re-download automatically. If possible, avoid using collar.Applying paused, not chargingUpdate paused, not charging. Please plug collar in to complete upgrade. ApplyingFirmware update in progress. This may take several minutes. Do not unplug collar while red LED is blinking. Applying failedFirmware update failed. Upgrade will re-start automatically. If possible, avoid using collar. | New status (unexpected status), Unknown status | - | Downloading not started | Collar is offline. Charge collar in Wi-Fi range. If needed, connect collar to phone hot-spot. | Downloading paused, no Wi-Fi | Downloading paused, needs Wi-Fi connection. If needed, connect collar to phone hot-spot. | Downloading paused, low battery | Downloading paused, low battery. Make sure collar is charging. | Downloading paused, not charging | Downloading paused, not charging. Plug collar into charger. | Downloading | Downloading. Please be patient while firmware file downloads. If possible, avoid using collar. | Downloading failed | Downloading failed. Consider moving collar and charger into better Wi-Fi location. | Verifying | Verification in progress. This will take a few seconds. | Verifying failed | Verification failed. File will re-download automatically. If possible, avoid using collar. | Applying paused, not charging | Update paused, not charging. Please plug collar in to complete upgrade. | Applying | Firmware update in progress. This may take several minutes. Do not unplug collar while red LED is blinking. | Applying failed | Firmware update failed. Upgrade will re-start automatically. If possible, avoid using collar. | IOS TO DO | ANDROID TO DO |
| New status (unexpected status), Unknown status | - |
| Downloading not started | Collar is offline. Charge collar in Wi-Fi range. If needed, connect collar to phone hot-spot. |
| Downloading paused, no Wi-Fi | Downloading paused, needs Wi-Fi connection. If needed, connect collar to phone hot-spot. |
| Downloading paused, low battery | Downloading paused, low battery. Make sure collar is charging. |
| Downloading paused, not charging | Downloading paused, not charging. Plug collar into charger. |
| Downloading | Downloading. Please be patient while firmware file downloads. If possible, avoid using collar. |
| Downloading failed | Downloading failed. Consider moving collar and charger into better Wi-Fi location. |
| Verifying | Verification in progress. This will take a few seconds. |
| Verifying failed | Verification failed. File will re-download automatically. If possible, avoid using collar. |
| Applying paused, not charging | Update paused, not charging. Please plug collar in to complete upgrade. |
| Applying | Firmware update in progress. This may take several minutes. Do not unplug collar while red LED is blinking. |
| Applying failed | Firmware update failed. Upgrade will re-start automatically. If possible, avoid using collar. |
