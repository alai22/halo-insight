---
title: "ME03-US49. FW: Collar calibration process (phase 1)"
sidebar_label: "ME03-US49. FW: Collar calibration process (phase 1)"
sidebar_position: 128
last_modified: "Jun 18, 2021"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| APPROVED |
| Galina Lonskaya, Egor Dolgalev, Anastasia Brechko |
| HALO-6294 - Manual Calibration Process Closed |# User story

\> As an account owner, I want to perform 'indoor'/'outdoor' calibration so that my collar can better determine 'indoor'/'outdoor' location.

# Acceptance criteria

| AC | Description | Source requirement | Overall logic | Calibration process | Calibration process manual cancelling | Calibration re-running | Delete 'outdoor'/'indoor' calibration data set | Help Center |
|---|---|---|---|---|---|---|---|---|
| ME03-US49-AC01 | Default 'outdoor'/'indoor' calibration level should be applied for all collars by default. The collars with the default 'outdoor'/'indoor' calibration level should be considered as 'calibrated'.Note 1: 'Default' calibration level will be calculated by Egor. | - |
| ME03-US49-AC02 | If the collar has the 'SatTreshhold' parameter, then: the collar should be considered as 'not calibrated' (default 'outdoor'/'indoor' calibration level should be applied for this collar).Tech note: 'SatTreshhold' (Collars→Configuration→SatThreshold). This is a parameter from the backend server which is used now to adjust collars with indoors/outdoors problems. We will reuse this parameter for new algorithm to force the user to calibrate the collar because we expect to have the same problem without calibration. | - |
| ME03-US49-AC03 | If the collar is not calibrated, then:GPS LED should be blinking red during the whole time when the collar isn't calibrated, see the blinking pattern description in ME03-US49-AC27. | - |
| ME03-US49-AC27 | If the collar isn't calibrated, then GPS LED should be blinking following the normal tempo that used on the collar: 100msec ON, 900msec OFF (when not paired over BLE); and 900msec ON, 100msec OFF (when paired over BLE). | - |
| ME03-US49-AC02, AC03, AC27 are postponed. It was discussed by Egor and Michael on FW call on February 12 2021. |
| ME03-US49-AC04 | Phase 1 restriction: One 'outdoor'/'indoor' calibration data set will be used for all fences stored on the collar.Note: From Michael's perspective it might be easy to store calibration data for several fences. But it's difficult to remove the calibration data. Egor agreed with this, but at the moment we are following the described restriction. | - |
| Step 0 Calibration process initiation |
| ME03-US49-AC05 | The calibration process can be initiated by the end user in case all of the following conditions are satisfied:the collar should not be in any 'calibration mode 'state, see the states below;the collar should be plugged into power.Note: Calibrating 'calculations' do not begin until AFTER collar is removed from power. | - |
| ME03-US49-AC06 | In case the conditions described in ME03-US49-AC05 are satisfied and the end user presses ON button three times within 2 sec, then:the beep signal and vibration should be produced onсe by the collar, see the pattern details in Table 1 - Collar interfaces in calibration mode;'waiting for unplugging/calibration start' state should be enabled on the collar;GPS LED should remain blinking and continue in 'waiting for unplugging/calibration start' and while in "calibration mode", see the blinking pattern description in ME03-US49-AC26; | - |
| ME03-US49-AC26 | GPS LED in 'waiting for unplugging/calibration start' and while in "calibration mode" should be blinking red following the special tempo: 1 sec - ON, 1 sec - OFF. | - |
| Step 1 Waiting for unplugging/'quick indoor' calibration start |
| ME03-US49-AC29 | If the collar is in 'waiting for unplugging/calibration start' state more than 3 min and still plugged into the power, then: the calibration should be canceled, the same steps as for manual canceling should be applied next, see ME03-US49-AC22. | - |
| ME03-US49-AC30 | Precondition: The collar is in 'waiting for unplugging/calibration start' state.If the collar is unplugged from the power, then:GPS LED should remain blinking and continue during the whole calibration process, see the blinking pattern description in ME03-US49-AC26;Logo LED should start blinking and continue during the whole calibration process, see the details related to LED color in ME03-US49-AC07 and AC28;the 'quick indoor' calibration should be started, see the indoor calibration process description starting from ME03-US49-AC31. | - |
| ME03-US49-AC07 | Logo LED while being in 'calibration mode' should apply the following logic : the end user is calibrating 'indoors'→ whitethen end user should switch locations (indoor → outdoor or outdoor → indoor)→ magenta colorthe end user is calibrating 'outdoors'→ blue color | - |
| ME03-US49-AC28 | Logo LED in 'calibration mode' should be blinking following the special tempo: 900 ms - ON, 100 ms - OFF. | - |
| ME03-US49-AC08 | Logo LED/GPS LED should be blocked for the other feature usage when the collar is in calibration mode. | - |
| ME03-US49-AC09 | Speaker should be blocked for the other feature usage when the collar is in calibration mode. | - |
| ME03-US49-AC10 | Feedback feature should be disabled when the collar is in calibration mode. | - |
| ME03-US49-AC40 | GPS power saving feature should be disabled when the collar is in calibration mode. |  |
| Step 2 'Quick indoor' calibration before 'outdoor' calibration start |
| ME03-US49-AC31 | 'Quick indoor' calibration process should have 1 min of motion time starting at the time that the collar is unplugged. Duration of the frame for motion data gathering: 3 min.Note: timeout time is updated on April 1, 21. | - |
| ME03-US49-AC32 | The collar should auto adjust 'indoor' thresholds during the indoor calibration process while the collar is moving. | - |
| ME03-US49-AC33 | The end user with the collar in the hands should be moving around being 'indoor' during the 'indoor' calibration process.Note: this AC is mandatory, since the collar will not be able to update the threshold while the collar is stationary. | - |
| Step 3 Quick Indoor mode calibration completion |
| ME03-US49-AC34 | If the 'quick indoor' calibration is completed, then: the collar should keep beeping each 1 sec till the 'outdoor' calibration process will be started, see the start details in ME03-US49-AC37. | - |
| ME03-US49-AC36 | In case for 2 min the 'quick indoor' calibration data in motion wasn't gathered (less then 1 min of motion), then:the calibration should be canceled, the same steps as for manual canceling should be applied next, see ME03-US49-AC22. | - |
| Step 4 Outdoor mode calibration process |
| ME03-US49-AC37(added on March 3) | If the end user presses ON button once within 3 min after 'quick indoor' calibration completion, then:the 'outdoor' calibration process should be started. |  |
| ME03-US49-AC15 | If the 'outdoor' calibration isn't started within 3 min after 'quick indoor' calibration completion, then:the calibration should be canceled; the same steps as for manual canceling should be applied next, see ME03-US49-AC22. | - |
| ME03-US49-AC16 | 'Outdoor' calibration process should have 2 min of motion time. Duration of the frame for motion data gathering: 4 min. | - |
| ME03-US49-AC17 | The collar should auto adjust 'outdoor' thresholds during the 'outdoor' calibration process while the collar is moving. | - |
| ME03-US49-AC18 | The end user with the collar in the hands should be moving around being 'outdoors' during the outdoor calibration process.Note: this AC is mandatory, since the collar will not be able to update the threshold while the collar is stationary. | - |
| Step 5 Outdoor mode calibration completion |
| ME03-US49-AC19 | In case for 4 min the 'outdoor' calibration data in motion wasn't gathered (less then 2 min of motion), then:the calibration should be canceled, the same steps as for manual canceling should be applied next, see ME03-US49-AC22. | - |
| ME03-US49-AC20 | If the 'outdoor' calibration is completed, then: the collar should keep beeping each 1 sec till the 'indoor' calibration process will be started, see the start details in ME03-US49-AC38. | - |
| Step 6 Indoor calibration process |
| ME03-US49-AC38(added on March 3) | If the end user presses ON button once within 3 min after 'outdoor' calibration completion, then:the 'indoor' calibration process should be started. |  |
| ME03-US49-AC11 | Indoor calibration process should have 2 min of motion time starting at the time that the 'outdoor' calibration has been completed. Duration of the frame for motion data gathering: 4 min. | - |
| ME03-US49-AC12 | The collar should auto adjust 'indoor' thresholds during the indoor calibration process while the collar is moving. | - |
| ME03-US49-AC13 | The end user with the collar in the hands should be moving around being 'indoor' during the 'indoor' calibration process.Note: this AC is mandatory, since the collar will not be able to update the threshold while the collar is stationary. | - |
| Step 7 Indoor mode calibration completion |
| ME03-US49-AC35 | In case for 4 min the 'indoor' calibration data in motion wasn't gathered (less then 2 min of motion), then:the calibration should be canceled, the same steps as for manual canceling should be applied next, see ME03-US49-AC22. | - |
| ME03-US49-AC14 | If the 'indoor' calibration is completed, then: the collar should save settings, see the details in ME03-US49-AC21. | - |
| Step 8 Collar saves settings |
| ME03-US49-AC21 | After the calibration process completes successfully, the following behavior should be applied: сollar should consider itself as 'calibrated';сollar should make a long beep and 1 sec vibration, see the pattern details in Table 1 - Collar interfaces in calibration mode;Collar should report 'GPS Calibration Completed' to backend; Logo LED/GPS LED/Speaker should be reverted to normal behavior;Feedback feature should be reverted to normal behavior;Power saving feature should be reverted to normal behavior;Thresholds should be saved in collar memory (FFS) along with fence ID, last GPS coordinate (If there were settings already [for that fence], then previous settings are overwritten);Collar should stop adjusting thresholds; uses saved thresholds. | - |
| ME03-US49-AC22 | If the collar is in 'waiting for unplugging/calibration start'/ 'calibration mode' and the end user presses ON button 2 times within 2 sec, then:сollar should make a beep signal and 1 sec vibration, see the pattern details in Table 1 - Collar interfaces in calibration mode;the calibration process should be stopped;the collar should report 'GPS Calibration Completed' to backend (existing UI on app)Logo LED/GPS LED/Speaker should be reverted to normal behavior;Feedback feature should be reverted to normal behavior;Power saving feature should be reverted to normal behavior;Thresholds should be loaded from collar memory (FFS) [if needed] or use default if there are no any data saved on FFS;Collar should stop adjusting thresholds; use the loaded thresholds. | - |
| ME03-US49-AC23 | The end user can re-calibrate the collar as many times as necessary. See the details in ME03-US49-AC04 | - |
| ME03-US49-AC24 | Phase 1 restriction: the 'outdoor'/'indoor' calibration data set cannot be deleted by the end user.Note: If the end user wants to change the 'outdoor'/'indoor' calibration data set, then she/he should re-run calibration, see ME03-US49-AC23. | - |
| ME03-US49-AC25 | If all fences are deleted, then the 'outdoor'/'indoor' calibration data set should not be deleted. | - |
| Note: Assumed that new Help Center article for Halo app users with this calibration process description will be created. |#### Table 1 - Collar interfaces in calibration mode

