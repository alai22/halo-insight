---
title: "ME21-US87. Check 'location service' on android when adding a collar and show error if off"
sidebar_label: "ME21-US87. Check 'location service' on android when adding a collar and show error if off"
sidebar_position: 452
last_modified: "Jan 08, 2025"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya |
| HALO-21369 - Android: ME21-US87. Check 'location service' status on android when adding a collar and show error if off Closed |
| 16 Sep 2024 the draft story is created |Table of Contents

Background User story Acceptance criteria

# Background

When adding an IoT device to Android mobile app, different settings and permissions are needed depending on the Android version:

1. **Device (smartphone)-Level "Location Service":**

- 
  - This service must be enabled on the device for Bluetooth and Wi-Fi scanning. It is different from the app's location permission. Users can toggle it via the**quick settings panel (see the screenshot below)**or**Settings \> Location**. If the service is off, the app cannot find nearby devices, so a check and error popup are needed.

2. App-Specific Permissions:

- 
  - **Android ≤ 11:**Only**Location permission**is required for Bluetooth scanning because it can indicate user location. (Before Android 12, there were no separate Bluetooth-specific permissions. Android treated Bluetooth scanning as a potential privacy risk for revealing location, so**Location permission**covered this functionality.)
  - **Android ≥12 :**Both**Location and Bluetooth permissions**are required for more granular control and privacy.

Context for the User Story:

This user story for checking the "location service" is necessary because the app needs both the location service enabled and the correct permissions to function properly. Even with app permissions granted, if the device’s location service is off, the app cannot scan for devices.

The location permission user story will be defined separately.

# User story

As Halo app account owner, I want the mob app to check if the 'location service' is turned on or off on my Android device, so that I am notified with an error popup if the location setting is turned off and can enable it to proceed with adding the collar.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| ME21-US87-AC01 | Preconditions:Halo mob app is opened on an Android deviceAND'Link Collar to Account' screen is shown (the screen can be opened within the FTUE Onboarding OR within 'Attach Collar' flow initiated from any other entry point in the app)ANDFOR Android ≤11: Location permission is granted AND Bluetooth setting is enabledFOR Android ≥12 : Both Location AND Bluetooth permission are granted AND Bluetooth setting is enabledIf the 'location service' is turned off, then:M295 Location is turned off popup should be displayed. | - |
| ME21-US87-AC02 | If I tap on the Settings button on M295 Location is turned off popup, then: System settings of the phone should be opened where I can manage Location service (Settings → Location). | The screen is presented as a sample (can be different on different Android devices) |
| ME21-US87-AC03 | Preconditions: the same as in ME21-US87-AC01If the 'location service' is turned on, then:I can proceed with adding the device without interruption. | - |
