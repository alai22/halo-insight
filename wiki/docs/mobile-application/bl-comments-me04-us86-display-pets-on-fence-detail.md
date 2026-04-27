---
title: "[BL ? comments?] ME04-US86. Display pets on Fence details"
sidebar_label: "[BL ? comments?] ME04-US86. Display pets on Fence details"
sidebar_position: 383
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Kirill Akulich, @Aleksey Zhukov, Alina Sharshun [X] , Hanna Chasnakova [X] |
| HALO-18969 - BE+MOB: ME04-US86. Display pets on Fence details Closed |
| Click here to expand...As of 10 Jan 2024:Mariya Kolyadacreated the initial version of US.As of 17 Jan 2024 Mariya Kolyada updated requrements in accordance to the latest agreements on BA call:Added ME04-US86-AC06Removed 'Dead battery' requirement |# Contents

User Stories Acceptance criteria

# User Stories

\> As a Halo acount owner I want to view if the pets listen the fence details for which I opened so that I can understand if my dogs will be safe inside this fence.

# Acceptance criteria

| AC | Description | iOs design | Android design | Condition | UI |
|---|---|---|---|---|---|
| ME04-US86-AC01 | PreconditionThere are 20 or more fences in the user's accountUser has at least one collar with assigned Pet.The app should display the Pets section on the Fence Card.NoteThe app should hide/display this section depending on data received from BE. |  |  |
| ME04-US86-AC02 | Pets section should consist of:Title: "Assigned to"Link to article:Label: "Learn more"URL: https://support.halocollar.com/hc/en-us/articles/20502151410455Pets carousel, whereeach element consists of:Pet Pin (same UI as on the Find card);Pet Name (same UI as on the Find card);Pet synchronization status icon (see ME04-US86-AC05).sorting in the list the same as on the Find card. |
| ME04-US86-AC03 | The app should update the 'Pets synchronization with fence' data if:User opens the Fence Card.User creates and saves a new fence.User edits and saves an existing fence.Every 5 seconds by default while the Fence Card is displayed on the screen (only data for this specific Fence Card should be updated, not all geofences, others should be updated every 15 sec as usual)Note for DeveloperIf implementation takes too much effort - notify BA so we postpone this request to post-MRGP scope. HALO-19379 - MOB: Update pet synchronization status every 5 seconds Ready for Development |
| ME04-US86-AC04 | The app should try to send the fence updates on the collar each time user creates or edits any fence. |
| ME04-US86-AC05 | Pet displaying rules in the list: ConditionUIPet's collar is offline or still in the process of synchronizationFence has NOT been saved on this collar yetPet pin is grayedSynchronization status icon with 2 arrowsPet's collar is onlineFence has been saved on this collarPet pin active viewNo synchronization status icon Pet's collar is onlineFence does NOT meet conditions to be placed on the collar (see [BL] ME04-US82. Save 20 closest fences on the collar)Fence has NOT been saved on this collarHide this Pet from the Fence Card | Pet's collar is offline or still in the process of synchronizationFence has NOT been saved on this collar yet | Pet pin is grayedSynchronization status icon with 2 arrows | Pet's collar is onlineFence has been saved on this collar | Pet pin active viewNo synchronization status icon | Pet's collar is onlineFence does NOT meet conditions to be placed on the collar (see [BL] ME04-US82. Save 20 closest fences on the collar)Fence has NOT been saved on this collar | Hide this Pet from the Fence Card |
| Pet's collar is offline or still in the process of synchronizationFence has NOT been saved on this collar yet | Pet pin is grayedSynchronization status icon with 2 arrows |
| Pet's collar is onlineFence has been saved on this collar | Pet pin active viewNo synchronization status icon |
| Pet's collar is onlineFence does NOT meet conditions to be placed on the collar (see [BL] ME04-US82. Save 20 closest fences on the collar)Fence has NOT been saved on this collar | Hide this Pet from the Fence Card |
| ME04-US86-AC06 | PreconditionThere are 20 or more fences in the user's accountUser has NO Pets' collars that meet conditions for this fence to be placed on the collar (see [BL] ME04-US82. Save 20 closest fences on the collar)The app should display an empty message 'No pets' in a place where pets list is usually displayed. |  |  |
