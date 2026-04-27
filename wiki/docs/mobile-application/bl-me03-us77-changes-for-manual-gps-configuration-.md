---
title: "[BL] ME03-US77. Changes for manual GPS configuration (change indoor/ outdoor naming)"
sidebar_label: "[BL] ME03-US77. Changes for manual GPS configuration (change indoor/ outdoor naming)"
sidebar_position: 213
last_modified: "May 30, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] |
| Click here to expand... HALO-11382 - MOB: Changes for manual GPS configuration (change indoor/ outdoor naming) Closed |
| Click here to expand...30 May 2022 Maria Shikareva [X] Marked the story as baselined (see ME03-F05. GPS signal levels configuration (ex. GPS calibration),ME03-F01. Collars list). |# Contents

General description User story Acceptance criteria 'Advanced Settings' screen 'GPS signal level settings' screen 'Cancel' message

# General description

This US is caused by the changes described in [Not implemented] ME07-US70. Rename indoor/ outdoor statuses.

# User story

\> As a Halo app account owner I want to see the updated UI for manual configuration tool so that it's wording and behavior are consistent with the wording on Pet Card.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status | AS IS | TO BE | AS IS | TO BE | AS IS | TO BE | AS IS | TO BE | AS IS | TO BE | 'Cancel' message | AS IS | TO BE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 'Advanced Settings' screen |
| ME03-US77-US01 | The name of the section on the "Advanced Settings" screen should be changed:AS ISTO BEIndoor/ Outdoor SettingsGPS signal level settings | Indoor/ Outdoor Settings | GPS signal level settings | Pic ME03-US77-P01 "Advanced Settings" screenLink to Zeplin | The same as on iOS.Link to Zeplin |
| Indoor/ Outdoor Settings | GPS signal level settings |
| ME03-US77-US02 | Precondition: the collar's FW supports manual GPS configuration feature.The description of the "GPS signal level settings" section on the "Advanced Settings" screen should be changed:AS ISTO BEHere you can change Halo's indoor/outdoor settings manually.Here you can change Halo's default settings manually. | Here you can change Halo's indoor/outdoor settings manually. | Here you can change Halo's default settings manually. |
| Here you can change Halo's indoor/outdoor settings manually. | Here you can change Halo's default settings manually. |
| ME03-US77-US03 | Precondition: the collar's FW doesn't support manual GPS configuration feature.The description of the "GPS signal level settings" section on the "Advanced Settings" screen should be changed:AS ISTO BEPlease update the firmware on your Halo in order to manually calibrate GPS.Please update the firmware on your collar in order to manually configure Halo's default settings. | Please update the firmware on your Halo in order to manually calibrate GPS. | Please update the firmware on your collar in order to manually configure Halo's default settings. | Pic ME03-US77-P02 "Advanced Settings - FW doesn't support" screen Link to Zeplin |  |
| Please update the firmware on your Halo in order to manually calibrate GPS. | Please update the firmware on your collar in order to manually configure Halo's default settings. |
| 'GPS signal level settings' screen |
| ME03-US77-US04 | The instruction on the top of the screen should be changed:AS ISTO BEIn order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog.In order to override Halo's default settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog. | In order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog. | In order to override Halo's default settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog. | Pic ME03-US77-P03 "GPS signal level Settings" screen Link to Zeplin | The same as for iOS.Link to Zeplin |
| In order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog. | In order to override Halo's default settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog. |
| ME03-US77-US05 | The app should display background colors for each part of slider:white (no background) → for GPS level less than left pin;magenta → for GPS level higher than left pin but less than the right pin;blue → for GPS level higher than right pin. |
| ME03-US77-US06 | 'Indoor'/ 'Outdoor' icons should be removed from pin bubbles. |
| ME03-US77-US07 | The following legend should be added to the 'GPS Signal Level Settings' screen:low GPS:a white icon;'Fence feedback will be paused' text;low GPS icon with 1 bar;'GPS level low' text;medium GPS:a magenta icon;'Fence feedback: return whistle only' text;medium GPS icon with 2 bars;'GPS level medium' text;high GPS:a blue icon;'Fence feedback will be active' text;high GPS icon with 3 bars;'GPS level high' text. |
| ME03-US77-US08 | The app should replace the following buttons:AS ISTO BE"Indoor" button with the level in numbersReturn to previous (\<min level in numbers\>) displayed in the white section of legend."Outdoor" button with the level in numbersReturn to previous (\<max level in numbers\>) displayed in the blue section of legend. | "Indoor" button with the level in numbers | Return to previous (\<min level in numbers\>) displayed in the white section of legend. | "Outdoor" button with the level in numbers | Return to previous (\<max level in numbers\>) displayed in the blue section of legend. |
| "Indoor" button with the level in numbers | Return to previous (\<min level in numbers\>) displayed in the white section of legend. |
| "Outdoor" button with the level in numbers | Return to previous (\<max level in numbers\>) displayed in the blue section of legend. |
| ME03-US77-US09 | 'Return to previous' should be visible only if the corresponding pin value differs from the previous one. |
| ME03-US77-US10 | The UI 'Revert to Halo Defaults' button should be also changed (see screen designs). |
| ME03-US77-US11 | The text of M204 Cancel GPS calibration should be changed:AS ISTO BETitle: Are you sure you want to discard Indoor/ Outdoor settings?Body: Any unsaved changes will be lost.Buttons: No, Continue editing; Discard.Title: Are you sure you want to discard GPS signal level settings?Body: Any unsaved changes will be lost.Buttons: No, Continue editing; Discard. | Title: Are you sure you want to discard Indoor/ Outdoor settings?Body: Any unsaved changes will be lost.Buttons: No, Continue editing; Discard. | Title: Are you sure you want to discard GPS signal level settings?Body: Any unsaved changes will be lost.Buttons: No, Continue editing; Discard. | - | - |
| Title: Are you sure you want to discard Indoor/ Outdoor settings?Body: Any unsaved changes will be lost.Buttons: No, Continue editing; Discard. | Title: Are you sure you want to discard GPS signal level settings?Body: Any unsaved changes will be lost.Buttons: No, Continue editing; Discard. |
