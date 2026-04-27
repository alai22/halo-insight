---
title: "[Duplicate] ME21-US08. Onboarding: Step 5: GPS calibration"
sidebar_label: "[Duplicate] ME21-US08. Onboarding: Step 5: GPS calibration"
sidebar_position: 237
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| DRAFT |
| Valeryia Chyrkun [X] |
| ADD new ticket |
| 05 Oct 2022 Maria Shikareva [X] Marked the story as 'Duplicate' because another story was created: [NI] ME21-US36. Onboarding: Updates for 'GPS Initialization' flow. |# Updates in comparison with the current flow:

- add Close button
- TBD with Lera

# General description

Duplicates [BL] ME03-US85. Collar Details: GPS Signal Level Settings

The main goals of adding GPS Calibration are the following:

- To explain LED meanings,
- To teach how to calibrate GPS properly (how to handle the device during the process)
- To teach users for the future how to check the accuracy of their device. Because we have a lot of complaints about GPS inaccuracy.

At the GPS Calibration step during onboarding we want users to build in the confidence that their collar works properly, we want them realize that GPS is accurate.

# User story

\> As an app user, I want to add my Halo to the app to proceed with the Onboarding process.

# Acceptance criteria

| AC | Description | Links, design | high GPS signal is not received yet | high GPS signal is received | centered by | when | Icon | meaning |
|---|---|---|---|---|---|---|---|---|
| ME03-US85-AC01 | When I leave 'Choose a Network' screen while adding the collar then I navigate to the 'Calibrate Your Collar' screen with the following elements:Title: Calibrate CollarSubtitle: Calibrate Your CollarText: Unplug your collar and take it outside, ideally to a location with an unobstructed view of the sky, until the GPS LED blinks blue and you see the collar's location displayed accurately on the map. ' Image of hand holding the collar by the strapText :'Hold the collar as shown while walking around outside during GPS Calibration. The collar should bounce slightly while you walk.'Button: 'Next' (always enabled)Button: Close. If I click this button then I navigated to 'Choose a Network' screen. |  |
| ME03-US85-AC02 | When I click 'Start Calibration' on 'Calibrate Your Collar', then I see 'GPS LED Behavior' screen with the following elements:Title: Calibrate CollarTitle: GPS LED BehaviorImage: Blink blue LEDText: GPS LED will blink blue while GPS signal strength is high.Image: Blink pink LEDText: GPS LED will blink pink while GPS signal strength is medium. It will be solid pink when downloading satellite position data via Internet.Image: turned off LEDText: GPS LED will off while GPS signal strength is low, or while collar is not moving.Image: blink red LEDText: GPS LED will blink red if calibration is required. Also you will receive in-app notification.Button: Start Calibration.Button: Close. When I click this button then I navigated to 'Learn More About GPS' screen. |  |
| ME03-US85-AC03 | Precondition: Bluetooth isn't turned on/ becomes turned of when user on the 'Calibrate Collar' screenIf I click 'Start Calibration' on 'GPS LED Behavior' screen and Bluetooth is not enabledORWhen I'm on the 'Calibrate collar' screen and Bluetooth is turned off on device then I see blue bar with the text:"Please turn Bluetooth ON in your device settings to continue. Bluetooth is needed to track the custom-configuration of GPS sensor."When I click 'Try again ' button then device repeat the attempt to restore connection.Note: Connection between a collar and device will be done by Bluetooth. When we show 'GPS LED Behavior' we should immediately try to pair collar with device before they hit 'Start Calibration'. |  |
| ME03-US85-AC04 | Blue bar (described on ME03-US85-AC03) should be displayed until user turns on the Bluetooth on the device. |  |
| ME03-US85-AC05 | Precondition: Collar is out of Bluetooth rangeIf I click 'Start Calibration' on 'GPS LED Behavior' screen and collar is out of Bluetooth range then I see the blue bar with:'Collar is out of Bluetooth range. Make sure the collar is nearby and turned on.' text'Try again' button. When I click 'Try again ' button then device repeat the attempt to restore connection. |  |
| ME03-US85-AC06 | Blue bar (described on ME03-US85-AC05) should be displayed until the collar is turned on and nearby (within Bluetooth range). |  |
| ME03-US85-AC07 | Precondition: Bluetooth is turned on and the process of GPS calibration is not completed.When I click 'Start Calibration' then I see the GPS Calibration screen with the following elements: high GPS signal is not received yethigh GPS signal is received Map BackgroundCard with'Current GPS signal level:' textGPS level icon (described in ME03-US85-AC09)'Searching for high GPS signal...' text'Map is not accurate? Request and update' text where 'Request an update' is a link to Map update flow.'Skip Calibration' buttonicon: When I click this icon then I navigated to 'GPS LED Behavior' screen.Map backgroundCard with'Current GPS signal level:' textGPS level icon (described in ME03-US85-AC09)'Press 'Done' once the location of the collar is shown accurately on the map (may take several minutes).' text'Map is not accurate? Request and update' text where 'Request an update' is a link to Map update flow.'Done' button (enabled) | Map BackgroundCard with'Current GPS signal level:' textGPS level icon (described in ME03-US85-AC09)'Searching for high GPS signal...' text'Map is not accurate? Request and update' text where 'Request an update' is a link to Map update flow.'Skip Calibration' buttonicon: When I click this icon then I navigated to 'GPS LED Behavior' screen. | Map backgroundCard with'Current GPS signal level:' textGPS level icon (described in ME03-US85-AC09)'Press 'Done' once the location of the collar is shown accurately on the map (may take several minutes).' text'Map is not accurate? Request and update' text where 'Request an update' is a link to Map update flow.'Done' button (enabled) | Version 3: |
| Map BackgroundCard with'Current GPS signal level:' textGPS level icon (described in ME03-US85-AC09)'Searching for high GPS signal...' text'Map is not accurate? Request and update' text where 'Request an update' is a link to Map update flow.'Skip Calibration' buttonicon: When I click this icon then I navigated to 'GPS LED Behavior' screen. | Map backgroundCard with'Current GPS signal level:' textGPS level icon (described in ME03-US85-AC09)'Press 'Done' once the location of the collar is shown accurately on the map (may take several minutes).' text'Map is not accurate? Request and update' text where 'Request an update' is a link to Map update flow.'Done' button (enabled) |
| ME03-US85-AC08 | User should be able to pan in/out the map background (see My Map). Default zoom level (TBD with devs 12? - should be close enough to see the details of user's premises) |  |
| ME03-US85-AC09 | The map background should be centered according to the table below:centered bywhenuser's phone locationthe location of user is defined and location of collar is not definedcollars' locationthe location of collar is defineddefault location (see BR-11 Map view settings.)unable to define user's of collar's location | user's phone location | the location of user is defined and location of collar is not defined | collars' location | the location of collar is defined | default location (see BR-11 Map view settings.) | unable to define user's of collar's location |  |
| user's phone location | the location of user is defined and location of collar is not defined |
| collars' location | the location of collar is defined |
| default location (see BR-11 Map view settings.) | unable to define user's of collar's location |
| ME03-US85-AC10 | The GPS icon and value should be displayed according to the table below: Iconmeaningsearching for any GPS signal (no GPS was previously caught)GPS signal strength is highGPS signal strength is mediumGPS signal strength is lowNo GPS signal |  | searching for any GPS signal (no GPS was previously caught) |  | GPS signal strength is high |  | GPS signal strength is medium |  | GPS signal strength is low |  | No GPS signal |  |
|  | searching for any GPS signal (no GPS was previously caught) |
|  | GPS signal strength is high |
|  | GPS signal strength is medium |
|  | GPS signal strength is low |
|  | No GPS signal |
| ME03-US85-AC11 | Analytics event should be added on how many users skip Calibration step vs. users who complete the calibration |  |
