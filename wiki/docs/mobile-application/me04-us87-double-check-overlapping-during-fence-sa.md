---
title: "ME04-US87. Double-check overlapping during fence saving"
sidebar_label: "ME04-US87. Double-check overlapping during fence saving"
sidebar_position: 670
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Kirill Akulich , Hanna Chasnakova [X] |
| HALO-18997 - MOB: ME04-US87. Double-check overlapping during fence saving Closed |
| Click here to expand...As of 10 Jan 2024:Mariya Kolyadacreated the initial version of US.As of 11 Jan 2024 Mariya Kolyada undated after call with customers. |# Contents

User Stories Acceptance criteria

# User Stories

\> As a Halo acount owner I want be forbidden to save overlapping fences so that my collar keeps my dog save without wrong feedback.

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US87-AC01 | If I trigger fence creation or edit, then the app should:Update the list of fences saved in the app cache.Implementation notesFE should request the list of 20 fences from BE.The collars that meet the same rules as those that BE sends every 15 sec on My Map. |
| ME04-US87-AC02 | When the app saves a fence after fence creation or edit, it should:Update the list of fences saved in the app cache.Check if fence overlaps any fences in user's account.Implementation notesFE should request the list of 20 fences from BE, display new fences on the Map. |
| ME04-US87-AC05 | Pprecondirtion: user has more than 20 fences.IF I put the 1st point of the fence THEN Update the list of fences saved in the app cacheAND Display a spinner while updatingAND Update the map UIAND Display a fence point if it does not overlap with any other fence on the mapImplementation notesFE should request the list of 20 fences from BE, display new fences on the Map. |
| ME04-US87-AC06 | Pprecondirtions:User has more than 20 fences.I put the 1st point of the fence IF the point overlaps another fenceTHEN do not display this point AND Display error that fence overlaps existing fences (see ME04-F00- M7 in ME04-F00. Add fence without GPS#TableME04-1Drawafenceerrors/warnings). |
| ME04-US87-AC03 | If the new fence overlaps any of the existing fences, then the app should:Update the map UI.Display error that fence overlaps existing fences (see ME04-F00- M7 in ME04-F00. Add fence without GPS#TableME04-1Drawafenceerrors/warnings). |
| ME04-US87-AC04 | If the new fence does NOT overlap any of the existing fences, then the app should:Save the fence update to user's account.Known issue: it is possible that we have fences not displayed on the map and which will be overlapped (e.g. I have more than 20 fences in the area where new one is created and the new one overlaps some of the not displayed fences) |
