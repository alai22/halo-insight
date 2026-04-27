---
title: "ME21-US89. Send SDK event 'сollar_taken_outside_first_time' to Braze"
sidebar_label: "ME21-US89. Send SDK event 'сollar_taken_outside_first_time' to Braze"
sidebar_position: 456
last_modified: "Nov 05, 2024"
author: "Mariya Kolyada"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| HALO-21408 - BE+MOB: Send SDK event 'сollar_taken_outside_first_time' to Braze (will be used as IAM trigger) Closed |
| 18 Sep 2024 Mariya Kolyada created the initial user story.11 Oct 2024 Mariya Kolyada updated the user story according to the final implementation. |Table of Contents

User story Acceptance criteria Implementation notes

# User story

\> As a Halo Marketing Team representative I want that the app notifies Braze when the collar has been taken outdoor for the first time after FTUE completion so that we can create a Braze campaign that navigates users to the Learn tab so increase probability that user proceed with learning before using a collar.

# Acceptance criteria

| AC | Description |
|---|---|
| ME21-US88-AC01 | Precondition:IF:I finished FTUE.Implementation noteBE can receive this information from MOB.ANDI bring one of my collars outside for the first time in my account.ANDMy collar changes the GPS Level to Outdoor/High (see How To Understand GPS Level values on GPS Signal Level Settings screen).ANDAny collar is less than 1 km away from my device's current location.THEN:The app should send SDK event: 'сollar_taken_outside_first_time' to BEAM → Braze. NotesThe GPS Level = Outdoor/High has been chosen on purpose instead of GPS initialization completion status.Once Braze receives the event - there still be some delay and more filters by users (e.g. has the Learn tab already been opened before, etc) before user will see the Braze campaign navigating to the Learn tab.The 'less than 1 km away' check is needed in case collar had some history data and for some reason by default assign to the collar it's previous location other than near to the user.The app will not send the event if at least one of the following conditions is met:The app cannot receive the collar's telemetry.Collars's GPS status is different from Outdoor/High.The app cannot receive user's location to calculate the distance between collar and user's device. |
| ME21-US88-AC02 | IF:I bring my second and next collars outside.THEN:NO event sending is needed. Implementation noteEvent sending should be done only on any first collar bringing outside + less 1 km from user after FTUE.This check is done both on MOB and BEAM sides:In mob cache, thus in case user logs in from another device or reinstalls the app, the data about the sent event will be missed and the app may send event to BEAM again.However, the BEAM sends it only once anyway. |
| ME21-US88-AC03 | IF:My collar has been unlinked from another Halo account for which this event has been sent.AND: I added the same collar to my Halo account.AND:I finished FTUE.ANDI bring this collars outside for the first time.ANDMy collar changes the GPS Level to Outdoor (see How To Understand GPS Level values on GPS Signal Level Settings screen).ANDAny collar is close enough to our current location (less than 1 km away).THEN:The app should send SDK event: 'сollar_taken_outside_first_time' to Braze again. NoteEvent sending should be connected to the user's Halo account, not to the collar device itself. |
| ME21-US88-AC04 | IF:Event has NOT been delivered successfully to Braze.THEN:The app should try to send it again until it is successfully delivered.Implementation noteThe app sends it to BEAM again and again until success.BEAM sends it to Braze again and again until success. |
| ME21-US88-AC05 | See details of the Braze event here:https://docs.google.com/spreadsheets/d/1Jb8i1DJRr-uxO8w9x1ieRA351QFsOsmDWdCB26db84o/edit?gid=727237032#gid=727237032 |# Implementation notes

| IN | Implementation notes |
|---|---|
| ME21-US89-IN01 | For BE:Parallel processing of 2 collars at the same time and sending of 2 events is not an issue that we should focus on fixing.It seems it should NOT be a frequent case. And it is possible to filter on the Braze side so that the same user doesn't view the same campaign again. |
