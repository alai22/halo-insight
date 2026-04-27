---
title: "ME21-US22. Onboarding: Add subtitles to onboarding video"
sidebar_label: "ME21-US22. Onboarding: Add subtitles to onboarding video"
sidebar_position: 256
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Links to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Maria Shikareva [X] Nikita Krisko Siarhei Leushunou [X] Yekaterina Hovin |
| Click here to expand... HALO-13038 - MOB+BE: ME21-US22. Onboarding: Add subtitles to onboarding video Closed HALO-15131 - BE+MOB [Investigate]: Check tools for merging a file with closed captioning into onboarding video Closed |
| Click here to expand...29 Dec 2022 Maria Shikareva [X] Added ME21-US22-AC08 as discussed with Kirill Akulich. |# Contents

User story Acceptance criteria iOS changes Android changes Implementation notes

# User story

\> As a Halo app user I want to be able to watch Onboarding videos with subtitles so that it's more convenient for me and I should not turn the sound ON specially for watching those videos.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |  | Closed captioning ON | Closed captioning OFF | button state | toast appearing |  |
|---|---|---|---|---|---|---|---|---|---|
| ME21-US22-AC01 | Closed captioning should be added to all Onboarding videos.See ME21-US22-IN01 below. |  |  |
| ME21-US22-AC02 | By default the app should start displaying the video with closed captioning turned ON. | - | - |
| ME21-US22-AC03 | A user should be able to turn the closed captioning on/off. | - | - |
| ME21-US22-AC04 | English should be a closed captioning language by default.As of 14 Dec 2022 : English is the only language added. | - | - |
| iOS changes |
| ME21-US22-AC05 | A 'cc' button should be added to the existing player.Note: on iOS this functionality exists by default, tapping on this button is also handled by iOS. | - | n/a |
| Android changes |
| ME21-US22-AC06 | The following UI changes should be made:need to remove 'Previous' and 'Next' buttons;need to show a video scale above the native Android bar.QA note: it seems to be already implemented, need just to double check this.need to specify custom layout for player to add CC button;need to add a 'cross' iconit should be visible with other controls only. HALO-14521 - Android: Impossible to close prompting videos on Android. Closed | n/a | Link to Zeplin |
| ME21-US22-AC07 | When a user taps 'cc' button, then the app should:turn off/ on closed captioning;display the corresponding toast;change the 'cc' button state.Closed captioning ONClosed captioning OFFbutton statetoast appearingSubtitles/ CC turned onSubtitles/ CC turned offNote: from development perspective the toast should be the same as we use in Dog Park 'Added to calendar' (see ME20-US13-AC10 in ME20-US13. Add session to calendar). |  |  | Subtitles/ CC turned on | Subtitles/ CC turned off | n/a | - |
|  |  |
| Subtitles/ CC turned on | Subtitles/ CC turned off |
| ME21-US22-AC06 | When a user taps 'x' button, then the app should:close the video;keep the previous screen opened. | - | - |
| ME21-US22-AC07 | If a file with subtitles is missing, then the app should not show any error and should display a video without closed captioning. | - | - |
| ME21-US22-AC08 | 'cc' button should be hidden in the following cases:if a video doesn't have subtitles;when the video isn't loaded (and therefore we don't know whether the video contains subtitles or not). |  |  |# Implementation notes

| ID | Description |
|---|---|
| ME21-US22-IN01 | BE should add a file with closed captioning to config together with links for onboarding videos.https://app.frame.io/reviews/c38a4e6d-38d5-4375-bc7c-d37bde78fa79/6c967400-32b3-4762-802c-5f3158715dec |
| ME21-US22-IN02 | File should have a special format and should be provided by the Halo team. |
| ME21-US22-IN03 | For future: we'll use different languages for subtitles only; video and sound will remain the same. |
