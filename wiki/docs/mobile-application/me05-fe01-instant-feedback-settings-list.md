---
title: "ME05-FE01. Instant feedback settings (list)"
sidebar_label: "ME05-FE01. Instant feedback settings (list)"
sidebar_position: 104
last_modified: "Sep 15, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story (checked by dev team) |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| TBD |### User story

\> As an account owner, I'd like to the feedback settings list so that I can select the necessary option for adjustment

Contents

User story As an account owner, I'd like to the feedback settings list so that I can select the necessary option for adjustment Acceptance Criteria Feedback Settings: entry point Feedback Settings: prevention card in the expanded view

### Acceptance Criteria

| AC | Text | iOS impl-n status/UI design | Android impl-n status / UI design | Feedback Settings: entry point | Feedback settings screen: prevention/encouragement card is minimized | Feedback Settings: prevention card in the expanded view | Feedback Settings: Encouragements card in the expanded view |
|---|---|---|---|---|---|---|---|
| ME05-FE01-AC01 | Precondition: Pet card is opened.If I tap on the Feedback Settings and settings data from BE is successfully received, then:the Feedback Settings screen should be opened with the minimized prevention and encouragement cards, see Pic 1. | IOS READY | ANDROID TO DO |
| ME05-FE01-AC02 | Precondition: Pet card is opened.If I tap on the Feedback Settings and Connection issue happens, then:the Feedback Settings screen should be opened with the following text (instead of cards): "Settings are not available right now. Check your phone's Internet connection and retry." text + "Retry" button should be displayed. |  |  |
| ME05-FE01-AC03 | Precondition: Pet card is opened.If I tap on the Feedback Settings and Communication issue happens, then:the Feedback Settings screen should be opened with the following text (instead of cards): "Settings are not available right now. Please try again later. If issue continues, please contact to our contact support." text |  |  |
| ME05-FE01-AC04 | The Feedback Settings screen should consist of:Back icon"Feedback Settings" titlePet avatar + Halo ring\<Pet name\>"Feedback settings changed: \<time ago\>" text or "Default feedback settings" text, see the details in ME05-FE01-AC05/6Minimized Prevention card consists of:"Prevention" title"Adjust the settings used to prevent unwanted and unsafe behaviors" textDown arrow iconMinimized Encouragements card consists of:"Encouragements" title"Adjust the settings used to encourage good behaviors" textDown arrow iconTab bar | IOS READYPic 1 - Feedback Settings | ANDROID TO DOPic 1 - Feedback Settings |
| ME05-FE01-AC05 | If there are no changes in the feedback settings default configuration, then:"Default feedback settings" text should be displayed at the Feedback Settings screen. | IOS READY | ANDROID TO DO |
| ME05-FE01-AC06 | If there are changes in the feedback settings default configuration, then:"Feedback settings changed: \<time ago\>" text should be displayed at the Feedback Settings screen, see BR-16 Passed time format. | IOS READY | ANDROID TO DO |
| ME05-FE01-AC07 | If I tap on the minimized Prevention/Encouragement card, then:the Prevention/Encouragement card should be expanded. | IOS READY | ANDROID TO DO |
| ME05-FE01-AC08 | If I tap on the expanded Prevention/Encouragement card, then:the Prevention/Encouragement card should be minimized. | IOS READY | ANDROID TO DO |
| ME05-FE01-AC09 | Only one card could have an expanded state at a time. | IOS READY | ANDROID TO DO |
| ME05-FE01-AC10 | The app should hide the expanded info when I tap a short info line of the card. | IOS READY | ANDROID TO DO |
| ME05-FE01-AC11 | The Prevention card in the expanded view consists of:"Prevention" title"Adjust the settings used to prevent unwanted and unsafe behaviors" textUp arrow iconWarnings tile consists of:"Warning Feedback" tile consists of:Sound mode icon + \<Sound name\>orVibration mode icon + \<Vibration name\>Right arrow icon"Boundary Feedback" tile consists of:"Boundary Feedback" titleSound mode icon + \<Sound name\>orVibration mode icon + \<Vibration name\>orStatic mode icon + "Static" label + Icon with static level + \<Static level\>Right arrow icon"Emergency Feedback" tile consists of:Sound mode icon + \<Sound name\>orVibration mode icon + \<Vibration name\>orStatic mode icon + "Static" label + Icon with static level + \<Static level\>Right arrow iconNote: Static icon doesn't reflect the static level. The icon is staticSee the feedback/notification dependency logic in:Table ME05-1 Feedbacks and Notifications logic description for Fence Zone | IOS READY | ANDROID TO DO |
| ME05-FE01-AC12 | If I tap on the Warning Feedback tile, then: the Warning Feedback adjustment screen should be displayed. See the continuation in TBD | IOS READY | ANDROID TO DO |
| ME05-FE01-AC13 | If I tap on the Boundary Feedback tile, then: the Boundary Feedback adjustment screen should be displayed. See the continuation in TBD | IOS READY | ANDROID TO DO |
| ME05-FE01-AC14 | If I tap on the Emergency Feedback tile, then: the Emergency Feedback adjustment screen should be displayed. See the continuation in TBD | IOS READY | ANDROID TO DO |
| ME05-FE01-AC15 | The Encouragement card in the expanded view should consist of:"Encouragement" title"Adjust the settings used to encourage good behaviors" textUp arrow icon"Good Behavior" tile consists of:"Good behavior" titleSound mode icon + \<Choosen sound name\>Right arrow icon"Return Whistle" tile consists of:"Return whistle" titleSound mode icon + \<Choosen sound name\>Right arrow icon"Heading Home" tile consists of:"Heading Home" titleSound mode icon + \<Choosen sound name\>Right arrow icon | IOS READY | ANDROID TO DO |
| ME05-FE01-AC16 | If I tap on the Good Behavior tile, then:the Good Behavior adjustment screen should be displayed. See the continuation TBD | IOS READY | ANDROID TO DO |
| ME05-FE01-AC17 | If I tap on the Return Whistle tile, then:the Return Whistle adjustment screen should be displayed. See the continuation TBD | IOS READY | ANDROID TO DO |
| ME05-FE01-AC18 | If I tap on the Heading Home tile, then:the Heading Home adjustment screen should be displayed. See the continuation TBD | IOS READY | ANDROID TO DO |
