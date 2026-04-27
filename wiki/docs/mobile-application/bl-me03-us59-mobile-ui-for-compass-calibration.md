---
title: "[BL] ME03-US59. Mobile UI for compass calibration"
sidebar_label: "[BL] ME03-US59. Mobile UI for compass calibration"
sidebar_position: 154
last_modified: "Jul 26, 2021"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED (SQ) |
| Maria Shikareva [X], Pavel Leonenko (MOB), Anastasia Brechko (QA) |
| HALO-7777 - MOB: Compass calibration (+FW dependency) Closed Ballpark estimations:MOB: 2-3SPQA MOB: 3SP |
| 14 Jul 2021, 15 Jul 2021 Maria Shikareva [X] Changes are highlighted in blue (while development it turned out that it's easier to have a connection with the collar all the time but not restore it if lost):ME03-US59-AC09, ME03-US59-AC10, ME03-US59-AC11, ME03-US59-AC13, ME03-US59-AC14 are updated;ME03-US59-AC25 is added.20 Jul 2021 Maria Shikareva [X] Added FW implementation notes (based on "Compass Calibration - Final" email from 19 Jul 2021 .23 Jul 2021 Maria Shikareva [X] ME03-US59-IN06 is added after FW daily 23 Jul 2021 (for more clarity how the collar sends push-notifications).26 Jul 2021 Maria Shikareva [X] The story is marked as baselined (see [Removed from the app] ME03-F06. Compass calibration). |General description User story Acceptance criteria Bluetooth connection error handling when pairing the app with the collar FW implementation notes

# General description

At the moment there's an issue with compass inside the collar (the collar is constantly re-calibrating its compass), so the Halo team is going to release a new FW version that will no longer calibrate the compass continuously and it's gonna use the compass calibration that was done in the factory (that will fix the issue with the compass). But some users may need to do compass calibration by themselves in the app (if. for example, the factory data gone). There are two ways how they can do it: 1) through a button and LED on the collar (the same as for indoor/ outdoor calibration); 2) create UI in the mobile app (the benefit is that we can also explain what to do): the user taps on a button "Start a compass calibration process", then moving around to configurate until it's done. To speed up the development this can be done as a separate button in the collars list/ new section "Advanced settings" → "Start a compass calibration process", without any screen explanation, the article can be added later.

# User story

\> As an account owner I want to have an opportunity to calibrate compass in the collar in the mobile app when required so that to be able to perform this action on my own.

# Acceptance criteria

