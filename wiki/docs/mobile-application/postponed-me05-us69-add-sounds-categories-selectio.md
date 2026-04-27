---
title: "(Postponed) ME05-US69. Add sounds categories selection for Custom 1 and Custom 2"
sidebar_label: "(Postponed) ME05-US69. Add sounds categories selection for Custom 1 and Custom 2"
sidebar_position: 472
last_modified: "Dec 16, 2024"
author: "Mariya Kolyada"
---

Page info| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| DRAFT |
| Mariya Kolyada |
| HALO-21952 - MOB+BE: ME05-US69. Add sounds categories selection for Custom 1 and Custom 2 Open |
| As of 21 Nov 2024 Mariya Kolyada separated this story from the ME05-US68. |# Contents

Contents User story Acceptance criteria Table ME05-US69-T01. Sound categories and presence in Feedbacks Table ME05-US69-T02. Sounds and presence in categories

# User story

\> As Halo app account owner I want to view screen with groups of sounds for Custom 1 and 2 from which I can open sounds lists for each group so I can save my time on searching throuh the whole long list of sounds.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| ME05-US69-US01 | Return the extra Sound screen between Feedback Settings and Sounds Lists screens for Custom 1 and Custom 2 feedbacks. | Figma Link |
| ME05-US69-US02 | The app should display or hide extra step with the Sound screen based on the following logic:If the Feedback (Warning, Boundary, Emergency, Whistle, Custom 1, Custom 2) has only one sound category, then the app should:Hide the extra step with the Sounds screen and navigate directly to the Sounds list screen.Otherwise, the Sound screen should be presented.NoteRight now only Custom 1 and Custom 2 feedbacks will have more than one sound category. |
| ME05-US69-US03 | The app should display a list of categories and sort them on the Sounds screen according to the data received from the BE. |
| ME05-US69-US04 | The Sound screen should consist of:Cancel button (iOS) or Cross button (Android)'Sound' title'Category' subtitleSounds categories list from BE |
| ME05-US69-US05 | Each element of the Sounds categories list from BE should consist of the following elements:Category Name;'Selected sound name' - only if the selected sound is presented in this category;Right arrow. |
| ME05-US69-US06 | Only one category within one corresponding feedback can be used with the chosen sound at the same time. |
| ME05-US69-US07 | If I tap on the sound category tile, then the app should:Display the list of sounds corresponding to the tapped category. |
| ME05-US69-US08 | The Sounds list screen title should match the sound category tile label. |
| ME05-US69-US09 | The app should display a list of Sounds within each category and sort them on the Sounds List screen according to the data received from the BE. |
| ME05-US69-US10 | The BE should send the list of sounds and categories based on the requirements defined below:Table ME05-US69-T01. Sound categories and presence in FeedbacksTable ME05-US69-T02. Sounds and presence in categories |  |### Table ME05-US69-T01. Sound categories and presence in Feedbacks

| Requirement ID | Feedback | Category presence in feedback | 'Prevention Sounds' category | 'Whistle Sounds' category | 'Other Sounds' category |
|---|---|---|---|---|---|
| ME05-US69-TL01-ID01 | Warning |  |  |  |
| ME05-US69-TL01-ID02 | Boundary |  |  |  |
| ME05-US69-TL01-ID03 | Emergency |  |  |  |
| ME05-US69-TL01-ID04 | Whistle |  |  |  |
| ME05-US69-TL01-ID05 | Custom 1 |  |  |  |
| ME05-US69-T01-ID06 | Custom 2 |  |  |  |### Table ME05-US69-T02. Sounds and presence in categories

| Requirement ID | New title | WAV file name | ID | Sound presence in the category | 'Prevention Sounds' category | 'Whistle Sounds' category | 'Other Sounds' category |
|---|---|---|---|---|---|---|---|
| ME05-US69-T02-ID01 | “Good Boy” | Good Boy 1 | 45018043-4D8E-4634-829E-DA8FE717FA59 |  |  |  |
| ME05-US69-T02-ID02 | “Good Girl” 1 | Good Girl 1 | 8C3401CF-37BC-48FE-9F42-149B8087C743 |  |  |  |
| ME05-US69-T02-ID03 | “Good Girl” 2 | Good Girl 2 | FF917737-2FA8-4841-AE9D-DE9037BD11A8 |  |  |  |
| ME05-US69-T02-ID04 | “Good Girl” 3 | Good Girl 3 | D66AEAF1-4D23-4FD0-B8B9-2E511437BD98 |  |  |  |
| ME05-US69-T02-ID05 | “You did it!” | You Did it | 90870922-97A4-4567-A9E6-4D78FC922418 |  |  |  |
| ME05-US69-T02-ID06 | “You’re going home” | You Going Home | A4B4EDC8-DD0D-4C1E-AA5B-3AC92CA73DAF |  |  |  |
| ME05-US69-T02-ID07 | “Kiss” Command | Kisses X3 | 435591AD-F17C-4704-93E4-005D24BC755A |  |  |  |
| ME05-US69-T02-ID09 | Single Beep | pip_1x | EFDBD7F3-FF64-4A21-9D8B-41DA6C9ECF31 |  |  |  |
| ME05-US69-T02-ID09 | Double Beep 1 | pip_2x | 4254B9D6-84E1-411D-AF82-70251E921798 |  |  |  |
| ME05-US69-T02-ID10 | Double Beep 2 | 0540F687-9B36-471C-A049-EF0010FB73BF | 0540F687-9B36-471C-A049-EF0010FB73BF |  |  |  |
| ME05-US69-T02-ID11 | Attention Beeps | invisible_fence | 33B9A1DE-B7BD-4411-BBFB-B6BD72EF91E4 |  |  |  |
| ME05-US69-T02-ID12 | Clicker | 9B05D376-282F-4D45-A820-7A35E675D38F | 9B05D376-282F-4D45-A820-7A35E675D38F |  |  |  |
| ME05-US69-T02-ID13 | Double Clicker | 45FC2B67-1F97-470F-BA13-B4A8A30D3EE4 | 45FC2B67-1F97-470F-BA13-B4A8A30D3EE4 |  |  |  |
| ME05-US69-T02-ID14 | “Tsch!“ Command | Tsst | 9C54396F-AC16-4F7E-82A3-8E757B964F4A |  |  |  |
| ME05-US69-T02-ID15 | “Hey“ Command 1 | Hey 1 | DF2FBA94-B46A-469E-A5BA-2570DD691EE0 |  |  |  |
| ME05-US69-T02-ID16 | “Hey“ Command 2 | Hey 2 | B3CE42D9-55CB-4E70-A052-3CD7C9D63341 |  |  |  |
| ME05-US69-T02-ID17 | Long Whistle | Whistle Long 1 | C25BA909-A2CE-431E-8F19-B2D46BF2BF05 |  |  |  |
| ME05-US69-T02-ID18 | Short Whistle 1 | Whistle Short 1 | EA93C13F-A03A-43E5-81F3-A8BE8C0EA345 |  |  |  |
| ME05-US69-T02-ID19 | Silent Recall Whistle (21 Khz) | dog whistle good | 744ABA7A-DC1A-4FD4-A8BA-7BFB8E031431 |  |  |  |
| ME05-US69-T02-ID20 | Silent Keep Away Beep (24 Khz) | dog whistle bad | A61A8E24-E763-45E1-9A02-1CBA73B7CBD2 |  |  |  |
| ME05-US69-T02-ID21 | Short Whistle 2 | Whistle Short 2 | C6B1A827-6F44-4562-8431-FCE6D9907A6B |  |  |  |
