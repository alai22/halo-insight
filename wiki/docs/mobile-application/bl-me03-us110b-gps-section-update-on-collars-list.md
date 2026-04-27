---
title: "(BL) ME03-US110b. GPS section update on Collar's list"
sidebar_label: "(BL) ME03-US110b. GPS section update on Collar's list"
sidebar_position: 479
last_modified: "Jan 30, 2025"
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-15526 - MOB: Redirect to Initializing GPS screen from Collar's list, Advanced Settings menu updates Closed |
| Click here to expand...As of: 24 Mar 2023 Ekaterina Dupanova created initial draft of the story23 Aug 2023 Ekaterina Dupanova updated the screen in ME03-US110-AC05. UI design is updated due to the bug, see https://softeq.slack.com/archives/C016JEX414M/p1691653939344959?thread_ts=1691583336.255649&cid=C016JEX414M 30 Jan 2025 baselined to ME03-F11 by Galina Lonskaya |# Contents

User story Acceptance criteria

# User story

As a Halo app user I want to be able to View Collar's GPS state at any time so that to make sure the collar is working properly and my pet is safe.

As a Halo app user I want to know when the collar needs calibration and initiate it so as to make sure the collar is working properly.

# Acceptance criteria

| AC | Description | Links, design | As is | To be | As is | To be |
|---|---|---|---|---|---|---|
| 'Collar's List' screen updates |
| ME03-US110-AC05 | Add 'GPS' tile below 'Collar Diagnostic' tile | Zeplin: iOS | Android |
| ME03-US110-AC05 | Precondition: Collar requires initializationThe 'GPS' tile should show:icon on pet avatar on top of the screenicon and 'Initialization required' text'Initialize' button |  |
| ME03-US110-AC06 | Upon clicking on 'Initialize' button, the app redirects to 'GPS Initialization' flow that starts with this screen. |  |
| ME03-US110-AC07 | Precondition: Collar does not require initializationThe app should display satellite position data AND GPS signal icon (states of the icon are listed in ME07-F03-AC12)No changes to the logic of display of Satellite position data that was used in the Advanced Settings menu item, this is for referenceIf the GloExp/GpsEXP date is more than \<Today's date\>, then 'Satellite position data' section contains the following text: '\<number of days till SGEE file expiration\> days remaining' ( Last update: \<date\>)' , e.g. '7 days remaining (Last update: 01.01.2022)' . Where the number of days should be rounded upward and the date format is MM.DD.YYYYWhere:\<number of days till SGEE file expiration\> = \<GloExp/GpsEXP\> - \<Today date\>,GloExp/GpsEXP are expiration date received from the collar on Daily Diagnostics,\<Today date\> is a local date of app user\<date\> is a date of uploading of SGEE file that are currently used by collar | Zeplin |
| ME03-US110-AC08 | No changes to the logic of display of Satellite position data that was used in the Advanced Settings menu item, only UI changes apply:Precondition: the collar's FW doesn't support SGEE feature.The system displays the following items:'GPS' title;'For the greatest location accuracy, please upgrade the firmware of your collar. If your firmware status indicates ‘up-to-date’, please notify Customer Support.' text;Change icon color:As isTo beGrey warning iconChange color of the warning icon: | Grey warning icon | Change color of the warning icon: |  |
| Grey warning icon | Change color of the warning icon: |
| ME03-US110-AC09 | No changes to the logic of display of Satellite position data for that was used in the Advanced Settings menu item, only text and UI changes apply:Precondition: GloExp/GpsEXP date is less than Today date. SGEE data on the collar is outdatedThe system displays the following items:'GPS' title;'No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and leave it powered on while charging.', text Change Icon color:As isTo beGrey warning iconChange color of the warning icon: | Grey warning icon | Change color of the warning icon: | Zeplin: iOS | Android |
| Grey warning icon | Change color of the warning icon: |
