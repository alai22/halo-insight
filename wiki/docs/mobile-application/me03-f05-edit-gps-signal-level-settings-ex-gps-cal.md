---
title: "ME03-F05. Edit GPS signal level settings (ex. GPS calibration)"
sidebar_label: "ME03-F05. Edit GPS signal level settings (ex. GPS calibration)"
sidebar_position: 130
last_modified: "Jan 16, 2025"
author: "Galina Lonskaya"
---

| Document status | Test cases status | Document owners | Links to Jira tickets | Changes history |
|---|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 30 May 2022 |
| Maria Shikareva [X] Timofey Burak [X] Eugene Paseka Zakhar Makarevich Kirill Akulich [X] Vladislav Mejidau [X] |
| Click here to expand... HALO-6756 - MOB: Open 'Outdoor/Indoor Custom Configuration' article (Help Center) from the Collar expanded card Closed HALO-6760 - BE: Open 'Outdoor/Indoor Custom Configuration' article (Help Center) from the Collar expanded card Closed HALO-7880 - FW: Manual GPS calibration (improved logic for Indoor/Outdoor determination) Closed HALO-8000 - BE: [NT] MQTT contract: manual GPS calibration (outdoor/indoor threshold adjustment) Closed HALO-8002 - [RI] Manual indoor/ outdoor configuration Closed HALO-8007 - MOB: [NT] Investigation: manual GPS calibration Closed HALO-8266 - BE [+MOB, BE]: Implement GPS metric configuration for: Use 'Slider' in order to adjust indoor/outdoor level (manual calibration) Closed HALO-9085 - BE [+FW]: Add Manual GPS calibration FirmwareFeature Closed HALO-10575 - MOB +BE: Manual GPS calibration. Complete BE and integrate Closed HALO-11382 - MOB: Changes for manual GPS configuration (change indoor/ outdoor naming) Closed HALO-14004 - MOB: Changes a wording for manual GPS configuration Closed |
| Click here to expand...29 Apr 2022 Maria Shikareva [X] Baselined [BL] ME03-US64. Use slider for outdoor/indoor threshold adjustment, [BL] ME03-US73. UI changes for manual indoor/outdoor configuration, [BL] ME03-US76. BLE 'real-time' indication (indoor/ outdoor calibration), [BL] ME03-US78. Add a warning pop-up when the user drags pin a lot, [BL] ME03-US55. Open 'Indoor/Outdoor configuration' article from the expanded collar card.30 May 2022 Maria Shikareva [X] Baselined [BL] ME03-US77. Changes for manual GPS configuration (change indoor/ outdoor naming).14 Oct 2022 Maria Shikareva [X] Baselined [NI] ME03-US77. Change of wording for manual GPS configuration. |# Contents

General description User story Discussed options Use cases Use case ME03-F05-UC01 "Mobile app calculates GPS status on its own" Acceptance criteria Bluetooth connection error handling when pairing the app with the collar Bar with current GPS level Low/ high GPS pins and thresholds Current GPS pin and status 'Return to previous' buttons Revert to System Default Cancel button Save GPS Signal Level settings Reconnecting with collar during GPS calibration process Implementation Notes

# General description

As of 30 Jul 2021 current GPS calibration doesn't work precisely at the moment. The users notice that the app show indoors when the collar is outdoors and vice versa. The end users leave these comments on Markets and ask about it in Solvvy. Also there's an email "HALO: Refunds statistics" from Sep 22, 2021 from which it's clear that inaccurate GPS and poor feedback/ fence performance are among of the main reasons for return (for refund) and warranty (for replacement): 17.6% for GPS (accuracy) category and 12.4% for Feedback/ Fence Performance.

Update as of 05 Oct 2021 Auto GPS calibration logic doesn't improve precision of the location determination.

So it was decided to give the users UI for manual indoor/outdoor adjustment for each user to be able to set the best outdoor/indoor threshold positioning on their own.

