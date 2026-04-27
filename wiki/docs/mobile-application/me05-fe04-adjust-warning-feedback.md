---
title: "ME05-FE04. Adjust Warning Feedback"
sidebar_label: "ME05-FE04. Adjust Warning Feedback"
sidebar_position: 684
last_modified: "Sep 15, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issues |
|---|---|---|---|
| Baseline story (checked by DEV team) |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| TBD |### User story

\> As an account owner, I would like to view the Warning Feedback screen so that I can set the proper settings for Warning Feedback.

Content

User story Acceptance criteria Warning Feedback: entry point Warning Feedback: UI and data Warning Feedback: test on collar Warning Feedback: save settings

### Acceptance criteria

| AC | Text | iOS impl-n status/UI design | Android impl-n status / UI design | Warning Feedback: entry point | Warning Feedback: UI and data | Warning Feedback: Sound mode adjustment | Warning Feedback: Vibration mode adjustment | Warning Feedback: test on collar | Warning Feedback: save settings | Warning Feedback: Bluetooth connection |
|---|---|---|---|---|---|---|---|---|---|---|
| ME05-FE04-AC01 | If I tap on the Warning Feedback tile at the Feedback Settings screen, then:The Warning Feedback screen should be displayed with the default or previously chosen mode (Sound or Vibrate), see Pic 1. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC02 | The Warning Feedback screen should consist of:Back icon"Warning Feedback" heading"Done" button"Choose a method that will warn \<Pet name\> to stop their current behavior" text"Mode" titleTab with "Sound" icon + "Sound" label (selected)Tab with "Vibrate" icon + "Vibrate" label"Sound" title\<Sound Name\> + Right arrow iconSound discrete slider:"Volume" headingTrack with thumbThumb with the value label"1" value label (the smallest value)"15" value label (the largest value)"Test on Collar" buttonTab bar | IOS DONEPic 1 Warning Feedback with the selected Sound tab | ANDROID TO DOThe same screen as for iOS |
| ME05-FE04-AC03 | By default the following Warning Feedback settings should be applied:Mode: SoundSound: Fast beepingVolume: 4 | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC04 | Precondition: Warning Feedback screen with the selected Sound mode is displayed.If I tap on the tile with the Sound, then:the Sounds screen should be opened, see ME05-FE02. Sound list. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC05 | The slider should be controlled by clicking the thumb and dragging it (click and drag) or clicking the track (click jump). | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC06 | The slider should use 15 invisible spaced tick marks along the slider track, and the thumb should snap to them only. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC07 | The thumb should be displayed with the corresponded value label. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC08 | If I tap on the "Vibrate" tab, then the following elements should be displayed:Selected "Vibrate" tab"Vibration" title\<Vibration name\> + Right arrow"Test on Collar" button | IOS DONE | OPTIONAL FOR ANDROIDNote: for Android, the tile isn't tappable and the right arrow should not be displayed |
| ME05-FE04-AC09 | Precondition: Warning Feedback screen with the selected Vibrate mode is displayed.If I tap on the tile with the Vibration, then:the Vibrations screen should be opened, see ME05-FE03. Vibration list. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC10 | By default "Heart Beat" sound should be selected in the Vibration list. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC11 | Precondition: Warning Feedback screen is displayed with the Sound or Vibrate tab selected.If I tap on the Test on Collar button, then see the description in TBD. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC12 | The "Done" button should appear, only after I edit something at the Warning Feedback screen. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC13 | If I tap on the Done button and the Warning Feedback saving is performed successfully, then:the Feedback Settings screen should be opened with the updated Warning Feedback settings. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC14 | If I tap on the Done button and the Warning Feedback saving isn't performed successfully, then:ME14-F01 Unified errors handling mechanism should be applied. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC15 | If I tap on the Back button and there are no changes at the Warning Feedback screen, then:The Pet Settings screen without changes should be opened. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC16 | If I tap on the Back button and there are any changes, then:the warning M50 Unsaved Changes message should be displayed. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC17 | Precondition: the Warning feedback screen is opened, the settings are updated (but not saved).If I tap on My Map tab, then:the warning M50 Unsaved Changes message should be displayed. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC18 | Precondition: the Warning feedback screen is opened, the settings are updated (but not saved).If I go to the Settings screen and log out, then:Feedback setting updates should not be saved;I should be logged out of the app.Note: the simplest approach is described. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC19 | Precondition: Warning Feedback screen is opened.The Bluetooth connection should be interrupted while navigating to other tabs. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC20 | Precondition: the user is on one of the following tabs: Training, Notifications, or Settings, but the Warning Feedback screen is opened on My Map.The Bluetooth connection should be restored after getting back to the Warning Feedback screen. | IOS DONE | ANDROID TO DO |
| ME05-FE04-AC21 | See the logic of Bluetooth reconnection here: ME14-EP01 Automatic Bluetooth reconnection/disconnection | IOS DONE | OPTIONAL FOR ANDROID |
