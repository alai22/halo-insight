---
title: "[BL] ME04-US93. Change status icons on Fence details"
sidebar_label: "[BL] ME04-US93. Change status icons on Fence details"
sidebar_position: 395
author: "Kiryl Trafimau"
---

| Document status | Document owners | Link to JIRA issues | Affected requirements | History of changes |
|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau Mariya Kolyada |
| HALO-19456 - MOB: Change status icons on Fence details Closed |
| [BL ? comments?] ME04-US86. Display pets on Fence details |
|  |# Contents

User Stories Acceptance criteria

# User Stories

\> As a Halo acount owner I want to view if the pets listen the fence details for which I opened so that I can understand if my dogs will be safe inside this fence.

# Acceptance criteria

| AC | Description | iOs design | Android design | Condition | UI |
|---|---|---|---|---|---|
| ME04-US93-AC01 | Pet displaying rules in the list: Pet icon displayed depending on connectivity status of the collar:offline-ghostedalso ghosted if another reason why the same pet pin is ghosted on the My Map:GPS initialization requiredCollar is dead ('charge your collar')On entering the app/no connection between collar and app ('updating...', 'attempting to connect...')online-normalStatus icon displayed based on synchronization statuscheck-synchronizedelipsis-not synchronizedConditionUIPet's collar is onlineFence has NOT been saved on this collar yetPet pin is normalSynchronization status icon (elipsis)Pet's collar is onlineFence has been saved on this collar yetPet pin is normalSynchronized status icon (check)Pet's collar is offline (or another reason why the same pet pin is ghosted on My Map)Fence has NOT been saved on this collar yetPet pin is ghostedSynchronization status icon (elipsis)Pet's collar is offline (or another reason why the same pet pin is ghosted on My Map)Fence has been saved on this collarPet pin is ghostedSynchronized status icon (check) | Pet's collar is onlineFence has NOT been saved on this collar yet | Pet pin is normalSynchronization status icon (elipsis) | Pet's collar is onlineFence has been saved on this collar yet | Pet pin is normalSynchronized status icon (check) | Pet's collar is offline (or another reason why the same pet pin is ghosted on My Map)Fence has NOT been saved on this collar yet | Pet pin is ghostedSynchronization status icon (elipsis) | Pet's collar is offline (or another reason why the same pet pin is ghosted on My Map)Fence has been saved on this collar | Pet pin is ghostedSynchronized status icon (check) |  |  |
| Pet's collar is onlineFence has NOT been saved on this collar yet | Pet pin is normalSynchronization status icon (elipsis) |
| Pet's collar is onlineFence has been saved on this collar yet | Pet pin is normalSynchronized status icon (check) |
| Pet's collar is offline (or another reason why the same pet pin is ghosted on My Map)Fence has NOT been saved on this collar yet | Pet pin is ghostedSynchronization status icon (elipsis) |
| Pet's collar is offline (or another reason why the same pet pin is ghosted on My Map)Fence has been saved on this collar | Pet pin is ghostedSynchronized status icon (check) |
