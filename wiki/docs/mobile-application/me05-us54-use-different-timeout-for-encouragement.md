---
title: "ME05-US54. Use different timeout for Encouragement"
sidebar_label: "ME05-US54. Use different timeout for Encouragement"
sidebar_position: 705
last_modified: "Jun 23, 2023"
author: "Galina Lonskaya"
---

| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya Eugene Paseka Zakhar Makarevich Timofey Burak [X] Kirill Akulich Valeria Malets |
| HALO-14233 - BE+MOB: ME05-US54. Use different timeout for Encouragement Closed |
| 12 Oct 2022 draft story is created |# Contents

Background User story Acceptance criteria Change timeout for applying Encouragement for a single pet Change timeout for applying Encouragement for multiple pets

# Background

As of 10/12/2022 'connectivity' error toast message is displayed, when the instant feedback is not delivered due to timeout

# User story

\> As an account owner, I want to have bigger timeout for Encouragements so that Encouragements might be delivered even when it takes more than 3 seconds.

# Acceptance criteria

| AC | Text | Change timeout for applying Encouragement for a single pet | Change timeout for applying Encouragement for multiple pets |  |
|---|---|---|---|---|
| ME05-US53-AC01 | The acceptance criteria below should be applied for the following scenarios:When the user applies Encouragement from the pet cardWhen the user taps the 'Test on collar' button from:'Good behavior feedback' settings screen'Return whistle feedback' settings screen'Heading home feedback' settings screen |
| ME05-US53-AC02 | The timeout for sending instant encouragement to the pet described within ME05-US52-AC02 should be changed from 3 seconds to 10 seconds. Note: timeout for preventions should stay the same |
| ME05-US53-AC03 | The timeout for sending instant encouragement to the pets described within ME05-US52-AC03 should be changed from 3 seconds to 10 seconds. Note: timeout for preventions should stay the same |
| ME05-US53-AC04 | Encouragement timeout should be configurable on BE side. |
