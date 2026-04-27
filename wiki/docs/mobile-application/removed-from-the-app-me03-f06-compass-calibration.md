---
title: "[Removed from the app] ME03-F06. Compass calibration"
sidebar_label: "[Removed from the app] ME03-F06. Compass calibration"
sidebar_position: 164
author: "Maria Shikareva [X]"
---

| Document status | Test cases status | Document owners | Links to JIRA | Change history |
|---|---|---|---|---|
| REVISED |
| NEED UPDATE as of 06 Aug 2021 |
| Maria Shikareva [X], Pavel Leonenko (MOB), Anastasia Brechko (QA) |
| HALO-7777 - MOB: Compass calibration (+FW dependency) Closed HALO-7883 - MOB: Add a note for Compass calibration on Advanced settings screen Closed HALO-7894 - BE: Add a link to Zendesk for Compass calibration Closed |
| 06 Aug 2021 Maria Shikareva [X] Designs are updated during baselining the following US: [Not implemented] ME03-US61. Add a note for Compass calibration on the "Advanced settings" screen.30 May 2022 Maria Shikareva [X] Baselined [BL] ME03-US64. Use slider for outdoor/indoor threshold adjustment.15 Sep 2022 Maria Shikareva [X] Updated ME03-F06-AC05 based on HALO-12047 - MOB. Compass Calibration. Cancel button is displayed if the Calibration started popup is closed only after calibration Closed . |General description User story Acceptance criteria General flow Bluetooth connection error handling when pairing the app with the collar FW implementation notes

# General description

At the moment there's an issue with compass inside the collar (the collar is constantly re-calibrating its compass), so the Halo team is going to release a new FW version that will no longer calibrate the compass continuously and it's gonna use the compass calibration that was done in the factory (that will fix the issue with the compass). But some users may need to do compass calibration by themselves in the app (if. for example, the factory data gone). There are two ways how they can do it: 1) through a button and LED on the collar (the same as for indoor/ outdoor calibration); 2) create UI in the mobile app (the benefit is that we can also explain what to do): the user taps on a button "Start a compass calibration process", then moving around to configurate until it's done. To speed up the development this can be done as a separate button in the collars list/ new section "Advanced settings" → "Start a compass calibration process", without any screen explanation, the article can be added later.

# User story

\> As an account owner I want to have an opportunity to calibrate compass in the collar in the mobile app when required so that to be able to perform this action on my own.

# Acceptance criteria

