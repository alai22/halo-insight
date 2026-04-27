---
title: "[BL] ME03-US76. BLE 'real-time' indication (indoor/ outdoor calibration)"
sidebar_label: "[BL] ME03-US76. BLE 'real-time' indication (indoor/ outdoor calibration)"
sidebar_position: 212
last_modified: "Apr 29, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] |
| Click here to expand... HALO-11307 - MOB: Manual indoor/ outdoor configuration - BLE 'real-time' indication Closed |
| Click here to expand...07 Apr 2022 Maria Shikareva [X] Added ME03-US76-US06 to handle cases when the current GPS level isn't received from the collar in the very beginning (when the user just opened 'Indoor/ Outdoor Settings' screen) as discussed with Kirill Akulich [X].29 Apr 2022 Maria Shikareva [X] Marked the story as baselined (see ME03-F05. Edit GPS signal level settings (ex. GPS calibration)). |# Contents

User story Acceptance criteria Precondition: the data is received from the collar every 1 second. Precondition: the data isn't received from the collar 2 seconds and more. Precondition: the data isn't received from the collar from the beginning

# User story

\> As a user I want to see an indication that the data about current GPS level is updated in real-time so that to understand that the manual indoor/ outdoor configuration tool is working even if I stand still.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status | AS IS | TO BE | AS IS | TO BE | AS IS | TO BE |
|---|---|---|---|---|---|---|---|---|---|
| Precondition: the data is received from the collar every 1 second. |
| ME03-US76-US01 | The instruction on the top of the screen should be changed:following changes should be done:AS ISTO BEIn order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below.Make sure the collar is ON your dog.In order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog.Note: this change is needed to highlight to the user that when transitioning between indoor/outdoor, the value does not change instantly, but - rather - over 10-15 seconds. It depend on the collar behavior (i.e. the collar has a median filter that don't allow numbers to fluctuate a lot). | In order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below.Make sure the collar is ON your dog. | In order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog. | Pic ME03-US76-P01 "Indoor/ Outdoor Settings" screen with real-time dataLink to Zeplin | The same as for iOS. |
| In order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below.Make sure the collar is ON your dog. | In order to override Halo's Indoor/Outdoor settings, use the manual configuration tool below. When moving in/out your house, expect the Halo GPS readings up to 15 seconds to adjust. Make sure the collar is ON your dog. |
| ME03-US76-US02 | The following changes should be done for the GPS signal pin:AS ISTO BECurrent GPS pin:'Current GPS' labelcurrent GPS Strength together with expected \<GPS status\> icon.GPS signal pin:'GPS Signal' label'current:' label with current GPS Strength. | Current GPS pin:'Current GPS' labelcurrent GPS Strength together with expected \<GPS status\> icon. | GPS signal pin:'GPS Signal' label'current:' label with current GPS Strength. | See Pic ME03-US76-P01 "Indoor/ Outdoor Settings" screen with real-time data. | The same as for iOS. |
| Current GPS pin:'Current GPS' labelcurrent GPS Strength together with expected \<GPS status\> icon. | GPS signal pin:'GPS Signal' label'current:' label with current GPS Strength. |
| ME03-US76-US03 | The blue dot on the 'GPS signal' pin should have a pulsing animation. | - | - |
| Precondition: the data isn't received from the collar 2 seconds and more. |
| ME03-US76-US04 | The following changes should be done:AS ISTO BECurrent GPS pin:'Current GPS' labelcurrent GPS Strength together with expected \<GPS status\> icon.GPS signal pin:'GPS Signal' label'\<X\>s ago:' label with latest GPS Strength received. | Current GPS pin:'Current GPS' labelcurrent GPS Strength together with expected \<GPS status\> icon. | GPS signal pin:'GPS Signal' label'\<X\>s ago:' label with latest GPS Strength received. | Pic ME03-US76-P02 "Indoor/ Outdoor Settings" screen with outdated dataLink to Zeplin | The same as for iOS. |
| Current GPS pin:'Current GPS' labelcurrent GPS Strength together with expected \<GPS status\> icon. | GPS signal pin:'GPS Signal' label'\<X\>s ago:' label with latest GPS Strength received. |
| ME03-US76-US05 | \<X\> should display the number of seconds when the latest data about GPS signal was received from the collar.Note: this will be displayed until the current data is received OR "Reconnecting with collar" bar is shown. | - | - |
| Precondition: the data isn't received from the collar from the beginning |
| ME03-US76-US06 | If the data isn't received during standard timeout (i.e. 10 sec), then the app should:display M70. No answer from the collar error message;not display a slider at all. | - | - |
