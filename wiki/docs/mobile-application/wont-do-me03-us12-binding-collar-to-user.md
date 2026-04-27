---
title: "[Won't do] ME03-US12. Binding collar to user"
sidebar_label: "[Won't do] ME03-US12. Binding collar to user"
sidebar_position: 39
author: "Galina Lonskaya"
---

| Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|
| ME03-EP01 New user / collar provisioning approach |
| WON'T DO |
| Nicolay Gavrilov |
| N/A |# Contents

User story Acceptance criteria

Won't do, because the app will no longer send requests to BE to confirm that the collar is online. Now the collar is bound even if it is offline. Collar-BE communication is no longer required.

# User story

\> As an owner I want my collar to be associated only with my account so that the other people can not use it.

# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US12-AC01 | The app displays the collar binding screen when an unbound device is added to the user account right after the sep with scanning/entering the serial number. | Collar Provisioning |
| ME03-US12-AC02 | In case the collar failed to bind to the user, the mobile app displays the corresponding error on the screen. |  |
| ME03-US12-AC03 | The binding screen has the following text: 'It may take about 1 minute' | N/A |
| ME03-US12-AC04 | When the user taps on the back button, the app displays the previous screen of the collar connection process. | N/A |
| ME03-US12-AC05 | The app has a visual indication for the overall number of user-collar provisioning process steps at the bottom of the screen. | N/A |
| ME03-US12-AC06 | The app allows binding a collar even if the device is offline. | N/A |
