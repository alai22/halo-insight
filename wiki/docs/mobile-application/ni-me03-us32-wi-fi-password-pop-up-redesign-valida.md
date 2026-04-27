---
title: "[NI] ME03-US32 Wi-Fi password pop-up redesign (validation and viewing the password)"
sidebar_label: "[NI] ME03-US32 Wi-Fi password pop-up redesign (validation and viewing the password)"
sidebar_position: 63
author: "Nicolay Gavrilov"
---

| Epic | Document status | Story owners | Link to JIRA Issue |
|---|---|---|---|
| ME03-EP02 Collar network connection setup |
| DRAFT |
| Nicolay Gavrilov, Pavel Leonenko |
| HALO-6489 - MOB: Wi-Fi password pop-up redesign (validation and viewing the password) Open Tech task: Custom pop-up system (5 sp) |# User story

\> As an owner I want be sure that I entered a valid Wi-Fi password, otherwise I would have to wait for a long time until I realize that something may be wrong with it.

# Design

| Current Design | New design |
|---|---|
|  |  |# Acceptance criteria

| AC | Text | Links / Notes / Designs / Wireframes |
|---|---|---|
| ME03-US32-01 | In case the selected network is WEP, the 'OK' button on the Wi-Fi password pop-up is enabled only in case the user entered: either 10 hexadecimal digits,or 26 hexadecimal digits,or 5 ASCII characters,or 13 ASCII characters. | WPA encryption allows passwords of up to 64 hexadecimal digits, or from 8 to 63 ASCII charactersAt the moment we can't tell if the selected Wi-Fi network is WEP-64 or WEP-128Screen designsButton disabled:Link to ZeplinButton enabled:Link to Zeplin |
| ME03-US32-02 | In case the selected network is either WPA or WPA2 or WPA_WPA2_MIXED, the 'OK' button on the Wi-Fi password pop-up is disabled when the user enters less than 8 characters in the password field. |
| ME03-US32-03 | In case the selected Wi-Fi network uses WEP encryption protocol, the mobile app validates that the entered password is:either 10 hexadecimal digits,or 26 hexadecimal digits,or 5 ASCII characters,or 13 ASCII characters.The validation happens on tapping the "OK" button on the pop-up. In case the validation is failed, the app displays an "Invalid password. Please try again" message right below the password field. The message disappears once the user deletes at least one character from the password field. | WEP encryption allows passwords of both hexadecimal and ASCII characters. Therefore we shouldn't forbid users to enter ASCII characters in the Wi-Fi AP password field.Screen designLink to Zeplin |
| ME03-US32-04 | The app does not allow the user to enter more than 63 characters in the password field and displays the 'invalid password' error message (see ME03-US32-03). The message disappears once the user deletes a character of the password. |
| ME03-US32-05 | The app does not allow the user to enter non-ASCII characters and displays the 'invalid password' error message (see ME03-US32-03). The message disappears once the user enters a valid password character or deletes a character from the password. |
| ME03-US32-06 | Users can tap on a button to view and hide the characters of the Wi-Fi password. | N/A |
| ME03-US32-07 | If the user enters 5 or 13 ASCII symbols in the password field for a WEP network, the mobile app converts them to 10 or 26 hexadecimal symbols respectively before sending them to the collar via BLE. The mobile app does not send additional zero bytes appended to password bytes array. Only the password bytes are sent. | N/A |
