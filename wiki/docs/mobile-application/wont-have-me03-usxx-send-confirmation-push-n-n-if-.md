---
title: "[Won't have] ME03-USXX. Send 'confirmation' push n-n if the collar is put on the dog if it's 2nd and subsequent occurrence during the day"
sidebar_label: "[Won't have] ME03-USXX. Send 'confirmation' push n-n if the collar is put on the dog if it's 2nd and subsequent occurrence during the day"
sidebar_position: 422
author: "Galina Lonskaya"
---

Page info| Document status | Document owners | Links to JIRA Issues | History of changes |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya |
| HALO-20418 - FW+BE+MOB: Send push n-n if the collar is put on the dog if it's 2nd and subsequent occurrence during the day Closed |
| 28 May 2024 the draft user story is created |# User story

\> As Halo collar account owner I want to get push-notification about the 2nd and subsequent succesfull cases when the collar is put on the dog correctly so that I can be confident that the 'contact tips' issue is fixed and make dog is protected and the static feedback will be sent to my dog when it's necessary.

Input from 5/29/2024 meeting:

We should send the push - notification after the second and subsequent successes (collar is put ON correctly) during the day with the text: 'The collar is put ON again'.

The stakeholders think that this notification should not bother the user and give him confidence. The user should learn to expect it (include into New learning curriculum)

At the same time this notification if the user didn't take the collar off and he/she gets this notification they expect that smth went wrong.

# Acceptance Criteria

| AC | Description | iOS/Android design |
|---|---|---|
| ME03-USXX-ACXX | Precondition: 'The collar is put ON correctly' event has happened earlier today* at least onceIf 'collar is put ON correctly' event happens 2nd or subsequent time during the day, then: the following push-notification should be sent:Title: TBDBody: 'The collar is put ON again'. TBDAsk Victor to provide title and body | - |
| ME03-USXX-ACXX | The push notification should be sent without sound (not critical)Add to the table with push-notifications | -- |
| ME03-USXX-ACXX | Choose 'icon' for this push-notification. Ask Ryan/Anatoly to choose icon for the notification list. | - |
| ME03-USXX-ACXX | *Today starts from 00:00 OR from 05:00 am local time ?TBD with Victor and Michael | - |
