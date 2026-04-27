---
title: "(NA) ME05-FE01-US01. Feedback Settings Screen"
sidebar_label: "(NA) ME05-FE01-US01. Feedback Settings Screen"
sidebar_position: 564
last_modified: "May 05, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links | History of Changes |
|---|---|---|
| Galina Lonskaya, Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-880/ios-feedback-settings-screen |
| 04/21/2025 draft is created |### User story

\> As Halo App account owner, I want to open the feedback settings list so that I can select the necessary feedback type for adjustment

Contents

User story As Halo App account owner, I want to open the feedback settings list so that I can select the necessary feedback type for adjustment Acceptance Criteria Entry Point to Feedback Settings screen Error handling when opening Feedback Settings screen Feedback Settings screen UI Minimized/maximized pet feedback cards: general description Minimized pet feedback card Expanded pet feedback card Pull-to-refresh on Feedback Settings screen

### Acceptance Criteria

| AC | Text | Entry Point to Feedback Settings screen | Error handling when opening Feedback Settings screen | Feedback Settings screen UI | Minimized/maximized pet feedback cards: general description | Minimized pet feedback card | Expanded pet feedback card | Pull-to-refresh on Feedback Settings screen |
|---|---|---|---|---|---|---|---|---|
| AC01 | Precondition: Manual Feedback sheet is opened.If I tap on the Gear icon and settings data from BE is successfully received, then:the Feedback Settings screen should be opened.FigmaNote: BE task is required to update API HALO-23058 - BE: Update Feedback List API to return info about the feedbacks of all pets with the assigned collars Open Pavel, please add details |
| AC02 | Precondition: Manual Feedback sheet is opened.If I tap on the Gear icon and something goes wrong, then:(Native apps) ME14-F04. Unified errors handling (REST API, screens with lists) should be appliedthe error text should start from 'Feedback Settings aren't available ...' |
| AC03 | The Feedback Settings screen should show the list of the pet feedback cards. |
| AC04 | Only pets with the assigned collars should be displayed in the list on the Feedback Settings screen. |
| AC05 | The list of the pet feedback cards should be sorted alphabetically A→ Z. |
| AC06 | The Feedback Settings screen should be scrollable if all cards doesn't fit into the screen |
| AC07 | If I tap on the Back button on the Feedback Settings screen, then:the Feedback Settings screen should be closedManual Feedback bottom sheet should be shown |
| AC08 | If I tap on the Info icon on the Feedback Settings screen, then: the standard Help screen should be opened, will be implemented later within https://linear.app/fueled/issue/HALO-220/ios-implement-need-help-screen-navigation-via-top-nav-bar |
| AC09 | Pet Feedback Card can have 2 states:minimizedexpanded |
| AC10 | If I tap on the arrow on the minimized card, then:the card should be expanded. |
| AC11 | If I tap on the arrow on the expanded card or the bottom part of the expanded card, then:the card should be minimized. |
| AC12 | Several pet feedback cards can be expanded at a time. |
| AC14 | If I open the Feedback Settings screen and only one pet with the assigned collar in the account, then: the pet feedback card should be expanded by default. |
| AC15 | If I open the Feedback Settings screen and 2+ pets with the assigned collars in the account, then:all cards should be minimized by default. |
| AC16 | The previous expanded/minimized state should be cached during a session (while the app remains open or in background) and reset to the default state on app relaunch (all cards collapsed when there are multiple pets and card expanded when there is one pet). |
| AC17 | The minimized card should consist of:pet avatar / placeholder + Halo ringpet nameDown arrow icon |
| AC18 | The expanded card should consist of:pet avatar / placeholder + Halo ringpet nameup arrow iconthe list of the tiles with the feedbacks |
| AC19 | The each feedback tile should consist of:Feedback iconFeedback type\< if sound or vibration, then sound/vibration name\> \<if static, then static level\>Right arrow iconNote: the logic of tap on the feedback type will be described in the next user stories |
| AC20 | Precondition: Feedback Settings screen is openedPull-to-refresh should be available on the screen, see the details in (Native apps) ME14-F05. Pull-to-refresh (general requirements) |