Update as of 23 Mar 2022: after a tech call it was decided to change implementation logic a bit and read data from the collar/ send data to the collar directly via BLE instead of using BE (see more details in Collar - Manual GPS calibration).

As of 30 May 2022: the wording for indoor/ outdoor was changed within [Not implemented] ME07-US70. Rename indoor/ outdoor statuses.

# User story

\> As a Halo app account owner I want to be able to adjust GPS signal levels thresholds so that the GPS status of my collar will be identified more precisely by the collar.

# Discussed options

Click here to expand...| Option 1Without "Test on collar" | Option 2With "Test on collar" (using temp) |
|---|---|
| User opens "GPS Signal Level Settings" screenBE send current threshold to mob appMob app set up Bluetooth connection and scan "Current GPS" via BluetoothUser adjust thresholdsUser taps on Save button and thresholds should be sent to collar via BEWhen mobile app gets the limits from BE and they are the same as received from collar via BluetoothCons:Main issue - probably the user should wait too long for new GPS status.A spinner should be displayed till limits should be applied. | User opens "GPS Signal Level Settings" screenBE send current threshold to mob appMob app set up Bluetooth connection; scan "Current GPS" via Bluetooth and get thresholdsUser adjust thresholdsUser taps on Test on Collar button and thresholds should be sent via BluetoothCollar should sent back correspondent GPS statusUser taps on Save button and only then thresholds will be sent on BE and synced with the collar.Note 1: FW can send back not only GPS status but also thresholds.Note 2: We should not notify the user if this specific characteristic.Cons:We should recommend the user not to move in order to receive reliable GPS status. |# Use cases

## Use case ME03-F05-UC01 "Mobile app calculates GPS status on its own"

