---
title: "(NA) ME05-FE01-US07. Sound list"
sidebar_label: "(NA) ME05-FE01-US07. Sound list"
sidebar_position: 568
last_modified: "May 06, 2025"
author: "Galina Lonskaya"
---

Page info| Document owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-886/ios-sound-list |
| 05/02/2025 draft is created by Galina Lonskaya |Contents

User story Acceptance Criteria Sound screen: entry point Basic Sounds/Vocal Sounds/Whistles screens Save chosen sound

### User story

\> As Halo app account owner, I want to view the screen with different sound categories so that I can select the appropriate sound for prevention/encouragement feedback and set it for my dog's collar

### Acceptance Criteria

| AC | Description | UI design | Sound screen: entry point | Basic Sounds/Vocal Sounds/Whistles screens | Save chosen sound |
|---|---|---|---|---|---|
| AC01 | Precondition: Feedback Settings screen is displayed (for instance: Level 1 Feedback). If I tap the tile with the sound, then:the Sound screen should be openeddifferent one for each type of feedback | Figma |
| AC02 | If I open the Sound screen, then:the currently selected sound should be displayed with a tick. | - |
| AC03 | If I open the Sound screen, then:the default sound related to this type of the feedback should be displayed with '(Default)' label. Note: this AC is not related to Custom 1 / Custom 2 Sound list. | - |
| AC04 | Sound list of each feedback should be sorted in accordance with UI design. Implementation notes:BE should update the order of the basis (full) list HALO-23057 - BE: Update the order of the sounds/vibrations in the basis list that is sent by BE to MOB Ready for Development MOB creates ordering on the basis of the received list Pavel please add details | - |
| AC05 | If I tap on the tile with sound, then:The spinner should be displayed at the screen;The previous sound playing should be stopped (if existed);The sound should be produced 1 time;The tick should be displayed with this sound (if it isn't displayed there before);The previously selected sound should be unselected. | - |
| AC06 | If I tap on the tile with a sound button and there is no assigned collar to a pet, then:M17 popup should be shown. Note: agreed to show it to simplify dev-t and it's very rare case | - |
| AC07 | If I tap on the tile with sound and the volume is off on the phone, then:the same behavior should be applied as for 'Test on Phone' button, see AC05 in (NA) ME05-FEXX. 'Test on Phone' button on Feedback Details screens | - |
| AC08 | If I open the Sounds screen, then:the playback of the selected sound shouldn't be started automatically. | - |
| AC09 | The sounds are stored on BE side and when mob app requests it, BE provides URL with the sound. | - |
| AC10 | If any changes are applied for the Sounds screen, then:the Done button should be enabled. | - |
| AC11 | If I tap on the Done button, then:the Sound screen should be closed \<Feedback Type\> screen with the chosen sound should be opened. | - |
| AC12 | If I select a sound different from the previously chosen and tap on the Cancel button, then:the Sound screen should be closed\<Feedback Type\> screen with the chosen sound should be opened.the previously chosen sound should be still displayed as chosen | - |
