---
title: "ME21-US34. Onboarding: Updates for 'Wi-Fi Setup' flow"
sidebar_label: "ME21-US34. Onboarding: Updates for 'Wi-Fi Setup' flow"
sidebar_position: 271
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Dmitry Kravchuk Siarhei Leushunou [X] Katherina Kaplina |
| Click here to expand... HALO-14142 - MOB: ME21-US34. Onboarding: Updates for 'Wi-Fi Setup' flow Closed |
| Click here to expand...20 Oct 2022 Maria Shikareva [X] Added clarification to ME21-US34-AC04 to avoid questions from QA team in future. |# Contents

User story Acceptance criteria 'Connect Your Halo Collar' screen 'Connect Your Halo to Wi-Fi' screen Add a question mark icon

# User story

\> As a Halo business owner I want to have the screens for the 'Connect Your Halo Collar' flow updated so that they are ready to be included into the Onboarding flow.

# Acceptance criteria

See navigation flow on the Miro board.

| AC | Description | iOS screens designs | Android screens designs | AS IS | TO BE | Main flow | Onboarding flow | AS IS | TO BE | Main flow | Onboarding flow |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 'Connect Your Halo Collar' screen |
| ME21-US34-AC01 | Entry point: a user tapped 'Next' on the 'Add Pet' screen. | Link to Zeplin | - |
| ME21-US34-AC02 | When a user taps a 'Setup Wi-Fi' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should navigate a user to the 'Connect Your Halo to Wi-Fi' screen. |
| 'Connect Your Halo to Wi-Fi' screen |
| ME21-US34-AC03 | The app should not display a 'Finding Available Network' screen anymore. Instead, the app should display the 'Connect Your Halo to Wi-Fi' screen with a spinner. | Link to Zeplin | Link to Zeplin |
| ME21-US34-AC04 | 'Connect Your Halo to Wi-Fi' screen should be changed:AS ISTO BEThe screen with a list of available Wi-Fi networks should consist of:Cancel button'Choose a Network' heading'Skip' button'Connect Collar to Your Wi-Fi' title'Available Networks' subtitleWi-Fi icon + \<Network SSID\> + 'i' icon'Wi-Fi channel warning' text'Can't find your network?' linkThe screen with a list of available Wi-Fi networks should consist of:'Cancel' button → if the screen is opened within the main flow;'\<' button → if the screen is opened within Onboarding;'Setup Wi-Fi' title;'Connect Your Halo to Wi-Fi' subtitle'Select the network where your Halo will be charged overnight. You can always add more networks later.' text;'Can't find your network?' link (should remain as is as described in ME03-F03-AC07);'Available 2.4 GHz Networks' subtitle;the list of found networks (should remain as is as described in ME03-F03-AC05);''Setup Wi-Fi Later' button.QA note: ME03-F03-AC05 is not valid anymore.QA note: logic for displaying 'Setup Wi-Fi Later' button should remain the same as for previous 'Skip' button (as described in ME03-F03-AC10, ME03-F03-AC12). | The screen with a list of available Wi-Fi networks should consist of:Cancel button'Choose a Network' heading'Skip' button'Connect Collar to Your Wi-Fi' title'Available Networks' subtitleWi-Fi icon + \<Network SSID\> + 'i' icon'Wi-Fi channel warning' text'Can't find your network?' link | The screen with a list of available Wi-Fi networks should consist of:'Cancel' button → if the screen is opened within the main flow;'\<' button → if the screen is opened within Onboarding;'Setup Wi-Fi' title;'Connect Your Halo to Wi-Fi' subtitle'Select the network where your Halo will be charged overnight. You can always add more networks later.' text;'Can't find your network?' link (should remain as is as described in ME03-F03-AC07);'Available 2.4 GHz Networks' subtitle;the list of found networks (should remain as is as described in ME03-F03-AC05);''Setup Wi-Fi Later' button. | Link to Zeplin | Link to Zeplin |
| The screen with a list of available Wi-Fi networks should consist of:Cancel button'Choose a Network' heading'Skip' button'Connect Collar to Your Wi-Fi' title'Available Networks' subtitleWi-Fi icon + \<Network SSID\> + 'i' icon'Wi-Fi channel warning' text'Can't find your network?' link | The screen with a list of available Wi-Fi networks should consist of:'Cancel' button → if the screen is opened within the main flow;'\<' button → if the screen is opened within Onboarding;'Setup Wi-Fi' title;'Connect Your Halo to Wi-Fi' subtitle'Select the network where your Halo will be charged overnight. You can always add more networks later.' text;'Can't find your network?' link (should remain as is as described in ME03-F03-AC07);'Available 2.4 GHz Networks' subtitle;the list of found networks (should remain as is as described in ME03-F03-AC05);''Setup Wi-Fi Later' button. |
| ME21-US34-AC05 | When a user taps on the '\<' button, the app should navigate a user to the 'Connect Your Halo Collar' screen. | - | - |
| ME21-US34-AC06 | The whole logic for Wi-Fi network scanning, Wi-Fi password validations and connecting rules should remain the same as described in ME03-F03. Collar Wi-Fi setup. | - | - |
| ME21-US34-AC07 | If no Wi-Fi APs are visible, the app should display the 'Connect Your Halo to Wi-Fi' screen with the corresponding caption (see design). | Link to Zeplin | Link to Zeplin |
| ME21-US34-AC08 | In case the app fails to get the list of available Wi-Fi AP from the collar, it displays the corresponding caption instead of the list of Wi-Fi networks (see the design). | Link to Zeplin | - |
| ME21-US34-AC09 | When all collar connection process steps are successfully completed:Main flowOnboarding flowLeave as is (as described in ME03-F03-AC10 and in [NI] ME21-US07. Add FW update screens to 'Add Collar' flow).The app should:hide the dialogue window with the list of Wi-Fi networks;navigates a user to the 'Halo Collar Updates' screen. | Leave as is (as described in ME03-F03-AC10 and in [NI] ME21-US07. Add FW update screens to 'Add Collar' flow). | The app should:hide the dialogue window with the list of Wi-Fi networks;navigates a user to the 'Halo Collar Updates' screen. | - | - |
| Leave as is (as described in ME03-F03-AC10 and in [NI] ME21-US07. Add FW update screens to 'Add Collar' flow). | The app should:hide the dialogue window with the list of Wi-Fi networks;navigates a user to the 'Halo Collar Updates' screen. |
| ME21-US34-AC10 | M33 Wi-Fi is not connected should be changed:AS ISTO BETitle: "Wi-Fi is Not Connected"Body: "If you skip Wi-Fi setup, your collar will be unable to receive wireless collar updates, new features, and bug fixes.'"Buttons "Connect Wi-Fi", "Skip"Title: "Connect Your Halo to Wi-Fi"Body: "It's important to connect your Halo Collar to Wi-Fi in order to optimize location update rate, battery life and overall collar performance."Buttons: "Setup Wi-Fi", "Continue Without Wi-Fi" | Title: "Wi-Fi is Not Connected"Body: "If you skip Wi-Fi setup, your collar will be unable to receive wireless collar updates, new features, and bug fixes.'"Buttons "Connect Wi-Fi", "Skip" | Title: "Connect Your Halo to Wi-Fi"Body: "It's important to connect your Halo Collar to Wi-Fi in order to optimize location update rate, battery life and overall collar performance."Buttons: "Setup Wi-Fi", "Continue Without Wi-Fi" | - | - |
| Title: "Wi-Fi is Not Connected"Body: "If you skip Wi-Fi setup, your collar will be unable to receive wireless collar updates, new features, and bug fixes.'"Buttons "Connect Wi-Fi", "Skip" | Title: "Connect Your Halo to Wi-Fi"Body: "It's important to connect your Halo Collar to Wi-Fi in order to optimize location update rate, battery life and overall collar performance."Buttons: "Setup Wi-Fi", "Continue Without Wi-Fi" |
| ME21-US34-AC11 | If a user taps "Setup Wi-Fi" button, then the app should:close the pop-up;leave 'Connect Your Halo to Wi-Fi' screen opened. |
| ME21-US34-AC12 | If a user taps "Continue Without Wi-Fi" button, then:Main flowOnboarding flowLeave as is (as described in ME03-F03-AC10 and in [NI] ME21-US07. Add FW update screens to 'Add Collar' flow).The app should:close the pop-up;navigate a user to the 'Halo Collar Updates' screen. | Leave as is (as described in ME03-F03-AC10 and in [NI] ME21-US07. Add FW update screens to 'Add Collar' flow). | The app should:close the pop-up;navigate a user to the 'Halo Collar Updates' screen. |
| Leave as is (as described in ME03-F03-AC10 and in [NI] ME21-US07. Add FW update screens to 'Add Collar' flow). | The app should:close the pop-up;navigate a user to the 'Halo Collar Updates' screen. |
| Add a question mark icon |
| ME21-US34-AC13 | A question mark tappable icon should be displayed at the left upper corner on the following Onboarding screens:'Connect Your Halo Collar' screen;'Connect Your Halo to Wi-Fi' screen. | - | - |
| ME21-US34-AC14 | When a user taps on a question mark icon, then the app should open the 'Need Help?' screen. | - | - |
