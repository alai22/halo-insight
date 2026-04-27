---
title: "ME04-US68. Log fence data to DB"
sidebar_label: "ME04-US68. Log fence data to DB"
sidebar_position: 667
last_modified: "Feb 26, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Svyatoslav Luzin |
| HALO-18076 - MOB+BE: ME04-US68. Log fence data to DB Closed |
| Click here to expand...As of 24 Oct 2023 :Mariya Kolyadacreated the initial version of US.As of 26 Oct 2023 and 10 Nov 2023 Mariya Kolyada:Updated after call with customers and 3 amigos with the team + added URL to jira.As of 14 Nov 2023Mariya Kolyada:Added development notes after 3 amigos with team.Deleted AC that is related to user data migration after account deletion and created a separate task for it.As of 16 Jan 2024 Mariya Kolyada:Moved requirements to fence images saving to separate user story that will be implemented within Post-MRGP scope: https://portal.softeq.com/display/HALO/%5BPostponed%5D+ME04-US88.+Log+fence+images+to+Azure+Blob+storage.As of 08 Feb 2024 Mariya Kolyada:Deleted parameters that already exist in DBRenamed the new parametersAs of 26 Feb 2024 Mariya Kolyada:Removed old building, road, and water unnecessary parametersAdded qty of seen intersection errors and whether fence intersects now |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo Product Owner I want to be able to reach the existing users' fence geo (country, state, etc) and intersection with other map elements data so that I can use it for the hypothesis generation and testing or share with CSAs for better support when needed.

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US68-AC01 | Log to the Halo DB the following additional fence data after each fence creation or edit:Fence center location CountryStateCityStreetPostal codeInteresting place name if fence on public placeFence areaBuilding parameters:Qty of seen building intersection errors (sum from each edit)Does the fence intersect the building now? (yes/no)Road parameters:Qty of seen road intersection errors (sum from each edit)Does the fence intersect the road now? (yes/no)Water parameters:Qty of seen water intersection errors (sum from each edit)Does the fence intersect a water now? (yes/no)Development notesDuring development, we should decide where is better to get geo data (country, state, etc):Paid Mapbox solution.Native iOs and Android free of charge (but it can have some mistakes in data).Seems reasonable to rediscuss with Michael on tech calls during implementation. |
| ME04-US68-AC02 | If user deletes fence, then the system should:Delete the fence data from DB.Development notesSeems that we already have such an approach for existing fence data, thus no changes are needed.AC is just for reminder to double-check during testing. |
| ME04-US68-AC03 | The solution should be expandable for future UI implementation in AAP.So that CSAs can open user's fences details in AAP UI. |
