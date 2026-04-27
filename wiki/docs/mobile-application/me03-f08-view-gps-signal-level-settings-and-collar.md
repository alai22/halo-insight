---
title: "ME03-F08. View GPS signal level settings and Collar Orientation"
sidebar_label: "ME03-F08. View GPS signal level settings and Collar Orientation"
sidebar_position: 631
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| BASELINED as of 17 Jan 2025 |
| Galina Lonskaya Pavel Leonenko |
| Click here to expand... HALO-12505 - MOB: ME03-US85. Add Collar: Calibration Closed HALO-13569 - MOB: Fix punctuation on the 'GPS Light Signals' screen Closed HALO-13581 - MOB: Fix UI for buttons on collar calibration flow Closed HALO-13849 - [MOB+BE] Rename the 'calibration' to the 'initialization' Closed HALO-13869 - MOB: Update map centering logic for GPS calibration flow Closed |
| Click here to expand...14 Oct 2022 Maria Shikareva [X] Baselined ME03-US85. Add Collar: GPS initialization screens, [BL] ME03-US90. Update map centering logic for GPS initialization flow05 Dec 2023 Kiryl Trafimau baselined (BL) ME03-US193. Update wording on GPS calibration screen01/17/2025 the baseline is updated by Galina Lonskaya |# User story

