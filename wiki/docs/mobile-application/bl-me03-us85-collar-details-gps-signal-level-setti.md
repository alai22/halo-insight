---
title: "[BL] ME03-US85. Collar Details: GPS Signal Level Settings"
sidebar_label: "[BL] ME03-US85. Collar Details: GPS Signal Level Settings"
sidebar_position: 244
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Valeryia Chyrkun [X] Timofey Burak [X] Nikita Krisko Siarhei Leushunou [X] |
| HALO-12505 - MOB: ME03-US85. Add Collar: Calibration Closed |
| Click here to expand...June 2022 story is created by Valeryia Chyrkun [X]12 Jul 2022 ME03-US85-AC12, AC13 are added by Galina Lonskaya 15 Jul 2022 ME03-US85-AC04 removed, ME03-US85-AC03 and ME03-US85-AC05 changed, ME03-US85-AC14- ME03-US85-AC15 added by Valeryia Chyrkun [X]20 Jul 2022 updated ME03-US85-AC1002 Aug 2022 Valeryia Chyrkun [X] updated the whole flow of GPS Calibration23 Aug 2022 Valeryia Chyrkun [X] added note to ME03-US85-AC15, added details to ME03-US85-AC05, updated ME03-US85-AC1924 Aug 2022 Valeryia Chyrkun [X] added note about 3-seconds delay to ME03-US85-AC0514 Oct 2022 Maria Shikareva [X] Marked the story as baselined (see ME03-F08. View GPS signal level settings and Collar Orientation).17 Jan 2025 Galina Lonskaya this US is baselined to ME03-F08. View GPS signal level settings and Collar Orientation |# G

# User story

\> As an app user, I want to see the screens with explanation on how to calibrate the GPS of my collar so a collar is ready to use and I'm informed on important nuances of collar.

# Acceptance criteria

