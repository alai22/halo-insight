---
title: "[Obsolete] ME05-US44 [AFFMP]: Retry applying feedback for the pets who did not receive it"
sidebar_label: "[Obsolete] ME05-US44 [AFFMP]: Retry applying feedback for the pets who did not receive it"
sidebar_position: 135
last_modified: "Mar 30, 2021"
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| ME05-EP02. Apply feedback for multiple pets |
| DRAFT |
| Nicolay Gavrilov |
| HALO-6589 - MOB [RI]: ME05-US43. Retry applying feedback for the pets who did not receive it Closed |# User story

\> As a user I want to have the 'Retry' button on the pop-up with the list of pets that didn't get the feedback so that I could quickly resend it to these pets. From the training standpoint, it is crucial to be able to apply feedback as fast as it is possibe so pets was aware why they received it.

# Acceptance criteria

| AC | Text | iOS design/notes | Android design/notes | iOS / Android implementation status | IOS TO DO | ANDROID TO DO |
|---|---|---|---|---|---|---|
| ME05-US44-AC01 | Users should be able to resend the feedback by tapping on the corresponding button on the pop-up with the list of pets that didn't get it. |  | TBD |
| ME05-US44-AC02 | When the user taps on the 'Retry' button, the feedback should be resent only to those pets that didn't get the feedback during the previous attempt. | - | - |
| ME05-US44-AC03 | After the user taps on the 'Retry' button, the app should close the pop-up and show the 'Apply feedback for multiple pets' action sheet with the spinner over the corresponding feedback button and with the disabled UI elements. | - | - |
| ME05-US44-AC04 | The cases with successful and unsuccessful applying the feedback for the pets should be handled as it is described in ME05-US24 [AFFMP]: 'Apply feedback for multiple pets' action sheet | - | - |
