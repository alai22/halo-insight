---
title: "(NA) ME04-US22. Fence breach events notifications"
sidebar_label: "(NA) ME04-US22. Fence breach events notifications"
sidebar_position: 586
last_modified: "May 07, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| iOS: Android: |
| 05 May 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to recieve the fence breach event notification so I can immediatelly react if needed.

# Acceptance criteria

| AC | Description | Design | Preconditions | Trigger | Notification | Precondition | Trigger | Notification | Precondition | Trigger | Notification | Push | Toast to be displayed instead |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME04-F17-AC01 | Update the following Push notification and displaying of the same notification on the Notifications list:PreconditionsTriggerNotificationThe fence is enabled for the petThe app is closedPet enters warning zoneNT1. Applied Warning FeedbackSee (NA) Appendix 15 - List of push notifications | The fence is enabled for the petThe app is closed | Pet enters warning zone | NT1. Applied Warning Feedback |  |
| The fence is enabled for the petThe app is closed | Pet enters warning zone | NT1. Applied Warning Feedback |
| ME04-F17-AC02 | Stop sending the following Push notifications and displaying of the same notifications on the Notifications list:PreconditionTriggerNotificationThe fence is enabled for the petThe app is closedPet reached fence boundaryNT2. Applied Boundary FeedbackPet enters emergency zoneNT3. Applied Emergency FeedbackSee (NA) Appendix 15 - List of push notifications | The fence is enabled for the petThe app is closed | Pet reached fence boundary | NT2. Applied Boundary Feedback | Pet enters emergency zone | NT3. Applied Emergency Feedback | - |
| The fence is enabled for the petThe app is closed | Pet reached fence boundary | NT2. Applied Boundary Feedback |
| Pet enters emergency zone | NT3. Applied Emergency Feedback |
| ME04-F17-AC03 | Start sending the following Push notifications and displaying of the same notifications on the Notifications list:PreconditionTriggerNotificationThe fence is enabled for the petThe app is closedPet is \<N\> mins in emergency zoneN - should be managed via configNT72. N Minutes in Emergency zonePet returns to safe zoneNT7. Pet returns in a fencePet runs beyond protection zoneNT73. Pet leaves Prevention zoneSee (NA) Appendix 15 - List of push notifications | The fence is enabled for the petThe app is closed | Pet is \<N\> mins in emergency zoneN - should be managed via config | NT72. N Minutes in Emergency zone | Pet returns to safe zone | NT7. Pet returns in a fence | Pet runs beyond protection zone | NT73. Pet leaves Prevention zone |  |
| The fence is enabled for the petThe app is closed | Pet is \<N\> mins in emergency zoneN - should be managed via config | NT72. N Minutes in Emergency zone |
| Pet returns to safe zone | NT7. Pet returns in a fence |
| Pet runs beyond protection zone | NT73. Pet leaves Prevention zone |
| ME04-F17-AC04 | The app should send fence breach event notifications as Push Notifications only if the app is closed. |
| ME04-F17-AC05 | If the app is opened on My Fences screen, then the app should:Check if one of the following cards is opened:Pet CardLive Fence Event CardIf:no - follow requirements from ME04-F17-AC06.yes - display nothing, no push, no snackbar. |
| ME04-F17-AC06 | If the app is opened on My Fences screen and neither Pet Card or Live Fence Event Card is opened, then the app should:Display the snackbars instead of push notifications:PushToast to be displayed insteadNT1. Applied Warning FeedbackFigmaNT72. One Minute in Emergency zoneFigmaNT7. Pet returns in a fenceFigmaNT73. Pet leaves Prevention zoneFigma | NT1. Applied Warning Feedback | Figma | NT72. One Minute in Emergency zone | Figma | NT7. Pet returns in a fence | Figma | NT73. Pet leaves Prevention zone | Figma |
| NT1. Applied Warning Feedback | Figma |
| NT72. One Minute in Emergency zone | Figma |
| NT7. Pet returns in a fence | Figma |
| NT73. Pet leaves Prevention zone | Figma |
| ME04-F17-AC07 | If the app is opened on any screen except My Fences screen, then the app should:Display the pop-up instead of NT1. Applied Warning Feedback.Display nothing for other fence breach event notifications. | Figma |
| ME04-F17-AC08 | The action on tap on the:Push notificationToast instead of push notificationButton in the pop-up instead of push notificationNotification on the Notifications listshould be implemented with a separate user stories in 2 iterations:(NA) ME04-US23. Action on fence breach event notification tap RC1(NA) ME04-US??. Action on fence breach event notification tap RC2 |
| ME04-F17-AC09 | Logic of feedback sending to pet by the collar remains without changes even though user does NOT recieve some push notifications. |
