---
title: "ME05-US53. Show special error when IF is not delivered due to time is out"
sidebar_label: "ME05-US53. Show special error when IF is not delivered due to time is out"
sidebar_position: 704
last_modified: "Jun 23, 2023"
author: "Galina Lonskaya"
---

| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya Eugene Paseka Timofey Burak [X] Kirill Akulich Valeria Malets |
| HALO-14213 - MOB: ME05-US53. Show special error when IF is not delivered due to time is out Closed |
| 12 Oct 2022 draft story is created |# Contents

Background User story Acceptance criteria Send feedback to one pet Send feedback to multiple pets Implementation notes

# Background

As of 10/12/2022 'connectivity' error toast message is displayed, when the instant feedback is not delivered due to timeout

# User story

\> As an account owner, I want to see a special toast when the instant feedback is not delivered because of time is out so that I can understand that I need to retry the instant feedback sending one more time.

# Acceptance criteria

| AC | Text | Send feedback to one pet | Send feedback to multiple pets |
|---|---|---|---|
| ME05-US53-AC01 | The acceptance criteria below should be applied for the following scenarios:When the user applies feedback from the pet cardWhen the user taps the' Test on collar' button from:'Emergency feedback' settings screen'Warning feedback' settings screen'Boundary feedback' settings screen'Good behavior feedback' settings screen'Return whistle feedback' settings screen'Heading home feedback' settings screen |
| ME05-US53-AC02 | If the instant feedback is not delivered to my pet due to the timeout (see ME05-US52-AC01, AC02), the following toast message should be displayed: the error toast icon'Feedback was not received by your dog due to network congestion. Please try again.' textNote 1: see the trigger described on tech level within ME05-IN53-AC01Note 2: toast message will be transferred to the table with toasts later (for BA) |
| ME05-US53-AC03 | If the instant feedback is not delivered to my pets due to the timeout (see ME05-US52-AC03), the following toast message should be displayed: 'Message took too long. Please try again.' Note: see the trigger described on tech level within ME05-IN53-AC01 |# Implementation notes

| IN | Description |
|---|---|
| ME05-IN53-AC01 | Feedback is completed with commandexpire. |