| AC | Description | iOS screen design / implementation status | Android screen design / implementation status | Bluetooth connection error handling when pairing the app with the collar |
|---|---|---|---|---|
| ME03-US59-AC01 | "Advanced Settings" icon should be added for every collar in the expanded list on the Collars list.Note: all other elements should remain the same as described in ME03-F01. Collars list. | Pic ME03-US59-P01 "Advanced settings" icon | Android |
| ME03-US59-AC02 | When the user taps on the "Advanced settings" icon, then the "Advanced settings" screen should be opened with the following UI elements:"Back" icon;'Advanced Settings' title;'Compass Calibration' section:'Compass Calibration' title;"Calibrate" button (see the details in ACs below);'Indoor/Outdoor Settings' title (for more details see ME03-US55. Open 'Indoor/Outdoor configuration' article from the expanded collar card). | Pic ME03-US59-P02 "Advanced settings" screen | Android |
| ME03-US59-AC03 | When the user taps on the "Back" icon, then the "Collars" screen should be opened with the expanded collar card that was shown before opening of the "Advanced Settings" screen. | - | - |
| ME03-US59-AC04 | When the user taps on the "Calibrate" button, then:the process of pairing via Bluetooth with the required collar should be started;the spinner should be displayed instead of the "Calibrate" button. | Pic ME03-US59-P03 "Advanced settings" screen with spinner | Android |
| ME03-US59-AC05 | Precondition: Bluetooth pairing with the collar has been initiated.If Bluetooth connection is set up successfully, then the command to the collar should be sent. | - | - |
| ME03-US59-AC06 | Precondition: the command to the collar has been sent.If the command has been sent successfully, then:the compass calibration process should be initiated;the following success message should be displayed:M193 Compass calibration started (assigned collar) → if the collar is assigned to the pet;M194 Compass calibration started (available collar) → if the collar is not assigned to the pet. | Pic ME03-US59-P04 "Advanced settings" screen with 'Cancel' button | The design for Android is similar to the iOS. |
| ME03-US59-AC07 | Precondition: M193/ M194 message is displayed.When the user taps on the "OK" button, then:the message should be closed;"Advanced settings" screen with the 'Cancel' button instead of a spinner should be displayed (see Pic ME03-US59-P04). | - | - |
| ME03-US59-AC08 | The time-out for displaying the "Cancel" button is 10 seconds. After this time the "Calibrate" button should be displayed instead. | - | - |
| ME03-US59-AC09 | When the user taps on the "Cancel" button, then:the command to cancel calibration should be sent to the collar;the spinner should be displayed instead of "Cancel" button. |  |  |
| ME03-US59-AC10 | Precondition: the command to cancel calibration is sent to the collar.If the command is sent successfully, then:the compass calibration process should be canceled;the following success message should be displayed: M195 Compass calibration cancelled;the "Calibrate" button should be displayed instead of spinner (only after the user taps "OK" in the M195 Compass calibration cancelled message).Note: if the collar has already finished calibration, the mobile app will not know anything about it (so we're not going to show this info to the user). We will show the M195 Compass calibration cancelled anyway. |  |  |
| ME03-US59-AC11 | If the user leaves the "Advanced Settings" screen/ re-launches the app, then:the connection should be stopped;the "Calibrate" button should be displayed instead of "Cancel".Note for Android: when the user folds the app, the Bluetooth is disconnected.Note for iOS: when the user folds the app, the Bluetooth is not disconnected. |  |  |
| ME03-US59-AC25 | Precondition: the connection was stopped when the user has left the screen/ folded the app.After returning to the screen/ re-launching the app the connection should not be restored. |  |  |
| ME03-US59-AC12 | Precondition: the command to the collar has been sent.If the command sending has failed for some reason, then:the compass calibration should not be started;the error message should be shown: M17 Technical error. |  |  |
| ME03-US59-AC13 | Precondition: the M17 error message is shown.When the user taps on the "OK" button, then:the error message should be closed;the "Advanced settings" screen should be opened (see Pic ME03-US59-P02) with "Calibrate" button displayed (even if the 10 seconds are not over: the mobile app will not track how much time left from those 10 seconds of timeout for "Cancel" button). |  |  |
| ME03-US59-AC14 | The smartphone should not keep Bluetooth connection with the collar, but should not restore it if lost. | - | - |
| ME03-US59-AC15 | The mobile app should not wait for the result of compass calibration.Note: if the compass calibration is successfully completed, then the user will get the push-notification (NT40 Compass calibration completed (assigned collar)/ NT41 Compass calibration completed (available collar) → it's already implemented. |  |  |
| ME03-US59-AC16 | The end user can re-calibrate the collar as many times as necessary. | - | - |
| ME03-US59-AC17 | If Bluetooth isn't enabled on the smartphone during the pairing, then the M178 Disabled Bluetooth error message should be displayed. | - | - |
| ME03-US59-AC18 | If the pairing with the required collar isn't successful due the collar isn't found, then the M70. No answer from the collar error message should be displayed. | - | - |
| ME03-US59-AC19 | The timeout for pairing with the collar should be 10 sec. | - | - |
| ME03-US59-AC20 | In case the app fails to unlock the collar with Rolling Codes, then the M124 Security error for provisioning message should be displayed. | - | - |
| ME03-US59-AC21 | If the pairing with the required collar isn't successful due to the communication error, then the M126 Communication error message should be displayed. |  |  |
| ME03-US59-AC22 | If the smartphone is offline when the app connects with the collar and there are no RCs cached, then the M125 Connection error message should be displayed. |  |  |
| ME03-US59-AC23 | Precondition: one of the error messages described in ME03-US59-AC17 — ME03-US59-AC22 is displayed.When the user taps on "OK" button ("Cancel" button in the M125 Connection error), then:the popup should be closed;the connection process should be stopped;"Advanced settings" screen should be opened (see Pic ME03-US59-P02). | - | - |
| ME03-US59-AC24 | Precondition: M125 Connection error is displayed.When the user taps on "Try Again" button, then:the popup should be closed;the connection process should be initiated again. |  |  |# FW implementation notes

| IN | Description |
|---|---|
| ME03-US59-IN01 | The collar should no longer save calibration data to the 0:\ drive repeatedly (as it used to save all the time previously). |
| ME03-US59-IN02 | The collar should save "manual" calibration results to the 2:\ drive. |
| ME03-US59-IN03 | On boot-up, the collar should load calibration data from the disk:first from the 2:\ drive (where user calibration results are saved);then from the 1:\ drive (where the factory results are saved). |
| ME03-US59-IN04 | After boot-up, automatic calibration should be continuously performed 'in the background', all the results should be saved to RAM only. |
| ME03-US59-IN05 | If there's 'magnetic' interference (note: the collar can now detect it), the following should happen:Background calibration process should be paused (it's made so that 'bad' data is not fed into calibration library);Heading should be considered 'invalid' and - therefore - previous/ last heading should be used until interference goes away. |
| ME03-US59-IN06 | The collar sends NT38 Compass calibration required (assigned collar)/ NT39 Compass calibration required (available collar) push-notifications in the following cases:when the collar doesn't have data about compass calibration;when the collar has data about compass calibration and/or the user starts Calibration process manually from the app. |
