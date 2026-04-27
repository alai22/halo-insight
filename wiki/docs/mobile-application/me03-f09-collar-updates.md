---
title: "ME03-F09. Collar Updates"
sidebar_label: "ME03-F09. Collar Updates"
sidebar_position: 632
last_modified: "Oct 28, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Test cases status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 28 Oct 2022 |
| Valeryia Chyrkun [X] Maria Shikareva [X] Timofey Burak [X] Nikita Krisko Anastasia Burlo [X] Dmitry Kravchuk Dmitriy Morozov [X] Alexei Zhukov |
| Click here to expand... HALO-12778 - MOB [NT]: Finalize solution for 'FW update' flow Closed HALO-12560 - MOB [+BE]: ME21-US07. Add FW update screens to 'Add Collar' flow Closed HALO-13311 - FW: Change 20% to 5% to start downloading FW update/ SGEE data Resolved HALO-13313 - FW: Battery LED should blink red + green during downloading and applying FW update Closed HALO-13802 - BE [+FW]: Add 'Battery LED blinking red and green' FirmwareFeature Closed HALO-13803 - FW [+BE]: Battery LED blinking red+green. MQTT: FirmwareFeature Ready for QA HALO-14049 - MOB: Collar offline is displayed for a few seconds Closed HALO-14053 - MOB: User is blocked on the 'Update Collar' screen when 'Done' button is disabled and there is no 'Skip' button Closed HALO-14189 - ME21-US38. Changes for 'Automatic Halo Collar Updates' screen logic (telemetry = null) Closed HALO-14191 - MOB+BE: [NI] ME21-US40. Changes for 'Automatic Halo Collar Updates' screen logic ('Skip' button after 5 minutes) Closed |
| Click here to expand...28 Oct 2022 Maria Shikareva [X] Baselined [NI] ME21-US07. Add FW update screens to 'Add Collar' flow, [BL] ME21-US38. Changes for 'Automatic Halo Collar Updates' screen logic (telemetry = null), [BL] ME21-US40. Changes for 'Automatic Halo Collar Updates' screen logic ('Skip' button after 5 minutes). |# Contents

Assumptions User story Acceptance criteria Error handling Google Analytics Implementation notes Technical details SGEE update algorithm: Firmware update algorithm: How to detect if collar is offline? How to understand that FW is up-to-date? What does different Firmware update statuses mean (with examples)?

# Assumptions

1. This story will be released as a next step for 'Add collar' flow after Wi-Fi setup.
2. An 'info' icon will be added to all screens within a separate story.
3. The collar starts FW updates/ SGEE downloading immediately as soon as all conditions are met (the collar starts charging when it has**at least 5%**of battery charged AND the collar is on charger).
4. Turning the collar OFF during the flow will be described within a separate story (see[NI] ME03-US12. Onboarding: general requirements for exceptional and alternative cases).
5. The collar will send FW update statuses to BE:
  1. if the collar is online, then immediately;
  2. if the collar is offline, then right after the collar becomes online → it will send all missed statuses (the collar has message queue).

6. If the FW package is deleted:
  1. during downloading phase - it's impossible, BE doesn't delete files at all;
  2. during applying phase - in this case TWIN won't be updated and the collar will try to download this file again.

7. The logic of receiving push-notifications when FW update is started/ completed will be described within a separate story (see[NI] ME03-US12. Onboarding: general requirements for exceptional and alternative cases).
8. There's no priority in updating FW/ downloading SGEE manifest/ downloading SGEE tar files.
9. It's OK to use "Collar Update" wording instead of "Firmware Update" → this is more clear to the users.
10. If connection is lost during FW update, the the collar waits for the same interface for 12 hours:
  1. if the connection appears using the same interface, then the collar starts FW update again;
  2. if connection doesn't appear, the the collar puts FW update to the queue to download it via any interface.

# User story

