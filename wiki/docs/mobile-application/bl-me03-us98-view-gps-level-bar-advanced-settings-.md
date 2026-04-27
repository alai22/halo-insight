---
title: "[BL] ME03-US98. View GPS level bar (Advanced Settings -> 'View' screen)"
sidebar_label: "[BL] ME03-US98. View GPS level bar (Advanced Settings -> 'View' screen)"
sidebar_position: 296
author: "Ekaterina Dupanova"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-15524 - MOB: View GPS level bar (Advanced Settings -\> 'View' option) Closed |
| Click here to expand...As of: 31 Jan 2023 Ekaterina Dupanova created initial draft of the story24 Mar 2023 Ekaterina Dupanovaupdated user story with the latest comments from business 16 Jan 2025 baselined to [BL] ME03-US85. Collar Details: GPS Signal Level Settings |# Contents

User story Acceptance criteria

# User story

As a Halo app user I want to be able to View GPS signal levels so as to make sure that my collar is working properly and my dog is safe.

# Acceptance criteria

| AC | Description | Links, design | As is | To be |
|---|---|---|---|---|
| UI updates for View mode (entry point 'GPS Signal Level Settings' menu (former "Advanced Settings' menu)→ 'Edit' option)Entry point:a user taps on the 'View' menu item in GPS Signal Level Settings menuBluetooth pairing with the collar has been initiated AND the data is received from the collar every 1 secondGPS signal level settings screen opens in View mode |
| ME03-US98-AC01 | UI elements for View mode should be the same as for Initializing GPS screen (including expand/collapse card functionality). Only the below updates should be added:As isTo beInitializing GPSGPS Signal Level SettingsWalk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes).When moving into/out of your house, expect the Halo GPS reading can take up to 15 seconds to adjust. Make sure the collar is ON your dog and oriented properly.Remove'Is the satellite background out of date or is there tree coverage in the way.' text'Request an update' Link'Skip initialization for now' button | Initializing GPS | GPS Signal Level Settings | Walk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). | When moving into/out of your house, expect the Halo GPS reading can take up to 15 seconds to adjust. Make sure the collar is ON your dog and oriented properly. |  | Remove'Is the satellite background out of date or is there tree coverage in the way.' text'Request an update' Link'Skip initialization for now' button | Zeplin: iOS |
| Initializing GPS | GPS Signal Level Settings |
| Walk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). | When moving into/out of your house, expect the Halo GPS reading can take up to 15 seconds to adjust. Make sure the collar is ON your dog and oriented properly. |
|  | Remove'Is the satellite background out of date or is there tree coverage in the way.' text'Request an update' Link'Skip initialization for now' button |
