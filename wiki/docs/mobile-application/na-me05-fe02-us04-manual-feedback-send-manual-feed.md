---
title: "(NA) ME05-FE02-US04. Manual Feedback: Send Manual Feedback to 1 pet"
sidebar_label: "(NA) ME05-FE02-US04. Manual Feedback: Send Manual Feedback to 1 pet"
sidebar_position: 561
author: "Galina Lonskaya"
---

| Document owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-807/[ios]-manual-feedback-send-manual-feedback-to-1-pet HALO-23078 - [iOS] Manual Feedback: Send Manual Feedback to 1 pet Open HALO-23079 - [Android] Manual Feedback: Send Manual Feedback to 1 pet Open |
| 18 Apr 2025 draft is created |# User story

\> As an account owner, I would like to apply a manual feedback so that I can quickly apply prevention or encouragement to train my pet.

Contents

User story Acceptance criteria Implementation Notes The general flow of sending feedback Expiration date

### Acceptance criteria

| AC | Text | UI design |
|---|---|---|
| AC01 | If I tap on any MF button (Recall, Level 1, Level 2, Level 3, Custom 1, Custom 2), then:MF sending should be initiatedthe animation should be startedother UI elements within the action sheet should be disabled. | Figma |
| AC02 | MF should be sent only to pets that are currently reachable and selected. | - |
| AC03 | If MF is initiated and it's possible to send MF via BLE, then:MF should be sent via BLE. | - |
| AC04 | If MF is initiated and the app failed to send MF via BLE, due to the following reasons:the collar is not connected via BLE ORthe collar is connected but not unlocked yetthen:the app should send MF both via the internet and BLE.Note: The app sends feedback via both channels simultaneously. The collar knows how to not play the feedback twice if both channels work. | - |
| AC04 | In case the app failed to send MF via BLE, the mobile app sends it via the internet. It displays the 'success' animation after the command was applied and upon the receipt of the corresponding response from the cloud. | - |
| AC06 | If MF is sent successfully either via BLE or Internet, then: the animation should be completed with a success icon.the 'success' haptic affect should be applied | AnimationFigma |
| AC07 | If MF is failed either via BLE and the Internet, then:the animation should be completed with a failure iconthe 'error' haptic affect should be appliedthe toast message should be shown Note: the separate toast will be used for several pets, see Figma | AnimationFigma |
| Notes:MF events should not be displayed in the Notification list.MF should not depend on the Fences On/Off mode. |### Implementation Notes

Implementation details

Mechanisms of "Manual Feedback" and "Test on Collar" (when setting up feedbacks) work the same way, so they should be implemented in one class.

Our implementation is located in InstantCommandManager - this class basically needs to be replicated, it's difficult to provide all the details in this doc.

Below are the main points.

#### The general flow of sending feedback

If collar firmware does NOT support CorrectionMethodsWithIdAndExpiration:

- If the collar is connected and unlocked via BLE right now - the app tries to perform the request over BLE with 2 seconds timeout
- If the attempt failed or was skipped - the app tries to do that via the Internet
- If the Internet attempt failed - the app tries to repeat the first step again (use BLE if connected&unlocked)

Otherwise:

- The app sends both requests (via the Internet and, if possible, via BLE) simultaneously.
  - Each request contains 2 additional fields:`InstantCommandNumber`and`MobileId`.
    - `InstantCommandNumber`is an integer used by collars to detect duplicated feedback requests. If a collar receives a request via BLE and then one more from BE and they have the same number and mobileID, only the first request will be executed. This number should be stored in a local storage (persistent).
    - `MobileId`is a`short`value retrieved from BE in a response when registering the app instance via`/account/mobile-data`API call. This must be done in parallel with downloading user profile / map data and other data on the app startup. Once`MobileId`is retrieved and saved to a local storage, there is no need to call this endpoint anymore.
    - `InstantCommandNumber`(the next number to be used, i.e. the last used number + 1) and`MobileId`are stored per each collar in a persistent storage. See`MobileDataService.cs`implementation for more details on when to save/update/clean them.

  - If one of requests (BLE or Internet) was executed successfully, the app should try to cancel the second one if it's possible.
    - Note: calls via BLE can only be canceled if they are still in the queue, but it's a BLE Module responsibility to decide that.

  - If one of requests failed, the app should wait for a response to the second request.

- If`OldCommandNumber`error is received via any channel (either BLE or Internet), and the response contains the last used number currently stored on the collar, the app should increment it and try again one more time.
- In any case (step 1 succeeded, or step 1 failed but 2 succeeded, or both steps failed), the app should remember the last used`InstantCommandNumber`+ 1 in the persistent storage.

#### Expiration date

In both scenarios above, when the app uses the Internet channel, it sends expiration date (BE won't send this request to the collar if API call takes too long).

To calculate it, we use estimated server time and add a delay to it:

- To estimate server time, we call`/system/server-date-time`and calculate the difference between the timestamp from the response and (the current time minus half of API call duration). See`TimeService.cs`.
- The delay value can be found in`/configuration`response:`runNegativeCorrectionExpiration`for Level 1/2/3,`runPositiveCorrectionExpiration`for Recall / Custom 1/2.


