---
title: "[Postponed] ME03-US50. Mobile UI for GPS calibration: instruction how to calibrate"
sidebar_label: "[Postponed] ME03-US50. Mobile UI for GPS calibration: instruction how to calibrate"
sidebar_position: 131
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED, Wording on some Zeplin screens may need updating (esp. Success/Fail screens). |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| HALO-6540 - MOB: ME03-US50. Mobile UI for GPS calibration: instruction how to calibrate (Part 1) Closed |
| 20 Oct 2021 Maria Shikareva [X] The story is marked as "Postponed". |# User story

\> As an account owner, I want to get the instructions how to calibrate GPS sensor and track the calibration process statuses so that I will be able to perform the GPS sensor calibration on my own. AS IS: at the moment (3/30/21), the calibration can be done only via direct interaction with the collar and there is no mobile UI for tracking of the statuses, but there is an article in Help Center with the instructions: https://support.halocollar.com/hc/en-us/articles/1500003312461-How-to-custom-configure-my-collar-s-indoor-outdoor-GPS-sensor.

User story Acceptance criteria 'Collars' screen updates 'Step 0 (Custom-Configure Your Halo’s GPS Sensor)' screen Pair the app with the collar via Bluetooth before viewing calibration steps Bluetooth connection error handling when pairing the app with the collar 'Step 1 - Step 7' : general requirements Reconnecting with collar during the whole calibration process: Step 1 - Step 7 'Step 1 - Step 7' screens: specific requirements 'Step 8' screen (successful calibration) 'Сanceled calibration' screen 'Failed Calibration' screen Implementation Notes

# Acceptance criteria

