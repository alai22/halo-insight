---
title: "ME03-US148. Log addings of a collar with FW older than 1.5.89 and trigger Braze on update"
sidebar_label: "ME03-US148. Log addings of a collar with FW older than 1.5.89 and trigger Braze on update"
sidebar_position: 638
author: "Mariya Kolyada"
---

Click here to expand...| Document status | Document owner | Link to JIRA issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| HALO-21844 - BE: ME03-US148. Log addings of a collar with FW older than 1.5.89 and trigger Braze on update Closed |
| Click here to expand...As of 14 Nov 2024 Mariya Kolyada created the initial version of user story |# Contents

User story Acceptance criteria Other non-dev updates

# User story

As a Halo account owner I want to be forbidden to add a collar with FW older than 1.5.89 and navigated to the support article with an explanation of how to upgrade the FW version so that I can use my collar with no further issues and have access to all features.

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-US148-AC01 | Precondition:My collar's FW is older than 1.5.89If I tap on the "Add Collar" button, then the app should:Log the this event to DB:TimestampUser IDCollar Serial NumberImplementation notesAgreed:Log as a separate events collar adding an attempt with the same Collar Serial Number but a different User ID.If the user deletes the account - no need to delete the event from DB. |
| ME03-US148-AC02 | Replace each time new log with the latest one. |
| ME03-US148-AC03 | If my collar notifies the system about a FW version update from a version older than 1.5.89, then the system should:Check if an unsuccessful adding try of this collar related to old FW happened: within 1 week;for the same User ID. |
| ME03-US148-AC04 | If happened corresponding defined conditions, then the system should:Send the Collar Updated event to Braze.See Braze event details here: collar_actual_firmware_applied |
| ME03-US148-AC05 | If did NOT happen corresponding defined conditions, then the system should NOT send any events. |
| ME03-US148-AC06 | Make the 1 week value configurable. |# Other non-dev updates

Update the following article by replacing a note related to that user needs to wait a bit with the note that they should wait for push/email notification about successful FW update.


