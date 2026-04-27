---
title: "ME03-US116. Show 'Connected to LTE' label on Collars list, if the collar cannot identify the title of the currently used LTE network"
sidebar_label: "ME03-US116. Show 'Connected to LTE' label on Collars list, if the collar cannot identify the title of the currently used LTE network"
sidebar_position: 336
last_modified: "Jun 07, 2024"
author: "Galina Lonskaya"
---

Page info| Document status | Story owners | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya |
| HALO-17499 - MOB: Show "LTE" label instead of empty space on Collars list and Pet Card Closed |
| History of changes29 Aug 2023 the draft story is created by Galina Lonskaya |Contents- [User story](#ME03US116.Show'ConnectedtoLTE'labelonCollarslist,ifthecollarcannotidentifythetitleofthecurrentlyusedLTEnetwork-Userstory)
- [Acceptance criteria](#ME03US116.Show'ConnectedtoLTE'labelonCollarslist,ifthecollarcannotidentifythetitleofthecurrentlyusedLTEnetwork-Acceptancecriteria)

Background and goalSofteq dev team has met the cases when the collar is connected to LTE, but doesn't return LTE operator name and the empty space is displayed on Collars list and Pet card. Agreed with Michael that the LTE label label should be displayed in these cases.

# User story

\> As Halo account owner I want to see 'Connected to LTE' label on Collars list so that I will not be confused by the empty space on the place of LTE network name on Collars list and be sure that LTE network is connected at the moment.

# Acceptance criteria

| AC | Description | name Links |
|---|---|---|
| ME03-US116-AC01 | If the collar is currently connected to LTE network, but not provide 'LTE network' name, then: 'Connected to LTE' label should be displayed on Collars list screen. |  |
