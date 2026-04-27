---
title: "[Not implemented] ME04-US50. Create new fence/Edit fence posts: Hybrid GPS logic update"
sidebar_label: "[Not implemented] ME04-US50. Create new fence/Edit fence posts: Hybrid GPS logic update"
sidebar_position: 132
last_modified: "Apr 19, 2021"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| HALO-6561 - ME04-US50. Create a fence (mixed flow): Weak GPS logic update Closed |# User Story

\> As an account owner I want to see Hybrid GPS icon near the collar pin when I create/edit fence posts so that I can understand that the collar cannot identify collar's location precisely at the moment. The same logic has been already applied in [BL] ME07-US44. Return back 'Hybrid GPS' status

# Acceptance criteria

| AC | Description | iOS screen design /implementation status | Android screen design /implementation status |
|---|---|---|---|
| ME07-US50-AC01 | 'Hybrid GPS' status should be determined on the basis of GPS status instead of accuracy. The same logic as for [BL] ME07-US44. Return back 'Hybrid GPS' status. | - | - |
| Next ACs are implemented, just re-written in accordance with new approach for 'Hybrid' status determination. |
| ME07-US50-AC02 | Collar pin in 'Hybrid GPS/In between' status should have the following UI:Hybrid GPS icon should be displayed near the collar pin ;the collar pin should be whitened out.Note: the same UI as applied for pet pins on My Map. | Pic 1 Create New Fence -Collar in Hybrid GPS status, see Zeplin | The same UI as for iOS |
| ME07-US50-AC03 | ME04-US37-AC01 should be updated, see a new description below:Precondition: The app received at least one accurate and valid collar location during the current connection session.In case the collar cannot identify whether it 'outdoor' or 'indoor' during 'Create New Fence' process, then:the collar pin should be displayed in 'Hybrid GPS' status, see the details in ME07-US50-AC01. | - | - |
| ME07-US50-AC04 | ME04-US37-AC01 should be updated, see a new description below:Precondition: The app received at least one accurate and valid collar location during the current connection session.In case the collar cannot identify whether it 'outdoor' or 'indoor' during 'Edit Fence Posts' process, then:the collar pin should be displayed in 'Hybrid GPS' status, see the details in ME07-US50-AC01. | - | - |
| ME07-US50-AC05 | ME04-US37-AC02 should be updated, see the updated condition below:If the first received coordinate during the connection session is invalid/or in 'Hybrid GPS/In between status', then:the collar pin should be placed in my location (account owner's location);the collar pin should be displayed in 'Hybrid GPS' status, see the details in ME07-US50-AC01. | - | - |
| ME07-US50-AC06 | ME04-US37-AC03 should be updated, see the updated condition below:Precondition: GPS is disabled on the phoneIf the first received coordinate during the connection session is invalid/or in 'Hybrid GPS/In between' status, then:then the collar pin should be displayed in the сenter of the screen;the collar pin should be displayed in 'Hybrid GPS' status, see the details in ME07-US50-AC01. | - | - |
| ME07-US50-AC07 | ME04-US37-AC04 should be updated, see the updated condition below:If I tap on the "Add GPS"/"Move" button and the collar is in 'Hybrid GPS/In between' status, then:the following toast message should be displayed: "Poor signal received from GPS. Please try again.";the fence post location should not be updated. | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME07-US50-IN01 | The following logic for the location statuses calculation should be applied on Mob and BE for old FW versions:if the accuracy \<999, then 'outdoor' status;if the accuracy =999, then 'Hybrid GPS ('in-between'/'not available') status;If the accuracy \>999, then 'Indoors' status.NOTE: for backwards compatibility with historical app, new FW will force 'indoor' to use 1001+ values |
| ME07-US50-IN02 | The following approach should be applied for new FW versions: FW will send the location statuses themselves: 'outdoor', 'indoor', 'in-between/Hybrid GPS'.Note 1: MQTT and GAP/GATT contract should be updated accordingly.Note 2: The logic how FW should calculate statuses is presented here: ME03-US49. Collar calibration process (phase 1). |
