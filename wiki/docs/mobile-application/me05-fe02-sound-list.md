---
title: "ME05-FE02. Sound list"
sidebar_label: "ME05-FE02. Sound list"
sidebar_position: 682
last_modified: "Jul 26, 2024"
author: "Galina Lonskaya"
---

Page info| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story (checked by dev team) |
| REVISED |
| Galina Lonskaya, Anastasia Brechko, Vadim Pylsky [X] |
| n/a |Contents

User story Acceptance Criteria Sound screen: entry point Sound screen: UI Basic Sounds/Vocal Sounds/Whistles screens Save chosen sound Rule of the category and sound displaying in one line Other Table ME05-FE02 Sound list

### User story

\> As Halo app account owner, I want to view the screen with different sound categories so that I can select the appropriate sound for prevention/encouragement feedback and set it for my dog's collar

### Acceptance Criteria

| AC | Description | UI design | Sound screen: entry point | Sound screen: UI | Basic Sounds/Vocal Sounds/Whistles screens | Save chosen sound | Rule of the category and sound displaying in one line | Other |
|---|---|---|---|---|---|---|---|---|
| ME05-FE02-AC01 | Precondition: My Map tab → Pet Card → Feedback Settings → Prevention/Encouragement → Any \<Feedback Type\> Settings screen is displayed (for instance: Warning Feedback). If I tap on the tile with the sound, then:the Sound screen should be opened. See Pic 1. | - |
| ME05-FE02-AC02 | The Sound screen should consist of:Cancel button (iOS) or Cross button (Android)'Sound' title'Category' subtitle'Basic Sounds' tile + Right arrow'Vocal Sounds' tile + Right arrow'Whistles' tile + Right arrow | Pic 1 - Sound |
| ME05-FE02-AC03 | The name of the currently chosen sound should be displayed in a corresponding category tile of the Sound screen. | - |
| ME05-FE02-AC04 | Only one category can be with the chosen sound at the one moment of time. | - |
| ME05-FE02-AC05 | Precondition: Sound screen is opened.If I tap on the Basic Sounds, then:the Basic Sounds screen should be opened. See Pic 2.See the sounds included in the list in Table ME05-FE02 Sound list below. | Pic 2 - Basic Sounds |
| ME05-FE02-AC06 | Precondition: Sound screen is opened. If I tap on the Vocal Sounds tile, then:the Vocal Sounds screen should be opened, see the sounds included in the list in Table ME05-FE02 Sound list. | Pic 3 - Vocal Sounds |
| ME05-FE02-AC07 | Precondition: Sound screen is opened. If I tap on the Whistles tile, then:the Whistles screen should be opened, see the sounds included in the list in Table ME05-FE02 Sound list below. | Pic 4 - Whistles |
| ME05-FE02-AC08 | If I open the Whistles or the Vocal Sounds or the Basic Sounds screen and it has currently selected sound, then:the currently selected sound should be displayed with a tick. | - |
| ME05-FE02-AC09 | Basic Sounds/Vocal Sounds/Whistles lists should be sorted alphabetically. | - |
| ME05-FE02-AC10 | Precondition: the Whistles or the Vocal Sounds or the Basic Sounds screen is opened.If I tap on the tile with sound, then:The spinner should be displayed at the screen;The previous sound playing should be stopped (if existed);The sound should be produced 1 time;The tick should be displayed with this sound (if it isn't displayed there before);The previously selected sound should be unselected. | - |
| ME05-FE02-AC11 | If I tap on the tile with sound and BE is unavailable, then the error M17 Technical error should be displayed. | - |
| ME05-FE02-AC12 | If I tap on the tile with sound and the volume is off on the phone, then:the toast message should be displayed for 4 sec: 'Please increase the volume on your mobile device'. | - |
| ME05-FE02-AC13 | If I open the Whistles or the Vocal Sounds or the Basic Sounds screen, then:the playing of the selected tile shouldn't be started automatically. | - |
| ME05-FE02-AC14 | If I select a sound different from the previously chosen and tap on the Back button, then:the Sound screen should be opened;the previously chosen sound should be still displayed as selected. | - |
| ME05-FE02-AC15 | If any changes are applied for the Whistles or the Vocal Sounds or the Basic Sounds screen, then:the Done button should be available. | - |
| ME05-FE02-AC16 | If I tap on the Done button, then:\<Feedback Type\> screen with the chosen sound should be opened. | - |
| ME05-FE02-AC17 | There are 3 options of a sound and category placing in one line:If category doesn’t have chosen sound - it’s name fills all available width of the cell before the arrow icon;If category has chosen sound, and there's enough space for both labels - both labels displayed fully; If category has chosen sound, and there's no enough space to fit both of them, following rules are applied:category name has priority to be shown fully, so sound name should be cut first;on the other hand, sound name has minimal length of 110px, and cannot be cut shorter - if sound name has already been cut to 110px, and category still doesn't fit - category should be also cut. | - |
| ME05-FE02-AC18 | PTN files for sounds should be used on the collar. |  |
| ME05-FE02-AC19 | TBD files for sounds should be used for playing on the mob side.Tech note: the sounds are stored on BE side and when mob app requests it, BE provides URL with the sound. |  |
| ME05-FE02-AC20 | Sound lists should be sorted alphabetically: A→ Z. |  |
| ME05-FE02-AC21 | The default sound for Warning Prevention is 'Fast beeping' sound. |  |
| ME05-FE02-AC22 | The default sound for Whistle Encouragement is 'Cesar's short whistle' sound. |  |
| ME05-FE02-AC23 | The default sound for Good Dog Encouragement is 'Cesar: You did it!' sound. |  |
| ME05-FE02-AC24 | The default sound for Go Home Encouragement is 'Cesar: You're going home' sound. |  |### Table ME05-FE02 Sound list

|  | WAV file name | Title | ID | Category |
|---|---|---|---|---|
| 1 | pip_2x | Double beep | 4254B9D6-84E1-411D-AF82-70251E921798 | Basic Sounds |
| 2 | pip_1x | Short beep | EFDBD7F3-FF64-4A21-9D8B-41DA6C9ECF31 | Basic Sounds |
| 3 | invisible_fence | Fast beeping | 33B9A1DE-B7BD-4411-BBFB-B6BD72EF91E4 | Basic Sounds |
| 4 | 45FC2B67-1F97-470F-BA13-B4A8A30D3EE4 | Double clicker | 45FC2B67-1F97-470F-BA13-B4A8A30D3EE4 | Basic Sounds |
| 5 | 9B05D376-282F-4D45-A820-7A35E675D38F | Clicker | 9B05D376-282F-4D45-A820-7A35E675D38F | Basic Sounds |
| 6 | Whistle Short 1 | Cesar's short whistle | EA93C13F-A03A-43E5-81F3-A8BE8C0EA345 | Whistles |
| 7 | Whistle Long 1 | Cesar's long whistle | C25BA909-A2CE-431E-8F19-B2D46BF2BF05 | Whistles |
| 8 | Tsst | Cesar: 'tsch!' | 9C54396F-AC16-4F7E-82A3-8E757B964F4A | Basic Sounds |
| 10 | Kisses X3 | Cesar: Kiss | 435591AD-F17C-4704-93E4-005D24BC755A | Basic Sounds |
| 11 | Hey 1 | Cesar: Hey | DF2FBA94-B46A-469E-A5BA-2570DD691EE0 | Vocal Sounds |
| 12 | You Going Home | Cesar: You're going home | A4B4EDC8-DD0D-4C1E-AA5B-3AC92CA73DAF | Vocal Sounds |
| 13 | Good Girl 2 | Cesar: Good girl (2) | FF917737-2FA8-4841-AE9D-DE9037BD11A8 | Vocal Sounds |
| 14 | Good Girl 1 | Cesar: Good girl | 8C3401CF-37BC-48FE-9F42-149B8087C743 | Vocal Sounds |
| 15 | Good Boy 1 | Cesar: Good boy | 45018043-4D8E-4634-829E-DA8FE717FA59 | Vocal Sounds |
| 16 | 0540F687-9B36-471C-A049-EF0010FB73BF | Buzzing | 0540F687-9B36-471C-A049-EF0010FB73BF | Basic Sounds |
| 17 | dog whistle bad | Silent Whistle: Keep away (24 Khz) | A61A8E24-E763-45E1-9A02-1CBA73B7CBD2 | Whistles |
| 18 | dog whistle good | Silent Whistle: Come back (21 Khz) | 744ABA7A-DC1A-4FD4-A8BA-7BFB8E031431 | Whistles |
| 19 | Whistle Short 2 | Whistle Short 2 | C6B1A827-6F44-4562-8431-FCE6D9907A6B | Whistles |
| 20 | Hey 2 | Cesar: Hey (2) | B3CE42D9-55CB-4E70-A052-3CD7C9D63341 | Vocal Sounds |
| 21 | You Did it | Cesar: You did it! | 90870922-97A4-4567-A9E6-4D78FC922418 | Vocal Sounds |
| 22 | Good Girl 3 | Cesar: Good girl (3) | D66AEAF1-4D23-4FD0-B8B9-2E511437BD98 | Vocal Sounds |
