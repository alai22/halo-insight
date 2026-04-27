---
title: "[BL] ME03-US94. View GPS level bar (Advanced collar settings)"
sidebar_label: "[BL] ME03-US94. View GPS level bar (Advanced collar settings)"
sidebar_position: 291
author: "Ekaterina Dupanova"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-15054 - MOB: View GPS level bar on 'Initializing GPS' screen (Onboarding flow, Add Collar flow) Closed |
| Click here to expand...As of: 12 Dec 2022 Ekaterina Dupanova created initial draft of the story31 Jan 2023 Ekaterina Dupanova finalized the US for View mode 12 May 2023 Ekaterina Dupanovaadded ME03-US94-AC2323 Jun 2023 Ekaterina Dupanova removed ME03-US94-AC2117 Jan 2025 baselined to ME03-F08. View GPS signal level settings and Collar Orientation |# Contents

User story Acceptance criteria

# User story

\> As a Halo app user I want to see the GPS level bar on 'Initializing GPS' screen so that I can see the GPS level changing in real time and understand the current level of the GPS signal.

# Acceptance criteria

| AC | Description | Links, design | As is | To be |  | Start point | ... | Final point | GPS signal strength |
|---|---|---|---|---|---|---|---|---|---|
| Changes to controls location on My Map ('Initializing GPS' screen) |
| ME03-US94-AC01 | Move 'Compass' and 'Center on the collar's location' buttons higher on the screen. |  |
| ME03-US94-AC22 | Text under Initializing GPS should be: As is To beWalk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes).Take your collar outdoors where you can see the most open sky. Walk around until until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). | Walk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). | Take your collar outdoors where you can see the most open sky. Walk around until until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). | Zeplin: iOS | Android |
| Walk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). | Take your collar outdoors where you can see the most open sky. Walk around until until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). |
| Entry point:a user taps on the 'Start Initialization' button in the Onboarding flow OR during Add Collar flowBluetooth pairing with the collar has been initiated AND the data is received from the collar every 1 second. |
| ME03-US94-AC02 | Add the following elements to the 'Initializing GPS' screen:\<GPS level value\> (Note: in parenthesis besides Medium/High/Low). If GPS level is No or No data - no value should be shown, otherwise (High/Medium/Low) - show GPS value'Learn more about GPS levels' link. |  |
| ME03-US94-AC04 | 'Initializing GPS' screen should have 2 states:MaximizedMinimized | Zeplin: iOS | Android |
| ME03-US94-AC05 | The app should open Maximized Initializing GPS card by default |  |
| ME03-US94-AC06 | Collapsed 'Initializing GPS' level card should have the following UI elements:Expand buttonGPS level iconCurrent GPS Signal Level titleGPS level and explanatory textCurrent GPS level value |  |
| ME03-US94-AC07 | Maximized 'Initializing GPS' level card should have the following UI elements:Collapse buttonGPS level iconCurrent GPS Signal Level titleGPS level and explanatory textCurrent GPS level value GPS level bar'Is the satellite background...' text and 'Request an update' link |  |
| ME03-US94-AC10 | The GPS level bar should consist of the following UI elements:'Low' label:background color for the 'low' section should be grey (=no background)'medium' (no label, just the section on the scale):background color for the 'medium' value should be magenta'High' label:background color for the 'high' label should be blueGPS signal pinthe GPS signal pin should indicate the dynamic change of the GPS levelScale with values (see ME03-US94-AC13) | Zeplin: iOS | Android |
| ME03-US94-AC11 | The blue dot on the 'GPS signal' pin should have a pulsing animation. |  |
| ME03-US94-AC12 | Current GPS signal strength level should be displayed in grey parenthesis besides high/med/low/no textNote 1: сurrent GPS level should be taken via Bluetooth from the collar. |  |
| ME03-US94-AC13 | The following values should be applied within the barStart point...Final pointGPS signal strength502000, and \>2000 | 50 | 2000, and \>2000 |  |
| 50 | 2000, and \>2000 |
| ME03-US94-AC14 | The mobile app should display all GPS values rounded to 10. |  |
| ME03-US94-AC15 | Current GPS signal strength level should be updated each 1 sec. |  |
| ME03-US94-AC16 | 'Learn more about GPS levels' link should open 'GPS level explanation' screen (see 'Learn more about GPS levels' link -\> 'GPS level explanation' screen) |  |
| Entry point:a user taps on the 'Start Initialization' button in the Onboarding flow OR during Add Collar flowNo GPS signal is received |
| ME03-US94-AC23 | The app should:Show No GPS icon.Show 'No GPS' grey textDisable the GPS level barHide Signal level pin. |  |
| Entry point:a user taps on the 'Start Initialization' button in the Onboarding flow OR during Add Collar flowBluetooth pairing with the collar has not been set up |
| ME03-US94-AC17 | The app should:Display 'Reconnecting With Collar' toastShow spinner instead of GPS icon.Show 'Please move closer to your collar' textDisable the GPS level barHide Signal level pin. | Zeplin: iOS | Android |
| Entry point:The collar’s FW does not support manual GPS calibration featurea user taps on the 'Start Initialization' button in the Onboarding flow OR during Add Collar flow |
| ME03-US94-AC18 | The app should disable the GPS level barThe app should hide 'GPS Signal' pinThe app should not show GPS value in parenthesis. |  |
| Entry point:Initializing GPS screen (Onboarding flow, Add Collar flow) is open |
| ME03-US94-AC19 | PreconditionBluetooth pairing with the collar has been initiated AND the data has been received from the collar every 1 second → BLE connection was lostThe app should:Display 'Reconnecting With Collar' toastShow spinner instead of GPS icon.Show 'Please move closer to your collar' textDisable the GPS level barHide Signal level pin. |  |
| View GPS Signal Levels (smaller screens) |
| ME03-US94-AC20 | UI for small screens is shown in 'Links, design' section (to the right). Note: no difference with bigger screens, this criteria is for reference. |  |
| Entry point:a user taps on the 'Start Initialization' button in the Onboarding flow OR during Add Collar flowCollar doesn't support current GPS |
| ME03-US94-AC23 | The app should disable the GPS level barThe app should hide 'GPS Signal' pinThe app should not show GPS value in parenthesis. |  |
