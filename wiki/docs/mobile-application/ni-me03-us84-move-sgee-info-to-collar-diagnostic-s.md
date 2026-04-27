---
title: "(NI) ME03-US84. Move SGEE info to \"Collar Diagnostic\" screen"
sidebar_label: "(NI) ME03-US84. Move SGEE info to \"Collar Diagnostic\" screen"
sidebar_position: 225
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Katherina Kaplina, Timofey Burak [X], Dmitriy Morozov [X], Alexei Zhukov |
| HALO-11875 - MOB+BE: Move SGEE info to "Collar Diagnostic" screen from "Advanced Settings" Ready for Development |
| Click here to expand... |# Contents

General description User story Acceptance criteria

# General description

This US contains improvements for the 'Collar Diagnostic' section in the app discussed during 2022-05-12 Meeting notes: Sprint 83 Demo and 2022-05-16 Meeting notes: BA call (Monday).

# User story

\> As a Halo app account owner I want to see more details about my Halo collar's hardware performance so that to better understand what's happening on the collar and what are the possible issues.

# Acceptance criteria

| AC | Description | iOS screen designs | Android screen designs | AS IS | TO BE |
|---|---|---|---|---|---|
| ME03-US84-AC01 | 'Satellite Position Data' should be moved from the 'Advanced Settings' screen to the 'Collar Diagnostic' screen.BA note: first, SGEE info is not a setting. Second, this info also comes in DD. Third, it influences collar's GPS behavior therefore it's better to display this info on the 'Collar Diagnostic' screen. | - | - |
| ME03-US84-AC02 | The app should display a new 'Satellite Position Data' field in the GPS section. | Pic ME03-US84-P01 "Collar Diagnostic" screen, SGEE data is up-to-dateLink to Zeplin | Link to Zeplin |
| ME03-US84-AC03 | Precondition: GloExp/GpsEXP date is more than Today date (i.e. SGEE data isn't outdated).The app should display the following info in a new 'Satellite Position Data' field: \<number of days till SGEE file expiration\> days remainingWhere:\<number of days till SGEE file expiration\> = \<GloExp/GpsEXP\> - \<Today date\>ANDGloExp/GpsEXP are expiration date received from the collar on Daily DiagnosticsAND\<Today date\> is a local date of an app userANDthe number of days is rounded upward.Note 1: the logic for displaying it should remain as is (as of 18 May 2022), see ME03-F01-AC66.Note 2: the system should not display 'Last update' anymore. | - | - |
| ME03-US84-AC04 | Precondition: Collar doesn't support the SGEE feature.The app should display the following info in a new 'Satellite Position Data' field:Upgrade the firmware of your collar. | Pic ME03-US84-P02 "Collar Diagnostic" screen, SGEE feature isn't supportedLink to Zeplin | Link to Zeplin |
| ME03-US84-AC05 | 'Upgrade' should be a tappable link.Link: https://support.halocollar.com/hc/en-us/articles/360048638273.When the user taps on the link, the app should initiate opening a Zendesk article in the browser. | - | - |
| ME03-US84-AC06 | Precondition: SGEE data is outdated (i.e. GloExp/GpsEXP date is less than Today date) OR SGEE data doesn't exist in DD (but FW supports SGEE data)The app should display the following info in a new 'Satellite Position Data' field:No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and do not turn if off. Use Halo Help for troubleshooting. | Pic ME03-US84-P03 "Collar Diagnostic" screen, SGEE data is outdatedLink to Zeplin | Link to Zeplin |
| ME03-US84-AC07 | 'Halo Help' should be a tappable link.Link: https://cdn.solvvy.com/deflect/customization/halocollar/support.html?solvvyWF=1cb4c86a-7bd9-4c95-a498-5a63b84b7297When a user taps on it, the app should initiate 'Halo Help' opening with predefined question typed: Troubleshooting → Troubleshooting Guide. | - | - |
| ME03-US84-AC08 | Precondition: 'Halo Help' is opened from the 'Collar Diagnostic' screen.When a user taps on the 'Back' icon, the app should open the 'Collar Diagnostic' screen. |  |  |
| ME03-US84-AC09 | The triggers for the indication that there's an issue within GPS section should be changed:AS ISTO BEThe app should indicate that there's an issue with GPS module when:GPS_fail \> 0 ANDGPS_msg_cnt = 0ANDOnTime is not 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row.The app should indicate that there's an issue with GPS module in case of any of the cases below (at least 1):1st case:GPS_fail \> 0 ANDGPS_msg_cnt = 0ANDOnTime is not 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row.2nd case:Collar doesn't support the SGEE feature.3rd case: SGEE data is outdated. | The app should indicate that there's an issue with GPS module when:GPS_fail \> 0 ANDGPS_msg_cnt = 0ANDOnTime is not 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row. | The app should indicate that there's an issue with GPS module in case of any of the cases below (at least 1):1st case:GPS_fail \> 0 ANDGPS_msg_cnt = 0ANDOnTime is not 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row.2nd case:Collar doesn't support the SGEE feature.3rd case: SGEE data is outdated. | - | - |
| The app should indicate that there's an issue with GPS module when:GPS_fail \> 0 ANDGPS_msg_cnt = 0ANDOnTime is not 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row. | The app should indicate that there's an issue with GPS module in case of any of the cases below (at least 1):1st case:GPS_fail \> 0 ANDGPS_msg_cnt = 0ANDOnTime is not 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row.2nd case:Collar doesn't support the SGEE feature.3rd case: SGEE data is outdated. |
| ME03-US84-AC10 | Several instructions (texts for issues with GPS) can be displayed at a time. | - | - |
