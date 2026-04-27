---
title: "ME05-FE07. Adjust Emergency Feedback"
sidebar_label: "ME05-FE07. Adjust Emergency Feedback"
sidebar_position: 687
last_modified: "Sep 15, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story |
| TEAM REVIEW |
| Galina Lonskaya, Vadim Pylsky [X], Anastasia Brechko |
| TBD |### User story

\> As an account owner, I want to view the Emergency Feedback screen so that I can set the proper settings for Emergency Feedback.

Content

User story Acceptance criteria Emergency Feedback: entry point Emergency Feedback: UI and data Emergency Feedback: sound mode adjustment Emergency Feedback: vibration mode adjustment Emergency Feedback: static mode adjustment Emergency Feedback: test on collar

### Acceptance criteria

| AC | Text | iOS impl-n status/UI design | Android impl-n status / UI design | Emergency Feedback: entry point | Emergency Feedback: UI and data | Emergency Feedback: sound mode adjustment | Emergency Feedback: vibration mode adjustment | Emergency Feedback: static mode adjustment | Emergency Feedback: test on collar | Emergency Feedback: save settings | Emergency Feedback: Bluetooth connection |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ME05-FE06-AC01 | If I tap on the Emergency Feedback tile at the Feedback Settings screen, then:The Emergency Feedback screen should be displayed with the default or previously chosen mode (Sound or Vibrate or Static), see Pic 1. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC02 | The Emergency Feedback screen should consist of:Back icon"Emergency Feedback" heading"Done" button"Choose a method to correct unsafe behaviors that continue after the warning is received" text"Mode" titleTab with "Sound" icon + "Sound" labelTab with "Vibrate" icon + "Vibrate" label (selected)Tab with "Static" icon + "Static" label (selected)"Level" titleTrack with thumbThumb with the value label"1" value label (the smallest value)"15" value label (the largest value)Tab bar | IOS DONEPic 1 Emergency Feedback with the selected tab | ANDROID TO DOThe same screen as for iOS |
| ME05-FE06-AC03 | By default the following Emergency Feedback settings should be applied:Mode: StaticStatic level: 4 | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC04 | The Sound mode is adjusted as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC05 | The Vibration mode is adjusted as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC06 | The Static mode is adjusted as described in ME05-FE04. Adjust Warning Feedback. | IOS READY | ANDROID TO DO |
| ME05-FE06-AC07 | Testing on Collar process is the same as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC08 | Save Settings process is the same as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
| ME05-FE06-AC09 | The Bluetooth connection process is the same as described in ME05-FE04. Adjust Warning Feedback. | IOS DONE | ANDROID TO DO |
