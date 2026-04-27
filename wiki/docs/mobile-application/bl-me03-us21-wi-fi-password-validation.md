---
title: "[BL] ME03-US21 Wi-Fi password validation"
sidebar_label: "[BL] ME03-US21 Wi-Fi password validation"
sidebar_position: 54
author: "Nicolay Gavrilov"
---

| Epic | Document status | Story owners | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| ME03-EP02 Collar network connection setup |
| REVISED |
| Nicolay Gavrilov, Pavel Leonenko |
| HALO-3253 - MOB: ME03-US21 Wi-Fi password validation Closed |
| 22 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As an owner I want be sure that I entered a valid Wi-Fi password, otherwise the collar will not properly connect to my Wi-Fi access point.

# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US21-01 | In case the selected network is WEP, the 'OK' button on the Wi-Fi password pop-up is enabled only in case the user entered: either 10 hexadecimal digits,or 26 hexadecimal digits,or 5 ASCII characters,or 13 ASCII charactersin the password field. | WPA encryption allows passwords of up to 64 hexadecimal digits, or from 8 to 63 ASCII characters;At the moment we can't tell if the selected Wi-Fi network is WEP-64 or WEP-128WEP encryption allows passwords of both hexadecimal and ASCII characters. Therefore we shouldn't forbid users to enter ASCII characters in the Wi-Fi AP password field. |
| ME03-US21-02 | In case the selected network is either WPA or WPA2 or WPA_WPA2_MIXED, the 'OK' button on the Wi-Fi password pop-up is disabled when the user enters:either less than 8 characters;or more than 63 ASCII charactersor more than 64 hexadecimal charactersin the password field. |
| ME03-US21-03 | The 'OK' button on the Wi-Fi password pop-up is disabled when the user enters at least one non-ASCII character in the password field. |
| ME03-US21-04 | If the user enters 5 or 13 ASCII symbols in the password field for a WEP network, the mobile app converts them to 10 or 26 hexadecimal symbols respectively before sending them to the collar via BLE. The mobile app does not send additional zero bytes appended to password bytes array. Only the password bytes are sent. | N/A |
