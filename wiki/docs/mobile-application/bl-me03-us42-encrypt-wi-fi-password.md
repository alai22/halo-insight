---
title: "[BL] ME03-US42 Encrypt Wi-Fi password"
sidebar_label: "[BL] ME03-US42 Encrypt Wi-Fi password"
sidebar_position: 79
author: "Galina Lonskaya"
---

| Epic | Document status | Story owners | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| ME03-EP02 Collar network connection setup |
| REVISED |
| Galina Lonskaya, Pavel Leonenko, Eugene Paseka, Anastasia Brechko |
| HALO-4021 - BE+MOB: ME03-US42 Encrypt Wi-Fi password Closed |
| 22 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As an owner I want that my Wi-Fi password is encrypted, so that I can be sure that attacker will not steal password over BLE channel.

# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US42-AC01 | Precondition: "Please enter the password for \<Wi-Fi network\>" popup is displayed.If I enter the Wi-Fi password and submit it, then:the popup is closed and the spinner is displayed;the password should be sent to BE to be encrypted, then:if the mobile app gets the encrypted password, then:the "Connecting Collar to Wi-Fi" process should be started the encrypted password should be sent to the collar,if the collar decrypts the password and submits that the password is valid, then:the "Connecting Collar to Wi-Fi" process should proceed. | N/A |
| ME03-US42-AC02 | For 'Open' networks, password encryption is not required, since there is no password for this type of networks. | N/A |
| ME03-US42-AC04 | If the collar can't decrypt the password, then:M124 Security error for provisioning error with error code 10 should be displayed. | N/A |
| ME03-US42-AC05 | If I try to enter a Wi-Fi password more than 100 times per last 24 hours for 1 collar (no matter for 1 Wi-Fi access point or several), then:M145 Too many attempts to enter Wi-Fi password error should be displayed.The Wi-Fi setup shouldn't proceed. | N/ANote: BE should calculate the number of attempts |
| ME03-US42-AC06 | The number of attempts and hours should be configurable on the BE side. | N/A |
| ME03-US42-AC07 | While "password" encryption (communication with BE), the ME14-F01 Unified errors handling mechanism should be used. | N/A |
