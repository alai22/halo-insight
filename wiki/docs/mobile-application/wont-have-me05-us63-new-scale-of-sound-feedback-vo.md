---
title: "[Won't have] ME05-US63. New scale of sound feedback volume"
sidebar_label: "[Won't have] ME05-US63. New scale of sound feedback volume"
sidebar_position: 428
last_modified: "Jul 22, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issues | History of changes |
|---|---|---|---|
| DRAFT |
| Mariya Kolyada |
| HALO-19579 - MOB, BE, FW: HC4: New scale of sound feedback volume Resolved |
| Click here to expand...As of 01 Jul 2024 :Mariya Kolyadacreated the initial version of US. |### User story

\> As an account owner, I would like to be able to set higher feedback volume for Halo 4 collar so that my dog respond better to feedback and I can here myself if my dog recieved feedback.

Content

User story Acceptance criteria Warning Feedback: UI and data

### Acceptance criteria

| AC | Text | iOS design | Android design | Warning Feedback: UI and data | Warning Feedback: Sound mode adjustment | Assign collar to pet | MOB-BE-FW tech updates |
|---|---|---|---|---|---|---|---|
| ME05-FE63-AC01 | Update the sound discrete slider:"Volume" headingBlue track with thumbDark grey track between 1 and 15 volume values.Light grey track between 15 and 25 volume values.Thumb with the value label"1" value label (the smallest value)"15" value label (the largest value for collars generation less than 4)"Only from Halo 4" label"25" value label (the largest value for collars generation from 4 and more) | TBD |  |
| ME05-FE63-AC02 | By default, the following Warning Feedback settings should be applied:Mode: SoundSound: Fast beepingVolume: 4 - ??? Should be 1 according to trainings??? |  |  |
| ME05-FE63-AC03 | The slider should use 25 invisible spaced tick marks along the slider track, and the thumb should snap to them only. |  |  |
| ME05-FE63-AC04 | PreconditionСollar generation assigned to pet is less than 4.The app should allow dragging the thumb only till 15 tick. |  |  |
| ME05-FE63-AC05 | PreconditionСollar generation assigned to pet is equal to or more than 4.ORNo collar is assigned to pet.The app should allow dragging the thumb till 25 tick. |  |  |
| ME05-FE63-AC06 | PreconditionPet's sound feedback volume is more than 15.If I assign a collar of a generation less than 4 to the pet, then the app should:Display the 'Change sound feedback volume' error pop-up.NoteIf user assigns the collar of generation 4 or unassigns the collar of any generation - no validation is needed. |  |  |
| ME05-FE63-AC07 | 'Change sound feedback volume' error pop-up should consist of:Header: TBDBody text: TBD "Your Halo collar is older than Halo 4. Please update the sound feedback volume up to 15 "Button: Ok |  |  |
| ME05-FE63-AC08 | BE should send on collar volume levels, not "decibels" both via BLE and MQTT. | - | - |
| ME05-FE63-AC09 | The new FW version should convert the volume from the special FW levels for all collar generations (H1, H2, H3, H4, and other future ones). [0] = 0, [1] = 0, [2] = 0, [3] = 0, [4] = 1, [5] = 2, [6] = 3, [7] = 4, [8] = 6, [9] = 8, [10] = 11, [11] = 13, [12] = 16, [13] = 19, [14] = 21, [15] = 23, [16] = 24, [17] = 26, [18] = 27, [19] = 28, [20] = 31 | - | - |
| ME05-FE63-AC09 | Old FW will proceed to work with H1, H2, and H3 in the following way:Either BE sends volume levels via BLE, or "decibels" via MQTT, FW converts it to the special FW levels using the following function:((correct-\>vol * 2) + 1) | - | - |
| ME05-FE63-AC10 | "Decibels" should be removed from the BE-MOB contract as well. | - | - |
