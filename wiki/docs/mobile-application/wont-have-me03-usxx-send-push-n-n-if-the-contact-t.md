---
title: "[Won't have] ME03-USXX. Send push n-n if the contact tips lost contact with the pet after having сontact earlier today"
sidebar_label: "[Won't have] ME03-USXX. Send push n-n if the contact tips lost contact with the pet after having сontact earlier today"
sidebar_position: 418
author: "Galina Lonskaya"
---

Page info| Document status | Document owners | Links to JIRA Issues | History of changes |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya |
| HALO-20417 - FW+MOB+BE: Send push n-n if the contact tips lost contact with the pet after having сontact earlier today Closed |
| 28 May 2024 the draft user story is created |# User story

\> As Halo collar account owner I want to get push-notification about the fact that the contact tips lost the contact with the dog skin so that I can be aware about 'contact tips' issue, find the dog and readjust the collar.

# Acceptance Criteria

| AC | Description | iOS/Android design |
|---|---|---|
| ME03-USXX-AC01 | Precondition: Last 'Collar is put ON correctly' event (= 'contact tips touch the pet skin') has happened today and there was no failed tests after it. If the pet is moving at the moment, than: 'Contact tips' test should performed each 10 seconds. Add links on ACs describing 'Contact tips' tests | - |
| ME03-USXX-AC02 | Precondition: Last 'Collar is put ON correctly' event has happened today and after this event 'the contact tips lost contact with the pet ' n-n hasn't been sent. If the 'Contact tips' test fails, then: the following push-notification should be sent: Title: TBDBody: \<Dog's name\>' Halo is off the dog or the contact tips don't touch the \<Dog's name\>'s skin, please readjust the collar. + But anyway your dog is protected since with use vibration instead of static while the issue isn't fixed. Ask Victor to come up with the text for push-notification | - |
| ME03-USXX-AC03 | The push-notification XXX is critical, should have sound. Add to the table of push-notifications | - |
| ME03-USXX-AC04 | Choose 'icon' for this push-notification. Ask Ryan/Anatoly to choose icon for the notification list. | - |
| ME03-USXX-AC05 | If the 'Contact tips' test fails, then: 'Contact tips' test should be performed each 3 seconds till: 'contact tips' test will be successful (in case of success, see ME03-USXX. Give audible feedback if the collar is put on the dog correctly) |  |
