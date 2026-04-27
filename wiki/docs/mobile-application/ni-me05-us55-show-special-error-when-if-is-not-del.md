---
title: "[NI] ME05-US55. Show special error when IF is not delivered to multiple pets due to time is out"
sidebar_label: "[NI] ME05-US55. Show special error when IF is not delivered to multiple pets due to time is out"
sidebar_position: 284
last_modified: "Nov 28, 2022"
author: "Galina Lonskaya"
---

| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya Dmitry Kravchuk |
|  |
| 25 Oct 2022 draft story is created |# Contents

Background User story Acceptance criteria Implementation notes

# Background

As of 10/12/2022 'connectivity' error toast message is displayed, when the instant feedback is not delivered due to timeout

# User story

\> As an account owner, I want to see a special toast when the instant feedback is not delivered to several pets because of time is out so that I can understand that I need to retry the instant feedback sending one more time.

# Acceptance criteria

| AC | Text |
|---|---|
| ME05-US55-AC01 | Precondition: ME05-US24 [AFFMP]: 'Apply feedback for multiple pets' action sheet is opened. If the user applied feedback for multiple pets and more than one pet didn't get the feedback due to the timeout, the app should show the following pop-up:Header: Feedback to Some Pets Could Not Be ConfirmedText: Your feedback didn't reach one or more pets. Retry to these pets only?Button: Try again Button: Cancel To close the pop-up users should tap on the 'OK' button. |
| ME05-US55-AC02 | If the user applied feedback for multiple pets and more than one/several pet didn't get the feedback due to the timeout and other pet didn't receive feedback due to the collar is out of Wi-Fi/Bluetooth/Cellular range, then the app should show the following pop-up:Header: Feedback to Some Pets Could Not Be ConfirmedText: Your feedback didn't reach one or more pets. Retry to these pets only?Button: Try again Button: Cancel To close the pop-up users should tap on the 'OK' button. |# Implementation notes

| IN | Description |
|---|---|
| ME05-IN53-AC01 | Feedback is completed with commandexpire. |