\> As a Halo app user I want to have my collar ready-to-go with updated FW and up-to-date satellite data so that to be sure that I have the latest performance improvements and the most accurate location data.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | Icon | SGEE status in the app | SGEE status from BE | GPS light meaning image | Icon | FW update status in the app | FW update status from BE | Battery light meaning image/ animation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Preconditions: a user has successfully configured Wi-FiORa user skipped configuring Wi-Fi and tapped 'Continue Without Wi-Fi' button. |
| ME03-F09-AC01 | The app should open a 'Wait for Your Collar to Update' screen with the following elements:'Collar Update' title;'Wait for Your Collar to Update' subtitle;an image;'Every time you plug your collar in to charge and it is connected to the Internet by Wi-Fi or LTE, it will automatically make sure it is updated." text;'Next' button.Question mark will be added separately: HALO-14143 - MOB: ME21-US35. Onboarding: Updates for 'Collar Update' flow Closed | Link to Zeplinhttps://miro.com/app/board/o9J_l3oJd20=/?moveToWidget=3458764530508949581&cot=14 | Zeplin |
| ME03-F09-AC02 | When a user taps the 'Next' button, then the app should:check whether FW update and satellite data are up-to-date;display the 'Automatic Halo Collar Updates' screen with the following UI elements:'Collar Update' title;'Back' button;'Automatic Halo Collar Updates' subtitle;'Automatic Collar Updates usually occur at night and take several minutes to complete. Once the Satellite Position Data and Collar Updates are 'Up-To-Date', tap 'Done'.' text;Warning icon + 'Please leave your Halo plugged in while it is updating.''Satellite Position Data' section:'Satellite Position Data' subtitle;an icon;\<SGEE update status\>GPS light meaning image depending on the status (see ME03-F09-AC05 below)'Collar Update' section: 'Collar Update Status' subtitlean icon\<current FW update status\>Battery light meaning animation depending on the status (see ME03-F09-AC06 below).'Done' button (see ME03-F09-AC08 below for more details).Note: the app should be able to get the updated data from BE as soon as possible so that to show relevant statuses to a user. | Link to Zeplin | Link to Zeplin |
| ME03-F09-AC03 | When a user taps 'Back' button, then the app should open the previous 'Wait for Your Collar to Update' screen. | - | - |
| ME03-F09-AC04 | The app should display the following SGEE status and an icon:IconSGEE status in the appSGEE status from BEGPS light meaning imageWaiting for update...UnknownOutdatedIncompletean image with pink LEDInitializing your Halo Collar. Please wait.telemetry = nullUp-to-dateUpToDatean image with no LED blinkingCollar offlineany status AND the telemetry is outdated (more than 5 min)Note 1: case - the collar is offline (i.e. telemetry is outdated) but according to the latest data SGEE data is up-to-date. Agreed with Timofey that in this case we will show a 'Collar offline' status because there's a possibility that SGEE data is already outdated (e.g. the telemetry was sent far ago and status 'up-to-date' wasn't updated accordingly). Note 2: if the collar is added to the account, Wi-Fi is set up, but the collar is new (i.e. has never sent telemetry), then for a few seconds a user can see that the collar is offline though in fact the collar is online but a new telemetry hasn't been sent yet. So that to handle this case we need an 'Initializing... ' status. |  | Waiting for update... | UnknownOutdatedIncomplete | an image with pink LED | Initializing your Halo Collar. Please wait. | telemetry = null |  | Up-to-date | UpToDate | an image with no LED blinking |  | Collar offline | any status AND the telemetry is outdated (more than 5 min) | - | - |
|  | Waiting for update... | UnknownOutdatedIncomplete | an image with pink LED |
| Initializing your Halo Collar. Please wait. | telemetry = null |
|  | Up-to-date | UpToDate | an image with no LED blinking |
|  | Collar offline | any status AND the telemetry is outdated (more than 5 min) |
| ME03-F09-AC05 | The app should display the following FW update status and an icon:IconFW update status in the appFW update status from BEBattery light meaning image/ animationFW version \< 01.00.00FW version ≥ 01.01.00FW version supports 'green+red' LED blinkingFW version doesn't support 'green+red' LED blinkingUpdate starting momentarily...Unknownan image with green LEDNote: it was agreed with Timofey Burak [X] that we'll use animation in all cases but sometimes it will consist of 1 frame. .json animationsUpdating. Please be patient while your collar updates. If possible, please do not use your collar.DownloadingUpdating. Please be patient while your collar updates. If possible, please do not use your collar. Verifyinganimation: red + green blinkinganimation: red blinkingUpdating...ApplyingInitializing your Halo Collar. Please wait.telemetry = nullan image with green LED(for further spec purposes we'll consider these statuses as 'negative')Update paused. Your collar has a low battery. Make sure your collar is plugged in and charging.DownloadDelayedLowBatteryan image with green LEDUpdate paused. Please plug in your collar to charge to complete the update.ApplyDelayedNotChargingan image with red LEDUpdate paused. Please plug in your collar to charge to complete the update. DownloadDelayedNotOnChargerUpdate failed. Please try moving your collar and charger into a better Wi-Fi location.Update failed. Please try moving your collar and charger into a better Internet connection location.DownloadFailedan image with green LEDUpdate failed. Your update will restart automatically. If possible, please do not use your collar.VerifyFailedUpdate failed. Your update will restart automatically. If possible, please do not use your collar. ApplyFailedCollar offline. Please plug in your collar to charge in Wi-Fi range. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB.Collar offline. Please plug in your collar to charge in Wi-Fi or LTE range. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB.DownloadNotStartedORany status AND the telemetry is outdated (more than 5 min)an image with no LED blinkingUpdate paused. Wi-Fi connection not detected. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB.Update paused. Internet connection not detected. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB.DownloadDelayedIncompatibleNetworkan image with green LEDUp-to-dateSee an implementation note below.animation: green blinkingNote 1: the statuses and the logic for their displaying should be the same as on the Collars list (incl. FW features).Note 2: even if the collar is offline (i.e. telemetry is outdated) but according to the latest data current FW version is up-to-date (the same as expected), the app will display "Up-To-Date' status → the same behavior as on the Collars list.Note 3: the logic for '5 minutes' outdated telemetry should be the same as for displaying 'Outdated' status on the Pet card. | FW version \< 01.00.00 | FW version ≥ 01.01.00 | FW version supports 'green+red' LED blinking | FW version doesn't support 'green+red' LED blinking |  | Update starting momentarily... | Unknown | an image with green LEDNote: it was agreed with Timofey Burak [X] that we'll use animation in all cases but sometimes it will consist of 1 frame. .json animations | Updating. Please be patient while your collar updates. If possible, please do not use your collar. | Downloading | Updating. Please be patient while your collar updates. If possible, please do not use your collar. | Verifying | animation: red + green blinking | animation: red blinking | Updating... | Applying | Initializing your Halo Collar. Please wait. | telemetry = null | an image with green LED | (for further spec purposes we'll consider these statuses as 'negative') | Update paused. Your collar has a low battery. Make sure your collar is plugged in and charging. | DownloadDelayedLowBattery | an image with green LED | Update paused. Please plug in your collar to charge to complete the update. | ApplyDelayedNotCharging | an image with red LED | Update paused. Please plug in your collar to charge to complete the update. | DownloadDelayedNotOnCharger | Update failed. Please try moving your collar and charger into a better Wi-Fi location. | Update failed. Please try moving your collar and charger into a better Internet connection location. | DownloadFailed | an image with green LED | Update failed. Your update will restart automatically. If possible, please do not use your collar. | VerifyFailed | Update failed. Your update will restart automatically. If possible, please do not use your collar. | ApplyFailed | Collar offline. Please plug in your collar to charge in Wi-Fi range. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | Collar offline. Please plug in your collar to charge in Wi-Fi or LTE range. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | DownloadNotStartedORany status AND the telemetry is outdated (more than 5 min) | an image with no LED blinking | Update paused. Wi-Fi connection not detected. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | Update paused. Internet connection not detected. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | DownloadDelayedIncompatibleNetwork | an image with green LED |  | Up-to-date | See an implementation note below. | animation: green blinking |
| FW version \< 01.00.00 | FW version ≥ 01.01.00 | FW version supports 'green+red' LED blinking | FW version doesn't support 'green+red' LED blinking |
|  | Update starting momentarily... | Unknown | an image with green LEDNote: it was agreed with Timofey Burak [X] that we'll use animation in all cases but sometimes it will consist of 1 frame. .json animations |
| Updating. Please be patient while your collar updates. If possible, please do not use your collar. | Downloading |
| Updating. Please be patient while your collar updates. If possible, please do not use your collar. | Verifying | animation: red + green blinking | animation: red blinking |
| Updating... | Applying |
| Initializing your Halo Collar. Please wait. | telemetry = null | an image with green LED |
| (for further spec purposes we'll consider these statuses as 'negative') | Update paused. Your collar has a low battery. Make sure your collar is plugged in and charging. | DownloadDelayedLowBattery | an image with green LED |
| Update paused. Please plug in your collar to charge to complete the update. | ApplyDelayedNotCharging | an image with red LED |
| Update paused. Please plug in your collar to charge to complete the update. | DownloadDelayedNotOnCharger |
| Update failed. Please try moving your collar and charger into a better Wi-Fi location. | Update failed. Please try moving your collar and charger into a better Internet connection location. | DownloadFailed | an image with green LED |
| Update failed. Your update will restart automatically. If possible, please do not use your collar. | VerifyFailed |
| Update failed. Your update will restart automatically. If possible, please do not use your collar. | ApplyFailed |
| Collar offline. Please plug in your collar to charge in Wi-Fi range. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | Collar offline. Please plug in your collar to charge in Wi-Fi or LTE range. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | DownloadNotStartedORany status AND the telemetry is outdated (more than 5 min) | an image with no LED blinking |
| Update paused. Wi-Fi connection not detected. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | Update paused. Internet connection not detected. If you don't have access to Wi-Fi, you can connect your collar to your phone's Wi-Fi hotspot or update by USB. | DownloadDelayedIncompatibleNetwork | an image with green LED |
|  | Up-to-date | See an implementation note below. | animation: green blinking |
| ME03-F09-AC06 | The app should not display anything in \<SGEE update status\> and \<current FW update status\> until it gets this data from BE (only a spinner will be visible for both sections).Note: as of 06 Jul 2022 the collar doesn't send info to the app directly about the progress of FW update, but there's a task for future: HALO-12792 - MOB: Update GAP/GATT protocol about Firmware Update Progress Open . | - | - |
| ME03-F09-AC07 | 'Done' should be:always visibleANDenabled only after FW and SGEE are updated. | - | - |
| ME03-F09-AC08 | When the user taps 'Done' button, then the app:should open the pop-up M260After user clicks 'Ok' the app should close the 'Automatic Halo Collar Updates' screen;open the next step as described in ME03-US85. Add Collar: GPS calibration screens. | - | - |
| ME03-F09-AC09 | Precondition: any negative status for Collar Update is displayed (see ME03-F09-AC06 - negative statuses are statuses with a grey triangle icon).The app should:show enabled 'Skip' button.Note 1: if the connection is lost on the collar during downloading FW update → the app will be able to know this info only if the collar has 2 connection types (Wi-Fi and LTE) and for now one of them is lost (using which FW update is downloading). If there was only 1 connection type available and now it's lost, then we'll never know 100% exactly that connection is lost, the collar just stops reporting, therefore the app will show a 'Skip' button after telemetry becomes outdated.Note 2: if the connection with BE is lost, the app will show a 'Skip' button after telemetry becomes outdated. | Link to Zeplin | Link to Zeplin |
| ME03-F09-AC10 | The app should have a countdown starting from 5 minutes after opening 'Automatic Halo Collar Updates' screen (not display it on UI).Note: for more details see ME03-F09-IN01, ME03-F09-IN02 below. |  |  |
| ME03-F09-AC11 | Precondition: a countdown is started.If the user leaves the screen and opens it again, the countdown will restart from the beginning.Note: it was agreed that this is the easiest solution from implementation perspective.Note 2: if a user brings the app to the background and then to the foreground (i.e. without closing this screen), the countdown will continue. |  |  |
| ME03-F09-AC12 | '5 minutes' should be a configurable value. |  |  |
| ME03-F09-AC13 | After 5 minutes a 'Skip' button should always be on the screen even if the status changed from negative to positive.Note: sometimes SGEE updates/ FW updates are too slow for some reasons (e.g. issues with some Internet providers, time lag for initializing a collar, etc.) and the user can be blocked on the 'Automatic Halo Collar Updates' screen without any option to leave the screen ('Skip' button appears only in case of any 'negative' status but the user can be blocked in case of any status). So to avoid this it was decided to have this 5 minutes timer. |  |  |
| ME03-F09-AC14 | If the app showed 'Skip' button earlier than 5 min (e.g. after a 'negative' status), and after that a status changed to any other, a countdown should not restart.ExampleA user entered the screen → a timer startedIn 1 minute download failed → the app displayed a 'Skip' buttonIn 0.5 minute download restarted → the app hides a 'Skip' buttonIn 3.5 minute timer ends → the app displays a 'Skip' button.In 5 minutes the status is changed to 'Up-to-date' → the app still displays a 'Skip' button. |  |  |
| ME03-F09-AC15 | When a user taps on a 'Skip' button, then the app should display a M259 Continue Without Update pop-up. | Link to Zeplin | - |
| ME03-F09-AC16 | Precondition: M259 Continue Without Update is opened.When the user taps on ' Resume Update' button, the app should:close the pop-up;keep the previous screen opened. | - | - |
| ME03-F09-AC17 | Precondition: M259 Continue Without Update is opened.When the user taps on 'Update Collar Later' button, the app should:close the pop-up and the screen;open the next step as described in ME03-US85. Add Collar: GPS calibration screens. | - | - |
| ME03-F09-AC18 | The content on all 3 screens should scrollable with a button/(s) always at the bottom. | - | - |
| Error handling |
| ME03-F09-AC19 | Connection and communication errors on first entering the "Your Halo Collar Update" screen should be handled according to ME14-F01 Unified errors handling, where "Collar Updates data is" wording should be used instead of \<items\>. | - | - |
| ME03-F09-AC20 | The app should not display M125 Connection error. | - | - |
| Google Analytics |
| ME03-F09-AC21 | The app should track:the following events:how much time a user spends on the FW update flow (starting from entering 'Wait for Your Collar to Update' screen and ending when the user taps 'Done' button or skips the flow by tapping 'Update Collar Later' button in the pop-up);whether the user completed the flow (tapped 'Done' button) or left the flow before completing (tapped 'Update Collar Later' button);the platform. | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME03-F09-IN01 | The best option to implement this is to use a timestamp of entering the screen.Other discussed optionsTrack time on appearing/ disappearing. Cons: if a user opens another screen above this one, the timer will stop. If a user brings the app to background, the timer will also stop.Show timer on appearing/ disappearing AND not stop timer when a user brings the app to background → there can be some issues that the app works in background, we don't notify anyone about that.There can be native iOS/ Android timers - agree to double check later and make as am improvement if required. |
| ME03-F09-IN02 | If a user changes the date/ time while timer is counting down, then on bringing to foreground the app will check this and show 'Skip' button MAXIMUM after 5 minutes (or even earlier). |# Technical details

#### SGEE update algorithm:

1. Collar periodically checks if Backend has newer version of SGEE files (period is defined in configuration);
2. If Backend has newer version of SGEE files collar automatically downloads and applies them;
3. Collar includes SGEE update status in each telemetry message (if supported);

#### Firmware update algorithm:

1. Collar's firmware is up to date;
2. New firmware is assigned to collar through admin panel;
3. Collar acknowledges that new firmware is available (through Twin) and starts update process. This process is basically endless until firmware is not up-to-date again. Throughout the update process collar reports status as it changes (in real-time);
4. When collar's firmware is up-to-date again process is considered completed, until new firmware is assigned to the collar;

#### How to detect if collar is offline?

Collar cannot update neither Firmware nor SGEE if it's not connected to internet. The most reliable way to detect if collar is not connected to internet that we currently have is to analyse timestamp of the latest telemetry message: for instance, if collar haven't sent telemetry for 5m (the longest expected period between two telemetry messages, LTE connection and "sleep" mode).

#### How to understand that FW is up-to-date?

If collar.firmwareUpdate field is null - it means that there's no new firmware version available for this collar. Even if collar is offline currently, the absence of the firmwareUpdate is reliable way to detect that collar's firmware is up-to-date.

#### What does different Firmware update statuses mean (with examples)?

| No. | Status | Description | Module | Collar S/N | Timestamp | Log |
|---|---|---|---|---|---|---|
| 0 | Unknown | Default value on collar side. Theoretically, should not be obtained ever.Note: in PROD database exists only one record of this status, on a collar with old version | - | 21h1272562rt | 2021-09-17 02:17:02 UTC | https://prnt.sc/9ehelNz0kYXy |
| 1 | DownloadDelayedIncompatibleNetwork | Collar status, means that collar doesn't have wi-fi connection to start firmware update.Note: supposed to be used in old FW only, before 'update over LTE' support | - | 21h2421274rt | 2022-07-02 10:40:44 UTC | https://prnt.sc/eIQmuobppuXE |
| 2 | DownloadDelayedLowBattery | Collar status, means that FW download cannot be started due to low battery. | - | 20h1440520rt | 2022-07-13 13:30:59 UTC | https://prnt.sc/w7sTy1achD6m |
| 3 | Downloading | Collar status, means that FW is currently being downloaded. | - |  |  |  |
| collar | 19h1250388rt | 2020-08-31 14:50:24 UTC | https://prnt.sc/01SXL_MqnHq0 |
| 4 | DownloadFailed | Collar status, means last FW update failed to be downloaded, process will be automatically restarted later. | - | 21h2380055rt | 2022-06-16 04:54:54 UTC | https://prnt.sc/OPFZjRdpExuQ |
| 5 | Verifying | Collar status, means that FW is downloaded and is currently being verified.Note: if specified, status is applied to a specific module. otherwise status is applied to the whole update process. | - |  |  |  |
| collar |  |  |  |
| wifi | 21h1301440rt | 2022-02-19 04:55:02 UTC | https://prnt.sc/pcrtZvBOoRlf |
| gps | 21h2491563rt | 2022-05-30 04:56:39 UTC | https://prnt.sc/XkMLo4KnbpfT |
| 6 | VerifyFailed | Collar status, means last FW update has failed due to verification error, process will be automatically restarted later.Note: seems like for this status module is always specified, showing which module exactly failed verification. | collar | 20h1481087rt | 2022-03-03 13:00:25 UTC | https://prnt.sc/1N4vBae8EssO |
| wifi | 21h2500501rt | 2022-05-03 16:07:37 UTC | https://prnt.sc/DdzNoyaKoXJ1 |
| gps | 22h2195553rt | 2022-07-21 23:14:51 UTC | https://prnt.sc/1hJ5TfV7f7ah |
| 7 | ApplyDelayedNotCharging | Collar status, means that FW is downloaded but cannot be applied due to collar not being on charge | - | 22h2090064rt | 2022-07-08 01:58:47 UTC | https://prnt.sc/HOEnpnsUZqbe |
| 8 | Applying | Collar status, means that FW is downloaded and is currently being applied.Note: if specified, status is applied to a specific module. otherwise status is applied to the whole update process. | - |  |  |  |
| collar |  |  |  |
| wifi | 21h1300553rt | 2021-12-29 07:50:24 UTC | https://prnt.sc/jxzBMdaMQu0q |
| gps | 22h2021832rt | 2022-05-25 01:45:03 UTC | https://prnt.sc/kblpqCkikadU |
| 9 | ApplyFailed | Collar status, means last FW update has failed to be applied ('module' value will indicate which part of FW failed to be applied), process will be automatically restarted later | - |  |  |  |
| collar | 21h1350690rt | 2022-02-06 01:01:25 UTC | https://prnt.sc/gmac1UMTKOT7 |
| wifi | 20h1330275rt | 2020-10-05 12:55:11 UTC | https://prnt.sc/EfuS3BJUGqbq |
| gps | 20h1360684rt | 2020-10-17 04:05:21 UTC | https://prnt.sc/QQsuqJWghgFK |
| 10 | DownloadDelayedNotOnCharger | Collar status, means that FW cannot be downloaded due to collar not being on charge | - | 20h1480903rt | 2022-07-26 23:20:43 UTC | https://prnt.sc/izxTXMW8i9An |
| 100 | Applied | Backend status, means that the latest FW update is completed successfully. Should not be obtainable on mobile side |  |  |  |  |
| 101 | DownloadNotStarted | Backend status, default value for new FW until actual collar status is obtained. Also, a fallback value on mobile side (any unknown value will be interpreted as download not being started) |  |  |  |  |
