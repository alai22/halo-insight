---
title: "(Native Apps) ME01-F10. Screen permissions check on opening"
sidebar_label: "(Native Apps) ME01-F10. Screen permissions check on opening"
sidebar_position: 488
last_modified: "Mar 17, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| READY |
| Mariya Kolyada, Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-428/[ios]-screen-permissions-check-after-the-app-launchAndroid: https://linear.app/fueled/issue/HALO-429/[android]-screen-permissions-check-on-opening |
| 24 Feb 2025 - 26 Feb 2025 Mariya Kolyada created the initial version of a user story based on split requirements from (Native apps) ME15-F02. User location pin27 Feb 2025 Mariya Kolyada rewrote the user story with the support of Dmitry Kravchuk.28 Feb 2025 Mariya Kolyada updated the user story to final version + added designs.17 Mar 2025 Mariya Kolyada updated ME01-F10-AC04 with new BLE pop-up. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want the app check for Bluetooth, Location and Notifications access so I can access all the features of the app.

# Acceptance criteria

| AC | Description | Design | Enable Permissions with updates* It has been mostly implemented within task Halo-91, update the app with missed ACs only. | AC | If user taps on Select for | Android | iOS | ≤11 | \>11 | ME01-F10-AC04-1 | ME01-F10-AC04-2 | ME01-F10-AC04-3 | Request Location Permission on Android | Screen opening | If user/app opens the following screen, | then the app should check the status of the following permissions: |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME01-F10-AC01 | Enable Permissions screen should work the following way:ACIf user taps on Select forAndroidiOS≤11\>11ME01-F10-AC01-1LocationSee Request Location Permission on AndroidM153 FigmaME01-F10-AC01-2BluetoothRequest Location permission (because BLE and Location are one permission)Native Android OS pop-upM142Figma ME01-F10-AC01-3NotificationsNative Android OS pop-up (Required for Android \>=13)M149Figma | ME01-F10-AC01-1 | Location | See Request Location Permission on Android | M153 Figma | ME01-F10-AC01-2 | Bluetooth | Request Location permission (because BLE and Location are one permission) | Native Android OS pop-up | M142Figma | ME01-F10-AC01-3 | Notifications | Native Android OS pop-up (Required for Android \>=13) | M149Figma | Figma* Screen design from Onboarding |
| ME01-F10-AC01-1 | Location | See Request Location Permission on Android | M153 Figma |
| ME01-F10-AC01-2 | Bluetooth | Request Location permission (because BLE and Location are one permission) | Native Android OS pop-up | M142Figma |
| ME01-F10-AC01-3 | Notifications | Native Android OS pop-up (Required for Android \>=13) | M149Figma |
| ME01-F10-AC02 | If the permission access has been granted (once or always), indicate permission as "ON" on the Enable Permissions screen. | - |
| ME01-F10-AC03 | If the permission access is declined or not precise (Android only), indicate permission as "OFF" on the Enable Permissions screen. | - |
| ME01-F10-AC04 | If a user taps on the "OFF" state, show the corresponding:ME01-F10-AC04-1ME01-F10-AC04-2ME01-F10-AC04-3Location figmaBluetooth figmaNotification figma | Location figma | Bluetooth figma | Notification figma | - |
| Location figma | Bluetooth figma | Notification figma |
| ME01-F10-AC05 | The app should disable the “Next” button until user has interacted with all 3 permissions. | - |
| ME01-F10-AC06 | If the app requests Location Permission on Android, it should display the M261 Precise Location Required before displaying the native Location Access pop-up.NoteSee the reason for implementation in Principle 5 https://developer.android.com/training/permissions/requesting#principles | Figma |
| ME01-F10-AC07 | If user/app opens the following screen,then the app should check the status of the following permissions:All screens with the Map:My FencesWalkCollar details: Tracking Details (out of this User story scope)Collar details: GPS Settings (out of this User story scope)User LocationAll screens with connection to the collar:My FencesWalk (out of this User story scope)More (out of this User story scope)Collar Details (out of this User story scope)BluetoothAdd Collar (out of this User story scope)BluetoothUser LocationAdd Beacon (out of this User story scope)BluetoothUser LocationDog Park (out of this User story scope)CameraAudio | All screens with the Map:My FencesWalkCollar details: Tracking Details (out of this User story scope)Collar details: GPS Settings (out of this User story scope) | User Location | All screens with connection to the collar:My FencesWalk (out of this User story scope)More (out of this User story scope)Collar Details (out of this User story scope) | Bluetooth | Add Collar (out of this User story scope) | BluetoothUser Location | Add Beacon (out of this User story scope) | BluetoothUser Location | Dog Park (out of this User story scope) | CameraAudio | - |
| All screens with the Map:My FencesWalkCollar details: Tracking Details (out of this User story scope)Collar details: GPS Settings (out of this User story scope) | User Location |
| All screens with connection to the collar:My FencesWalk (out of this User story scope)More (out of this User story scope)Collar Details (out of this User story scope) | Bluetooth |
| Add Collar (out of this User story scope) | BluetoothUser Location |
| Add Beacon (out of this User story scope) | BluetoothUser Location |
| Dog Park (out of this User story scope) | CameraAudio |
| ME01-F10-AC08 | If the app has all permissions required for the specified screen opening, then the app should display this screen. | - |
| ME01-F10-AC09 | If user has never either accepted or declined the required app permissions on this device, then the app should display the Enable Permissions screen (see requirements above in ME01-F10-AC01 – AC05).* The steps indicator at the top of the screen should be hidden.NotesThis scenario is possible if the user installs the app on the new device or reinstalls the app on the same device.On iOS: allowed once = has never either accepted or declined the required app permission. | - |
| ME01-F10-AC10 | In all other cases the app should try to request the required permission from the device OS, and the OS manages the further behavior.NotesThis AC includes:Denied PermissionAndroid only:Allowed onesNot precise location | - |
| ME01-F10-AC11 | If the OS declines permission requests after the app tries, then the app behavior is defined in individual user stories of each screen. | - |
