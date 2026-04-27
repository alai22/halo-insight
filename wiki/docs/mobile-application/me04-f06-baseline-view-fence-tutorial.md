---
title: "ME04-F06. Baseline: View Fence Tutorial"
sidebar_label: "ME04-F06. Baseline: View Fence Tutorial"
sidebar_position: 102
author: "Galina Lonskaya"
---

Click here to expand...| Document type | Document status | Document owners | Link to JIRA Issues | History of changes |
|---|---|---|---|---|
| Baseline story |
| BASELINED 02 Oct 2024 |
| Galina Lonskaya, Anastasia Brechko Ekaterina Dupanova Mariya Kolyada |
| HALO-4820 - Android: ME04-FE06. Fence Tutorials Closed HALO-17715 - MOB: ME04-US60. Update fence tutorial screens with info about auto-generation Closed |
| As of 04 Oct 2024 Ekaterina Dupanova baselined:[BL] ME04-US60. Update fence tutorial screens with info about auto-generation[BL] ME04-US42. View Fence Tutorials (baselined and archived) |Click here to expand...User story As a Halo account owner I want to see relevant instruction of fence creation that include explanation of auto-generation so that I can create/edit a fence by myself without any support . Acceptance criteria Fence creation tutorial. Step 1 Fence creation tutorial. Step 2 Fence creation tutorial. Step 3 Fence creation tutorial. Step 4 Fence creation tutorial. Step 5 The additional entry point to the Fence Creation Tutorial

# User story

\> As a Halo account owner I want to see relevant instruction of fence creation that include explanation of auto-generation so that I can create/edit a fence by myself without any support .

# Acceptance criteria

