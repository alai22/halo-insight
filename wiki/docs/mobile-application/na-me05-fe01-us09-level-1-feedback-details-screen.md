---
title: "(NA) ME05-FE01-US09: Level 1 Feedback Details Screen"
sidebar_label: "(NA) ME05-FE01-US09: Level 1 Feedback Details Screen"
sidebar_position: 565
last_modified: "May 05, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya, Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-888/ios-level-1-feedback-details |
| 02 May 2025 is created by Galina Lonskaya |### User story

\> As an account owner, I would like to view the Level 1 Feedback screen so that I can set the proper settings for Level 1 Feedback.

Content

User story Acceptance criteria Level 1 Feedback: entry point Level 1 Feedback: UI and data Level 1 Feedback: Sound mode adjustment Level 1 Feedback: Vibration mode adjustment Level 1 Feedback: test on collar Level 1 Feedback: save settings

### Acceptance criteria

| AC | Text | UI Design | Level 1 Feedback: entry point | Level 1 Feedback: UI and data | Level 1 Feedback: Sound mode adjustment | Level 1 Feedback: Vibration mode adjustment | Level 1 Feedback: test on collar | Level 1 Feedback: save settings |
|---|---|---|---|---|---|---|---|---|
| AC01 | If I tap on the Level 1 tile at the Feedback Settings screen, then:The Level 1 screen should be displayed with the default or previously chosen mode (Sound or Vibrate). | Figma |
| AC02 | By default the following Level 1 Feedback settings should be applied:Mode: SoundSound: Attention BeepsVolume: 4 | - |
| AC03 | Sound Slider Bar functionality is described and should be implemented within the separate user story: (NA) ME05-FE01-US02: Sound Bar Slider |  |
| AC04 | If I tap on the Sound, then:Sound List should be opened the is described and should be implemented within the separate user story: TBD | Figma |
| AC08 | If I tap the "Vibration", then the following screen | Figma |
| AC09 | Precondition: Level 1 Feedback screen with the selected Vibration mode is displayed.If I tap on the tile with the Vibration, then:the Vibrations screen should be opened, see (NA) ME05-FE01-US08. Vibration list | Figma |
| AC10 | By default "Quad Tap" should be selected in the Vibration list. |
| AC11 | Precondition: Level 1 Feedback screen is displayed with the Sound or Vibrate tab selected.If I tap on the Test on Collar button, then see the description in(NA) ME05-FE01-US05. 'Test on Collar' button on Feedback Details screen(NA) ME05-FE01-US06. 'Test on Collar' button: error handling |  |
| AC12 | The "Done" button should be enabled, only after I edit something at the Level 1 Feedback screen. |  |
| AC13 | If I tap on the Done button and the Level 1 Feedback saving is performed successfully, then:the Feedback Settings screen should be opened with the updated Level 1 Feedback settings. |  |
| AC14 | If I tap on the Done button and the Level 1 Feedback saving isn't performed successfully, then:Unified error handling mechanism should be applied, see https://linear.app/fueled/issue/HALO-377/ios-unified-error-handling-mechanism-general-rules |  |
| AC15 | If I tap on the Back button and there are no changes at the Level 1 Feedback screen, then:The Feedback Settings screen without changes should be opened. |  |
| AC16 | If I tap on the Back button and there are any changes, then:M50 Unsaved Changes dialog should be shown, Figma |  |
