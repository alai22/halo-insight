---
title: "ME06-US17. Display state of feedback settings on 'Feedback' tab"
sidebar_label: "ME06-US17. Display state of feedback settings on 'Feedback' tab"
sidebar_position: 81
last_modified: "Jun 12, 2020"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owners | Link to JIRA Issue |
|---|---|---|---|
| ME06. Trainings |
| APPROVED (SQ) |
| Nicolay Gavrilov |
| HALO-4059 - MOB GOAL: ME06-US17. Display state of feedback settings on 'Feedback' tab Closed |# User story

\> As a user I want to see the time of the last feendback settings changes on the "Feedback" tab so that I was sure that the settings are successfully saved when I tap on 'Done' button. With this info it also will be clear that the settings are not saved in case accidentally decide to leave the a feedback setting screen without saving the changes.

# UI design

| Old design | New design |
|---|---|
|  |  |# Acceptance criteria

| AC | Text | Notes/Links/Wireframes |
|---|---|---|
| ME06-US17-AC01 | So that the users will always see the feedback settings tab when the Pet Training screen is opened, the tab should be moved to the left. | N/A |
| ME06-US17-AC02 | The state of feedback settings is shown on the pet feedback settings tab. | N/A |
| ME06-US17-AC03 | 'Default feedback settings' caption is displayed in case none of the prevention or encouragement settings of the pet are changed from the defaults. | Link to the screen design in Zeplin |
| ME06-US17-AC04 | If at least one of the prevention or encouragement settings is changed, the "Feedback settings changed: \<time\>" caption is shown on the pet feedback settings tab. | Link to the screen design in Zeplin |
| ME06-US17-AC05 | "Feedback settings changed: \<time\>" indication works similarly to 'Last trained: \<time\>' indication on pet training cards. | BR-16 Passed time format |
| ME06-US17-AC06 | 'Default feedback settings' caption never appears again after the feedback settings were changed. | N/A |
