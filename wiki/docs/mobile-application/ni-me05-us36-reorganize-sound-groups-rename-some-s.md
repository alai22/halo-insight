---
title: "(NI) ME05-US36. Reorganize sound groups / rename some sounds"
sidebar_label: "(NI) ME05-US36. Reorganize sound groups / rename some sounds"
sidebar_position: 440
author: "Galina Lonskaya"
---

Page info| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Eugene Paseka Pavel Leonenko |
| HALO-20876 - BE+MOB: ME05-US36. Reorganize sound groups / rename some sounds Closed |
| 07 Aug 2024 draft user story is created10/10/2024 'Kiss' sound is returned back, minor comments in accordance with the design changes are applied |# User story

\> As Halo app account owner I want to rename and regroup sounds available for feedback setting so that it can be better organized, categorized, and made more intuitive for users to select during feedback setting.

# Acceptance criteria

| AC | Description | UI design | Warning, Boundary, Emergency feedback | Whistles | Good Dog | Go Home | Logic for users who adjusted feedback settings before new sound categorization is available |
|---|---|---|---|---|---|---|---|
| ME05-US36-US01 | The following sounds should be renamed: ME05-US36-ID01 – 04 AND ME05-US36-ID07 – 21, see 'New title' and 'Old title' columns in Table 1. New sound categorization below. | - |
| ME05-US36-US02 | The Sound screen (screen with categories) should be removed from all 'Edit Feedback Settings' flows: Warning Feedback Boundary Feedback Emergency Feedback Whistle Good Dog Go Home | the screen that should be removed |
| ME05-US36-US03 | If I tap on 'Sound' field, on \<any feedback\> type screen, then:a list with the sounds should be displayed, see below the specifics for each type of feedback. Note: previously the screen with categories was displayed. | the sound field that should be tapped |
| ME05-US36-US04 | Warning, Boundary, Emergency feedback should have the following limited list of sounds available for choice: see ME05-US36-ID01 – ID09 and the screen. | Figma |
| ME05-US36-US05 | The sound sequence should be the same as presented in ME05-US36-ID01 – ID09. |
| ME05-US36-US06 | The following titles should be assigned to the Sound screens for Preventions:'Warning Sounds' on 'Sound' screen for Warning Feedback'Boundary Sounds' on 'Sound' screen for Boundary Feedback'Emergency Sounds' on 'Sound' screen for Emergency Feedback |
| ME05-US36-US07 | The following subtitles should be added to the Sound screen: 'Choose a sound setting from the list for Warning Feedback.' text on 'Sound' screen for Warning Feedback'Choose a sound setting from the list for Boundary Feedback.' text on 'Sound' screen for Boundary Feedback'Choose a sound setting from the list for Emergency Feedback.' text on 'Sound' screen for Emergency Feedback | - |
| ME05-US36-US08 | Whistles should have the following limited list of sounds available for choice: see ME05-US36-ID10 – ID14 and the screen. | Figma |
| ME05-US36-US09 | The sound sequence should be the same as presented in ME05-US36-ID10 – ID14. |
| ME05-US36-US10 | The screen with sounds should have the following title and subtitle: Whistle SoundsChoose a sound setting from the list for Whistle Feedback. |
| ME05-US36-US11 | Good Dog should have the following limited list of sounds available for choice: see ME05-US36-ID15– ID19 and the screen. | Figma |
| ME05-US36-US12 | The sound sequence should be the same as presented in ME05-US36-ID15 – ID19. |
| ME05-US36-US13 | The screen with sounds should have the following title and subtitle: Good Dog SoundsChoose a sound setting from the list for Good Dog Feedback. |
| ME05-US36-US14 | Go Home should have the following limited list of sounds available for choice: see ME05-US36-ID20– ID21 and the screen. | Figma |
| ME05-US36-US15 | The screen with sounds should have the following title and subtitle: Go Home SoundsChoose a sound setting from the list for Go Home Feedback. |  |
| ME05-US36-US16 | If sound(s) for \<feedback type\> was(were) chosen before I updated my mob app to the version with a new categorization (limited list of sounds are available for each feedback), then:NO automatic changes in currently chosen sounds for all type of the feedback should be applied. | - |
| ME05-US36-US17 | If the sound(s) for \<feedback type\> was(were) chosen before I updated my app to the version with new sound categorization AND a sound isn't available for this feedback settingAND I go to Feedback Settings → Feedback Type screen and then tap on Sound field, then:the updated limited list of sounds should be opened; the previously chosen sound should NOT be displayed in the listNO sounds should be displayed with a tick | - |
| ME05-US36-US18 | Precondition: a list with the limited number of sounds is opened and previously chosen sound is not available for this feedback type anymore.If I tap on Cancel button, then: \<Feedback Type\> screen should be opened with previously selected sound. | - |
| ME05-US36-US19 | Precondition: a list with the limited number of sounds is opened and previously chosen sound is not available for this category anymore.If I tap on new sound become selected AND tap on Done button, then:new sound is shown as chosen on \<Feedback Type\> screen. AND I will not be able to come back to previously chosen sound anymore. | - |### Implementation notes