| AC | Description | Links, design |  | Start point | ... | Final point | GPS signal strength | As is | To be | Priority | Centered by | AC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Entry point: Settings → My Collars → Collar Details → Advanced Settings → GPS Signal Level Settings |
| Entry errors |
|  | If I tap on 'GPS Signal Level Settings' section and Bluetooth permission is not granted, then: M217 (for Android) and M143(for iOS). |  |
|  | If I tap on 'GPS Signal Level Settings' section and Bluetooth permission is denied, then: M143 "Bluetooth permission denied" message should be shown. |  |
|  | If I tap on 'GPS Signal Level Settings' section and Bluetooth permission is granted, BUT Bluetooth is turned off on the device, then: M178 should be shown. |  |
| 'GPS Signal Level Settings' screen |
| ME03-US85-AC12 | If I tap on 'GPS Signal Level Settings' section and Bluetooth permission is granted and Bluetooth is turned on the phone, then:'GPS Signal Level Settings' screen should be opened. | - |
|  | 'GPS Signal Level Settings' screen should consists of: TBD |  |
| ME03-US85-AC15 | In case a user disables Bluetooth on the smartphone during the process of GPS Calibration (while user is on 'Calibrate Collar's GPS' screen with map), then user is navigated to screen with the following elements:title ''Calibrate Collar's GPS' the rest of the elements is the same as for 'Bluetooth is Disabled' (see ME03-F00-AC34 for details).tbd | TBD what to show |
|  | Default Zoom level on the map should be set up to 18. |  |
| ME03-US85-AC05 | Precondition: Collar is out of Bluetooth rangeIf I tap on 'Start Calibration' on 'GPS Light Signals' screen and I navigated to'Calibrate Collar's GPS' screen with map background and collar is out of Bluetooth range then I see the re-connection panel with:'Reconnecting with Collar.' textSee ME14-US09 Using blue panel to indicate Bluetooth reconnection for 'Create fence with a collar' flow and ME14-US14. Close "Reconnecting with collar" bar for details.Note 1: If I leave the screen with map background then I will no longer see the re-connection panel.Note 2: There should be delay of 3 seconds for showing the re-connection blue bar after user navigates to the 'Calibrate Collar's GPS' screen with map background. | - |
|  | 'Initializing GPS' screen should have 2 states:MaximizedMinimized |  |
|  | The app should open Maximized Initializing GPS card by default |  |
|  | Collapsed 'Initializing GPS' level card should have the following UI elements:Expand buttonGPS level iconCurrent GPS Signal Level titleGPS level and explanatory textCurrent GPS level value |  |
|  | The GPS level bar should consist of the following UI elements:'Low' label:background color for the 'low' section should be grey (=no background)'medium' (no label, just the section on the scale):background color for the 'medium' value should be magenta'High' label:background color for the 'high' label should be blueGPS signal pinthe GPS signal pin should indicate the dynamic change of the GPS levelScale with values (see ME03-US94-AC13) |  |
|  | The blue dot on the 'GPS signal' pin should have a pulsing animation. |  |
|  | Current GPS signal strength level should be displayed in grey parenthesis besides high/med/low/no textNote 1: сurrent GPS level should be taken via Bluetooth from the collar. |  |
|  | The following values should be applied within the barStart point...Final pointGPS signal strength502000, and \>2000 | 50 | 2000, and \>2000 |  |
| 50 | 2000, and \>2000 |
|  | The mobile app should display all GPS values rounded to 10. |  |
|  | Current GPS signal strength level should be updated each 1 sec via Bluettoth. |  |
|  | 'i' link should open 'GPS level explanation' screen (see 'Learn more about GPS levels' link -\> 'GPS level explanation' screen) |  |
|  | Precondition:User clicks on the 'Learn more about GPS levels' link in 'Initializing GPS' screenThe app opens 'GPS level explanation' screen that consists of the following elements:high GPS:a blue icon;'GPS level high' title;'Your collar will provide escalating preventions to keep your dog from leaving and return whistles to bring them back when they stop or turn around.' text.medium GPS:a magenta icon;'GPS level medium' title;'Your collar will use return whistles to keep your dog from leaving and get your dog to return.' text;low GPS or no GPS:a white icon;'Low GPS or no GPS' title;'Your collar will automatically pause fence feedback and the location and time displayed on my map will be from the last high or medium GPS position.' text'Close' button |  |
|  | Precondition: GPS signal strength is in the Low rangeLevel Pin on the GPS level bar should be disabled. |  |
|  | Precondition:GPS signal strength is in the Low rangePet pin should be:DisabledHave a 'paused' pet pin badge |  |
|  |  |  |
|  |  |  |
|  | Entry point:a user clicks on the 'GPS signal level settings' from the Advanced settingsANDNo data OR No GPS signal is receivedThe app should show the following text besides the GPS iconAs isTo be'No GPS''No GPS satellites detected' | 'No GPS' | 'No GPS satellites detected' |  |
| 'No GPS' | 'No GPS satellites detected' |
|  |
|  | No GPS signal is receivedThe app should:Show No GPS icon.Show 'No GPS' grey textDisable the GPS level barHide Signal level pin. | add screen |
| Entry point:a user taps on the 'Start Initialization' button in the Onboarding flow OR during Add Collar flowBluetooth pairing with the collar has not been set up |
|  | The app should:Display 'Reconnecting With Collar' toastShow spinner instead of GPS icon.Show 'Please move closer to your collar' textDisable the GPS level barHide Signal level pin. |  |
| Entry point:The collar’s FW does not support manual GPS calibration featurea user taps on the 'Start Initialization' button in the Onboarding flow OR during Add Collar flow |
|  | The app should disable the GPS level barThe app should hide 'GPS Signal' pinThe app should not show GPS value in parenthesis. |  |
| Entry point:Initializing GPS screen (Onboarding flow, Add Collar flow) is open |
|  | PreconditionBluetooth pairing with the collar has been initiated AND the data has been received from the collar every 1 second → BLE connection was lostThe app should:Display 'Reconnecting With Collar' toastShow spinner instead of GPS icon.Show 'Please move closer to your collar' textDisable the GPS level barHide Signal level pin. |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
| ME03-US85-AC06 | Blue re-connection panel (described on ME03-US85-AC05) should be displayed on the 'Calibrate Collar's GPS' screen with map background until the collar is turned on and nearby (within Bluetooth range). | - |
| ME03-US85-AC08 | User should be able to pan in/out the map background (see My Map). Default zoom level (TBD with devs 12? - should be close enough to see the details of user's premises) | - |
| ME03-US85-AC09 | When I go to 'Calibrate Collar's GPS' screen then I see map background centered according to the prioritization rules described below:PriorityCentered byAC1 location of CollarWhen collar location is available, then my map should be centered by collar location. When it's not, but user location data is available, then map background will be centered by user location. 2location of user's phoneWhen collar's location is not available, but user location data is available, then map background will be centered by user location. 3default location (see BR-11 Map view settings.)When neither collar's location not user's location is available, then I see the map centered by the default location.Note: All the outlined rules are referred only to the first showing of the map. E.g. if afterwards the user or collar changes position on the map we should not automatically center the map by its new position. | 1 | location of Collar | When collar location is available, then my map should be centered by collar location. When it's not, but user location data is available, then map background will be centered by user location. | 2 | location of user's phone | When collar's location is not available, but user location data is available, then map background will be centered by user location. | 3 | default location (see BR-11 Map view settings.) | When neither collar's location not user's location is available, then I see the map centered by the default location. | - |
| 1 | location of Collar | When collar location is available, then my map should be centered by collar location. When it's not, but user location data is available, then map background will be centered by user location. |
| 2 | location of user's phone | When collar's location is not available, but user location data is available, then map background will be centered by user location. |
| 3 | default location (see BR-11 Map view settings.) | When neither collar's location not user's location is available, then I see the map centered by the default location. |
