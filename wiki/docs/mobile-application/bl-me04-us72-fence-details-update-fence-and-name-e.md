---
title: "[BL] ME04-US72. Fence details. Update fence and name edit + delete"
sidebar_label: "[BL] ME04-US72. Fence details. Update fence and name edit + delete"
sidebar_position: 371
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| BASELINED in ME04-F20. Baseline: Edit Fence Name by Ekaterina Dupanova on 02 Oct 2024 |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Kirill Akulich |
| HALO-18636 - MOB: ME04-US72. Fence details. Update fence and name edit + delete Closed |
| Click here to expand...As of 08 Dec 2023:Mariya Kolyadacreated the initial version of US with links to draft designs in Figma. |# Contents

User Stories Acceptance criteria

# User Stories

\> As a Halo acount owner I want edit fence Name and delete fence action right on the Fence Details screen so that I can spend less time to find it and trigger the action.

# Acceptance criteria

| AC | Description | iOs design | Android design | 'Fence Details' screen + 'Edit Fence' screen | As Is | To Be |
|---|---|---|---|---|---|---|
| ME04-US72-AC01 | Renamethe button triggering the edit of the fence on the Fence Details screen:screen title on the 'Edit Fence Posts' screen.As IsTo BeEdit Fence PostsEdit Fence | Edit Fence Posts | Edit Fence |  |  |
| Edit Fence Posts | Edit Fence |
| ME04-US72-AC02 | Remove the 'Edit Fence details' button on the Fence Details screen. |
| ME04-US72-AC03 | Move the Fence Name to the center. |
| ME04-US72-AC04 | Add the clickable 'Pencil' icon to the right of the centered fence name end on the Fence Details screen.NoteThere is no corner case related to the too-long fence name because it can be a maximum of 20 characters. Thus there is always some space for the 'Pencil' icon. |
| ME04-US72-AC05 | If I click the 'Pencil' icon, then the app should:Display the 'Edit Fence Name' screen. |
| ME04-US72-AC06 | Add the 'Delete Fence' button below the 'Edit Fence' button. |
| ME04-US72-AC07 | If I click the 'Delete Fence' button, then the app should:Behave according to requirements in (Outdated) ME04-F03. Edit Fence Details#DeleteFence. |
