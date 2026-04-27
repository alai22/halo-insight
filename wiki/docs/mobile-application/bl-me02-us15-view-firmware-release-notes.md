---
title: "[BL] ME02-US15. View firmware release notes"
sidebar_label: "[BL] ME02-US15. View firmware release notes"
sidebar_position: 148
author: "Galina Lonskaya"
---

| Document status | Story owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko, Eugene Paseka |
| HALO-6857 - MOB: ME02-US15. View firmware release notes Closed |
| 15 Feb 2022 Maria Shikareva [X] Marked the story as baselined. |# User story

\> As an account owner, I want to review the firmware release notes so that I can understand why the new firmware version should be installed on my collar.

Acceptance criteria

| AC | Description | iOS UI/ implementation statusIOS TO DO | Android UI/ implementation statusANROID TO DO |
|---|---|---|---|
| ME02-US15-AC01 | 'Release Notes' button should be renamed to 'App Release Notes' on 'About' screen. | - | - |
| ME02-US15-AC02 | 'Firmware Release Notes' button should be added to 'About' screen and displayed below 'App Release Notes' button. | Pic 1 'About' screen with 'Firmware Release Notes' button. See Zeplin | The same screen as for iOS |
| ME02-US15-AC03 | If I tap on 'Firmware Release Notes' button, then:'https://support.halocollar.com/hc/en-us/articles/1500004830041-Firmware-Update-Release-Notes' link should be opened in default browser. | - | - |
| ME02-US15-AC04 | 'Halo' logo icon and 'Halo' label should be displayed in one line.Note: decided internally by dev team, reason: to display all menu options within one screen (iPhone 8) | - | - |Implementation Notes

| IN | Description |
|---|---|
| ME02-US15-AC01 | 'Firmware Release Notes' link should be stored on BE side. |
