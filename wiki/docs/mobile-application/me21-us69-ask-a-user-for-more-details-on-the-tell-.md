---
title: "ME21-US69. Ask a user for more details on the 'Tell Us About Yourself' screen"
sidebar_label: "ME21-US69. Ask a user for more details on the 'Tell Us About Yourself' screen"
sidebar_position: 414
last_modified: "Dec 10, 2024"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Jira ticket | Related requirements | History of changes |
|---|---|---|---|---|
| APPROVED |
| Galina Lonskaya Zakhar Makarevich Alina Sharshun [X] Dmitry Kravchuk Kirill Akulich Katherina Kaplina |
| HALO-12614 - BE+MOB: ME21-US69. Ask a user for more details on the 'Tell Us About Yourself' screen Closed |
| ME21-US09. Onboarding: flow completion |
| 09 Jul 2024 draft user story is created |# User story

\> As Halo mob app user, I want to provide additional information about myself through two new questions on the Tell us about yourself screen so that my future product experience will be personalized.

# Acceptance criteria

| AC | Description |  | AS IS | TO BE: see Figma | Q1 Have you trained dogs before? | Q2 What are your primary goals for your collar? | Updates for Users Who Signed Up via Third-Party Accounts |  |
|---|---|---|---|---|---|---|---|---|
| ME21-US69-AC01 | AS ISTO BE: see FigmaProgress barn/awill be added within the different user story: (NI) ME21-US70. Update 'progress bar' displaying logic in FTUE (Onboarding) flowQuestion mark iconn/aadded, see AC below: ME21-US69-AC12ButtonAdd Photo + photo placeholderremovedTitleTell Us Your NameWelcome to the Halo Pack!Text We will ..see the text in FigmaFieldFirst nameno changesFieldLast nameno changesNote with a linkPlan to share the Halo ... removedQuestion 1n/aadded, see AC below: ME21-US69-AC02 – AC03Question 2n/aadded, see AC below: ME21-US69-AC04 – AC09Button NextUI is updated, see AC below: ME21-US69-AC14 – 15 | Progress bar | n/a | will be added within the different user story: (NI) ME21-US70. Update 'progress bar' displaying logic in FTUE (Onboarding) flow | Question mark icon | n/a | added, see AC below: ME21-US69-AC12 | Button | Add Photo + photo placeholder | removed | Title | Tell Us Your Name | Welcome to the Halo Pack! | Text | We will .. | see the text in Figma | Field | First name | no changes | Field | Last name | no changes | Note with a link | Plan to share the Halo ... | removed | Question 1 | n/a | added, see AC below: ME21-US69-AC02 – AC03 | Question 2 | n/a | added, see AC below: ME21-US69-AC04 – AC09 | Button | Next | UI is updated, see AC below: ME21-US69-AC14 – 15 |
| Progress bar | n/a | will be added within the different user story: (NI) ME21-US70. Update 'progress bar' displaying logic in FTUE (Onboarding) flow |
| Question mark icon | n/a | added, see AC below: ME21-US69-AC12 |
| Button | Add Photo + photo placeholder | removed |
| Title | Tell Us Your Name | Welcome to the Halo Pack! |
| Text | We will .. | see the text in Figma |
| Field | First name | no changes |
| Field | Last name | no changes |
| Note with a link | Plan to share the Halo ... | removed |
| Question 1 | n/a | added, see AC below: ME21-US69-AC02 – AC03 |
| Question 2 | n/a | added, see AC below: ME21-US69-AC04 – AC09 |
| Button | Next | UI is updated, see AC below: ME21-US69-AC14 – 15 |
| ME21-US69-AC02 | The switcher should have two states: ON and OFF.Note: see ME21-US69-IN01 |
| ME21-US69-AC03 | By default, the switcher should be in the OFF position. |
| ME21-US69-AC04 | Checkbox options should have values presented in Figma. |
| ME21-US69-AC05 | By default, none of the checkboxes should be selected. |
| ME21-US69-AC06 | When a checkbox is selected, it should visually indicate that it is checked. |
| ME21-US69-AC07 | When a checkbox is deselected, it should visually indicate that it is unchecked. |
| ME21-US69-AC08 | I can select any combination of checkboxes from 0 to 4. |
| ME21-US69-AC09 | If the text for any checkbox option does not fit within the width of the screen, it should wrap to the next line. |
| ME21-US69-AC10 | If I sign up using Facebook, Gmail, or Apple ID, then: "Tell Us About Yourself" screen should be displayed as the first step of FTUE/Onboarding process. Note: this screen was previously skipped for users signing up via Facebook and other platforms |
| ME21-US69-AC11 | Precondition: I signed up using Facebook, Gmail, or Apple IDThe "Tell Us About Yourself" screen must pre-fill with the name retrieved from the third-party account. |
| ME21-US69-AC12 | The standard Questionmark icon should be added to the up right corner. See the source user story: ME21-US04. Onboarding: 'Questionmark' icon for user support (-\>Need Help screen) |
| ME21-US69-AC13 | If the content does not fit within the screen dimensions, the screen should be scrollable. |
| ME21-US69-AC14 | The Next button should be pinned to the bottom of the screen. |
| ME21-US69-AC15 | The "Next" button should have a different width. |Note: possibility to edit the answers to the added questions will be a separate PBI. Will be done later, included into FTUE Onboarding Kaizen

### Implementation notes

| IN | Description |
|---|---|
| ME21-US69-IN01 | 'Null' should be written in DB for the existing users who haven't provided an answer to 'Have your trained the dogs before'. |
| ME21-US69-IN02 | Amplitude events related to this screen should be added: |
| ME21-US69-IN03 | Nice to have (as of 7/29/2024 agreed with Victor O to postpone, since there is no BE capacity at the moment due to vacations):(1) changing the text of the checkbox options via backend configuration(2) enabling the addition and removing of checkbox options through backend configurationSee the link: https://softeq.slack.com/archives/C016D4R0P2S/p1721140959598309?thread_ts=1721129560.940259&cid=C016D4R0P2S |
