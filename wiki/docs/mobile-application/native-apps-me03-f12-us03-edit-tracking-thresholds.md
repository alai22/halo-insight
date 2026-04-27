---
title: "(Native apps) ME03-F12-US03. Edit Tracking Thresholds: 'High/Low GPS threshold' bar"
sidebar_label: "(Native apps) ME03-F12-US03. Edit Tracking Thresholds: 'High/Low GPS threshold' bar"
sidebar_position: 498
last_modified: "Mar 26, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links to Jira/Linear tickets | Changes history |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-404/[ios]-edit-tracking-thresholds-manage-highlow-gps-thresholds |
| 28 Feb 2025 draft story created by Galina Lonskaya |# Contents

User story Acceptance criteria

# User story

\> As a Halo app account owner I want to be able to adjust GPS signal levels thresholds so that the GPS status of my collar will be identified more precisely by the collar.

# Acceptance criteria

| AC | Description | Slider Adjustment Logic | Slider Limits: MIN and MAX gaps | Warning when try to exceed the limits for the first time. | Slider Touch Targets |
|---|---|---|---|---|---|
| ME03-F12-US03-AC01 | If Bluetooth connection with the collar has been set up, then:the spinner should be hiddenGPS level bar with 'Low/High GPS' sliders should be shown, see Figma |
| ME03-F12-US03-AC02 | If Bluetooth connection is lost on the 'Edit Tracking Thresholds' screen, then:the following logic should be applied (Native apps) ME03-F12-US05. Edit Tracking Thresholds: Reconnection with collar |
| ME03-F12-US03-AC03 | By default the sliders should be shown in accordance with the last saved 'Low/High GPS' values. Note 1: Low/high values should be taken from the collar directly via BLE. |
| ME03-F12-US03-AC04 | I should be able to drag 'Low/High GPS' sliders manually using 'long press' gesture. |
| ME03-F12-US03-AC05 | If I drag one of 2 sliders, then:the UI of the values with GPS level should be updated, see AC08-11the UI of the sliders should be updated, see AC06-07the green/orange/red band length should be updated accordinglythe corresponding "Return to previous" buttons should become shown, will be implemented within the separate story (Native apps) ME03-F12-US07. Edit Tracking Thresholds: Revert to Previous state |
| ME03-F12-US03-AC06 | If 'Low GPS' slider is long-pressed, then: the 'Low GPS' slider + value should enlarge, see Figma |
| ME03-F12-US03-AC07 | If 'High GPS' slider is long-pressed, then:the 'High GPS' slider + value should enlarge, see Figma |
| ME03-F12-US03-AC08 | 'High GPS' value should rest below the slider by default, see Figma Note: Despite the fact that values were interactive/tappable in the old app, they should not be in the new one, as decided by UI/UX designer. |
| ME03-F12-US03-AC09 | 'High GPS' value should shift above the slider when the 'High GPS' slider is long-pressed for better visibility (see Figma). |
| ME03-F12-US03-AC10 | 'High GPS' value should return below the 'High GPS' slider after long press completed. |
| ME03-F12-US03-AC11 | 'Low GPS' value should rest above the slider all the time, see Figma. |
| ME03-F12-US03-AC12 | If the slider gets between two strokes, then:the slider should be automatically moved to the nearest stroke. |
| ME03-F12-US03-AC13 | If 'Low GPS' and 'High GPS' sliders overlaps each other, then:the latest moved slider should be displayed above the other. |
| ME03-F12-US03-AC14 | 'Low GPS' and 'High GPS' values should be validated by the app, see the details in the tech notes below. |
| ME03-F12-US03-AC15 | I should be able to drag both sliders simultaneously only when one of the sliders surpasses the defined limits (either violating the MIN gap or MAX gap). |
| ME03-F12-US03-AC16 | MIN gap between "low GPS" and "high GPS" should be 50.Note 1: "50" value is configurable on BE.Note 2: Ryan is planning to change a gap from 50 to 100 + No automatic changes should be applied for the users who currently have the gap less than 100 |
| ME03-F12-US03-AC17 | MAX gap between "low GPS" and "high GPS" should be ~60% GPS bar. Note: see more details in the tech notes |
| ME03-F12-US03-AC18 | If I try to move a slider beyond these limits, then:the second slider automatically adjusts, and both sliders move together. The limits should not be violated.M235 popup Figma (see the old reference in Confluence M235 Low and High Thresholds.) should be shown. Note: we need this pop-up to prevent the user from moving the pin further without understanding how this will affect another pin. |
| ME03-F12-US03-AC19 | M235 popup should be shown only once: i.e. when I configure 'High/Low GPS' values for the very first time. Note 1: see more details in the tech notes |
| ME03-F12-US03-AC20 | The information that I have already seen M235 popup should be stored on the mobile side. |
| ME03-F12-US03-AC21 | If I log in to another account from the same device, then:the information should about M235 opening should be deleted by the mobile app. |
| ME03-F12-US03-AC22 | If I remove the Halo app from the device, then:the information should about M235 opening should be deleted by the mobile appNote for Android: AC cannot be irrelevant in case the user agreed not to remove personal data from the device after the app deleting. |
| ME03-F12-US03-AC23 | Touch targets for sliders should be highlighted with a color to indicate where I should tap |
| ME03-F12-US03-AC24 | When sliders move closer together, their touch targets must not overlap but instead remain circular and only touch at the edges. |Tech details

