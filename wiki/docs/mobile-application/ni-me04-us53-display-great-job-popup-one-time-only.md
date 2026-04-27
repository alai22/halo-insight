---
title: "[NI] ME04-US53. Display \"Great job\" popup one time only"
sidebar_label: "[NI] ME04-US53. Display \"Great job\" popup one time only"
sidebar_position: 196
author: "Valeryia Chyrkun [X]"
---

| Document status | Story owners | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED BY SQ |
| Valeryia Chyrkun [X] |
| HALO-10524 - MOB: ME04-US53. Display "Great job" popup one time only Closed |
| Click here to expand...17 Apr 2023 ME04-US53-AC05 is updated by Galina Lonskaya in accordance with the QA request |# User story

\> As Halo account owner, I want to view the pop-up message about successful adding of fence just one time after the first successful fence creation, so this pop-up will not bother me each time I create the fence.

# Acceptance criteria

| AC | Text | Average case | Exceptional cases Note for BA: this behavior the behavior described in 3 ACs below is acceptable, since we wanted to make this US easier to implement and not to involve BE team. |
|---|---|---|---|
| ME04-US53-AC01 | If I successfully added 3 fence posts while creating a fence for the first time in my Halo Collar app account, then:I should see the M139 Great job with the fence creation popup message. |
| ME04-US53-AC02 | If I successfully added 3 fence posts while creating a fence for the second/subsequent time in my Halo Collar app account, then:I should not see the M139 Great job with the fence creation popup message. |
| ME04-US53-AC03 | If I log into my Halo Collar account using another smartphone first time and I successfully added 3 fence posts while creating a fence, then:I should see the M139 Great job with the fence creation popup message no matter how many times I was previously creating fence. |
| ME04-US53-AC04 | If I successfully added 3 fence posts while creating a fence after re-installing of the Halo Collar app, then:I should see the M139 Great job with the fence creation popup message no matter how many times I was previously creating fence. |
| ME04-US53-AC05 | If I successfully added 3 fence posts while creating a fence after the data clearing on my device, then:I should see the M139 Great job with the fence creation popup message no matter how many times I was previously creating fence. |
