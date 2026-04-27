---
title: "(NA) ME04-F04. Unique Fence: Recommend to read the article"
sidebar_label: "(NA) ME04-F04. Unique Fence: Recommend to read the article"
sidebar_position: 522
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-669/[ios]-unique-fence-recommend-to-read-the-articleAndroid: https://linear.app/fueled/issue/HALO-670/[android]-unique-fence-recommend-to-read-the-article |
| 27 Mar 2025 Mariya Kolyada created the initial version of a user story.15 Apr 2025 Dmitry Kravchuk added tech details |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to be recommend to read teh article if I have unstandard fence so I make sure if it works properly for my case and dog never receives false feedback.

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-F04-AC01 | PreconditionAt least one of the following conditions are met:Fence intersects the road.Fence registered property had buildings inside and now has 0 buildings included inside the fence.Fence intersects the neighbouring buildings (buildings outside the registered property where the fence is created).If I tap the 'Save' button on:either 'Add Fence: Step 4. Name Fence' screen,or 'Edit Fence' screenthen the app should:Navigate to My Fences screen.Display added/edited fence on the map.Display the 'Unique Fence' pop-up over it.NoteIf there were 0 buildings inside fence before edit - no unique fence pop-up is needed. | Figma |
| ME04-F04-AC02 | If I tap the 'View Tips', then the app should:Leave the app.Open the https://halocollar.zendesk.com/hc/en-us/articles/20838599422103 link in the browser. |
| ME04-F04-AC03 | The link should be manageable via config.support.TipsForUniqueFencesArticleUrl from GET /configuration |
| ME04-F04-AC04 | If I tap the 'Continue' button, then the app should:Just close the pop-up. |Tech details

The intersection with the road will be calculated during the fence validation process, so we can use the value from thereBefore validation, we will need to determine which buildings are included in the parcel - Validation of intersections with objects on the map#Buildings. All other buildings would then be considered neighboring buildingsIf there were no buildings in the original parcel, the second and third conditions would not be consideredWe do not check intersections with neighboring buildings during validation. So this value has to be calculated separately

During editing, we take the parcel from the local cache (if it is there)If it is not there, we cannot determine if the parcel contains buildings inside, and we will not have neighboring buildings, as all buildings are considered main buildings.

It may be easier to do the calculation before exiting the save/edit fence screen and pass the value to the previous screen


