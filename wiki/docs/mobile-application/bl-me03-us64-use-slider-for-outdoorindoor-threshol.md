---
title: "[BL] ME03-US64. Use slider for outdoor/indoor threshold adjustment"
sidebar_label: "[BL] ME03-US64. Use slider for outdoor/indoor threshold adjustment"
sidebar_position: 162
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Pavel Leonenko Timofey Burak [X] Eugene Paseka Zakhar Makarevich Vladislav Mejidau [X] Maria Shikareva [X] |
| Click here to expand... HALO-6576 - BE [+FE, +MOB]: Manual GPS calibration Closed HALO-7880 - FW: Manual GPS calibration (improved logic for Indoor/Outdoor determination) Closed HALO-8000 - BE: [NT] MQTT contract: manual GPS calibration (outdoor/indoor threshold adjustment) Closed HALO-8002 - [RI] Manual indoor/ outdoor configuration Closed HALO-8007 - MOB: [NT] Investigation: manual GPS calibration Closed HALO-8261 - BE [+FW] [NT] : MQTT contract update for "Use 'Slider' in order to adjust indoor/outdoor level (manual calibration)" Closed HALO-8266 - BE [+MOB, BE]: Implement GPS metric configuration for: Use 'Slider' in order to adjust indoor/outdoor level (manual calibration) Closed HALO-9085 - BE [+FW]: Add Manual GPS calibration FirmwareFeature Closed HALO-9265 - MOB [+BE+FW] [NT]: Manual GPS calibration. Prepare screens + the whole logic Closed HALO-9266 - MOB [+BE,+FW]: Manual GPS calibration. iOS controls Closed HALO-9272 - MOB [+BE+FW] [NT]: Manual GPS calibration. Prepare screens + the whole logic (Part II) Closed HALO-9273 - MOB [+BE,+FW]: Manual GPS calibration. Android + iOS controls Closed HALO-10676 - MOB: Track events for indoor/ outdoor calibration Closed Ballpark (manual outdoor/indoor adj-t): MOB: 8-13 SP (Bluetooth connection, UI, communication with BE/collar)MOB QA: 8-13 SP (Bluetooth connection, UI, communication with BE/collar)BE: Update MQTT contract 1 spBE: Implement GPS metric configuration 3-5 SPBE QA: 2 SPQA end-to-end testing: 8-13 SP |
| Click here to expand...27 Oct 2021 Maria Shikareva [X] Added Jira links.10 Feb 2022 Maria Shikareva [X] Added ME03-US64-IN04, ME03-US64-IN05: it would be smart to track these events to understand whether users use this feature and whether it's helpful for them.14 Feb 2022 Maria Shikareva [X] Added a link to the article (see ME03-US64-US07) after receiving it from Harrison (see "Halo | The article for indoor/ outdoor calibration" email from February 11, 2022).18 Mar 2022 Maria Shikareva [X] Updated ME03-US64-AS10 as discussed with Kirill Akulich [X] during implementation phase.23 Mar 2022 Maria Shikareva [X] Made some changes after tech call updates (see Collar - Manual GPS calibration for more details) (highlighted in blue).24 Mar 2022 Maria Shikareva [X] Added ME03-US64-US52 to handle cases when the collar can't save new data.29 Apr 2022 Maria Shikareva [X] Marked the story as baselined (see ME03-F05. GPS signal levels configuration (ex. GPS calibration)) |# Contents

General description User story Discussed options Use cases Use case ME03-US64-UC01 "Mobile app calculates GPS status on its own" Acceptance criteria Bluetooth connection error handling when pairing the app with the collar Bar with current GPS level Outdoor/Indoor pins and thresholds Current GPS pin and status 'Indoor/ Outdoor' buttons Revert to System Default Cancel button Save outdoor/indoor settings Reconnecting with collar during GPS calibration process Dependency on compass calibration "Advanced Settings" screen Implementation Notes

# General description

As of 30 Jul 2021 current GPS calibration doesn't work precisely at the moment. The users notice that the app show indoors when the collar is outdoors and vice versa. The end users leave these comments on Markets and ask about it in Solvvy. Also there's an email "HALO: Refunds statistics" from Sep 22, 2021 from which it's clear that inaccurate GPS and poor feedback/ fence performance are among of the main reasons for return (for refund) and warranty (for replacement): 17.6% for GPS (accuracy) category and 12.4% for Feedback/ Fence Performance.

