---
title: "[BL] ME03-US75. Changes to \"My Collars\" screen"
sidebar_label: "[BL] ME03-US75. Changes to \"My Collars\" screen"
sidebar_position: 211
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Valeryia Chyrkun [X] |
| HALO-11278 - [RI] MOB: Changes to "My Collars" screen Closed |
| Click here to expand...Edited ME03-US75-AC01 as BE doesn't sends us data about the way the signal was receivedBallpark: 1SP (MOB), 1SP (QA) |# Contents

Contents General description User story Acceptance criteria

# General description

1. Changes for 'My Collars':
  1. 'Last heard' section should also be updated: need to display that the collar was heard via BLE/ Wi-Fi/ LTE.
  2. The icon for collar FW update should be changed to grey triangle with exclamation mark.

# User story

\> As a Halo app account owner I want to be aware of what connection is used on my collar for communication with app so that I can detect possible issues on time.

# Acceptance criteria

| AC | Description | Designs/ implementation status | Collar Update icon |  |
|---|---|---|---|---|
| Last heard |
| ME03-US75-AC01 | The text on 'Last Heard' field should be updated on the Collar list according to the following rules:If the collar was connected via Wi-Fi at the moment of receiving signal for 'Last heard' field, then I see the following text: '\<Timestamp\> ago via Wi-Fi'If the collar was connected via LTE at the moment of receiving signal for 'Last heard' field, then I see the following text: '\<Timestamp\> ago via LTE' | Zeplinneed to remove the word 'Bluetooth' on the screen |
| ME03-US75-AC02 | If the version is not 'up-to-date' than the system should display grey triangle icon instead of blue cycle icon on the Collar Update section near the 'Version \<Version name\> is available' text.The icon should not clickable |
| ME03-US75-AC03 | If the version is not 'up-to-date' than the system should display grey triangle icon on the Сollar photo instead of blue cycle icon on the Collar details section |
