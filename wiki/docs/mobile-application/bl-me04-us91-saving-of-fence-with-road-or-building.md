---
title: "[BL] ME04-US91. Saving of fence with road or building issues pop-ups"
sidebar_label: "[BL] ME04-US91. Saving of fence with road or building issues pop-ups"
sidebar_position: 375
last_modified: "Mar 27, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Kirill Akulich |
| HALO-19169 - MOB: ME04-US91. Saving of fence with road or building issues pop-ups Closed |
| Click here to expand...As of 19 Dec 2023:Mariya Kolyadacreated the initial version of USAs of 23 Jan 2024 Mariya Kolyadaupdated the language for the 'Unique Fence' pop-up.added ACs for building intersection and Mobile analytics. |# Contents

User Stories Acceptance criteria Mobile analytics

# User Stories

\> As a Halo acount owner I want to be proposed to view tips if I saving some unusual fence or no building intersection confirmation if my fence appears to be less then 15 feet close to building according to data so that I work with my fences correctly.

# Acceptance criteria

| AC | Description | iOs design | Android design | Road intersection or excluded building | Building intersection |
|---|---|---|---|---|---|
| ME04-US91-AC01 | PreconditionAt least one of the following conditions are met:Fence intersects the road.Building is excluded from the fence.If I save the fence data/border updates, then the app should:Save the fence to DB.Open Fence Card.Display the 'Unique Fence' pop-up over the Fence card.Note'Building is excluded from the fence' means that according to cadastral data, the parcel including this fence has building(s) but user moved the fence's border so there are no buildings inside it.If the parcel itself has no buildings - then the app should NOT display this pop-up. |  | TBD |
| ME04-US91-AC02 | 'Unique Fence' pop-up should consist of the following elements:Title: 'Unique Fence'Body: 'Discover safety tips for your unique fence to protect your dog.'Buttons:View TipsContinue | - | - |
| ME04-US91-AC03 | If I click the 'View Tips', then the app should:Leave the app.Open the https://halocollar.zendesk.com/hc/en-us/articles/20838599422103 link in the browser. | - | - |
| ME04-US91-AC04 | If I click the 'Continue' button, then the app should:Just close the pop-up.Display the Fence card. | - | - |
| ME04-US91-AC05 | PreconditionAt least one of the following conditions are met:Fence intersects the buildingIf I save the fence border updates, then the app should:Display the 'No building issue confirmation' pop-up over the Fence Edit screen. |  | TBD |
| ME04-US91-AC06 | 'No building issue confirmation' pop-up should consist of the following elements:Title: 'Are you sure?Body: 'It seems like your fence is intersecting a building. Please confirm the fence does not actually intersect a building, otherwise the Halo system will not work properly.'Buttons:Ok, confirmedBack |  | - |
| ME04-US91-AC07 | If I click the 'Ok, confirmed', then the app should:Just close the pop-up.Save the fence to user's account.Display the Fence card.NoteIf a user saves the fence with a road intersection as well, then the app will display the 'Unique Fence' pop-up over the Fence card.It is okay that user sees 2 pop-ups in such a case. | - | - |
| ME04-US91-AC08 | If I click the 'Back' button, then the app should:Close the pop-up.Display the Fence Edit screen back again. | - | - |## Mobile analytics

| Analytics | Description |
|---|---|
| ME04-US91-MA01 | Log each display of the 'Unique Fence' pop-up with data about the reason (road intersection/building exclusion/both) to the Azure AppInsights. |
| ME04-US91-MA02 | Save 'View Tips' VS 'Continue' clicks to Firebase. |
| ME04-US91-MA03 | Save 'Ok, confirmed' VS 'Back' clicks to Firebase. |