Update as of 05 Oct 2021 Auto GPS calibration logic doesn't improve precision of the location determination.

So it was decided to give the users UI for manual indoor/outdoor adjustment for each user to be able to set the best outdoor/indoor threshold positioning on their own.

Update as of 23 Mar 2022: after a tech call it was decided to change implementation logic a bit and read data from the collar/ send data to the collar directly via BLE instead of using BE (see more details in Collar - Manual GPS calibration).

# User story

\> As a Halo app account owner I want to be able to adjust indoor/outdoor thresholds so that the GPS status of my collar will be identified more precisely by the collar.

# Discussed options

Click here to expand...| Option 1without "Test on collar" | Option 2with "Test on Collar" (using temp) |  |
|---|---|---|
| User opens "Indoor/Outdoor Settings" screenBE send current threshold to mob appMob app set up Bluetooth connection and scan "Current GPS" via BluetoothUser adjust thresholdsUser taps on Save button and thresholds should be sent to collar via BEWhen mobile app gets the limits from BE and they are the same as received from collar via BluetoothCons:Main issue - probably the user should wait too long for new GPS status.A spinner should be displayed till limits should be applied. | User opens "Indoor/Outdoor Settings" screenBE send current threshold to mob appMob app set up Bluetooth connection; scan "Current GPS" via Bluetooth and get thresholdsUser adjust thresholdsUser taps on Test on Collar button and thresholds should be sent via BluetoothCollar should sent back correspondent GPS statusUser taps on Save button and only then thresholds will be sent on BE and synced with the collar.Note 1: FW can send back not only GPS status but also thresholds.Note 2: We should not notify the user if this specific characteristic.Cons:We should recommend the user not to move in order to receive reliable GPS status. |  |# Use cases

## Use case ME03-US64-UC01 "Mobile app calculates GPS status on its own"

1. User taps on "Indoor/Outdoor Settings" option.
2. The mobile app tries to get current thresholds from BE;
3. BE sends current thresholds to mob app.
  1. if the action is not successful, then the app should not open the next screen.

