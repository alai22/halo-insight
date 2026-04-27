---
title: "ME05-US58. UI/UX redesign of IF card and new entry point for sending IF"
sidebar_label: "ME05-US58. UI/UX redesign of IF card and new entry point for sending IF"
sidebar_position: 322
author: "Ekaterina Dupanova"
---

Page info| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Timofey Burak [X] |
| HALO-17012 - MOB: ME05-US58. UI/UX redesign of IF card and IF entry point changes Closed |
| History of changes19 Jun 2023 draft story is created by Ekaterina Dupanova 27 Jun 2023 story is proceeded by Galina Lonskaya since Kate is on vacation |Contents- [User story](#ME05US58.UI/UXredesignofIFcardandnewentrypointforsendingIF-Userstory)
- [Acceptance criteria](#ME05US58.UI/UXredesignofIFcardandnewentrypointforsendingIF-Acceptancecriteria)

Background and goalWe need to decrease number of steps required in order to send IF.

# User story

\> As Halo app account owner I want to have simpler UX of IF sending flow so that I can send IF feedbacks more quickly.

# Acceptance criteria

| AC | Description | Links | Sending IF entry point changes | Changes in pet selection after the opening of IF card | IF card redesigntechnically one card will be used for both cases when there is only one pet with the assigned collar in the account or more pets with the assigned collars some other minor UI updates of IF will be introduced. | General changes related to IF card | Pets on IF card | Selected pets on IF card | IF buttons on IF card |
|---|---|---|---|---|---|---|---|---|---|
| AttentionAll logic that is not described as changed with this user story should be stay the same (e.i. errors, etc.) |
| ME05-US58-AC01 | 'Sending IF' button should be removed from the Find card. | https://zpl.io/8lxByOKiphone SEhttps://zpl.io/7woLKqE |
| ME05-US58-AC02 | 'Hand' button (=send instant feedback (IF)) should be added to My Map. | https://zpl.io/noMA1Gr |
| ME05-US58-AC03 | 'Hand' button should be displayed above 'Map Settings' button. | - |
| ME05-US58-AC04 | No matter how many buttons are displayed on the right side of the screen (2,3,4), there must be the same vertical distance between all the buttons.Note for dev: it was mentioned on the ref that all buttons on the right side of the screen should be put in the container, in order to meet requirements mentioned within this AC. | - |
| ME05-US58-AC05 | 'Hand' button should be displayed on My Map, only if I have at least one pet with the assigned collar within my account. | - |
| ME05-US58-AC06 | Precondition: Pet card/Basic training is opened and I have 1 or more pets with the assigned collars in my account. If I tap 'Hand' button, then: IF card with the pet selected should be displayed (the pet to which the pet card or training belonged). Note for dev: the selection choice for the future reusing can be stored locally on the mobile device. | - |
| ME05-US58-AC07 | Precondition: My Map is opened and I have one pet only with the assigned collar in my account. If I tap 'Hand' button, then: IF card with the pet selected should be displayed. | - |
| ME05-US58-AC08 | Precondition: My Map is opened and I have more then one pet with the assigned collars in my account and the info the pet selection choice is availbale. If I tap 'Hand' button, then: IF card with the previously selected pets should be displayed. | - |
| ME05-US58-AC09 | Precondition: My Map is opened and I have more then one pet with the assigned collars in my account and there is no info about last selection choice. If I tap 'Hand' button, then: all pets should be displayed as selected. | - |
| ME05-US58-AC10 | In case last time when I opened IF card, I deselected all pets, then:when I open IF next time, all pets should be selected by default. | - |
| ME05-US58-AC11 | 'Apply feedback for \<Pet name\>'/'Select Pets to Apply feedback' title should be changed to 'Send Feedback to:' title. | - |
| ME05-US58-AC12 | '\<pet name\>’s feedback settings are available at the bottom of the pet card on My Map' text should not be displayed on IF card anymore. | - |
| ME05-US58-AC13 | 'Select All/Unselect All' button should be displayed only if I have more than 1 pet with the assigned collar.Note: previously this button displayed for all cases. | https://zpl.io/vMrdBlQhttps://zpl.io/dxEWAkKhttps://zpl.io/xmyoB1m |
| ME05-US58-AC14 | The pets with the assigned collars should be displayed under 'Send Feedback to' title in all cases, even when there is one pet with the assigned collar only. | - |
| ME05-US58-AC15 | In case all pet are not feet into the screen width, a horizontal scroll should be available to view pets and pet checkboxes should be displayed as non-cyclic carousel. | - |
| ME05-US58-AC16 | Pet sorting should happen when I open the IF card (no shuffling when I am already ON the IF card). | - |
| ME05-US58-AC17 | Sorting pets should be based on recent received telemetry when I open the IF card. | - |
| ME05-US58-AC18 | Pet checkbox tile element should consist of:\<Pet avatar or placeholder\> with Halo ring \<Pet name\>Tick or empty space and frame, see the details below. | - |
| ME05-US58-AC19 | If I tap on any non-selected pet on IF, then: the pet should become selected:the blue tick should be displayed;the blue frame should be displayed. |  |
| ME05-US58-AC20 | If I tap on any selected pet on IF, then: the pet should become unselected:the tick should disappear;the gray frame should be displayed. |  |
| ME05-US58-AC21 | IF buttons should be displayed as a non-cyclic carousel with horizontal swipe availability. Note: UI design of the buttons and animation are slightly updated. Please see UI design and decrease the animation in the size. | - |
| ME05-US58-AC22 | The part of the first IF button that is not fully fit should be always partly displayed when I just open IF card. Note: it's required in order the user might understand that element has horizontal scroll. | - |
| ME05-US58-AC23 | The sequence of the IF buttons should be the following:WarningBoundary Emergency WhistleGood DogGo Home | - |
