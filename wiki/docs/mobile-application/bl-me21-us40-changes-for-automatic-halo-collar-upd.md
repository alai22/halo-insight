---
title: "[BL] ME21-US40. Changes for 'Automatic Halo Collar Updates' screen logic ('Skip' button after 5 minutes)"
sidebar_label: "[BL] ME21-US40. Changes for 'Automatic Halo Collar Updates' screen logic ('Skip' button after 5 minutes)"
sidebar_position: 277
last_modified: "Oct 28, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Timofey Burak [X] Siarhei Leushunou [X] |
| HALO-14053 - MOB: User is blocked on the 'Update Collar' screen when 'Done' button is disabled and there is no 'Skip' button Closed HALO-14191 - MOB+BE: [NI] ME21-US40. Changes for 'Automatic Halo Collar Updates' screen logic ('Skip' button after 5 minutes) Closed |
| Click here to expand...28 Oct 2022 Maria Shikareva [X] Marked the story as baselined (ME03-F09. Collar Updates). |# Contents

General description User story Acceptance criteria Implementation notes

# General description

As of 07 Oct 2022 as was clarified during testing HALO-12560 - MOB [+BE]: ME21-US07. Add FW update screens to 'Add Collar' flow Closed : sometimes SGEE updates/ FW updates are too slow for some reasons (e.g. issues with some Internet providers, time lag for initializing a collar, etc.) and the user can be blocked on the 'Automatic Halo Collar Updates' screen without any option to leave the screen ('Skip' button appears only in case of any 'negative' status but the user can be blocked in case of any status). The idea is to show a 'Skip' button in 5 minutes after user entered this screen.

# User story

\> As a Halo app user I want to see a 'Skip' button on the 'Automatic Halo Collar Updates' screen after 5 minutes so that not to be blocked on this screen if updates take too much time.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| ME21-US40-AC01 | The app should have a countdown starting from 5 minutes after opening 'Automatic Halo Collar Updates' screen (not display it on UI).Note: for more details see ME21-US40-IN01, ME21-US40-IN02 below. | - | - |
| ME21-US40-AC02 | Precondition: a countdown is started.If the user leaves the screen and opens it again, the countdown will restart from the beginning.Note: it was agreed that this is the easiest solution from implementation perspective.Note 2: if a user brings the app to the background and then to the foreground (i.e. without closing this screen), the countdown will continue. | - | - |
| ME21-US40-AC03 | '5 minutes' should be a configurable value. | - | - |
| ME21-US40-AC04 | Precondition: the countdown came to 00:00.The app should show enabled 'Skip' button (on tapping the system, should behave as described in [NI] ME21-US07. Add FW update screens to 'Add Collar' flow).Note 1: if FW update statuses are negative, the system should show a 'Skip' button without waiting for countdown. | - | - |
| ME21-US40-AC05 | After 5 minutes a 'Skip' button should always be on the screen even if the status changed from negative to positive. | - | - |
| ME21-US40-AC06 | If the app showed 'Skip' button earlier than 5 min (e.g. after a 'negative' status), and after that a status changed to any other, a countdown should not restart.ExampleA user entered the screen → a timer startedIn 1 minute download failed → the app displayed a 'Skip' buttonIn 0.5 minute download restarted → the app hides a 'Skip' buttonIn 3.5 minute timer ends → the app displays a 'Skip' button.In 5 minutes the status is changed to 'Up-to-date' → the app still displays a 'Skip' button. | - | - |# Implementation notes

| ID | Description |  |
|---|---|---|
| ME21-US40-IN01 | The best option to implement this is to use a timestamp of entering the screen.Other discussed optionsTrack time on appearing/ disappearing. Cons: if a user opens another screen above this one, the timer will stop. If a user brings the app to background, the timer will also stop.Show timer on appearing/ disappearing AND not stop timer when a user brings the app to background → there can be some issues that the app works in background, we don't notify anyone about that.There can be native iOS/ Android timers - agree to double check later and make as am improvement if required. |  |
| ME21-US40-IN02 | If a user changes the date/ time while timer is counting down, then on bringing to foreground the app will check this and show 'Skip' button MAXIMUM after 5 minutes (or even earlier). |  |
