---
title: "ME05-FE03. Vibration list"
sidebar_label: "ME05-FE03. Vibration list"
sidebar_position: 683
last_modified: "Oct 16, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story (checked by dev team) |
| REVISED |
| Galina Lonskaya, Anastasia Brechko, Vadim Pylsky [X] |
| TBD |### User story

\> As an account owner, I want to view the vibration list so that I can select the necessary one for prevention.

Contents

User story As an account owner, I want to view the vibration list so that I can select the necessary one for prevention. Acceptance Criteria Vibration screen: entry point Vibration screen: UI Save vibration sound Table ME04-FE03-1 Vibrations list

### Acceptance Criteria

| AC | Description | iOS impl-n/UI design | Android impl-n UI design | Vibration screen: entry point | Vibration screen: UI | Save vibration sound |
|---|---|---|---|---|---|---|
| ME05-FE03-AC01 | Precondition: Warning Feedback or Boundary Feedback or Emergency Feedback screen is displayed (for instance: Warning Feedback)If I tap on the tile with the vibration, then:the Vibration screen should be opened. See Pic 1. | IOS DONEPic 1- Vibration | ANDROID TO DOThe same screen as for iOS |
| ME05-FE03-AC02 | The Vibration screen should consist of:Cancel buttonVibration titleDone button, see details in ME05-FE03-AC09List of vibrations. Each vibration tile consists of:\<Vibration name\>See the vibrations in Table ME04-FE03-1 Vibrations list. | IOS DONE | ANDROID TO DO |
| ME05-FE03-AC03 | Only one vibration can be selected with a tick at one point in time. | IOS DONE | ANDROID TO DO |
| ME05-FE03-AC04 | Vibrations should be sorted alphabetically. | IOS DONE | ANDROID TO DO |
| ME05-FE03-AC05 | If I tap on the tile with vibration, then:The spinner should be displayed at the screen;The previous vibration playing should be stopped (if existed);The vibration should be produced 1 time;The tick should be displayed within the tile of the chosen vibration (if it isn't displayed there before);The previously selected vibration should be unselected.Note: Instead of the real vibration, the sound of vibration should be produced. | IOS DONE | ANDROID TO DO |
| ME05-FE03-AC06 | If I tap on the tile with vibration and BE is unavailable, then the error M17 Technical error should be displayed.TBD with dev/qa the error | IOS DONE | ANDROID TO DO |
| ME05-FE03-AC07 | If I tap on the tile with vibration and the volume is off on the phone, then:the toast message should be displayed for 4 sec: "Please increase the volume on your mobile device". | IOS DONE | ANDROID TO DO |
| ME05-FE03-AC08 | If I select a vibration different from the previously chosen one and tap on the Back button, then:the Vibration screen should be opened;the previously chosen vibration should be still displayed as selected. | IOS DONE | ANDROID TO DO |
| ME05-FE03-AC09 | If any changes are applied for the Vibration screen, then:the Done button should be available. | IOS DONE | ANDROID TO DO |
| ME05-FE03-AC10 | If I tap on the Done button, then:\<Feedback Type\> screen with the chosen vibration should be opened. | IOS DONE | ANDROID TO DO |### Table ME04-FE03-1 Vibrations list

|  | WAV file name | A title which will be displayed at the Halo app | ID |
|---|---|---|---|
| 1 | accent | Accent | 1C92B738-496F-4C83-8682-E0C8E2D692B7 |
| 2 | alert | Alert | 15230474-400E-4D9F-9A48-613520EE63C5 |
| 3 | heartbeat | Heart beat | C470300F-578D-4830-8A98-A424BD3B8536 |
| 4 | rapid | Rapid | AB3600E0-2CAE-4E2E-A431-B20F54A0CF2A |
| 5 | staccato | Staccato | 5773E05F-7D18-4887-9C33-C89E9EE180D9 |
| 6 | buzz-buzz | Buzz-buzz | 60905A47-9ECE-480D-8493-5AEC97855050 |
