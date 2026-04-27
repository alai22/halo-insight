---
title: "[BL] ME03-US19. Update Wi-fi/LTE connection status / signal strength displaying at the Collars List"
sidebar_label: "[BL] ME03-US19. Update Wi-fi/LTE connection status / signal strength displaying at the Collars List"
sidebar_position: 50
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|---|
| Owner |
| ME03 Manage collars |
| REVISED |
| Galina Lonskaya |
| HALO-2910 - MOB+BE: ME03-US19. Update Wi-fi/LTE connection status / signal strength displaying Closed |
| 07 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# Intro

The primary collar communication type is Wi-fi. If Wi-fi isn't available or there is no signal, then LTE should be used. This logic is embedded into collar FW.

# User story

\> As an owner, I want to view state of Wi-Fi/Cellular connection state so that I can understand what communication type is used

| AC | Description | Collars list: Cellular tile | Collars list: Wi-Fi tile |  |
|---|---|---|---|---|
| ME03-US19-AC01 | If Wi-Fi is used currently, the following data should be displayed at Cellular tile:Crossed cellular icon"Cellular is paused" text"Currently using Wi-fi" text |
| ME03-US19-AC02 | If Cellular is used currently, then the following data should be displayed at Cellular tile at the Collars List:Cellular icon with correspond strength signal"Cellular" title + (\<Cellular signal strenght\>) title"Connected to" text+ \<Network name\> |
| ME03-US19-AC03 | Cellular can have the following signal strength level:Strong signal \> - 65 dBmGood signal - 65 to - 75 dBmFair signal -75 to - 85 dBmPoor signal \< - 85 dBm |
| ME03-US19-AC04 | The cellular icon can have the following states: |
| ME03-US19-AC05 | Precondition: Wi-Fi network is addedIf Wi-Fi isn't available, then the following data should be displayed at Wi-Fi tile at the Collars List:Wi-Fi crossed icon"Wi-fi" title"\<Network\> isn't available" text |
| ME03-US19-AC06 | Precondition: Wi-Fi network is added If Wi-Fi is connected, then the following data should be displayed at Wi-Fi tile at the Collars List:Wi-fi icon with correspond strength signal"Wi-Fi" title + "(\<Wi-Fi signal strenght\>)""Connected to" text+ \<Wi-Fi network\> |
| ME03-US19-AC07 | Wi-Fi can have the following signal strength level:Strong signal \> - 50 dBmGood signal - 50 to - 60 dBmFair signal - 60 to -70 dBmPoor signal \< -70 dBm |
| ME03-US19-AC08 | Wi-Fi icon can have the following states: |
| ME03-US19-AC09 | If Wi-Fi isn't added to the collar, then the following data should be displayed at Wi-Fi tile at the Collars List:Crossed wi-fi icon"Wi-Fi" title"Wi-Fi network is not yet added" textNote: This logic has been implemented. UI should be updated only. |
| ME03-US19-AC10 | If Wi-Fi isn't added to the collar and the collar has never connected via LTE, then the following data should be displayedat Wi-Fi tile at the Collars List:Crossed wi-fi icon"Wi-Fi" title"Wi-Fi network is not yet added" textat LTE tile at the collars List:Crossed LTE icon"Cellular" title"Cellular isn't available" text |
| ME03-US19-AC11 | "Details" button should be removed out of Cellular tile. |
