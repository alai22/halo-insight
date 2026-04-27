---
title: "[BL] ME03-US92. Update UI on 'Initializing GPS' screen"
sidebar_label: "[BL] ME03-US92. Update UI on 'Initializing GPS' screen"
sidebar_position: 289
author: "Ekaterina Dupanova"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-14700 Closed |
| Click here to expand...As of: 16 Nov 2022 Ekaterina Dupanova created initial draft of the story 01 Dec 2022 Ekaterina Dupanova updated all requirements in the US due to dramatic design changes of the GPS level bar12 Dec 2022 Ekaterina Dupanova removed GPS level bar from requirements as this is a separate scope that should not be included to onboarding MRGP release.As of 16 Dec 2022 Ekaterina Dupanova updated requirements for Zoom value. It turned out that default zoom level of 20 looks bad, so we had to adjust it to 18. Also added the 'crossed' GPS level icon for 'Outdated/disconnected/unknown' statuses to make sure it matches the logic of icons displaying on the Pet Card01/16/2024 baselined to [BL] ME03-US85. Collar Details: GPS Signal Level Settings |# Contents

User story Acceptance criteria

# User story

\> As a Halo app user I want to view a clearer explanation of how to initialize GPS so that I understand how to do it correctly.

# Acceptance criteria

| AC | Description | Links, design | As is | To be | As is | To be | As is | To be | Text | Meaning (for reference) |
|---|---|---|---|---|---|---|---|---|---|---|
| ME03-US92-US02 | Change title: As isTo beInitialize Collar's GPSInitializing GPS | Initialize Collar's GPS | Initializing GPS | iOSAndroid |
| Initialize Collar's GPS | Initializing GPS |
| ME03-US92-US03 | Change location of the text under the title: move to topChange the text:As isTo beMove around until GPS Signal Level is high, and the collar's location is displayed accurately on the map (this may take several minutes).Walk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). | Move around until GPS Signal Level is high, and the collar's location is displayed accurately on the map (this may take several minutes). | Walk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). |  |
| Move around until GPS Signal Level is high, and the collar's location is displayed accurately on the map (this may take several minutes). | Walk around with your collar outdoors where you can see the most open sky. Continue until the GPS Signal Level is High and the collar icon is shown accurately on the map (this may take several minutes). |
| ME03-US92-US05 | Default Zoom level on the map should be set up to 18. |  |
| ME03-US92-US06 | Change view, location and explanatory subtext of the GPS icon:As isTo beTextMeaning (for reference)Please move closer to your collarconnecting to collarNote: meaning is for reference, no change in requirementsHigh Note: no change.GPS signal strength is highNote: meaning is for reference, no change in requirementsMediumNote: no change.GPS signal strength is mediumNote: meaning is for reference, no change in requirementsLowNote: no change.GPS signal strength is lowNote: meaning is for reference, no change in requirementsNo GPS signalNote: no change.No GPS signal / Unknown signalNote: meaning is for reference, no change in requirementsNo DataNoData shows when the collar returns invalid location. In this scenario, no collar pin is shown. |  |  | Please move closer to your collar | connecting to collarNote: meaning is for reference, no change in requirements |  |  | High Note: no change. | GPS signal strength is highNote: meaning is for reference, no change in requirements |  |  | MediumNote: no change. | GPS signal strength is mediumNote: meaning is for reference, no change in requirements |  |  | LowNote: no change. | GPS signal strength is lowNote: meaning is for reference, no change in requirements |  |  | No GPS signalNote: no change. | No GPS signal / Unknown signalNote: meaning is for reference, no change in requirements |  |  | No Data | NoData shows when the collar returns invalid location. In this scenario, no collar pin is shown. |  |
|  |  | Please move closer to your collar | connecting to collarNote: meaning is for reference, no change in requirements |
|  |  | High Note: no change. | GPS signal strength is highNote: meaning is for reference, no change in requirements |
|  |  | MediumNote: no change. | GPS signal strength is mediumNote: meaning is for reference, no change in requirements |
|  |  | LowNote: no change. | GPS signal strength is lowNote: meaning is for reference, no change in requirements |
|  |  | No GPS signalNote: no change. | No GPS signal / Unknown signalNote: meaning is for reference, no change in requirements |
|  |  | No Data | NoData shows when the collar returns invalid location. In this scenario, no collar pin is shown. |