On this screen, BLE connection is mandatory.The Current GPS Level Characteristic - 0x05 is used for both receive and write dataTo use this characteristic, the collar must be in Unlocked statusThis Collar BLE GAP/GATT describes what data we receive from the collar, what data we send, and also uses notifications to get the write status.

The minimum and maximum values on the scale are static - MinGpsLevel = 50 and MaxGpsLevel = 2000. However, we must calculate the actual minimum values after we have obtained the LowerBoundaryFormulaConstant and LowerBoundaryFormulaMultiplierThe formulas are derived from certain rules that are used on the collar to determine the limit of the difference between LowerBoundary and UpperBoundary. The formulas to calculate areMinimalUpperBoundaryGpsValue = (int)((MinDifferenceInGps + LowerBoundaryFormulaConstant) / (1 - LowerBoundaryFormulaMultiplier));MinimalLowerBoundaryGpsValue = MinimalUpperBoundaryGpsValue - MinDifferenceInGps;MinDifferenceInGps is the value we get from the GET /configuration ManualGpsCalibration.MinGapLimit field

Every time the LowerBoundary and UpperBoundary values on the scale are changed, they must be validatedValidation of the value changeIf LowerBoundary changes:

- The maximum difference is calculated by formula:`maxDiffInGpsForUpper = (int)((1 - _lowerBoundaryFormulaMultiplier) * UpperBoundary - _lowerBoundaryFormulaConstant).RoundToLowerTen()`
- If`newLowerBoundary \< MinimalLowerBoundaryGpsValue`, then`LowerBoundary = MinimalLowerBoundaryGpsValue`and`UpperBoundary = MinimalUpperBoundaryGpsValue`
- Else if`UpperBoundary - NewLowerBoundary \<= MinDifferenceInGps`
  - If`newLowerBoundary + MinDifferenceInGps \> MaxGpsLevel,`then`LowerBoundary = MaxGpsLevel - MinDifferenceInGps`,`UpperBoundary = MaxGpsLevel`
  - Else`UpperBoundary = newLowerBoundary + MinDifferenceInGps`,`LowerBoundary = newLowerBoundary`

- Else if`UpperBoundary - newLowerBoundary \> maxDiffInGpsForUpper`, it means that the maximum limit has been violated.
  - If a message is shown to the user
    - Interrupt editing
    - `LowerBoundary = UpperBoundary - maxDiffInGpsForUpper`

  - Else
    - Find`maxDiffInGpsForLowerBoundary = ((int)(((1 - _lowerBoundaryFormulaMultiplier) * lowerBoundary - _lowerBoundaryFormulaConstant) / _lowerBoundaryFormulaMultiplier)).RoundToLowerTen());`
    - `UpperBoundary = newLowerBoundary + maxDiffInGpsForLowerBoundary`,`LowerBoundary = newLowerBoundary`

- Else`LowerBoundary = newLowerBoundary`

If UpperBoundary changes

- The maximum difference is calculated by formula:`maxDiffInGpsForUpper = (int)((1 - _lowerBoundaryFormulaMultiplier) * newUpperBoundary - _lowerBoundaryFormulaConstant).RoundToLowerTen()`
- If`newUpperBoundary \< MinimalUpperBoundaryGpsValue`, then`LowerBoundary = MinimalLowerBoundaryGpsValue`and`UpperBoundary = MinimalUpperBoundaryGpsValue`
- Else if`newUpperBoundary - LowerBoundary \<= MinDifferenceInGps`
  - If`newUpperBoundary - MinDifferenceInGps \< MinGpsLevel`-`LowerBoundary = MinGpsLevel`,`UpperBoundary = MinGpsLevel + MinDifferenceInGps`
  - Else`LowerBoundary = newUpperBoundary - MinDifferenceInGps`,`UpperBoundary = newUpperBoundary`

- Else if`newUpperBoundary - LowerBoundary \> maxDiffInGpsForUpper`, it means that the maximum limit has been violated.
  - If a message is shown to the user
    - Interrupt editing
    - Find`maxDiffInGpsForLowerBoundary = ((int)(((1 - _lowerBoundaryFormulaMultiplier) * LowerBoundary - _lowerBoundaryFormulaConstant) / _lowerBoundaryFormulaMultiplier)).RoundToLowerTen());`
    - `UpperBoundary = LowerBoundary + maxDiffInGpsForLowerBoundar`

  - Else
    - `LowerBoundary = newUpperBoundary - maxDiffInGpsForUpper`,`UpperBoundary = newUpperBoundary`

- Else`UpperBoundary = newUpperBoundary`

In the current implementation, we do not show the popup and do not interrupt the user when we violate MinDifferenceInGps. So when UpperBoundary - LowerBoundary \< MinDifferenceInGps, we need to check if we need to show a message to the user.

The original LowerBoundary and UpperBoundary that are received from the collar must also be checked against the logic for changing valuesThe LowerBoundary and UpperBoundary values may need to be converted to some sort of unit of measure in order to be displayed on the scale on the screen. In this case, the converted values are used for displaying only

In our code all the logic for validating changes can be seen in ManualGpsCalibrationControllerBase. There you can also find more detailed comments on the formulas.


