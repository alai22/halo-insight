---
title: "[Won't have] ME03-USXX. Give audible feedback if the collar is put on the dog correctly"
sidebar_label: "[Won't have] ME03-USXX. Give audible feedback if the collar is put on the dog correctly"
sidebar_position: 416
author: "Galina Lonskaya"
---

Page info| Document status | Document owners | Links to JIRA Issues | History of changes |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya |
| HALO-9709 - FW: Give audible feedback if the collar is put on the dog correctly Closed |
| 28 May 2024 the draft user story is created |# User story

\> As Halo collar account owner I want to hear special sound indicating that the contact tips have contact with the skin at once after putting the collar on the dog so that I can be sure that I can safely allow my dog to go and static feedback will be delivered to the dog if it's required.

Note: We want to introduce a new habit for the user that should become his/her daily routine. Each time the user puts the collar on the dog, he/she should remember that they can be sure the dog is safe only if they hear a special sound signal from the collar. This recommendation will be included in New learning curriculum (see https://paws.productboard.com/entity-detail/features/27392327).

# Acceptance Criteria

| AC | Description | iOS/Android screen designs |
|---|---|---|
| ME03-USXX-AC01 | Precondition: NO 'The collar is put ON correctly' events happened today* OR 'The collar is put ON correctly' event(s) has happened today but after that 'contact tips' failed event has been registered. If:the static is chosen as feedback for at least one feedback typethe collar is not on charger the collar starts moving then:'skin contact' test should be performed each 3 seconds. | - |
| ME03-USXX-ACXX | The 'contact tips' test should consist of 10 checks. Note: the approximate duration of the test is 0.1 second. | - |
| ME03-USXX-ACXX | If 10/10 checks are positive during one test, then: 'Contact tips' test considered as successful.Check with FW developers after impl-n and testing and update the logic if required | - |
| ME03-USXX-ACXX | If 'skin contact' test is successful, then: the collar should produce sound: TBD sound, the task is added to Product Board https://paws.productboard.com/entity-detail/features/27392339 backup #1: the collar LED makes TBD signal, see the separate storybackup #2: the pet card should display corresponding 'connecting status', see the separate storythe more infrequent checks should be performed, see the detailed description in ME03-USXX. Send push n-n if the contact tips lost contact with the pet after having сontact earlier today. Note: ask FW developers to put new sound on the collar Open questions: Is it enough to have one successfully passed test in a row in order to be sure that the contact tips touch the skin reliably? Probably we need to have TBD successful tests in a row before providing this info? | - |
| ME03-USXX-ACXX | If 1/10 checks or more are failed during one test session, then: 'Contact tips' test should be considered as failed. Check with FW developers after impl-n and testing and update the logic if required | - |
| ME03-USXX-ACXX | If the 'contact tips' test is failed, then: the user should not get any indication about this failurethe 'contact tips' test should be repeated, see the detailed description in ME03-USXX-AC01 | - |
| ME03-USXX-ACXX | *Today - define understanding of what does it means (00:00) | - |
|  | Note: If the user doesn't use contact tips, he/she just will not know if he or she should get this Collar is ON / OF. So there is no need to change default feedback settings . Note: FW don't know if the contact tips are used or not | - |