4. Mobapp opens an "Indoor/Outdoor Settings" screen;
5. Mob app sets up Bluetooth connection.
6. Mob app reads current indoor/ outdoor settings via BLE.
7. Mob app is constantlyscanningcurrent GPS level.
8. User adjust thresholds.
9. Mob app calculates and displays correspondent status on the basis of the thresholds.
10. User taps on "Done" button and thresholds should be sent to the collarvia BEvia BLE directly.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status | Bluetooth connection error handling when pairing the app with the collar | Slider UI | Start point | ... | Final point | GPS signal strength | Outdoor/Indoor pins and thresholds | Current GPS pin and status | Revert to System Default | Cancel button | Save outdoor/indoor settings | Reconnecting with collar during GPS calibration process |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME03-US64-US01 | Precondition: the collar's FW doesn't support manual GPS calibration feature.The system should display the following text on the the "Advanced Settings" screen:Please update the firmware on your Halo in order to manually calibrate GPS.To display this note mobile app will use info from BE that was received on opening the "Collars list" screen. | Pic ME03-US64-P01 "Advanced Settings" screenLink to Zeplin | Link to Zeplin |
| ME03-US64-US02 | Precondition: the collar's FW doesn't support manual GPS calibration feature.If the user taps on the 'Indoor/Outdoor Settings' button on the "Advanced Settings" screen, then the 'Indoor/Outdoor configuration' article in Help Center should be opened in the default mobile browser as described in [BL] ME03-US55. Open 'Indoor/Outdoor configuration' article from the expanded collar card. | - | - |
| ME03-US64-US03 | Precondition: the collar's FW supports manual GPS calibration feature.When the user taps on the 'Indoor/Outdoor Settings' button on the "Advanced Settings" screen, then the mobile app should open 'Indoor/Outdoor Settings' screen.the mobile app tries to get thresholds from BE,where "thresholds" statement imply the "lower" and "upper" Boundaries from FW perspective (see Terminology).'Advanced Settings' screen should be disabled and the overall spinner should be shown. | - | - |
|  | The user should be able to tap the 'Indoor/Outdoor Settings' button regardless of synchronization status. |  |  |
| ME03-US64-US04 | This functionality should be available for any subscription plan. | - | - |
| ME03-US64-US05 | Precondition: the thresholds are received from BE.The 'Indoor/Outdoor Settings' screen should have the following elements:"Cancel" button"Indoor/Outdoor Settings" title\<In order to override Halo's automatically calculated Indoor/Outdoor settings, use the manual configuration tool below.\> texta "collar" icon;'Please read the article to understand the risks of overriding the calculated thresholds" text."The article" should be a clickable link (see ME03-US64-US06 below).If the app knows that the user has previously opened the article, then the actions described in ME03-US64-US09 should be performed. | Pic ME03-US64-P02 "Indoor/ Outdoor Settings" screen with a spinnerLink to Zeplin | Link to Zeplin |
| ME03-US64-US06 | When the user taps on "the article" link, then the app should open Help Center article in the default mobile browser. | - | - |
| ME03-US64-US07 | The link to the article: https://support.halocollar.com/hc/en-us/articles/4423813191959. | - | - |
| ME03-US64-US08 | The link to the article should be stored on BE side. | - | - |
| ME03-US64-US09 | When the user returns back to the app after reading the article, the app should:start the process of pairing via Bluetooth with the required collar;display another state of "Indoor/ Outdoor Settings" screen (see UI design):'I've read the article and under"The article" should be a clickable link (see ME03-US64-US06).a spinner. | Pic ME03-US64-P03 "Indoor/ Outdoor Settings" screen with a spinnerLink to Zeplin | Link to Zeplin |
| ME03-US64-US10 | Info that the user has already opened the article should be saved on the mobile side (the mobile app should delete this info when account is changed). | - | - |
| ME03-US64-US11 | Precondition: Bluetooth pairing with the collar has been initiated.If Bluetooth connection is set up successfully, then the app should:hide the spinner;read current indoor/ outdoor settings;display the updated "Manual Calibration" section;GPS level bar"min" labelbar with deducted GPS level displayed in grey;"Indoor" pin with the level in numbers displayed;"Outdoor" pin with the level in numbers displayed;current GPS pin:'Current GPS' labelcurrent GPS Strength together with expected \<GPS status\> icon."max" label; "Indoor" button with the level in numbers displayed;Disabled by default. "Outdoor" button with the level in numbers displayed;Disabled by default."Revert to Halo Defaults" button. | Pic ME03-US64-P04 "Indoor/ Outdoor Settings" screen with initial valuesLink to Zeplin | Link to Zeplin |
| ME03-US64-US12 | Precondition: the thresholds are not received from BE.If the mobile app couldn't get the values from BE (e.g. there's no Internet connection), then the mobile app:should not open the 'Indoor/Outdoor Settings' screen;should perform a Unified error handling mechanism on the "Advanced settings" screen. | - | - |
| ME03-US64-US13 | The timeout for pairing with the collar should be 10 sec. | - | - |
| ME03-US64-US14 | If Bluetooth isn't enabled on the smartphone during the pairing, then the system should display M181 Bluetooth is disabled (calibration process) error message. | - | - |
| ME03-US64-US15 | If the pairing with the required collar isn't successful due the collar isn't found, then the system should display M70. No answer from the collar error message. | - | - |
| ME03-US64-US16 | In case the app fails to unlock the collar with Rolling Codes, then the system should display M124 Security error for provisioning error message. | - | - |
| ME03-US64-US17 | If the pairing with the required collar isn't successful due to the communication error, then the system should display M126 Communication error message. | - | - |
| ME03-US64-US18 | If the smartphone is offline when the app connects with the collar and there are no RCs cached, then the system should display M125 Connection error message. | - | - |
| ME03-US64-US19 | Precondition: one of the error messages described in ME03-US64-AC14 — ME03-US64-AC18 is displayed.When the user taps on "OK" button ("Cancel" button in the M125 Connection error), then the system should:close the pop-up;stop the connection process;close the "Indoor/ Outdoor Setting" screen;open the "Advanced Settings" screen. | - | - |
| ME03-US64-US20 | Precondition: M125 Connection error is displayed.When the user taps on "Try Again" button, then the system should:close the pop-up;initiate the connection process again;display a spinner over the "Manual calibration" section. | - | - |
| Bar with current GPS level |
| ME03-US64-US21 | Current GPS signal strength level should be displayed in grey within "GPS level" bar.Note 1: сurrent GPS level should be taken via Bluetooth from the collar. | - | - |
| ME03-US64-US22 | The following values should be applied within the bar:Slider UIStart point...Final pointGPS signal strength502000, and \>2000 | 50 | 2000, and \>2000 | - | - |
| 50 | 2000, and \>2000 |
| ME03-US64-US23 | The mobile app should display all GPS values rounded to 10.Note: this will be done on the mobile side. | - | - |
| ME03-US64-US24 | Current GPS signal strength level should be updated each 1 sec. | - | - |
| ME03-US64-US25 | By default currently used Outdoor/Indoor thresholds should be displayed.Note 1: they should be taken from BE the collar directly via BLE.Note 2: if the settings on BE have changed while the user was adjusting GPS values on the "Indoor/ Outdoor Settings" screen (e.g. another user has calibrated the collar manually via the button on the collar), then after saving the new values will be saved on BE. | - | - |
| ME03-US64-US26 | The user should be able to adjust Outdoor/Indoor threshold placement manually by dragging the pin itself OR a bubble with numbers in order to change its positioning. | - | - |
| ME03-US64-US27 | When the user moves the Indoor/ Outdoor pin, then the UI should change in the following way:the pin with previous values should become disabled and not draggable but visible;the previous values should not be displayed on the disabled pin;an enabled pin with new values should be displayed;the corresponding "Indoor"/ "Outdoor" button should become enabled (depends on which pin is dragged);"Done" button should become visible and enabled. | Pic ME03-US64-P05 "Indoor/ Outdoor Settings" screen with changed valuesLink to Zeplin | Link to Zeplin |
| ME03-US64-US28 | Precondition: BE the collar didn't send current thresholds for some reason (e.g. when BE didn't get the latest Boundaries from the collar and didn't save it to database).In this case:the app should display Outdoor/Indoor pins on default values:Indoor - 250;Outdoor - 800.when the user starts moving them, then no disabled pins should stay on the bar;"Done" button is always visible;"Indoor"/ "Outdoor" buttons should stay disabled. | - | - |
| ME03-US64-US29 | MIN gap between "Indoor" and "Outdoor" threshold should be 50. | - | - |
| ME03-US64-US30 | "50" value should be configurable on BE. | - | - |
| ME03-US64-US31 | MAX gap between "Indoor" and "Outdoor" threshold should not be specified. | - | - |
| ME03-US64-US32 | The app should not allow to create a gap more than MIN.If the gap becomes 50 and the user moves the Indoor pin to the right next to the Outdoors, then the Outdoor pin should be accordingly moved to the right with the MIN gap 50.If the Outdoor pin reaches max, then the app should forbid to drag Indoor pin to the right less then MIN. | - | - |
| ME03-US64-US33 | If Indoor and Outdoor pins overlaps each other, the latest moved pin should be displayed above the other. | - | - |
| ME03-US64-US34 | The app should not allow to drag the current GPS pin. |  |  |
| ME03-US64-US35 | \<GPS status\> icon should be dynamic and change in real-time on the bases of chosen thresholds. | - | - |
| 'Indoor/ Outdoor' buttons |
| ME03-US64-US36 | By default the buttons should be disabled. | - | - |
| ME03-US64-US37 | After user drags and releases the pin, then: the corresponding button should become enabled if the chosen value differs from the initial oneANDthe button should become disabled if the values are equal. | - | - |
| ME03-US64-US38 | When the user taps on the button, then:the current corresponding pin should be "automatically" moved to the previously saved value;the button should become disabled. | - | - |
| ME03-US64-US39 | When the user taps on the "Revert to System Default" button, then the app should:apply default (factory) thresholds:250 for Indoor;800 for Outdoor. | - | - |
| ME03-US64-US40 | "Default" thresholds should be configurable on BE side. | - | - |
| ME03-US64-US41 | When the user taps on the "Cancel" button and some changes were made, then the app should display M204 Cancel GPS calibration. | - | - |
| ME03-US64-US42 | When the user taps on the "Cancel" button and no changes were made OR the user taps on the "Discard" button on M204, then the app should:break Bluetooth connection with the collar;close the "Indoor/Outdoor Settings" screen;open the "Advanced settings" screen with no changes saved (i.e. the previously saved settings should be applied). | - | - |
| ME03-US64-US43 | When the user taps on the "No, continue editing" button on M204, then the app should:close the pop-up;keeps the 'Indoor/ Outdoor Settings' screen opened. | - | - |
| ME03-US64-US44 | When the user taps on the "Done" button, then the system should:display a spinner over the whole screen;send new thresholds to the collar via BE BLE, see ME03-US64-IN01close the "Indoor/Outdoor Settings" screen;break Bluetooth connection with the collar;open the "Advanced settings" screen with the updated info about synchronization status (see "Advanced Settings" screen section below).Note: see ME03-US64-IN02 below. | - | - |
| ME03-US64-US52 | Precondition: new thresholds are sent to the collar.If the collar cannot save the values OR the collar doesn't respond, then the mobile app should display the following message: M225. Failed to send data.Title: Failed to Save DataBody: Sorry, we are currently unable to save new settings. Please try again. If issue persists, please contact Halo customer support.Button: OKNote: standard time-out for 5 seconds should be used here. | - | - |
| ME03-US64-US45 | In case the Bluetooth connection with the collar is lost, then: the app should start the process of automatic reconnection with the collar. | - | - |
| ME03-US64-US46 | If after 3 seconds of automatic reconnection attempts the Bluetooth connection with the collar is not restored, then the app should display: "Reconnecting with collar" bar;a spinner should be displayed over a "Manual Calibration" section as described in ME03-US64-US09. | - | - |
| ME03-US64-US47 | In case Bluetooth connection with the collar is restored, then the system should:hide a "Reconnecting with collar" bar;display a "Manual Calibration" section a described in ME03-US64-US11. | - | - |
| ME03-US64-US48 | The user should be able to close 'Reconnecting With Collar' bar (for more details see ME14-US14. Close "Reconnecting with collar" bar). | - | - |
| ME03-US64-US49 | If any Bluetooth connection error happens, then the app should:hide the "Reconnecting with collar" panel;perform actions as described in ME03-US64-US16 – ME03-US64-US20. |  |  |
| QA NotesNote for QA. Android behavior: restore Bluetooth connection after app restoring and the screen unlocking. iOS behavior: there is no disconnection |
| Dependency on compass calibration |
| ME03-US64-US50 | Precondition: the compass calibration was initiated.When the user taps on the "Calibrate" button on the "Advanced Settings" screen, then:the process of pairing via Bluetooth with the required collar should be started;the overall spinner should be displayed instead of the small spinner on the "Calibrate" button. | - | - |
| "Advanced Settings" screen |
| ME03-US64-US51 | The system should display a Configuration sync process status on the the "Advanced Settings" screen (see screen designs). | Pic ME03-US64-P05 "Advanced Settings" screen with synchronized statusLink to ZeplinPic ME03-US64-P06 "Advanced Settings" screen with synchronizing statusLink to Zeplin | Link to Zeplin |# Implementation Notes

See Tech notes: ME03-US64. Use slider for outdoor/indoor threshold adjustment.

| IN | Description |
|---|---|
| ME03-US64-IN01 | Note: sending should be performed via BE BLE. |
| ME03-US64-IN02 | BE should add a new info about manual GPS settings to Configuration Sync Process. |
| ME03-US64-IN03 | Mobile app should pull BE every 15 sec on the "Advanced settings" screen (as discussed with Pavel Leonenko on the MOB refinement, 27 Oct 2021 ) |
| ME03-US64-IN04 | The app should track:the following events:a user enters "Indoor/ Outdoor Settings" screen;a user successfully saves new settings by tapping "Done" button.the platform. |
| ME03-US64-IN05 | These events should be sent to Google Analytics. |
