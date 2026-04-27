---
title: "[Postponed] ME03-USXX. Send cat. issue if the contact tips lose contact with the skin too many times throughout the day"
sidebar_label: "[Postponed] ME03-USXX. Send cat. issue if the contact tips lose contact with the skin too many times throughout the day"
sidebar_position: 417
author: "Galina Lonskaya"
---

Page info| Document status | Document owners | Links to JIRA Issues | History of changes |
|---|---|---|---|
| DRAFT |
| Kiryl Trafimau Galina Lonskaya |
| HALO-20420 - FW+BE+MOB: Send cat. issue if the contact tips lose contact with the skin too many times throughout the day Open |
| 30 May 2024 the draft user story is created |# User story

\> As Halo collar account owner I want to get notified when the there is a catasctrophic issue with the contact tips so that I can claim the warranty replacement of the collar

# Acceptance Criteria

| AC | Description |
|---|---|
| ME03-USXX-ACXX | IF Based on Daily Diagnostic catastrophic issue happened according to the rule in the tableTHEN I should see the error text on the Collar diagnostic issue according to the rule in the tableAND I should see grey text on the Collar diagnostic issue according to the rule in the tableAND the Event to Braze should be sent AND the collar receives the command (isDisabled=true) to start Actions (vibrating and blinking) |Rules

| Section name | Error name | Error validations | Error text to be displayed on the Diagnostics screen in red | Grey text in the diagnostics screen |
|---|---|---|---|---|
| Other | Contact tips issue | Counter 'skin contact test failed'\>TBDNOTE: Maybe we need an extra condition as we usually do for catastrophic issues to ensure that the issue persists e.g. AND \> than 1 DD in a row | 'Contact tips issue'Note: Should be approved by Michael | 'An issue was detected with the contact tips. Tap here to review our warranty and Protection Plans or contact support for further instructions.'tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103contact support = link to the Dog ParkNote: Should be approved by Michael |Note for BA: Add proper row to Appendix 14 when requirements are approved

## Implementation notes

| ID | Implementation note |
|---|---|
| ME03-USXX-IN01 |  |