| IN | Description |
|---|---|
| ME05-US36-IN01 | Backward compatibility BE should store both API endpoints for old sound categorization and for new sound categorization, no mandatory update should be required.Can be discussed in more details with Eugene Paseka and Pavel Leonenko |### Table 1. New sound categorization

| Requirement ID | New title | Old title | WAV file name | ID | Preventions |  | Whistles |  | Good Dog |  | Go Home |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ME05-US36-ID01 | Single Beep | Short beep | pip_1x | EFDBD7F3-FF64-4A21-9D8B-41DA6C9ECF31 |
| ME05-US36-ID02 | Double Beep 1 | Double beep | pip_2x | 4254B9D6-84E1-411D-AF82-70251E921798 |
| ME05-US36-ID03 | Double Beep 2 | Buzzing | 0540F687-9B36-471C-A049-EF0010FB73BF | 0540F687-9B36-471C-A049-EF0010FB73BF |
| ME05-US36-ID04 | Attention Beeps | Fast beeping | invisible_fence | 33B9A1DE-B7BD-4411-BBFB-B6BD72EF91E4 |
| ME05-US36-ID05 | Clicker | Clicker | 9B05D376-282F-4D45-A820-7A35E675D38F | 9B05D376-282F-4D45-A820-7A35E675D38F |
| ME05-US36-ID06 | Double Clicker | Double clicker | 45FC2B67-1F97-470F-BA13-B4A8A30D3EE4 | 45FC2B67-1F97-470F-BA13-B4A8A30D3EE4 |
| ME05-US36-ID07 | “Tsch!“ Command | Cesar: 'tsch!' | Tsst | 9C54396F-AC16-4F7E-82A3-8E757B964F4A |
| ME05-US36-ID08 | “Hey“ Command 1 | Cesar: Hey | Hey 1 | DF2FBA94-B46A-469E-A5BA-2570DD691EE0 |
| ME05-US36-ID09 | “Hey“ Command 2 | Cesar: Hey (2) | Hey 2 | B3CE42D9-55CB-4E70-A052-3CD7C9D63341 |
| ME05-US36-ID10 | Long Whistle | Cesar's long whistle | Whistle Long 1 | C25BA909-A2CE-431E-8F19-B2D46BF2BF05 |
| ME05-US36-ID11 | Short Whistle 1 | Cesar's short whistle | Whistle Short 1 | EA93C13F-A03A-43E5-81F3-A8BE8C0EA345 |
| ME05-US36-ID12 | Silent Whistle 1 (21 Khz) | Silent Whistle: Come back (21 Khz) | dog whistle good | 744ABA7A-DC1A-4FD4-A8BA-7BFB8E031431 |
| ME05-US36-ID13 | Silent Whistle 2 (24 Khz) | Silent Whistle: Keep away (24 Khz) | dog whistle bad | A61A8E24-E763-45E1-9A02-1CBA73B7CBD2 |
| ME05-US36-ID14 | Short Whistle 2 | Whistle Short 2 | Whistle Short 2 | C6B1A827-6F44-4562-8431-FCE6D9907A6B |
| ME05-US36-ID15 | “Good Boy” | Cesar: Good boy | Good Boy 1 | 45018043-4D8E-4634-829E-DA8FE717FA59 |
| ME05-US36-ID16 | “Good Girl” 1 | Cesar: Good girl | Good Girl 1 | 8C3401CF-37BC-48FE-9F42-149B8087C743 |
| ME05-US36-ID17 | “Good Girl” 2 | Cesar: Good girl (2) | Good Girl 2 | FF917737-2FA8-4841-AE9D-DE9037BD11A8 |
| ME05-US36-ID18 | “Good Girl” 3 | Cesar: Good girl (3) | Good Girl 3 | D66AEAF1-4D23-4FD0-B8B9-2E511437BD98 |
| ME05-US36-ID19 | “You did it!” | Cesar: You did it! | You Did it | 90870922-97A4-4567-A9E6-4D78FC922418 |
| ME05-US36-ID20 | “You’re going home” | Cesar: You're going home | You Going Home | A4B4EDC8-DD0D-4C1E-AA5B-3AC92CA73DAF |
| ME05-US36-ID21 | “Kiss” Command | Cesar: Kiss | Kisses X3 | 435591AD-F17C-4704-93E4-005D24BC755A |
