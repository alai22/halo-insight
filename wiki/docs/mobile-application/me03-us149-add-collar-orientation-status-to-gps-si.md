---
title: "ME03-US149. Add 'collar orientation' status to 'GPS Signal Level Settings' screen"
sidebar_label: "ME03-US149. Add 'collar orientation' status to 'GPS Signal Level Settings' screen"
sidebar_position: 476
last_modified: "Jan 16, 2025"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Pavel Leonenko Vadzim Litvin [X] Valeria Malets |
| HALO-22079 - MOB+[FW]: ME03-US149. Add 'collar orientation' status to 'GPS Signal Level Settings' screen Closed HALO-22125 - BE: Add 'Collar orientation' Zendesk article to a config file Closed |
| Click here to expand...As of 16 Dec 2024 Galina Lonskaya created the initial version of US. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo account owner, I want to view the 'collar orientation' status while viewing the 'GPS Signal Level Settings' screen so that I can ensure the collar is worn correctly and the GPS signal is not affected by improper collar orientation.

# Acceptance criteria

| AC | Description | iOS UI design | Collar Orientation UI | Other changes | AS IS | TO BE |
|---|---|---|---|---|---|---|
| ME03-US149-AC01 | 'Collar Antenna Orientation' section should be added to 'GPS Signal Level Settings' screen. | FigmaNOTE: The UI changes described in this user story were applied in Figma by a BA, not a UI/UX designer. Developer, please make it pixel-perfect yourself, ensuring consistency with the rest of the screen. Check the spacing, alignment, colors, and icon sizes.As we discussed on the ref session, please keep the grey divider above 'Edit GPS signal level settings' screen, please not remove it |
| ME03-US149-AC02 | If the сollar is worn correctly on the dog (GPS antenna is facing upward (orientation_quality: 0 = good)), then: ' Correct (facing sky)' icon + status should be displayed on 'GPS Signal Level Settings' screen. |  |
| ME03-US149-AC03 | If the сollar is worn almost correctly on the dog (GPS antenna is facing sideways (orientation_quality: 1 = in between)), then: ' Nearly Correct (facing side)'icon + status should be displayed on 'GPS Signal Level Settings' screen. |
| ME03-US149-AC04 | If the сollar is worn incorrectly on the dog (GPS antenna is facing downward, orientation_quality: 2 = bad), then: ' Incorrect (facing ground)' icon + status should be displayed on 'GPS Signal Level Settings' screen. |
| ME03-US149-AC05 | If there is no info about collar orientation at the moment, then:' Unavailable ' icon + status should be displayed on 'GPS Signal Level Settings' screen. |
| ME03-US149-AC12 NEW | If there is outdated info about collar orientation (orientation_quality: 3 = undetermined), then:'Analyzing: continue walking with dog' icon + status should be displayed on 'GPS Signal Level Settings' screen. |
| ME03-US149-AC06 | If the collar FW version is outdated and doesn't support 'collar orientation' feature, then: No section with info about collar orientation should be shown on 'GPS Signal Level Settings' screen (note: but ME03-US149-AC10 and ME03-US149-AC11 should be applied). |
| ME03-US149-AC07 | If the mob app version is outdated and doesn't support 'collar orientation' feature, but collar FW version is up-to-date, then: the OLD UI (without any changes described in this user story) should be shown on 'GPS Signal Level Settings' screen. |
| ME03-US149-AC08 | If I tap on 'i' icon displayed next to 'Collar Orientation', then:the following article should be shown: https://support.halocollar.com/hc/en-us/articles/28624506114967-Collar-OrientationNote 1: BE task to add this link to the config: HALO-22125 - BE: Add 'Collar orientation' Zendesk article to a config file Closed Note 2: as of 12/18/2024 the article link is requested from Halo, write them one more time on Jan 2-3, see 'Halo | Article request creation: collar orientation' email |
| ME03-US149-AC09 | The collar orientation status should be synced with collar each 1 sec (If BLE is connected) |
| ME03-US149-AC10 | The following text should be changed on 'GPS Signal Level Settings' screen:AS ISTO BEWhen moving between a high signal area or a low signal area, expect the GPS signal level can take up to 5 seconds to adjust. Make sure the collar is ON your dog and oriented properly. GPS signal level can take up to 5 seconds to adjust. | When moving between a high signal area or a low signal area, expect the GPS signal level can take up to 5 seconds to adjust. Make sure the collar is ON your dog and oriented properly. | GPS signal level can take up to 5 seconds to adjust. | - |
| When moving between a high signal area or a low signal area, expect the GPS signal level can take up to 5 seconds to adjust. Make sure the collar is ON your dog and oriented properly. | GPS signal level can take up to 5 seconds to adjust. |
| ME03-US149-AC11 | 'Learn more about GPS level' link UI should be updated on 'GPS Signal Level Settings' screen. :'Learn more about GPS level' should be removed;'i' icon should be shown next to 'Current GPS Signal Level'. | - |
