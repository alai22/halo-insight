---
title: "ME03-US147. Forbid to add a collar with FW older than 1.5.89"
sidebar_label: "ME03-US147. Forbid to add a collar with FW older than 1.5.89"
sidebar_position: 637
last_modified: "Nov 07, 2024"
author: "Mariya Kolyada"
---

Click here to expand...| Document status | Document owner | Link to JIRA issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| HALO-21286 - BE+MOB: ME03-US147. Forbid to add a collar with FW older than 1.5.89 Closed HALO-21827 - BE: ME03-US147-AC02. Activate Collar SIM card when forbid to add a collar with FW older than 1.5.89 Closed |
| Click here to expand...As of 17 Oct 2024 Mariya Kolyada created the initial version of user storyAs of 07 Nov 2024 Mariya Kolyada added ME03-US147-AC02. |# Contents

User story Acceptance criteria

# User story

As a Halo account owner I want to be forbidden to add a collar with FW older than 1.5.89 and navigated to the support article with an explanation of how to upgrade the FW version so that I can use my collar with no further issues and have access to all features.

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-US147-AC01 | Precondition:My collar's FW is older than 1.5.89If I tap on the "Add Collar" button, then the app should:Display M298 Collar's FW is older than 1.5.89 pop-up. |
| ME03-US147-AC02 | Precondition:My collar's FW is older than 1.5.89If I tap on the "Add Collar" button, then the sytem should:Automatically activate collar SIM card.NoteThis is needed so BE gets to know about the collar FW update made with wire.If the collar has no internet access BE won't know anything about the update and the user will be still forbidden to add a collar even after the update. |