| AC | Text | iOS UI design | Android UI design | Fence creation tutorial. Step 1 | Element | To be | Fence creation tutorial. Step 2 | Element | To be | Fence creation tutorial. Step 3 | Element | To be | Fence creation tutorial. Step 4 | Element | To be | Fence creation tutorial. Step 5 | Element | Description | The additional entry point to the Fence Creation Tutorial |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-FE06-AC01 | Precondition:the Find Card is displayed.If I click on the 'Add Fence' button and I haven't seen the fence creation tutorial previously, then:'Halo Fences Basics' screen should be displayed.Exception 1: If I re-install the app on the same smartphone, then the fence creation tutorial will be displayed again.Exception 2: If I log into the app using the other smartphone, then the tutorial will be displayed again.Exception 3: If I log out from the first account, log in/log out using the other account and then log into the first account, then the fence creation tutorial will be displayed again.Note: "seen"/''unseen" status should be saved locally on the mobile side. |  |  |
| ME04-FE06-AC02 | 'Halo Fences Basics' screen should consist of the following UI elements:ElementTo beImageSee designsHeaderHalo Fences Basics Body textHalo Fences establish enclosed virtual safe zones stored in your dog's Halo Collar. Prevention Feedback alerts your dog as they approach the virtual fence boundary lines, ensuring they remain securely within the designated limits. Build fences anywhere, whether over water bodies, driveways, or in public parks.Left down buttonSkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed.Right down buttonNextAction on click:Open step 2 of the Fence tutorial. | Image | See designs | Header | Halo Fences Basics | Body text | Halo Fences establish enclosed virtual safe zones stored in your dog's Halo Collar. Prevention Feedback alerts your dog as they approach the virtual fence boundary lines, ensuring they remain securely within the designated limits. Build fences anywhere, whether over water bodies, driveways, or in public parks. | Left down button | SkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed. | Right down button | NextAction on click:Open step 2 of the Fence tutorial. | 'Halo Fences Basics' screen |  |
| Image | See designs |
| Header | Halo Fences Basics |
| Body text | Halo Fences establish enclosed virtual safe zones stored in your dog's Halo Collar. Prevention Feedback alerts your dog as they approach the virtual fence boundary lines, ensuring they remain securely within the designated limits. Build fences anywhere, whether over water bodies, driveways, or in public parks. |
| Left down button | SkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed. |
| Right down button | NextAction on click:Open step 2 of the Fence tutorial. |
| ME04-FE06-AC03 | Precondition:'Halo Fences Basics' screen is displayed.If I tap on the Next button, then:'Creating a Fence' screen should be displayed. |  |  |
| ME04-FE06-AC15 | 'Creating a Fence' screen should have the following UI elements:ElementTo beImageSee designsHeaderCreating a FenceBody textChoose a location by moving the map or entering a street address.We’ll recommend a fence based on publicly available property lines and our safety guidelines.Left down buttonSkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed.Right down buttonNextAction on click:Open step 3 of the Fence tutorial. | Image | See designs | Header | Creating a Fence | Body text | Choose a location by moving the map or entering a street address.We’ll recommend a fence based on publicly available property lines and our safety guidelines. | Left down button | SkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed. | Right down button | NextAction on click:Open step 3 of the Fence tutorial. | 'Creating a Fence' screen |  |
| Image | See designs |
| Header | Creating a Fence |
| Body text | Choose a location by moving the map or entering a street address.We’ll recommend a fence based on publicly available property lines and our safety guidelines. |
| Left down button | SkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed. |
| Right down button | NextAction on click:Open step 3 of the Fence tutorial. |
| ME04-FE06-AC05 | Precondition: 'Creating a Fence' screen is displayed.If I tap on the Next button, then:'Create Fences Anywhere' screen should be displayed. |  |  |
| ME04-FE06-AC16 | 'Create Fences Anywhere' screen should consist of the following UI elements:ElementTo beImageSee designsHeaderCreate Fences AnywhereBody textYou can make fences in your yard, a friend's house, the beach, a campground—anywhere.Going off-grid? Make fences ahead of time if you'll be traveling out of cellular coverage.Left down buttonSkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed.Right down buttonNextAction on click:Open step 4 of the Fence tutorial. | Image | See designs | Header | Create Fences Anywhere | Body text | You can make fences in your yard, a friend's house, the beach, a campground—anywhere.Going off-grid? Make fences ahead of time if you'll be traveling out of cellular coverage. | Left down button | SkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed. | Right down button | NextAction on click:Open step 4 of the Fence tutorial. | 'Create Fences Anywhere' screen |  |
| Image | See designs |
| Header | Create Fences Anywhere |
| Body text | You can make fences in your yard, a friend's house, the beach, a campground—anywhere.Going off-grid? Make fences ahead of time if you'll be traveling out of cellular coverage. |
| Left down button | SkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed. |
| Right down button | NextAction on click:Open step 4 of the Fence tutorial. |
| ME04-FE06-AC07 | Precondition: 'Create Fences Anywhere' screen is displayed.If I tap on the Next button, then:'Editing a Fence' screen should be displayed. |  |  |
| ME04-FE06-AC17 | 'Editing a Fence' screen should consist of the following UI elements:ElementTo beImageSee designsHeaderEditing a FenceBody textAdd a post by tapping any midpointTap and drag any post to moveSelect a post and tap the trash can to deleteLeft down buttonSkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed.Right down buttonNextAction on click:Open the 5th step of the Fence tutorial. | Image | See designs | Header | Editing a Fence | Body text | Add a post by tapping any midpointTap and drag any post to moveSelect a post and tap the trash can to delete | Left down button | SkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed. | Right down button | NextAction on click:Open the 5th step of the Fence tutorial. | 'Editing a Fence' screen |  |
| Image | See designs |
| Header | Editing a Fence |
| Body text | Add a post by tapping any midpointTap and drag any post to moveSelect a post and tap the trash can to delete |
| Left down button | SkipAction on click:The fence creation tutorial should be closed and the 'Create Fence' flow should be displayed. |
| Right down button | NextAction on click:Open the 5th step of the Fence tutorial. |
| ME04-FE06-AC18 | Precondition: 'Editing a Fence' screen is displayed.If I tap on the Next button, then:'Halo Fence Guidelines' screen should be displayed. |  |  |
| ME04-FE06-AC19 | 'Halo Fence Guidelines' screen should have the following UI elements:ElementDescriptionImageSee designsHeaderHalo Fence GuidelinesBody textAt least 15ft outside your entire homeAt least 15ft from public roadsAligned with existing barriers (like fences or hedges)Opened step indicatorLeft down button-Right down buttonI'm ReadyAction on click:Close the Fence tutorial.Display the screen over which the tutorial has been opened. | Image | See designs | Header | Halo Fence Guidelines | Body text | At least 15ft outside your entire homeAt least 15ft from public roadsAligned with existing barriers (like fences or hedges) | Opened step indicator | Left down button | - | Right down button | I'm ReadyAction on click:Close the Fence tutorial.Display the screen over which the tutorial has been opened. | 'Halo Fence Guidelines' screen |  |
| Image | See designs |
| Header | Halo Fence Guidelines |
| Body text | At least 15ft outside your entire homeAt least 15ft from public roadsAligned with existing barriers (like fences or hedges) |
| Opened step indicator |
| Left down button | - |
| Right down button | I'm ReadyAction on click:Close the Fence tutorial.Display the screen over which the tutorial has been opened. |
| ME04-FE06-AC09 | I can swipe the tutorial screens back and forward. |  |  |
| ME04-FE06-AC12 | Precondition: 'Create New Fence' screen or 'Edit Fence' screen is displayed.I can see the 'Question mark' icon. |  |  |
| ME04-FE06-AC13 | Precondition: "Create New Fence" screen or "Edit Fence Posts" screen is displayed.If I tap on the "Question mark" icon, then:the fence creation tutorial should be displayed.The tutorial consists of the following screens:Fence creation tutorial. Step 1 - Halo Fences BasicsFence creation tutorial. Step 2 - Creating a FenceFence creation tutorial. Step 3 - Create Fences AnywhereFence creation tutorial. Step 4 - Editing a FenceFence creation tutorial. Step 5 - Halo Fence GuidelinesNote: see the logic for navigation between screens above. | 'Create New fence' with "?" icon |  |
| ME04-FE06-AC14 | Precondition: Any of the following screens is displayed:Fence creation tutorial. Step 1 - Halo Fences BasicsFence creation tutorial. Step 2 - Creating a FenceFence creation tutorial. Step 3 - Create Fences AnywhereFence creation tutorial. Step 4 - Editing a FenceIf I tap on the Skip button, then the tutorial should be closed. |  |  |
