---
title: "[Won't have] ME03-US51. Mobile UI for GPS calibration: show the 'custom'/'default'/'not supported' label"
sidebar_label: "[Won't have] ME03-US51. Mobile UI for GPS calibration: show the 'custom'/'default'/'not supported' label"
sidebar_position: 137
last_modified: "Mar 29, 2021"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| CLIENT REVIEW |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko, Eugene Paseka |
| HALO-6600 - MOB: ME03-US51. Mobile UI for GPS calibration: show 'custom'/'default' label Closed HALO-6697 - BE: ME03-US51. Mobile UI for GPS calibration: show 'custom'/'default' label Closed |# User story

\> As an account owner, I want to view the 'custom'/'default'/'not supported' label at 'Indoor/Outdoor Settings' tile (the expanded collar card) so that I can understand the state of 'Indoor/Outdoor settings'.

# Acceptance criteria

| AC | Description | iOS screens /implementation status | Android screens /implementation status |
|---|---|---|---|
| Note (dependency): The described story (ME03-US51) should be done after or in parallel with ME03-US50. Mobile UI for GPS calibration: instruction how to calibrate. |
| ME03-US51-AC01 | Precondition: 'Collar' card is displayed as expanded at 'Collars' screen.If the collar 'Outdoor/Indoor Settings' are customized, then: 'Custom' label should be displayed within 'Outdoor/Indoor Settings' tile. | Pic 1 The expanded collar card with the state of 'Outdoor/Indoor settings'See Zeplin | The same screen as for iOS |
| ME03-US51-AC02 | Precondition: 'Collar' card is displayed as expanded at 'Collars' screen. If the collar 'Outdoor/Indoor Settings' are default, then:'Default' label should be displayed within 'Outdoor/Indoor Settings' tile. |
| ME03-US51-AC03 | Precondition: 'Collar' card is displayed as expanded at 'Collars' screen.If the collar 'Outdoor/Indoor Settings' cannot be changed by the end user using the collar, then:'Not supported. Collar requires FW update.' label should be displayed within 'Outdoor/Indoor Settings' tile. |
