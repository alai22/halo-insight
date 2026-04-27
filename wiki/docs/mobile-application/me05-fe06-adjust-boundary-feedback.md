---
title: "ME05-FE06. Adjust Boundary Feedback"
sidebar_label: "ME05-FE06. Adjust Boundary Feedback"
sidebar_position: 686
last_modified: "Sep 15, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story |
| TEAM REVIEW |
| Galina Lonskaya, Vadim Pylsky [X], Anastasia Brechko |
| TBD |### User story

\> As an account owner, I would like to view the Boundary Feedback screen so that I can set the proper settings for Boundary Feedback.

Content

User story Acceptance criteria Boundary Feedback: entry point Boundary Feedback: UI and data Boundary Feedback: test on collar Boundary Feedback: save settings

### Acceptance criteria

| AC | Text | iOS impl-n status/UI design | Android impl-n status / UI design | Boundary Feedback: entry point | Boundary Feedback: UI and data | Boundary Feedback: sound mode adjustment | Boundary Feedback: vibration mode adjustment | Boundary Feedback: Static mode adjustment | Boundary Feedback: test on collar | Boundary Feedback: save settings | Boundary Feedback: Bluetooth connection |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ME05-FE06-AC01 | If I tap on the Boundary Feedback tile at the Feedback Settings screen, then:The Boundary Feedback screen should be displayed with the default or previously chosen mode (Sound or Vibrate or Static), see Pic 1. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC02 | The Boundary Feedback screen should consist of:Back icon"Boundary Feedback" heading"Done" button"Choose a method to correct unsafe behaviors that continue after the warning is received" text"Mode" titleTab with "Sound" icon + "Sound" labelTab with "Vibrate" icon + "Vibrate" label (selected)Tab with "Static" icon + "Static" label (selected)"Vibration" title\<Vibration name\> + Right arrow"Test on Collar" button"Test on Collar" buttonTab bar | IOS DONEPic 1 Boundary Feedback with the selected tab | ANDROID TO DOThe same screen as for iOS |
| ME05-FE06-AC03 | By default the following Boundary Feedback settings should be applied:Mode: VibrationVibration: Heart Beat | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC04 | The Sound mode is adjusted as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC05 | The Vibration mode is adjusted as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC06 | If I tap on the "Static" tab, then the following elements should be displayed:Selected "Static" tab"Level" titleTrack with thumbThumb with the value label"1" value label (the smallest value)"15" value label (the largest value)"Test on Collar" button | IOS READYThe same screen as for Android | ANDROID TO DO |
| ME05-FE06-AC07 | The slider should be controlled by clicking the thumb and dragging it (click and drag) or clicking the track (click jump). | IOS READY | ANDROID TO DO |
| ME05-FE06-AC08 | The slider should use 15 invisible spaced tick marks along the slider track, and the thumb should snap to them only. | IOS READY | ANDROID TO DO |
| ME05-FE06-AC09 | The thumb should be displayed with the corresponded value label. | IOS READY | ANDROID TO DO |
| ME05-FE06-AC10 | Static Level 4 should be used by default | IOS READY | ANDROID TO DO |
| ME05-FE06-AC11 | Testing on Collar process is the same as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC12 | Save Settings process is the same as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC13 | The Bluetooth connection process is the same as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