| Calibration stage/step | Speaker | Vibration motor | Logo LED | GPS LED |
|---|---|---|---|---|
| 'calibration start' | 1 beep (#define tone_pattern_1 \{ 10, 0 \}) | 200 ms vibration | Normal state | Normal state |
| 'waiting for unplugging/calibration calculation start' | - | - | Normal state | Blinking red;Tempo: 1 sec - ON, 1 sec - OFF. |
| 'Quick indoor' calibration before 'outdoor' calibration start | - | - | Blinking white/magenta/blue, see AC07;Tempo: 900 ms - ON, 100 ms - OFF. |
| 'waiting for the start of 'outdoor' calibration | 1 beep per 1 sec \{ 50, 0 \} | 200 ms vibration per 1 sec |
| 'outdoor' calibration process | - | - |
| 'waiting for the start of 'indoor' calibration | 1 beep per 1 sec \{ 50, 0 \} | 200 ms vibration per 1 sec |
| 'indoor' calibration process | - | - |
| 'calibration' canceling (both manual and timeout) | 'fail' tone (#define tone_pattern_2 \{ 5, 5, 10, 0 \}) | 100 ms vibration, 100 ms pause, 100ms vibration | Back to normal state | Back to normal state |
| 'calibration' success | 'pass' tone (#define tone_pattern_4 \{ 100, 0 \}) | 2000 ms vibration | Back to normal state | Back to normal state |
