---
title: "ME05-US64. Add 'Test on Phone' button to Feedback Type screens"
sidebar_label: "ME05-US64. Add 'Test on Phone' button to Feedback Type screens"
sidebar_position: 457
last_modified: "Oct 28, 2024"
author: "Galina Lonskaya"
---

Page info| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Pavel Leonenko Dmitry Kravchuk Oleksii Semelit Anton Zimin [X] Valeria Malets |
| HALO-21409 - MOB: ME05-US64. Add 'Test on Phone' button to Feedback Type screens + 'Volume' label text update Closed |
| 23 Sep 2024 draft user story is created |# User story

\> As Halo app account owner I want to use 'Test on Phone' button on the Edit Feedback Setting screen so that I can play sounds on phone without going to Sound list.

# Acceptance criteria

| AC | Description | UI design | Text Updates |
|---|---|---|---|
| ME05-US64-US01 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration' AND the collar IS linked to this pet'Test on Phone' button should be displayed before 'Test on Collar' button. Notes for DEV/QA:'Test on Phone' button should not be displayed when 'Static' mode is selected (no changes)'Test on Collar' button should still be displayed in the center of the screen when 'Static' mode is selected (no changes) | Figma (Sound selected)Figma (Vibration selected) |
| ME05-US64-US02 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration' AND the collar is NOT linked to this pet'Test on Phone' button should be centered on the screen. Note for DEV/QA: 'Test on Collar' is not displayed in case the collar is not linked to a pet (no changes) | Figma (No Collar Linked) Figma (No Collar Linked) |
| ME05-US64-US03 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration'If I tap on 'Test on Phone' button, then: the standard spinner with an overlay should be displayed over the entire screen while getting the sound to be ready to be playedthe sound should be produced 1 time. Notes for DEV/QA:this is the almost the same logic as used on Sounds listsound should be played in the same volume as set on the phone at the moment (no dependency on Collar Volume level) | - |
| ME05-US64-US04 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration'If I tap on 'Test on Phone' button and sound is not available due to any reason, then: M17 Technical error should be displayed.Notes for DEV/QA:this is the same logic and error as used on Sounds listwe cannot use here unified error handling mechanism, since it's increase the complexity of the user story | - |
| ME05-US64-US05 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound' OR 'Vibration'If I tap on 'Test on Phone' button and the volume is off on the phone, then:the toast message should be displayed for 4 sec: 'Please increase the volume on your mobile device'.Note for DEV/QA:this is the same logic and toast message as used on Sounds list | - |
| ME05-US64-US06 | If the titles 'Test on Phone' and 'Test on Сollar' do not fit, then: they should be truncated with three dotsboth buttons should resize equally to remain the same size. | - |
| ME05-US64-US07 | Precondition: \<Feedback type\> screen with the following selected mode is opened: 'Sound'.'Volume' text label should be changed to 'Collar Volume' text | - |### Amplitude Events

| IN | Description |
|---|---|
| ME05-US64-AI01 | Done within the separate task |