\> As Halo Collar account owner, I want to see the screens with explanation on how to initialize the GPS of my collar, what do the LED colors mean, to make sure the map is updated and displays the right location, so a collar is ready to use and I'm informed on important nuances of collar.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |  | Start point | ... | Final point | GPS signal strength | Priority | Centered by | Description | Collar Pin on 'GPS Level Settings' screen | AC | Condition | As is | To be |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Entry point: Settings → My Collars → Collar Details → Advanced Settings → GPS Signal Level Settings |
| ME03-F08-AC02 | If I tap on 'GPS Signal Level Settings' section and Bluetooth permission is denied, then: Android: M217 "Location and Bluetooth permission denied" message (Android) should be showniOS: M143 "Bluetooth permission denied" message should be shown. | - | - |
| ME03-F08-AC03 | If I tap on 'GPS Signal Level Settings' section and Bluetooth permission is granted, BUT Bluetooth is turned off on the device, then: M178 Disabled Bluetooth should be shown. | - | - |
| 'GPS Signal Level Settings' screen |
| ME03-F08-AC04 | If I tap on 'GPS Signal Level Settings' section and Bluetooth permission is granted and Bluetooth is turned on the phone, then:'GPS Signal Level Settings' screen should be opened with the maximized card at the bottom by default. |  |  |
| ME03-F08-AC05 | The card should have 2 states:MaximizedMinimized |  |  |
| ME03-F08-AC06 | If I tap on '?' icon, then: the following article should be opened https://www.halocollar.com/understanding-your-halo-collars-gps/. |  |  |
| ME03-F08-AC07 | The card at the bottom of the screen should consist of: 'Current GPS Signal Level' title + 'i' icon\<GPS state \> + \<GPS level value\>GPS level bar that consists of 3 parts: 'Low' label:background color for the 'low' section should be grey (=no background)'medium' (no label, just the section on the scale):background color for the 'medium' value should be magenta'High' label:background color for the 'high' label should be blue GPS signal pin: the GPS signal pin should indicate the dynamic change of the GPS level'Collar Antenna Orientation' described within different US'Edit GPS signal level settings' button Note: High/Medium/Low ranges are provided by BE side |  |  |
| ME03-F08-AC08 | Precondition:User clicks on the 'Learn more about GPS levels' link in 'Initializing GPS' screenThe app opens 'GPS level explanation' screen that consists of the following elements:high GPS:a blue icon;'GPS level high' title;'Your collar will provide escalating preventions to keep your dog from leaving and return whistles to bring them back when they stop or turn around.' text.medium GPS:a magenta icon;'GPS level medium' title;'Your collar will use return whistles to keep your dog from leaving and get your dog to return.' text;low GPS or no GPS:a white icon;'Low GPS or no GPS' title;'Your collar will automatically pause fence feedback and the location and time displayed on my map will be from the last high or medium GPS position.' text'Close' button |  |  |
| ME03-F08-AC09 | Current GPS signal strength level should be displayed in grey parenthesis besides high/med/low/no text |  |  |
| ME03-F08-AC10 | If GPS level is No or No data - no value should be shown, otherwise (High/Medium/Low) - show GPS value |  |  |
| ME03-F08-AC11 | The following values should be applied within the barStart point...Final pointGPS signal strength502000, and \>2000 | 50 | 2000, and \>2000 |  |  |
| 50 | 2000, and \>2000 |
| ME03-F08-AC12 | The mobile app should display all GPS values rounded to 10. |  |  |
| ME03-F08-AC13 | Current GPS signal strength level should be updated each 1 sec. |  |  |
| ME03-F08-AC14 | The blue dot on the 'GPS signal' pin should have a pulsing animation. |  |  |
| ME03-F08-AC15 | Entry point:No GPS signal is receivedThe app should:Show 'No GPS' grey textDisable the GPS level barHide Signal level pin. |  |  |
| Bluetooth issue handling while being on 'GPS Signal Level Settings' screen |
| ME03-F08-AC16 | If I turn off Bluetooth on the smartphone while being on 'GPS Signal Level Settings' with map), then: the following screen state should be shown:Close button 'GPS Level Settings' screen title '?' icon 'Bluetooth Is Disabled' title 'Please turn Bluetooth ON in your device settings to continue. Bluetooth is needed to pair your Halo collar and connect it to the app.' |  |  |
| ME03-F08-AC17 | Entry point:a user open 'GPS Level Settings screen'Bluetooth pairing with the collar has not been set up OR Bluetooth pairing with the collar has been initiated AND the data has been received from the collar every 1 second BUT then BLE connection was lostThe app should:Display 'Reconnecting With Collar' toast.Show 'Please move closer to your collar' textDisable the GPS level barHide Signal level pin.Note 1: If I leave the screen with map background then I will no longer see the re-connection panel.Note 2: There should be delay of 3 seconds for showing the re-connection blue bar after user navigates to the 'GPS Signal Level Settings' screen with map background. |  |  |
| ME03-F08-AC18 | The re-connection panel should be displayed on the 'GPS Signal Level Settings' screen with map background until the collar is turned on and nearby (within Bluetooth range). | - | - |
| Map Background on 'GPS Signal Level Settings' screen |
| ME03-F08-AC19 | User should be able to pan in/out the map background (see My Map). | - |  |
| ME03-F08-AC20 | Default map zoom level 18. |  |  |
| ME03-F08-AC21 | When a user goes to 'GPS Signal Level Settings' screen, then the app should display map background centered according to the prioritization rules described below:The app should center the map on the collar always (not only on the first showing of the map) based on the logic below.I.e. if afterwards collar changes position on the map, the app should automatically center the map by its new position.PriorityCentered byDescription1 location of CollarWhen collar location is available, then my map should be centered by collar location. When it's not, but user location data is available, then map background will be centered by user location. 2location of user's phoneWhen collar's location is not available, but user location data is available, then map background will be centered by user location. 3default location (see BR-11 Map view settings.)When neither collar's location not user's location is available, then I see the map centered by the default location. | 1 | location of Collar | When collar location is available, then my map should be centered by collar location. When it's not, but user location data is available, then map background will be centered by user location. | 2 | location of user's phone | When collar's location is not available, but user location data is available, then map background will be centered by user location. | 3 | default location (see BR-11 Map view settings.) | When neither collar's location not user's location is available, then I see the map centered by the default location. |  |  |
| 1 | location of Collar | When collar location is available, then my map should be centered by collar location. When it's not, but user location data is available, then map background will be centered by user location. |
| 2 | location of user's phone | When collar's location is not available, but user location data is available, then map background will be centered by user location. |
| 3 | default location (see BR-11 Map view settings.) | When neither collar's location not user's location is available, then I see the map centered by the default location. |
| ME03-F08-AC22 | The app should display a 'Compass' button when a user adjusts the map angle. | - | - |
| ME03-F08-AC23 | When a user taps on the 'Compass' button, the app should:re-orient the screen and revert the map view back to its original direction;hide the 'Compass' icon. | - | - |
| ME03-F08-AC24 | "Center on the collar's location" button should be added to the map on the 'GPS Signal Level Settings' screen. | - | - |
| ME03-F08-AC25 | Precondition: 'GPS Signal Level Settings' screen is displayed; my map area is centered on the collar's location.If a user drags the map, then the app should:stop centering the map on the collar's pin;display the "Center on the collar's pin" button | - | - |
| ME03-F08-AC26 | Precondition: 'GPS Signal Level Settings' screen is displayed; my map area isn't centered on the collar's location.If a user taps on the "Center on the collar's pin" button, then the app should:center the map on the collar's pin;hide the "Center on the collar's pin" button. | - | - |
| ME03-F08-AC27 | The app should display the "Center on the collar's pin" button above the "Compass" button (in case they both are displayed together).Note: as of 9/21/22 on iOS buttons are replacing with animation; on Android each button has its own place. | - | - |
| ACConditionAs isTo beME03-F08-AC28Hasn't been connected to GPS beforeNo Pet Pin at allAnimated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma)ME03-F08-AC29Attempt to connect over BLEAnimated 'connectivity attempt' icon (see ME05-US59-AC18)ME03-F08-AC30Connected via BLE + GPS is low or no GPS'Feedback paused' icon (see ME07-F09-AC107)'BLE active' icon (see Figma)ME03-F08-AC31Connected via BLE + GPS medium or highNo icons over Pet Pin | ME03-F08-AC28 | Hasn't been connected to GPS before | No Pet Pin at all | Animated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma) | ME03-F08-AC29 | Attempt to connect over BLE | Animated 'connectivity attempt' icon (see ME05-US59-AC18) | ME03-F08-AC30 | Connected via BLE + GPS is low or no GPS | 'Feedback paused' icon (see ME07-F09-AC107) | 'BLE active' icon (see Figma) | ME03-F08-AC31 | Connected via BLE + GPS medium or high | No icons over Pet Pin |
| ME03-F08-AC28 | Hasn't been connected to GPS before | No Pet Pin at all | Animated 'BLE connection attempt' icon: simple animation (e.g., blinking or transitioning in/out) to highlight the reconnection state (see Figma) |
| ME03-F08-AC29 | Attempt to connect over BLE | Animated 'connectivity attempt' icon (see ME05-US59-AC18) |
| ME03-F08-AC30 | Connected via BLE + GPS is low or no GPS | 'Feedback paused' icon (see ME07-F09-AC107) | 'BLE active' icon (see Figma) |
| ME03-F08-AC31 | Connected via BLE + GPS medium or high | No icons over Pet Pin |
| ME03-F08-AC32 | If the collar isn't assigned to a pet, then:the Halo Ring of pin color should be grey. |  |  |
| ME03-F08-AC33 | If the user adjusts GPS signal level settings and saves on the 'Edit GPS signal level settings' screen, then: the adjusted settings should apply to the GPS Signal Level Settings' screen |  |  |
