---
title: "ME05-US61. Save the Instant Feedback carousel state"
sidebar_label: "ME05-US61. Save the Instant Feedback carousel state"
sidebar_position: 707
last_modified: "Sep 12, 2023"
author: "Galina Lonskaya"
---

Page info| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya Pavel Leonenko |
| HALO-17557 - MOB: ME05-US61. Save the Instant Feedback carousel state Closed |
| History of changes07 Sep 2023 draft story is created by Galina Lonskaya |Contents- [User story](#ME05US61.SavetheInstantFeedbackcarouselstate-Userstory)
- [Acceptance criteria](#ME05US61.SavetheInstantFeedbackcarouselstate-Acceptancecriteria)

Background and goalSome of the Halo App users wrote in the app feedbacks that it's not convenient each time to scroll to the required IF icon.

# User story

\> As Halo app account owner, I want the IF icon carousel state to be saved when I close the IF card, so that when I reopen the IF card, I can continue viewing the IF icon carousel from where I left off.

# Acceptance criteria

| AC | Description | Links |
|---|---|---|
| ME05-US61-AC01 | When I interacts with the carousel by swiping through the IF buttons on the IF card, the app should save the current state of the carousel locally on the mobile device when the IF card is closed. | - |
| ME05-US61-AC02 | When I reopen the IF card, then the same state of the IF carousel should be displayed as I've seen the last time when I've opened the IF card. | - |
| ME05-US61-AC03 | If the data about the IF carousel state is not exist/lost, then the default state of IF carousel should be displayed. Note: the data might be lost due to the following factors: app reinstallation app data clearing | See Zeplin |
