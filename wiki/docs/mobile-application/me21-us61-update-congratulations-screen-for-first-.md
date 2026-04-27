---
title: "ME21-US61. Update 'Congratulations' screen for first time users"
sidebar_label: "ME21-US61. Update 'Congratulations' screen for first time users"
sidebar_position: 357
author: "Kiryl Trafimau"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Kirill Akulich Dmitry Kravchuk |
| HALO-17865 - MOB: ME21-US61. Update 'Congratulations' screen for first time users Closed HALO-21274 - [Critical] MOB: Rename 'Take Collar Outside' button to 'Continue to My Map' on 'Congratulations' screen Closed |
| 09 Jul 2024 the user story draft is created03 Sep 2024 'Take Collar Outside' is renamed to 'Continue to My Map' |Table of Contents

User story Acceptance criteria

# User story

\> As a Halo account owner I want to view the updates Congratulations screen so that I can receive WoW first time experience and view m as soon as possible.

# Acceptance criteria

| AC | Description | Item | AS IS | TO BE: Figma link |
|---|---|---|---|---|
| ME21-US61-AC01 | UI of 'Almost Ready' screen should be updated. See the table below. ItemAS ISTO BE: Figma link Imageblue 'tick'Removed TitleAlmost Ready!Congratulations!Text:Before you attempt to use your Halo Collar ...See new text in FigmaImage-Animation should be shown, see ME21-US61-AC02Button Start Halo TrainingContinue to My Map, see ME21-US61-AC03SubtitleDo you have another Halo Collar?RemovedTextTo add it now, click the link below. You can also add it later from Settings \> My Collars.RemovedFrame with the text-See 'Important Reminder:' frame, see ME21-US61-AC04ButtonAdd Another CollarNo changesButtonPlusRemovedBackground colorWhiteNo changesNote for QA: 'Congratulations' screen is displayed only when attaching the collar within FTUE onboarding. When attaching the collar from Settings / Pet Card / Find card 'Congratulations' screen is not displayed. | Image | blue 'tick' | Removed | Title | Almost Ready! | Congratulations! | Text: | Before you attempt to use your Halo Collar ... | See new text in Figma | Image | - | Animation should be shown, see ME21-US61-AC02 | Button | Start Halo Training | Continue to My Map, see ME21-US61-AC03 | Subtitle | Do you have another Halo Collar? | Removed | Text | To add it now, click the link below. You can also add it later from Settings \> My Collars. | Removed | Frame with the text | - | See 'Important Reminder:' frame, see ME21-US61-AC04 | Button | Add Another Collar | No changes | Button | Plus | Removed | Background color | White | No changes |
| Image | blue 'tick' | Removed |
| Title | Almost Ready! | Congratulations! |
| Text: | Before you attempt to use your Halo Collar ... | See new text in Figma |
| Image | - | Animation should be shown, see ME21-US61-AC02 |
| Button | Start Halo Training | Continue to My Map, see ME21-US61-AC03 |
| Subtitle | Do you have another Halo Collar? | Removed |
| Text | To add it now, click the link below. You can also add it later from Settings \> My Collars. | Removed |
| Frame with the text | - | See 'Important Reminder:' frame, see ME21-US61-AC04 |
| Button | Add Another Collar | No changes |
| Button | Plus | Removed |
| Background color | White | No changes |
| ME21-US61-AC02 | The following animation should be shown on 'Congratulations' screen, see the file: congratulations_screen_revised.jsonNote: the animation is illustrative in nature, not real pet pin is displayed |
| ME21-US61-AC03 | Precondition: 'Congratulations' screen is opened. If I tap on the 'Continue to My Map' button, then the following should happen:'My Map' tab should open;the pet card of the newly added pet should be displayed in the default view. |
| ME21-US61-AC04 | The 'Important Reminder' frame should appear simultaneously with the animation start, using a 'fade-in' effect. |
| ME21-US61-AC05 | Two bottom buttons should be pinned to the bottom of the screen. |
