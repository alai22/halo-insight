---
title: "(NA) ME05-FE01-US04. 'Test on Phone' button on Feedback Details screens"
sidebar_label: "(NA) ME05-FE01-US04. 'Test on Phone' button on Feedback Details screens"
sidebar_position: 566
last_modified: "May 02, 2025"
author: "Galina Lonskaya"
---

Page info| Story owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-883/ios-test-on-phone-button-on-feedback-details-screens |
| 21 Apr 2025 draft user story is created |# User story

\> As Halo app account owner I want to use 'Test on Phone' button on the Edit Feedback Setting screen so that I can play sounds on phone without going to Sound list.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| AC01 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration' 'Test on Phone' button should be displayed before 'Test on Collar' button in the same row. Notes for DEV/QA:'Test on Phone' button should not be displayed when 'Static' mode is selected | Figma (Sound selected)Figma (Vibration selected) |
| AC02 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration'If I tap on 'Test on Phone' button, then: the spinner should be displayed over button while getting the sound to be ready to be played and playbackthe sound should be produced 1 time. Notes for DEV/QA:sound should be played in the same volume as set on the phone at the moment (no dependency on Collar Volume level) | Figma |
| AC03 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration'If I tap on 'Test on Phone' button and sound is not available due to any reason, then: M17 Technical error should be displayed.Notes for DEV/QA:this is the same logic and error as used on Sounds listwe cannot use here unified error handling mechanism, since it's increase the complexity of the user story | - |
| AC05 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration'If I tap on 'Test on Phone' button and the volume is off on the phone, then:the toast message should be displayed for 4 sec: 'Please increase the volume on your mobile device'.Note for DEV/QA:this is the same logic and toast message as used on Sounds list | Figma |
| AC06 | If the titles 'Test on Phone' and 'Test on Сollar' do not fit, then: they should be truncated with three dotsboth buttons should resize equally to remain the same size. | - |