1. User taps on " Settings" option.
2. Mobapp opens an "GPS Signal Level Settings" screen;
3. Mob app sets up Bluetooth connection.
4. Mob app reads current GPS level settings via BLE.
5. Mob app is constantly scanning current GPS level.
6. User adjust thresholds.
7. Mob app calculates and displays correspondent status on the basis of the thresholds.
8. User taps on "Done" button and thresholds should be sent to the collar via BLE directly.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status | Bluetooth connection error handling when pairing the app with the collar | Slider UI | Start point | ... | Final point | GPS signal strength | Low/ high GPS pins and thresholds | Current GPS pin and status | Revert to System Default | Cancel button | Save GPS Signal Level settings | Reconnecting with collar during GPS calibration process |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Entry point: the collar's FW supports manual GPS calibration feature;a user taps on the 'GPS Signal Level Settings' button on the "Advanced Settings" screen. |
| ME03-F05-AC01 | This functionality should be available for any subscription plan. | - | - |
| ME03-F05-AC02 | The 'GPS Signal Level Settings' screen should have the following elements:"Cancel" button"GPS Signal Level Settings" title\<In order to override Halo's default settings, use the manual configuration tool below. When moving into/out of your house, expect the Halo GPS readings can take up to 15 seconds to adjust. Make sure the collar is ON your dog.\> textNote: we need a note about 15 sec to highlight to the user that when transitioning between low/ high GPS levels, the value does not change instantly, but - rather - over 10-15 seconds. It depend on the collar behavior (i.e. the collar has a median filter that don't allow numbers to fluctuate a lot).a "collar" icon;'Please read the article to understand the risks of overriding the calculated thresholds." text."The article" should be a clickable link (see ME03-F05-AC03 below).If the app knows that the user has previously opened the article, then the actions described in ME03-F05-AC06 should be performed. | Pic ME03-F05-P01 "GPS Signal Level Settings" screen with a spinnerLink to Zeplin | Link to Zeplin |
| ME03-F05-AC03 | When the user taps on "the article" link, then the app should open Help Center article in the default mobile browser. | - | - |
| ME03-F05-AC04 | The link to the article: https://support.halocollar.com/hc/en-us/articles/4423813191959. | - | - |
| ME03-F05-AC05 | The links to the articles should be stored on BE side. | - | - |
| ME03-F05-AC06 | When the user returns back to the app after reading the article, the app should:start the process of pairing via Bluetooth with the required collar;display another state of "GPS Signal Level Settings" screen (see UI design):'I've read the article and understand the risks of overriding the default settings.' text."The article" should be a clickable link (see ME03-F05-AC03).a spinner. | Pic ME03-F05-P02 "GPS Signal Level Settings" screen with a spinnerLink to Zeplin | Link to Zeplin |
| ME03-F05-AC07 | Info that the user has already opened the article should be saved on the mobile side (the mobile app should delete this info when account is changed). | - | - |
| ME03-F05-AC08 | Precondition: Bluetooth pairing with the collar has been initiated AND the data is received from the collar every 1 second.If Bluetooth connection is set up successfully, then the app should:hide the spinner;read current GPS Signal Level settings and formula ratiosBL \>= 17 + 0.66BUBL \<= BU - 50Note: these ration should also be sent by the collar via BLE so that to avoid issues with old FWs if these values will be changed.display the updated "Manual Calibration" section;GPS level bar"min" labelbar with deducted GPS level displayed in grey;"low GPS" pin with the level in numbers displayed;"high GPS" pin with the level in numbers displayed;background colors for each part of slider:white (no background) → for GPS level less than left pin;magenta → for GPS level higher than left pin but less than the right pin;blue → for GPS level higher than right pin.GPS signal pin:'GPS signal' label'current:' label with current GPS Strength."max" label;legend:low GPS:a white icon;'Fence feedback will be paused' text;low GPS icon with 1 bar;'GPS level low' text;medium GPS:a magenta icon;'Fence feedback: return whistle only' text;medium GPS icon with 2 bars;'GPS level medium' text;high GPS:a blue icon;'Fence feedback will be active' text;high GPS icon with 3 bars;'GPS level high' text."Return to previous (\<min level in numbers\>)" button displayed in the white section of legend.Disabled by default.'Return to previous' should be visible only if the corresponding pin value differs from the previous one."Return to previous (\<max level in numbers\>)" button displayed in the blue section of legend.Disabled by default.'Return to previous' should be visible only if the corresponding pin value differs from the previous one."Revert to Halo Defaults" button. | Pic ME03-F05-P03 "GPS Signal Level Settings" screen with initial valuesLink to Zeplin | Link to Zeplin |
| ME03-F05-AC09 | The blue dot on the 'GPS signal' pin should have a pulsing animation. |  |  |
| ME03-F05-AC10 | Precondition: the data isn't received from the collar 2 seconds and more.If Bluetooth connection is set up successfully, then the app should display the following updates in the "Manual Calibration" section:GPS signal pin:'GPS Signal' label'\<X\>s ago:' label with latest GPS Strength received. |  |  |
| ME03-F05-AC11 | \<X\> should display the number of seconds when the latest data about GPS signal was received from the collar.Note: this will be displayed until the current data is received OR "Reconnecting with collar" bar is shown. |  |  |
| ME03-F05-AC12 | If all content doesn't fit the screen, the app should display a scroll for the whole screen except the header (Cancel + GPS Signal Level Settings title). |  |  |
| ME03-F05-AC13 | The timeout for pairing with the collar should be 10 sec. | - | - |
| ME03-F05-AC14 | If Bluetooth isn't enabled on the smartphone during the pairing OR the permission was denied, then the system should display M181 Bluetooth is disabled (calibration process) error message. | - | - |
| ME03-F05-AC15 | If the pairing with the required collar isn't successful due the collar isn't found OR the app didn't receive data during standard timeout (i.e. 10 sec), then the system should: display M70. No answer from the collar error message;not display a slider at all. | - | - |
| ME03-F05-AC16 | In case the app fails to unlock the collar with Rolling Codes, then the system should display M124 Security error for provisioning error message. | - | - |
| ME03-F05-AC17 | Precondition: one of the error messages described in ME03-F05-AC14 — ME03-F05-AC16 is displayed.When the user taps on "OK" button, then the system should:close the pop-up;stop the connection process;close the "GPS Signal Level Setting" screen;open the "Advanced Settings" screen. | - | - |
| Bar with current GPS level |
| ME03-F05-AC18 | Current GPS signal strength level should be displayed in grey within "GPS level" bar.Note 1: сurrent GPS level should be taken via Bluetooth from the collar. | - | - |
| ME03-F05-AC19 | The following values should be applied within the bar:Slider UIStart point...Final pointGPS signal strength502000, and \>2000 | 50 | 2000, and \>2000 | - | - |
| 50 | 2000, and \>2000 |
| ME03-F05-AC20 | The mobile app should display all GPS values rounded to 10.Note: this will be done on the mobile side. | - | - |
| ME03-F05-AC21 | Current GPS signal strength level should be updated each 1 sec. | - | - |
| ME03-F05-AC22 | By default currently used low/ high GPS level thresholds should be displayed.Note 1: they should be taken from the collar directly via BLE. | - | - |
| ME03-F05-AC23 | The user should be able to adjust low/ high GPS level threshold placement manually by dragging the pin itself OR a bubble with numbers in order to change its positioning. | - | - |
| ME03-F05-AC24 | When the pin gets between two strokes, then:the value of the pin should not change;the pin should be automatically moved to the nearest stroke. |  |  |
| ME03-F05-AC25 | When the user moves low/ high GPS level pin, then the UI should change in the following way:the pin with previous values should become disabled and not draggable but visible;the previous values should not be displayed on the disabled pin;an enabled pin with new values should be displayed;the corresponding "Return to previous" button should become enabled (depends on which pin is dragged);"Done" button should become visible and enabled. | Pic ME03-F05-P04 "GPS Signal Level Settings" screen with changed valuesLink to Zeplin | Link to Zeplin |
| ME03-F05-AC26 | Precondition: the collar didn't send current thresholds for some reason.In this case:the app should display GPS levels pins on default values:low GPS- 470;high GPS - 580.when the user starts moving them, then no disabled pins should stay on the bar;"Done" button is always visible;"Return to previous" buttons should stay disabled. | - | - |
| ME03-F05-AC27 | MIN gap between "low GPS" and "high GPS" threshold should be 50. | - | - |
| ME03-F05-AC28 | "50" value should be configurable on BE. | - | - |
| ME03-F05-AC29 | MAX gap between "low GPS" and "high GPS" threshold should not be specified. | - | - |
| ME03-F05-AC30 | The app should not allow to create a gap more than MIN.If the gap becomes 50 and the user moves the low GPS pin to the right next to the high GPS, then the high GPS pin should be accordingly moved to the right with the MIN gap 50.If the high GPS pin reaches max, then the app should forbid to drag low GPS pin to the right less then MIN. | - | - |
| ME03-F05-AC31 | Precondition:GPS Signal Level Settings screen with active slider is displayedANDthe user drags low/ high GPS pins.The user should not be allowed to drag pins in a way when the difference between low and high GPS pins exceeds the maximum calculated by the existing formula: BL\>= 17 + 0.66BU.Note: this AC is required to avoid the situation when limits become negative so that low GPS/ high GPS values are calculated incorrectly. | - | - |
| ME03-F05-AC32 | When the user tries to drag pin more than allowed, the app should display a warning pop-up: M235 Low and High Thresholds.Note: we need this pop-up to prevent the user from moving the pin further without understanding how this will affect another pin. |  |  |
| ME03-F05-AC33 | The app should display M235 Low and High Thresholds only once: i.e. when the user configures the values for the very first time. Note: the app should remember showing this pop-up. |  |  |
| ME03-F05-AC34 | If low GPS and high GPS pins overlaps each other, the latest moved pin should be displayed above the other. | - | - |
| ME03-F05-AC35 | Low/ high GPS pins can overlap the "min" or "max" labels. | - | - |
| ME03-F05-AC36 | The app should not allow to drag the current GPS pin. |  |  |
| ME03-F05-AC37 | \<GPS status\> icon should be dynamic and change in real-time on the bases of chosen thresholds. | - | - |
| 'Return to previous' buttons |
| ME03-F05-AC38 | By default the buttons should be disabled. | - | - |
| ME03-F05-AC39 | After user drags and releases the pin, then:the corresponding button should become enabled if the chosen value differs from the initial oneANDthe button should become disabled if the values are equal. | - | - |
| ME03-F05-AC40 | When the user taps on the button, then:the current corresponding pin should be "automatically" moved to the previously saved value;the button should become disabled. | - | - |
| ME03-F05-AC41 | When the user taps on the "Revert to System Default" button, then the app should:apply default (factory) thresholds:470 for low GPS;580 for high GPS. | - | - |
| ME03-F05-AC42 | "Default" thresholds should be configurable on BE side. | - | - |
| ME03-F05-AC43 | When the user taps on the "Cancel" button and some changes were made, then the app should display M204 Cancel GPS calibration. | - | - |
| ME03-F05-AC44 | When the user taps on the "Cancel" button and no changes were made OR the user taps on the "Discard" button on M204, then the app should:break Bluetooth connection with the collar;close the "GPS Signal Level Settings" screen;open the "Advanced settings" screen with no changes saved (i.e. the previously saved settings should be applied). | - | - |
| ME03-F05-AC45 | When the user taps on the "No, continue editing" button on M204, then the app should:close the pop-up;keeps the 'GPS Signal Level Settings' screen opened. | - | - |
| ME03-F05-AC46 | When the user taps on the "Done" button, then the system should:display a spinner over the whole screen;send new thresholds to the collar via BLE, see ME03-F05-IN01close the "GPS Signal Level Settings" screen;break Bluetooth connection with the collar;open the "Advanced settings" screen with the updated info about synchronization status (see "Advanced Settings" screen section below). | - | - |
| ME03-F05-AC47 | Precondition: new thresholds are sent to the collar.If the collar cannot save the values OR the collar doesn't respond, then the mobile app should display the following message: M225. Failed to send data.Note: standard time-out for 5 seconds should be used here. | - | - |
| ME03-F05-AC48 | In case the Bluetooth connection with the collar is lost, then: the app should start the process of automatic reconnection with the collar. | - | - |
| ME03-F05-AC49 | If after 3 seconds of automatic reconnection attempts the Bluetooth connection with the collar is not restored, then the app should display:"Reconnecting with collar" bar;a spinner should be displayed over a "Manual Calibration" section as described in ME03-F05-AC06. | - | - |
| ME03-F05-AC50 | In case Bluetooth connection with the collar is restored, then the system should:hide a "Reconnecting with collar" bar;display a "Manual Calibration" section a described in ME03-F05-AC08. | - | - |
| ME03-F05-AC51 | The user should be able to close 'Reconnecting With Collar' bar (for more details see ME14-US14. Close "Reconnecting with collar" bar). | - | - |
| ME03-F05-AC52 | If any Bluetooth connection error happens, then the app should:hide the "Reconnecting with collar" panel;perform actions as described in ME03-F05-AC13 – ME03-F05-AC17. |  |  |
| QA NotesNote for QA. Android behavior: restore Bluetooth connection after app restoring and the screen unlocking. iOS behavior: there is no disconnection |# Implementation Notes

See Tech notes: ME03-F05. Use slider for outdoor/indoor threshold adjustment.

| IN | Description |
|---|---|
| ME03-F05-IN01 | Note: sending should be performed via BLE. |
| ME03-F05-IN02 | Mobile app should pull BE every 15 sec on the "Advanced settings" screen (as discussed with Pavel Leonenko on the MOB refinement, 27 Oct 2021 ) |
| ME03-F05-IN03 | The app should track:the following events:a user enters "GPS Signal Level Settings" screen;a user successfully saves new settings by tapping "Done" button.the platform. |
| ME03-F05-IN04 | These events should be sent to Google Analytics. |
