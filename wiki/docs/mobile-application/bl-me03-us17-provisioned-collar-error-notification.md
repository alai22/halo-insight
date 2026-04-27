---
title: "[BL] ME03-US17. Provisioned collar error notifications"
sidebar_label: "[BL] ME03-US17. Provisioned collar error notifications"
sidebar_position: 45
author: "Nicolay Gavrilov"
---

| Epic | Document status | Document owner | Link to JIRA Issue | Key | Summary | T | Created | Updated | Due | Assignee | Reporter | P | Resolution | Changes history |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME03-EP01 New user / collar provisioning approach |
| REVISED |
| Nicolay Gavrilov |
| Key Summary T Created Updated Due Assignee Reporter P Resolution HALO-2802 MOB: ME03-US17. Provisioning error notification Jan 08, 2020 Oct 22, 2021 Pavel Leonenko Galina Lonskaya Fixed | HALO-2802 | MOB: ME03-US17. Provisioning error notification |  | Jan 08, 2020 | Oct 22, 2021 |  | Pavel Leonenko | Galina Lonskaya |  | Fixed |
| HALO-2802 | MOB: ME03-US17. Provisioning error notification |  | Jan 08, 2020 | Oct 22, 2021 |  | Pavel Leonenko | Galina Lonskaya |  | Fixed |
| 22 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# Contents

User story Acceptance criteria

# User story

\> As an owner I want to be notified if my device a collar provisioning error occured so that I know what do I need to do in this case.

# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US17-AC01 | The app displays M124 Security error for provisioning on the 'Connecting collar to Wi-Fi AP and IoT Hub' and 'Add fence with collar' screens in the following cases:Decrypted from the Rolling Code Incrementing Code \< stored internal IC (Error code: 2)Decrypted from the Rolling Code Incrementing Code \> stored internal IC + 10000 (Error code: 3) | Collar ProvisioningM124 Security error for provisioning |
| ME03-US17-AC02 | The app displays the M17 Technical error on the BLE pairing, 'Connecting collar to Wi-Fi AP and IoT Hub' and 'Add fence with collar' screens:Decrypted from the Rolling Code SN is not equal to own Collar SN (Error code: 4)Decrypted Rolling Code has wrong payload format (Error code: 1)Encrypted SN characteristic does not exist | Collar ProvisioningThe error may occur when the Collar connects to the smartphone via BLE |
