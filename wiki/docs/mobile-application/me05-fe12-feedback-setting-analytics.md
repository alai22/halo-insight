---
title: "ME05-FE12. Feedback setting analytics"
sidebar_label: "ME05-FE12. Feedback setting analytics"
sidebar_position: 692
last_modified: "Oct 17, 2024"
author: "Galina Lonskaya"
---

#### Table 1 - Clicked CTAs events

| ID | Event Name | Event properties | Description | Jira task |
|---|---|---|---|---|
| ME05-FE12-CTA01 | Feedback Settings | Screen Name = My MapPet ID | The user taps on the Feedback Settings button on the Pet card. This button is accessible only if the pet card is expanded. | HALO-21581 - MOB: Add Amplitude events for 'Feedback Management' flow Closed |
| ME05-FE12-CTA02 | Select Feedback Setting | Screen Name = Feedback SettingsPet IDPattern IDPattern NameType = \<Warning, Boundary, Emergency, Good Dog, Go Home, Whistle\> | The taps on the tile (Warning ... Go Home) with right arrow on the Feedback Settings screen. note: there are 6 tiles to choose |
| ME05-FE12-CTA03 | Edit Feedback Pattern | Screen Name = Edit Feedback SettingPet IDMode = \<Sound, Vibration, Static\>Type = \<Warning, Boundary, Emergency, Good Dog, Go Home, Whistle\> | The user taps on the Sound/Vibration field on \<Feedback Type\> screen. |
| ME05-FE12-CTA04 | Select Feedback Pattern | Screen Name = Pattern ListPet IDPattern IDPattern NameMode = \<Sound, Vibration, Static\>Type = \<Warning, Boundary, Emergency, Good Dog, Go Home, Whistle\> | The user taps on the pattern (Sound or Vibration) on the list of Patterns. |
| ME05-FE12-CTA05 | Save Feedback Pattern | Screen Name = Pattern ListPet IDPattern IDPattern NameMode = \<Sound, Vibration, Static\>Type = \<Warning, Boundary, Emergency, Good Dog, Go Home, Whistle\> | The user taps on the Done button in the top navigation bar on the list of Patterns (Sounds OR Vibrations). |
| ME05-FE12-CTA06 | Cancel | Current screen Edit Feedback Pattern screen | The user taps on the Cancel button in the top navigation bar |  |
| ME05-FE12-CTA07 | Back | Current Screen Name Destination Screen Name | The user taps on the Back button in the top navigation bar Note 1: closing of modal windows, popups, log out, changing of the tabs will not be logged. Note 2: tap on 'Android system Back' button, swipe to right on iOS, tap on the root tab bar button should be logged. Note 3: QA should test taps on Back button on 'Edit Feedback Setting' and 'Feedback' settings screen within HALO-21580 - MOB: Log 'Back' action for all screens (unified event logging) Closed | HALO-21580 - MOB: Log 'Back' action for all screens (unified event logging) Closed |
| ME05-FE12-CTA08 | Test on Collar | Screen Name = Edit Feedback SettingPet IDCollar IDPattern IDPattern Name Mode = \<Sound, Vibration, Static\>Type = \<Warning, Boundary, Emergency, Good Dog, Go Home, Whistle\>Level | The user taps on 'Test on Collar' button on \<Feedback Type\> screen. | HALO-21581 - MOB: Add Amplitude events for 'Feedback Management' flow Closed |
| ME05-FE12-CTA09 | Popup button | TitleBodyButton labelM50 'Unsaved changes' popup | The user taps the button on the popup message. |  |
| ME05-FE12-CTA10 | Test on Phone | Screen Name = Edit Feedback SettingPet IDPattern IDPattern Name Mode = \<Sound, Vibration, Static\>Type = \<Warning, Boundary, Emergency, Good Dog, Go Home, Whistle\>Level | The user taps on 'Test on Phone' button on \<Feedback Type\> screen. | HALO-21564 - MOB: Add Amplitude event for ME05-US64. Add 'Test on Phone' button to Feedback Type screens Closed |Table 2 - Custom events

|  | Event Name | Type | Main Parameters | Description | Amplitude/DB | Jira task |
|---|---|---|---|---|---|---|
| ME05-FE12-CE01 | Saved Feedback Type | UserId, MobileId, SessionId | Pet IDPattern IDPattern NameMode = \<Sound, Vibration, Static\>Type = \<Warning, Boundary, Emergency, Good Dog, Go Home, Whistle\>From levelTo level | Log when the user saves changes on \<Feedback Type\> screen via a tap on the Done button on \<Feedback Type\> screen |  | HALO-21581 - MOB: Add Amplitude events for 'Feedback Management' flow Closed |
| ME05-FE12-CE02 | Viewed Popup | UserId, MobileId, SessionId | TitleBodyPrimary Button labelSecondary Button labelM50 'Unsaved changes' popup See all popup messages: https://portal.softeq.com/pages/viewpage.action?pageId=93009004 | Log when the popup message is displayed |  |
|  |  |  |  |  |  |  |Table 3 - Viewed screen events

|  | Event Name | Type | Main Parameters | Additional Parameters | Amplitude/DB | Jira task |  |
|---|---|---|---|---|---|---|---|
| ME05-FE12-CTA01 |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
