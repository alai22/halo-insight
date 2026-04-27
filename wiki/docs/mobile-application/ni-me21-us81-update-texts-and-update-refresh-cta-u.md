---
title: "(NI) ME21-US81. Update texts and update Refresh CTA UI/UX on 'Join the Pack' screen (Alpha test feedback)"
sidebar_label: "(NI) ME21-US81. Update texts and update Refresh CTA UI/UX on 'Join the Pack' screen (Alpha test feedback)"
sidebar_position: 445
last_modified: "Sep 06, 2024"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Jira ticket | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Kirill Akulich |
| HALO-21293 - [High] MOB: Update texts and update Refresh CTA UI/UX on 'Join the Pack' screen Closed |
| 09/06/2024 Galina Lonskaya created the user story |Table of Contents

User story Acceptance criteria Implementation Notes

# User story

n/a, alpha-test feedback, change to ME21-US58. Add 'No Pack Membership' handling after 'Enable Permissions' screen

# Acceptance criteria

| AC# | Description | Comments, designs |
|---|---|---|
| ME21-US81-AC01 | 'Unfortunately, we didn’t find a Pack Membership Plan associated with \<halo app account owner email\>. A Pack Membership Plan is required to use a collar.' text displayed on 'Join the Pack' screenshould be changed to 'Unfortunately, we didn’t find a Pack Membership Plan associated with \<halo app account owner email\>. ' | See the initial requirements in ME21-US58-AC02Figma |
| ME21-US81-AC02 | 'Benefits of Joining:' text displayed on 'Join the Pack' screenshould be changed to'Collar needs a Pack Membership'. |
| ME21-US81-AC03 | 'Have a plan already?' text and 'Refresh' button displayed on 'Join the Pack' screenshould be removed from the screen. |
| ME21-US81-AC04 | If I tap on 'Send Sign Up Instructions' button, the following change should be applied to ME21-US58-AC04:'Send Sign Up Instructions' should be changed to 'Retry Account Search' button, not to 'Resend Instructions' button as it was previously. | See the initial requirements in ME21-US58-AC04 |
| ME21-US81-AC05 | If I tap on 'Retry Account Search' button, then the logic of 'Retry' button should be reused: see all logic and error handling in ME19-US160. Refresh user's subscription to make sure there is no mismatch between Stripe and BE with one exception: after mismatch resolving the first screen of the collar adding should be shown. | See the initial requirements in ME21-US58-AC09 |# Implementation Notes

| IN | Description |
|---|---|
| ME21-IN81-AC01 | - |
