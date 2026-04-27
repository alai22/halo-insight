---
title: "ME04-US64. Fence edit. Add roads, buildings and water intersection validation"
sidebar_label: "ME04-US64. Fence edit. Add roads, buildings and water intersection validation"
sidebar_position: 349
last_modified: "Feb 05, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-18050 - MOB: ME04-US64. Fence edit. Add roads, buildings and water intersection validation Closed |
| Click here to expand...As of 12 Oct 2023 - 16 Oct 2023 :Mariya Kolyadacreated the initial version of US.As of 17 Oct 2023 - 18 Oct 2023 :Mariya Kolyada finalized the US with the final text version and comments after refinement + Added Jira ticketAs of 17 Jan 2024 Mariya Kolyada added ME04-US62-AC03 with resources.As of 29 Jan 2024 Mariya Kolyada added AC04 and AC05.As of 05 Feb 2024 Mariya Kolyada updated AC04 and removed AC05. |# Contents

User Story Acceptance criteria Table ME04-US64-T1

# User Story

\> As a Halo acount owner I want to be notified if my fence intersects forbidden and unsafe zones so that I can adjust fence borders and prevent my dog from wrong feedback or presense on unsafe zone.

# Acceptance criteria

| AC | Description | Case | Count from and/or resource | Edit screen opened from | Behavior |
|---|---|---|---|---|---|
| ME04-US62-AC01 | Add new roads, buildings, and water intersection validation described in the Table below. |
| ME04-US62-AC02 | The app should display these warnings just to warn but allow to save the edited fence even user leaves the intersection without changes. |
| ME04-US62-AC03 | The app should use different resources to validate intersections following requirements:CaseCount from and/or resourcePost is on the road bordering the parcel:that included fence before editwhere cadastral data exists Count from parcel borderParcel resource (currently ReportAll)Post is on the road bordering the parcel:that didn't include the fence before the editand/orwhere no cadastral data existsCount from road Map resource (currently Mapbox)Post is on the waterMap resource (currently Mapbox)Post is on the buildingMap resource (currently Mapbox) | Post is on the road bordering the parcel:that included fence before editwhere cadastral data exists | Count from parcel borderParcel resource (currently ReportAll) | Post is on the road bordering the parcel:that didn't include the fence before the editand/orwhere no cadastral data exists | Count from road Map resource (currently Mapbox) | Post is on the water | Map resource (currently Mapbox) | Post is on the building | Map resource (currently Mapbox) |
| Post is on the road bordering the parcel:that included fence before editwhere cadastral data exists | Count from parcel borderParcel resource (currently ReportAll) |
| Post is on the road bordering the parcel:that didn't include the fence before the editand/orwhere no cadastral data exists | Count from road Map resource (currently Mapbox) |
| Post is on the water | Map resource (currently Mapbox) |
| Post is on the building | Map resource (currently Mapbox) |
| ME04-US62-AC04 | If I open the Fence Edit screen, then the app should:Behave according to the following requirements:Edit screen opened fromBehaviorFence Details CardDisplay the intersection warnings.Creation → Fence preview with the Edit New Fence main actionHide the intersection warningsCreation → Fence preview with water and/or roadHide the intersection warningsCreation → No cadastral data toastDisplay the intersection warnings next after 'Not supported location' toast | Fence Details Card | Display the intersection warnings. | Creation → Fence preview with the Edit New Fence main action | Hide the intersection warnings | Creation → Fence preview with water and/or road | Hide the intersection warnings | Creation → No cadastral data toast | Display the intersection warnings next after 'Not supported location' toast |
| Fence Details Card | Display the intersection warnings. |
| Creation → Fence preview with the Edit New Fence main action | Hide the intersection warnings |
| Creation → Fence preview with water and/or road | Hide the intersection warnings |
| Creation → No cadastral data toast | Display the intersection warnings next after 'Not supported location' toast |## Table ME04-US64-T1

| № | Icon | Warning on the screen | Trigger | Displaying time |
|---|---|---|---|---|
| ME04-US64-M1 |  | Your fence appears to be closer than 15 feet from a house/building. | The fence border is less than 15 feet from or intersects the building inside the fence. | Temporarily toast (4 seconds) |
| ME04-US64-M2 |  | There appears to be water inside your fence safe area. | The fence border intersects the water object (lake or river). |
| ME04-US64-M3 |  | Your fence appears to be too close to the road. | The fence border is less than 15 feet from or intersects the road. |
