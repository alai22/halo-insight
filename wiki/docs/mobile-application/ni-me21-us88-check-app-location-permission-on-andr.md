---
title: "(NI) ME21-US88. Check 'app location permission' on android when adding a collar/beacon and show error if off"
sidebar_label: "(NI) ME21-US88. Check 'app location permission' on android when adding a collar/beacon and show error if off"
sidebar_position: 453
last_modified: "Sep 24, 2024"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya Pavel Leonenko |
| HALO-21375 - MOB: Unify handling Location and Bluetooth availability ( incl. update 'Location permission denied' popup logic when adding a collar) Ready for Development |
| 16 Sep 2024 the draft story is created |Table of Contents

Background User story Acceptance criteria

# Background

App-Specific Permissions:

- 
  - **Android ≤ 11:**Only**Location permission**is required for Bluetooth scanning because it can indicate user location. (Before Android 12, there were no separate Bluetooth-specific permissions. Android treated Bluetooth scanning as a potential privacy risk for revealing location, so**Location permission**covered this functionality.)
  - **Android ≥12 :**Both**Location and Bluetooth permissions**are required for more granular control and privacy.

# User story

As Halo app account owner, I want the mob app to check if the 'app location permission' is turned on or off on my Android device, so that I am notified with an error popup if the location permission is turned off and can enable it to proceed with adding the collar.

# Acceptance criteria

| AC | Description | UI design | AS IS | TO BE | Add Beacon |
|---|---|---|---|---|---|
| ME21-US88-AC01 | M217 "Location and Bluetooth permission denied" message (Android) text should be updated: AS ISTO BETitle: Access to Bluetooth DeniedBody: The Halo app does not have access to Bluetooth. Bluetooth is required, in order to configure your collar and apply feedback to your pet. In Android the ability to scan for nearby Bluetooth devices is tied to Location permission. Please enable access in Settings of your mobile device.Button: CancelButton: SettingsTitle: Location and Bluetooth Access DeniedBody: Android requires location access to scan for nearby Bluetooth devices. Please turn on bluetooth and location access to use your Halo Collar. Button: CancelButton: Settings | Title: Access to Bluetooth DeniedBody: The Halo app does not have access to Bluetooth. Bluetooth is required, in order to configure your collar and apply feedback to your pet. In Android the ability to scan for nearby Bluetooth devices is tied to Location permission. Please enable access in Settings of your mobile device.Button: CancelButton: Settings | Title: Location and Bluetooth Access DeniedBody: Android requires location access to scan for nearby Bluetooth devices. Please turn on bluetooth and location access to use your Halo Collar. Button: CancelButton: Settings | - |
| Title: Access to Bluetooth DeniedBody: The Halo app does not have access to Bluetooth. Bluetooth is required, in order to configure your collar and apply feedback to your pet. In Android the ability to scan for nearby Bluetooth devices is tied to Location permission. Please enable access in Settings of your mobile device.Button: CancelButton: Settings | Title: Location and Bluetooth Access DeniedBody: Android requires location access to scan for nearby Bluetooth devices. Please turn on bluetooth and location access to use your Halo Collar. Button: CancelButton: Settings |
| ME21-US88-AC02 | Preconditions:Halo mob app is opened on an Android device with OS ≤11AND'Link Collar to Account' screen is shown (the screen can be opened within the FTUE Onboarding OR within 'Attach Collar' flow initiated from any other entry point in the app)If the location permission is denied, then:M297 Denied location permission (Android: Add Collar, Add beacon) message should be shown. | - |
| ME21-US88-AC03 | Preconditions:Halo mob app is opened on an Android device with OS ≥12 AND'Link Collar to Account' screen is shown (the screen can be opened within the FTUE Onboarding OR within 'Attach Collar' flow initiated from any other entry point in the app)If both Bluetooth and Location permissions are denied, then:M217 "Location and Bluetooth permission denied" message (Android) popup should be displayed. | - |
| ME21-US88-AC04 | Preconditions:Halo mob app is opened on an Android device with OS ≤11ANDMy Beacons screen is shownIf the location permission is denied and I tap on 'Add Beacon' button, then:M297 Denied location permission (Android: Add Collar, Add beacon) message should be displayed. | - |
| ME21-US88-AC05 | Preconditions:Halo mob app is opened on an Android device with OS≥12ANDMy Beacons screen is shownIf the location permission is denied and I tap on 'Add Beacon' button, then:M217 "Location and Bluetooth permission denied" message (Android) popup should be displayed. | - |