| AC | Description | iOS screen design / implementation status | Android screen design / implementation status |
|---|---|---|---|
| General flow |
| ME03-F06-AC01 | When the user taps on the "Calibrate" button on the "Advanced Settings" screen, then:the process of pairing via Bluetooth with the required collar should be started;the overall spinner should be displayed on the "Calibrate" button (instead of the small spinner). | Pic ME03-F06-P01 "Advanced settings" screen with spinnerLink to Zeplin | Link to Zeplin |
| ME03-F06-AC02 | Precondition: Bluetooth pairing with the collar has been initiated.If Bluetooth connection is set up successfully, then the command to the collar should be sent. | - | - |
| ME03-F06-AC03 | Precondition: the command to the collar has been sent.If the command has been sent successfully, then:the compass calibration process should be initiated;the following success message should be displayed:M193 Compass calibration started (assigned collar) → if the collar is assigned to the pet;M194 Compass calibration started (available collar) → if the collar is not assigned to the pet. | Pic ME03-F06-P02 "Advanced settings" screen with 'Cancel' buttonLink to Zeplin | The design for Android is similar to the iOS. |
| ME03-F06-AC04 | Precondition: M193/ M194 message is displayed.When the user taps on the "OK" button, then:the message should be closed;"Advanced settings" screen with the 'Cancel' button instead of a spinner should be displayed (see Pic ME03-F06-P02). | - | - |
| ME03-F06-AC05 | The time-out for displaying the "Cancel" button is 15 seconds from the moment of opening M193/ M194. After this time the "Calibrate" button should be displayed instead. | - | - |
| ME03-F06-AC06 | When the user taps on the "Cancel" button, then:the command to cancel calibration should be sent to the collar;the spinner should be displayed instead of "Cancel" button. | - | - |
| ME03-F06-AC07 | Precondition: the command to cancel calibration is sent to the collar.If the command is sent successfully, then:the compass calibration process should be canceled;the following success message should be displayed: M195 Compass calibration cancelled;the "Calibrate" button should be displayed instead of spinner (only after the user taps "OK" in the M195 Compass calibration cancelled message).Note: if the collar has already finished calibration, the mobile app will not know anything about it (so we're not going to show this info to the user). We will show the M195 Compass calibration cancelled anyway. | - | - |
| ME03-F06-AC08 | If the user leaves the "Advanced Settings" screen/ re-launches the app, then:the connection should be stopped;the "Calibrate" button should be displayed instead of "Cancel".Note for Android: when the user folds the app, the Bluetooth is disconnected.Note for iOS: when the user folds the app, the Bluetooth is not disconnected. | - | - |
| ME03-F06-AC09 | Precondition: the connection was stopped when the user has left the screen/ folded the app.After returning to the screen/ re-launching the app the connection should not be restored. | - | - |
| ME03-F06-AC10 | Precondition: the command to the collar has been sent.If the command sending has failed for some reason, then:the compass calibration should not be started;the error message should be shown: M17 Technical error. | - | - |
| ME03-F06-AC11 | Precondition: the M17 error message is shown.When the user taps on the "OK" button, then:the error message should be closed;the "Advanced settings" screen should be opened with "Calibrate" button displayed (even if the 15 seconds are not over: the mobile app will not track how much time left from those 15 seconds of timeout for "Cancel" button). | - | - |
| ME03-F06-AC12 | The smartphone should keep Bluetooth connection with the collar, but should not restore it if lost. | - | - |
| ME03-F06-AC13 | The mobile app should not wait for the result of compass calibration.Note: if the compass calibration is successfully completed, then the user will get the push-notification (NT40 Compass calibration completed (assigned collar)/ NT41 Compass calibration completed (available collar) → it's already implemented. | - | - |
| ME03-F06-AC14 | The end user can re-calibrate the collar as many times as necessary. | - | - |
| Bluetooth connection error handling when pairing the app with the collar |
| ME03-F06-AC15 | If Bluetooth isn't enabled on the smartphone during the pairing, then the M178 Disabled Bluetooth error message should be displayed. | - | - |
| ME03-F06-AC16 | If the pairing with the required collar isn't successful due the collar isn't found, then the M70. No answer from the collar error message should be displayed. | - | - |
| ME03-F06-AC17 | The timeout for pairing with the collar should be 10 sec. | - | - |
| ME03-F06-AC18 | In case the app fails to unlock the collar with Rolling Codes, then the M124 Security error for provisioning message should be displayed. | - | - |
| ME03-F06-AC19 | If the pairing with the required collar isn't successful due to the communication error, then the M126 Communication error message should be displayed. | - | - |
| ME03-F06-AC20 | If the smartphone is offline when the app connects with the collar and there are no RCs cached, then the M125 Connection error message should be displayed. | - | - |
| ME03-F06-AC21 | Precondition: one of the error messages described in ME03-F06-AC17 — ME03-F06-AC22 is displayed.When the user taps on "OK" button ("Cancel" button in the M125 Connection error), then:the popup should be closed;the connection process should be stopped;"Advanced settings" screen should be opened (see Pic ME03-F06-P02). | - | - |
| ME03-F06-AC22 | Precondition: M125 Connection error is displayed.When the user taps on "Try Again" button, then:the popup should be closed;the connection process should be initiated again. | - | - |
| ME03-F06-AC23 | "Learn more" should be a link to a Zendesk article on how the collar compass can be calibrated. The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/4404268910231. |  |  |# FW implementation notes

| IN | Description |
|---|---|
| ME03-F06-IN01 | The collar should no longer save calibration data to the 0:\ drive repeatedly (as it used to save all the time previously). |
| ME03-F06-IN02 | The collar should save "manual" calibration results to the 2:\ drive. |
| ME03-F06-IN03 | On boot-up, the collar should load calibration data from the disk:first from the 2:\ drive (where user calibration results are saved);then from the 1:\ drive (where the factory results are saved). |
| ME03-F06-IN04 | After boot-up, automatic calibration should be continuously performed 'in the background', all the results should be saved to RAM only. |
| ME03-F06-IN05 | If there's 'magnetic' interference (note: the collar can now detect it), the following should happen:Background calibration process should be paused (it's made so that 'bad' data is not fed into calibration library);Heading should be considered 'invalid' and - therefore - previous/ last heading should be used until interference goes away. |
| ME03-F06-IN06 | The collar sends NT38 Compass calibration required (assigned collar)/ NT39 Compass calibration required (available collar) push-notifications in the following cases:when the collar doesn't have data about compass calibration;when the collar has data about compass calibration and/or the user starts Calibration process manually from the app. |