| AC | Description | iOS IU design / implementation status | Android IU design / implementation status | 'Collars' screen updates | 'Step 0 (Custom-Configure Your Halo’s GPS Sensor)' screen | Pair the app with the collar via Bluetooth before viewing calibration steps |  | Bluetooth connection error handling when pairing the app with the collar | 'Step 1 - Step 7' : general requirements | Reconnecting with collar during the whole calibration process: Step 1 - Step 7 | 'Step 1 - Step 7' screens: specific requirements | 'Step 8' screen (successful calibration) | 'Сanceled calibration' screen | 'Failed Calibration' screen |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Note: See the calibration process description on FW side in ME03-US49. FW: Collar calibration process (phase 1). |
| ME03-US50-AC01 | 'Outdoor/Indoor Settings' tile should be added to 'Collars' screen, see pic 1.Note: see initial requirements for 'Collars' screen in ME03-F01. Collars list. | Pic 1 Collars list with 'Outdoor/Indoor Settings' tile, see Zeplin | The same screen as for iOS |
| ME03-US50-AC02 | 'Outdoor/Indoor Settings' tile should consist of: 'Outdoor/Indoor Settings' title + 'Right arrow' icon |
| ME03-US50-AC03 | If I tap on 'Outdoor/Indoor Settings' tile on 'Collars' screen, then:'Step 0' screen should be opened. | Pic 2 Step 0, see Zeplin | The same screen as for iOS |
| ME03-US50-AC04 | 'Step 0' screen should consist of: 'Close' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Start' button, see the details in 'Pair the app with the collar via Bluetooth before viewing calibration steps' section (ME03-US50-AC08 and further)'Default Settings' button (will be implemented within the separate story, see the details in ME03-US52. Mobile UI for GPS calibration: 'Default Settings' screen) |
| ME03-US50-AC05 | If I tap on 'Close' button on 'Step 0' screen, then:'Collars' screen should be opened with the expanded collar card that was shown before the opening of 'Step 0' screen. | - | - |
| ME03-US50-AC06,07,08 | - | - | - |
| ME03-US50-AC09 | If I tap on 'Start' button on 'Step 0' screen, then:the process of pairing via Bluetooth with the required collar should be started;'Step 0' screen should be disabled and the overall spinner should be shown, see pic 4. | Pic 4 Step 0 + Spinner, see Zeplin | The same screen as for iOS |
| ME03-US50-AC10 | Precondition: 'Step 0' screen should be opened and Bluetooth pairing with the collar has been initiated.If Bluetooth connection is set up successfully and the calibration process isn't in progress at the moment, then:'Step 1' should be opened, see the details in ME03-US50-AC35. | - | - |
| ME03-US50-AC11 | Precondition: 'Step 0' screen should be opened and Bluetooth pairing with the collar has been initiated.If Bluetooth connection is set up successfully and the calibration process is in progress at the moment, then:the screen corresponded to the current state of the calibration process should be displayed. | - | - |
| Precondition for all AC within this section: 'Step 0' screen should be opened and Bluetooth connection with collar was initiated. |
| ME03-US50-AC12 | If Bluetooth isn't enabled on the smartphone during the pairing, then:M181 Bluetooth is disabled (calibration process) error should be displayed.Note: after the tap on OK button, the popup should be closed and connection process should be stopped. | - | - |
| ME03-US50-AC13 | If the pairing with the required collar isn't successful due the collar isn't found, then:the M70. No answer from the collar error should be displayed.Note: after the tap on OK button, the popup should be closed and connection process should be stopped. | - | - |
| ME03-US50-AC14 | The timeout for pairing with the collar should be 10 sec. | - | - |
| ME03-US50-AC15 | In case the app fails to unlock the collar with Rolling Codes on 'Step 0'screen, then: Bluetooth connection attempt should be stopped;the M124 Security error for provisioning message should be displayed.Note: after the tap on OK button, the popup should be closed and connection process should be stopped. | - | - |
| ME03-US50-AC16 | If the pairing with the required collar isn't successful due to the communication error, then:M126 Communication error message should be displayed. | - | - |
| ME03-US50-AC17 | If the smartphone is offline when the app connects with the collar and there are no RCs cached, then:Bluetooth connection attempt should be stopped; M125 Connection error message should be displayed. Note: after the tap on 'Cancel' button, the popup should be closed and connection process should be stopped; after the tap on 'Try Again' button, the connection process should be initiated again | - | - |
| ME03-US50-AC18 | Each calibration step (1-7) consists of:'Cancel' buttonImageTitleBody'Step' label + \<number of the currently displayed step\> + 'of 8' labelProgress bar (optional: presented not on all screens)Label with tip (optional: presented not on all screens)Countdown timer with \<MM:SS\> (optional: presented not on all screens) | See pic 6-12 and the specific requirements below. | - |
| ME03-US50-AC19 | The smartphone should keep Bluetooth connection with the collar during Step 1 - Step 7. | - | - |
| ME03-US50-AC20 | The following data should be updated via Bluetooth on Steps 1-7 each 1 sec:current calibration state;time on countdown timer;amount of the gathered data displayed on the progress bar. | - | - |
| ME03-US50-AC21 | If the new calibration state is received, then:the step corresponded to the calibration state should be opened. | - | - |
| ME03-US50-AC22 | If Bluetooth connection is lost, then:the app should initiate the process of automatic reconnection with the collar, see the further description of 'Reconnecting with collar' functionality in 'Reconnecting with collar...' section. | - | - |
| ME03-US50-AC23 | Note: the 'Cancel Calibration' command will be described separately in ME03-US53. Mobile UI for GPS calibration: cancel 'calibration process' via Bluetooth. Within 'ME03-US50', after the tap on 'Cancel' button, no 'cancel' command will be sent. If I tap on 'Cancel' button on any of 'Step 1-7' screens, then:data update performed 1 sec should be paused, see the details in ME03-US50-AC20;'Close Custom-Configuration Instruction' popup should be shown:Title: Close Custom-Configuration Instruction Body: At the moment you can just close the custom-configuration instruction. In order to cancel custom-configuration process, you need to press ON button three times within 2 sec. In case of successful cancelation, the сollar will make a beep signal and 1 sec vibration. Logo LED/GPS LED/Speaker should be reverted to normal behavior.Button: OK | Pic 5 | - |
| ME03-US50-AC24 | Precondition: 'Close Custom-Configuration Instruction' popup is shown. If I tap on 'OK' button, then: the smartphone breaks Bluetooth connection with the collar;'Collars' list should be opened with the expanded collar card that was shown before the opening of 'Outdoor/Indoor' settings. | - | - |
| ACs below are valid for any of the following screens: Step 1 - Step 7 |
| ME03-US50-AC25 | In case the Bluetooth connection with the collar is lost, then: the app should start the process of automatic reconnection with the collar. | - | - |
| ME03-US50-AC26 | If after 3 seconds of automatic reconnection attempts the Bluetooth connection with the collar is not restored, then:the app should display "Reconnecting with collar" bar. | - | - |
| ME03-US50-AC27 | In case Bluetooth connection with the collar is restored, then: "Reconnecting with collar" bar should be hidden. | - | - |
| ME03-US50-AC28 | I can close 'Reconnecting With Collar' bar. See the details in ME14-US14. Close "Reconnecting with collar" bar | - | - |
| ME03-US50-AC29 | In case the app fails to unlock the collar with Rolling Codes, then: the app should stop the automatic reconnection attempts;the app should hide the "Reconnecting with collar" panel;M124 Security error for provisioning error message should be displayed. | - | - |
| ME03-US50-AC30 | If the smartphone is offline when the app reconnecting with the collar and there are no RCs cached, then:the app should stop the automatic reconnection attempts, the app should hide the "Reconnecting with collar" panel, M125 Connection error should be displayed. | - | - |
| ME03-US50-AC31 | If Bluetooth is turned off on the smartphone during the calibration process, then:M181 Bluetooth is disabled (calibration process) error should be displayed. | - | - |
| ME03-US50-AC32 | If the reconnection with the required collar isn't successful due to the communication error, then:M126 Communication error message should be displayed. | - | - |
| ME03-US50-AC33 | Precondition: M125 Connection error is opened.If I tap on the 'Cancel' button, then:the error message should be closed;'Step 0' screen should be opened.Note: If the user taps 'Try again' button the app sends another request to the Halo BE. | - | - |
| ME03-US50-AC34 | Precondition: M124 Security error for provisioning, M181 Bluetooth is disabled (calibration process), M126 Communication error error message is opened.If I tap on 'OK' button, then:the error message should be closed;'Step 0' screen should be opened. | - | - |
| Note for QA. Android behavior: restore Bluetooth connection after app restoring and the screen unlocking. iOS behavior: there is no disconnection |
| ME03-US50-AC35 | 'Step 1' screen should consists of:'Cancel' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Step' label + \<number of the currently displayed step\> + 'of 8' label | Pic 6 Step 1, see Zeplin | The same screen as for iOS |
| ME03-US50-AC36 | 'Step 2' screen should consists of:'Cancel' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Step' label + \<number of the currently displayed step\> + 'of 8' label'Waiting for unplugging' labelCountdown timer with \<MM:SS\> | Pic 7 Step 2, see Zeplin |
| ME03-US50-AC37 | 'Step 3' screen should consists of:'Cancel' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Step' label + \<number of the currently displayed step\> + 'of 8' labelProgress bar displayed amount of gathered data while moving 'Amount of gathered data while moving' labelCountdown timer with \<MM:SS\> | Pic 8 Step 3, see Zeplin |
| ME03-US50-AC38 | 'Step 4' screen should consists of:'Cancel' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Step' label + \<number of the currently displayed step\> + 'of 8' label'Waiting for pressing ON button' labelCountdown timer with \<MM:SS\> | Pic 9 Step 4, see Zeplin |
| ME03-US50-AC39 | 'Step 5' screen should consists of:'Cancel' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Step' label + \<number of the currently displayed step\> + 'of 8' labelProgress bar displayed amount of gathered data while moving'Amount of gathered data while moving' labelCountdown timer with \<MM:SS\> | Pic 10 Step 5, see Zeplin |
| ME03-US50-AC40 | 'Step 6' screen should consists of:'Cancel' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Step' label + \<number of the currently displayed step\> + 'of 8' label'Waiting for pressing ON button' labelCountdown timer with \<MM:SS\> | Pic 11 Step 6, see Zeplin |
| ME03-US50-AC41 | 'Step 7' screen should consists of:'Cancel' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Step' label + \<number of the currently displayed step\> + 'of 8' labelProgress bar displayed amount of gathered data while moving'Amount of gathered data while moving' labelCountdown timer with \<MM:SS\> | Pic 12 Step 7, see Zeplin |
| ME03-US50-AC42 | 'Step 8' screen should consist of:'Close' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Finish' button | Pic 13 Step 8, see Zeplin | The same screen as for iOS |
| ME03-US50-AC43 | If I tap on 'Finish' button on 'Step 8' screen, then:the same behavior as described in ME03-US50-AC24 should be applied. | - | - |
| ME03-US50-AC44 | If I tap on 'Close' button 'Step 8' screen, then:the same behavior as described in ME03-US50-AC24 should be applied. | - | - |
| ME03-US50-AC45 | If the calibration is canceled by me manually (using the ON button on collar), then:'Canceled Calibration' screen should be displayed. | Pic 14 'Canceled calibration' screen, see Zeplin | The same screen as for iOS |
| ME03-US50-AC46 | 'Canceled Calibration' screen should consist of:'Close' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team |
| ME03-US50-AC47 | If I tap on 'Close' button on 'Canceled Calibration' screen, then:the same behavior as described in ME03-US50-AC05 should be applied. | - | - |
| ME03-US50-AC48 | If I tap on 'Start' button on 'Canceled Calibration' screen, then:the same behavior as described in ME03-US50-AC09 should be applied. | - | - |
| ME03-US50-AC49 | If the time dedicated to the calibration step is over, but the step isn't completed, then:'Failed Calibration' screen should be displayed. | Pic 15 'Failed calibration' screen, see Zeplin | The same screen as for iOS |
| ME03-US50-AC50 | 'Failed Calibration' screen should consist of:'Close' buttonImageTitle TBD text with Halo teamBody TBD text with Halo team'Start' button |
| ME03-US50-AC51 | If I tap on 'Close' button on 'Failed Calibration' screen, then:the same behavior as described in ME03-US50-AC05 should be applied. | - | - |
| ME03-US50-AC52 | If I tap on 'Start' button on 'Failed Calibration' screen, then:the same behavior as described in ME03-US50-AC09 should be applied. | - | - |
| ME03-US50-AC53 | If any of the screens above doesn't fit all content, then:the screens should be scrollable.Note: which part of the screen is scrollable should be clarified with UI/UX designer during dev phase. | - | - |# Implementation Notes

| IN | Description |
|---|---|
| ME03-US50-IN01 | For more details, see the email: HALO | 3/16/2021 Tech Call Meeting Notes |
| ME03-US50-IN02 | See the table with indoor/outdoor calibration states prepared by Michael: Calibration process instructions.xlsx. Should be revisited during the dev phase. |
