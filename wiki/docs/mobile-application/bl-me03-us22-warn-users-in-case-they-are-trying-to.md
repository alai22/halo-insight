---
title: "[BL] ME03-US22. Warn users in case they are trying to connect to a \"bad\" Wi-Fi channel"
sidebar_label: "[BL] ME03-US22. Warn users in case they are trying to connect to a \"bad\" Wi-Fi channel"
sidebar_position: 203
last_modified: "Apr 11, 2022"
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owner | Link to JIRA Issue | Change history |
|---|---|---|---|
| DRAFT |
| Valeryia Chyrkun [X] |
| HALO-10908 - MOB+BE: Warn users in case they are trying to connect to a "bad" Wi-Fi channel Closed Ballpark estimation: MOB - 3SP, QA -3SP |
| As of 24 Mar 2022 - added ME03-US22-AC08 and edited ME03-US22-AC06As of 04/04/2022 - added the necessary space in the text of message on the ME03-US22-AC05 and ME03-US22-AC08 |# General description

Currently, we receive from the collar for each network (SSID) the following data: // Scan information response structure typedef struct rsi_scan_info_s Unknown macro: \{ // channel number of the scanned AP uint8_t rf_channel; // security mode of the scanned AP uint8_t security_mode; // rssi value of the scanned AP uint8_t rssi_val; // network type of the scanned AP uint8_t network_type; // SSID of the scanned AP uint8_t ssid[RSI_SSID_LEN]; // BSSID of the scanned AP uint8_t bssid[RSI_MAC_ADDR_LEN]; // reserved uint8_t reserved[2]; \} rsi_scan_info_t;

Useful article sent by Michael: https://www.networkworld.com/article/2215287/coping-with-wi-fi-s-biggest-problem-interference.html

# Contents

General description User story Acceptance criteria

# User story

\> As an Owner I want to be warned if I connect to 'bad' Wi-Fi network so that I could have stable and quick connection.

# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US22-AC01 | The list of Wi-Fi networks should contain indication of 'bad' Wi-Fi. If the network is considered 'bad' then the following elements should be displayed:\<Network SSID\>'Wi-Fi channel warning' text + 'i' icon | iOS Android |
| ME03-US22-AC02 | 'Wi-Fi channel warning' text + 'i' icon is displayed if at least one rule is applicable: The Wi-Fi channel is not 1, 6 or 11 (for US) There are multiple networks (2 and more) on same channel with high RSSI (\<60dBm) |  |
| ME03-US22-AC03 | Precondition: both rules described in ME03-US22-AC02 are applied to a specific network If a network is not connected to channel 1, 6 or 11 and there's another network connected to the same channel as specific network, and if I click 'i' icon then I see a pop-up with the following elements:'Wi-Fi channel warning' title'This access point is on channel X. For 2.4 GHz networks it’s strongly recommended to use channels 1, 6 or 11, otherwise you may experience performance problems. ' text, where 'X' is a ordinary number of channel connected to the current SSID.'Learn more' button 'Close' button | iOS. Android |
| ME03-US22-AC04 | Precondition: The Wi-Fi channel is not 1, 6 or 11 (for US)If I click 'i' icon then I see a pop-up with the following elements:'Wi-Fi channel warning' title'This access point is on channel X. For 2.4 GHz networks it’s strongly recommended to use channels 1, 6 or 11, otherwise you may experience performance problems. ' text, where 'X' is a ordinary number of channel connected to the current SSID.'Learn more' button 'Close' button |
| ME03-US22-AC05 | Precondition: There are multiple networks (2 and more) on same channel with high RSSI (\<-60dBm)If I click 'i' icon then I see a pop-up with the following elements:'Wi-Fi channel warning' title'This network is on the same channel as one of the nearby networks. You may experience issues. Consider changing the channel' text'Learn more' button 'Close' button |  |
| ME03-US22-AC08 | Precondition: There are multiple networks (2 and more) on same channel with high RSSI (\<-60dBm) and some of them are hidden/not shown in the list ( does not match the requirements described in ME03-F03. Collar Wi-Fi setup#,ME03%2DF03%2DAC01,-The%20mobile%20app )If I click 'i' icon then I see a pop-up with the following elements:'Wi-Fi channel warning' title'This network is on the same channel as one of the nearby networks. You may experience issues. Consider changing the channel' text'Learn more' button 'Close' button |  |
| ME03-US22-AC06 | If I click 'Learn more' then I see Zendesk article about which Wi-fi channels are considered 'bad' and how to fix possible Wi-Fi issues. The link to the article is https://support.halocollar.com/hc/en-us/articles/4810783253911 If user navigates to the article from the pop-up, and afterwards returns back to the list of Wi-Fi connections, then the pop-up is closed |  |
| ME03-US22-AC07 | If I click 'Close', then the pop-up is closed. |  |
