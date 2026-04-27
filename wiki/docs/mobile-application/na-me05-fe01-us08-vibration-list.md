---
title: "(NA) ME05-FE01-US08. Vibration list"
sidebar_label: "(NA) ME05-FE01-US08. Vibration list"
sidebar_position: 570
last_modified: "May 05, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links | History of Changes |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-887/ios-vibration-list |
| 02 May 2025 is created by Galina Lonskaya |### User story

\> As an account owner, I want to view the vibration list so that I can select the necessary one for the feedback

Contents

User story As an account owner, I want to view the vibration list so that I can select the necessary one for the feedback Acceptance Criteria Vibration screen: entry point Vibration screen: UI

### Acceptance Criteria

| AC | Description |  | Vibration screen: entry point |  | Vibration screen: UI |  | Save chosen vibration |  |
|---|---|---|---|---|---|---|---|---|
| AC01 | Precondition: Level 1 or Level 2 or Level 3 screen is displayed If I tap on the vibration tab, then:the Vibration screen should be opened, see Figma |  |
| AC02 | The Vibration screen should consist of:Cancel buttonVibration titleDone button, see details in AC09List of vibrations. Each vibration tile consists of:\<Vibration name\>See the vibrations in Appendix 18 - Sound/Vibration Naming and Categorization |  |
| AC03 | Only one vibration can be selected with a tick at one point in time. |  |
| AC04 | Vibrations should be sorted as shown on the screen, see FigmaImplementation notes:BE should update the order of the basis (full) list HALO-23057 - BE: Update the order of the sounds/vibrations in the basis list that is sent by BE to MOB Ready for Development MOB creates ordering on the basis of the received list Pavel please add details |  |
| AC05 | If I tap on the tile with vibration, then:The spinner should be displayed at the screen;The previous vibration playing should be stopped (if existed);The vibration should be produced 1 time;The tick should be displayed within the tile of the chosen vibration (if it isn't displayed there before);The previously selected vibration should be unselected.Note: Instead of the real vibration, the sound of vibration should be produced. |  |
| AC06 | If I tap on the tile with vibration and BE is unavailable, then:M17 popup should be shown. Note: agreed to show it to simplify dev-t and it's very rare case |  |
| AC07 | If I tap on the tile with sound and the volume is off on the phone, then:the same behavior should be applied as for 'Test on Phone' button, see AC05 in (NA) ME05-FEXX. 'Test on Phone' button on Feedback Details screens | - |
| AC08 | If I select a vibration different from the previously chosen one and tap on the Back button, then:the Vibration screen should be opened;the previously chosen vibration should be still displayed as selected. |  |
| AC09 | If any changes are applied for the Vibration screen, then:the Done button should be enabled. |  |
| AC10 | If no changes are applied for the Vibration screen, then:the Done button should be disabled. |  |
| AC11 | If I tap on the Done button, then:\<Feedback Type\> screen with the chosen vibration should be opened. |  |
