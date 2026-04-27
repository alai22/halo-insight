---
title: "[BL] ME04-US42. View Fence Tutorials"
sidebar_label: "[BL] ME04-US42. View Fence Tutorials"
sidebar_position: 66
author: "Galina Lonskaya"
---

| Role | Epic | Document status | BA story owner | DEV, QA story owners | Link to JIRA Issue |
|---|---|---|---|---|---|
| Owner |
| ME04 Create fence |
| APPROVED BY SQ |
| Galina Lonskaya |
| Pavel Leonenko, Anastasia Brechko |
| HALO-3928 - MOB GOAL: ME04-US42. View Fence Tutorial screens Closed |# User story

\> As owner, I want to view the fence tutorials so that I can understand How to Put and manage fences.

# Acceptance criteria

| AC | Text | Notes / UI design | Fence creation tutorial | Fence management tutorial | The additional entry point to the Fence Creation Tutorial |
|---|---|---|---|---|---|
| ME04-US42-AC01 | Precondition: the "Find" action sheet is displayed.If I initiate the fence creation and I haven't seen the fence creation tutorial previously, then:"Fence creation tutorial - What is a Halo Fence?" screen should be displayed.Exception 1: If I re-install the app on the same smartphone, then the fence creation tutorial will be displayed again.Exception 2: If I log into the app using the other smartphone, then the tutorial will be displayed again.Exception 3: If I log out from the first account, log in/log out using the other account and then log into the first account, then the fence creation tutorial will be displayed again.Note: "seen"/''unseen" status should be saved locally on the mobile side. | Pic 1 Fence creation tutorial - What is a Halo Fence? |
| ME04-US42-AC02 | "Fence creation tutorial - What is a Halo Fence?" screenIf I tap on the Close button, then:the fence creation tutorial should be closed and the "Create New Fence" flow should be displayed. |
| ME04-US42-AC03 | Precondition: "Fence creation tutorial - What is a Halo Fence?" screen is displayed. If I tap on the Next button, then:"Fence creation tutorial - Fence Boundary Tips" screen should be displayed. | Pic 2 Fence creation tutorial - Fence Boundary Tips |
| ME04-US42-AC04 | Precondition: "Fence creation tutorial - Fence Boundary Tips" screen is displayed.If I tap on the Close button, then see the same behavior as described in ME04-US42-AC02. | - |
| ME04-US42-AC05 | Precondition: "Fence creation tutorial - Fence Boundary Tips" screen is displayed.If I tap on the Next button, then:"Fence creation tutorial - Fence Spacing Tips" screen should be displayed. | Pic 3 - Fence creation tutorial - Fence Spacing Tips |
| ME04-US42-AC06 | Precondition: "Fence creation tutorial - Fence Spacing Tips" screen is displayed.If I tap on the Close button, then see the same behavior as described in ME04-US42-AC02. |
| ME04-US42-AC07 | Precondition: "Fence creation tutorial - Fence Spacing Tips" screen is displayed.If I tap on the Next button, then:"Fence creation tutorial - How to Create Halo Fences" screen should be displayed. | Pic 4 - Fence creation tutorial - How to Create Halo Fences |
| ME04-US42-AC08 | Precondition: "Fence creation tutorial - How to Create Halo Fences" screen is displayed.If I tap on the "I'm Ready!" button, then:"Create New Fence" screen should be displayed. |
| ME04-US42-AC09 | I can swipe the tutorial screens back and forward. | - |
| ME04-US42-AC10 | Precondition: "Create New Fence - Add a name" screen is displayed.If I tap on the Done button, all validations are passed and I haven't seen the "Fence management" tutorial previously, then:"Fence management tutorial - Where to Put Halo Fences" screen should be displayed. See Pic 5.Note: "Where to Put Halo Fences" is displayed only once for the user.Exception 1: If I re-install the app on the same smartphone, then the fence management tutorial will be displayed again.Exception 2: If I log into the app using the other smartphone, then the tutorial will be displayed again.Exception 3: If I log out from the first account, log in/log out using the other account and then log into the first account, then the fence creation tutorial will be displayed again. | Pic 5 Fence management tutorial - Where to Put Halo Fences |
| ME04-US42-AC11 | Precondition: "Fence management tutorial - Where to Put Halo Fences" screen is displayed.If I tap on the "Got It!", then:My Map screen with the minimized fence card should be displayed. |
| ME04-US42-AC12 | Precondition: "Create New Fence" screen or "Edit Fence Posts" screen is displayed.I can see the "Question mark" icon. | Pic 6 Create New fence with "?" icon |
| ME04-US42-AC13 | Precondition: "Create New Fence" screen or "Edit Fence Posts" screen is displayed.If I tap on the "Question mark" icon, then:the fence creation tutorial should be displayed.The tutorial consists of the following screens:Pic 1 Fence creation tutorial - What is a Halo Fence?Pic 2 Fence creation tutorial - Fence Boundary TipsPic 3 Fence creation tutorial - Fence Spacing TipsPic 4 Fence creation tutorial - How to Create Halo FencesNote: see the logic for navigation between screens above. |
| ME04-US42-AC14 | Precondition: Any of the following screens is displayed:Pic 1 Fence creation tutorial - What is a Halo Fence?Pic 2 Fence creation tutorial - Fence Boundary TipsPic 3 Fence creation tutorial - Fence Spacing TipsIf I tap on the Close button, then the tutorial should be closed. | - |
