---
title: "ME03-F05. Battery Details"
sidebar_label: "ME03-F05. Battery Details"
sidebar_position: 625
last_modified: "Mar 19, 2025"
author: "Mariya Kolyada"
---

| Document owners | Linear/Jira ticket | History of changes |
|---|---|---|
| Mariya Kolyada Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-337/[ios]-battery-details |
| 06 Feb 2025 draft user story is created by Mariya Kolyada 10 Feb 2025 Mariya Kolyada updated story by adding new designs / text description.18 Feb 2025 Mariya Kolyada final updates after added tech details and designs. |User story: As Halo app account owner, I want to access Collar Battery Details so I know how long can I rely on the collar.

Tech details: The data used is the same as here. ME03-F01-US05. Collar Details: Battery section. (Tech detail section). Average battery life taken from Collar Diagnostiс

Acceptance Criteria:

All screen designs: Figma

| AC | Description | Screenshot to understand what part of the screen included in AC | AC | Remaining battery life | Battery charging level | Battery has catastrophic issues | No Collar Diagnostic for more than 30 days | No | Yes | AC | Condition | Design | AC | Condition | Design |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AC01 | App should display the following elements by following the rulesImageRemaining battery data (format BR-23 Battery level in time units)Details/recommendationsby following the rules:ACRemaining battery lifeBattery charging levelBattery has catastrophic issuesNo Collar Diagnostic for more than 30 daysNoYesAC01-1\> 1.5 h76-100%FigmaFigmaDisplay the 'Grey Triangle' on top of the appropriate battery icon.Replace the long text below the title.If user taps 'Halo Dog Park' link, then the app should open the 'Dog Park Areas' screen.'Dog Park Areas' will be implemented later HALO-247, the placeholder screen should be shown for now.FigmaAC01-251-75%FigmaAC01-326-50%FigmaAC01-44-25%FigmaAC01-5\<=1.5 h-FigmaDisplay 'Grey Triangle' on top of the almost discharged/fully discharged battery icon.No long text changing.AC01-6battery is discharged (expected discharge time \< current date)* See Tech details aboveFigmaAC01-7chargingFigmaFigma Same logic as if collar has some battery level (see above).AC01-8unknown* No telemetry has been received yet or BE returned telemetry without battery levelScreen is Impossible to open from collar details | AC01-1 | \> 1.5 h | 76-100% | Figma | Figma | Display the 'Grey Triangle' on top of the appropriate battery icon.Replace the long text below the title.If user taps 'Halo Dog Park' link, then the app should open the 'Dog Park Areas' screen.'Dog Park Areas' will be implemented later HALO-247, the placeholder screen should be shown for now.Figma | AC01-2 | 51-75% | Figma | AC01-3 | 26-50% | Figma | AC01-4 | 4-25% | Figma | AC01-5 | \<=1.5 h | - | Figma | Display 'Grey Triangle' on top of the almost discharged/fully discharged battery icon.No long text changing. | AC01-6 | battery is discharged (expected discharge time \< current date)* See Tech details above | Figma | AC01-7 | charging | Figma | Figma | Same logic as if collar has some battery level (see above). | AC01-8 | unknown* No telemetry has been received yet or BE returned telemetry without battery level | Screen is Impossible to open from collar details | All possible image states depending on battery level and other conditions: Figma |
| AC01-1 | \> 1.5 h | 76-100% | Figma | Figma | Display the 'Grey Triangle' on top of the appropriate battery icon.Replace the long text below the title.If user taps 'Halo Dog Park' link, then the app should open the 'Dog Park Areas' screen.'Dog Park Areas' will be implemented later HALO-247, the placeholder screen should be shown for now.Figma |
| AC01-2 | 51-75% | Figma |
| AC01-3 | 26-50% | Figma |
| AC01-4 | 4-25% | Figma |
| AC01-5 | \<=1.5 h | - | Figma | Display 'Grey Triangle' on top of the almost discharged/fully discharged battery icon.No long text changing. |
| AC01-6 | battery is discharged (expected discharge time \< current date)* See Tech details above | Figma |
| AC01-7 | charging | Figma | Figma | Same logic as if collar has some battery level (see above). |
| AC01-8 | unknown* No telemetry has been received yet or BE returned telemetry without battery level | Screen is Impossible to open from collar details |
| AC02 | App should display the Battery Health Status by following the rules:ACConditionDesignAC02-1No battery issues in Collar DiagnosticsFigmaAC02-2There are battery issues in Collar DiagnosticsFigmaAC02-3No Collar Diagnostic in more than 30 days or no data yetFigma | AC02-1 | No battery issues in Collar Diagnostics | Figma | AC02-2 | There are battery issues in Collar Diagnostics | Figma | AC02-3 | No Collar Diagnostic in more than 30 days or no data yet | Figma |  |
| AC02-1 | No battery issues in Collar Diagnostics | Figma |
| AC02-2 | There are battery issues in Collar Diagnostics | Figma |
| AC02-3 | No Collar Diagnostic in more than 30 days or no data yet | Figma |
| AC03 | App should display the Average Battery Life by following the rules:ACConditionDesignAC03-1No average battery life FigmaAC04-2Battery life has invalid values* less than 6 hours and more than 42 hoursAC05-3No Collar Diagnostics in more than 30 days or no data yetAC07-4Average battery life based on the latest 7 days data received via Collar DiagnosticFigma | AC03-1 | No average battery life | Figma | AC04-2 | Battery life has invalid values* less than 6 hours and more than 42 hours | AC05-3 | No Collar Diagnostics in more than 30 days or no data yet | AC07-4 | Average battery life based on the latest 7 days data received via Collar Diagnostic | Figma |  |
| AC03-1 | No average battery life | Figma |
| AC04-2 | Battery life has invalid values* less than 6 hours and more than 42 hours |
| AC05-3 | No Collar Diagnostics in more than 30 days or no data yet |
| AC07-4 | Average battery life based on the latest 7 days data received via Collar Diagnostic | Figma |
| AC04 | If user taps the 'View Disgnostic' button, then the app should open the Collar Diagnostics screen. | - |
| AC05 | If there is NO Battery-related catastrophic issues in Collar Diagnostics, then the app should hide the 'View Diagnostic' button. | - |
| AC05 | User can open the 'Need Help?' screen on the 'Questionmark' icon' tap on the header of the Collar Diagnostics screen. The functionality should be implemented later within a separate user story: HALO-220 | - |
| AC06 | If there is NO Remaining battery data in seconds, then the app should replace all time values with percentages. | - |
