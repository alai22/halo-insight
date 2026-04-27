---
title: "ME14-US36. Help to resolve connection issues during Wi-Fi setup"
sidebar_label: "ME14-US36. Help to resolve connection issues during Wi-Fi setup"
sidebar_position: 713
author: "Nicolay Gavrilov"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Nicolay Gavrilov Kirill Akulich [X] |
| HALO-10648 - xMOB+BE: ME14-US36. Help to resolve connection issues during Wi-Fi setup Closed |
| Click here to expand...14 May 2022 Nicolay Gavrilov added IDs to all of the pop-up messages18 May 2022 Nicolay Gavrilov edited the whole story to make it work with the current FW version19 May 2022 Nicolay Gavrilovadded ME14-US36-AC07 |# Contents

General Description Acceptance criteria Text updates New error messages

# General Description

At the moment when a user configures a Wi-Fi AP for the collar, during the process of connecting the collar to the configured AP the app shows the progress on the "Connecting to the \<Wi-Fi AP name\>" pop-up:

If an error occurs in the 2nd step of the process ("Connecting to the access point"), the collar makes 4 more attempts to connect. If the issue persists, the collar gives up the connection process and the app displays the “Move closer to access point or try again” error on the 5th failed attempt to connect to the access point.

If an error occurs in the 3rd - 5th steps ("Configuring IP address", "Connecting to the internet" and "Connecting to Halo secure cloud services") the collar will restart the process from the 2nd step. And in such cases the process never stops. The user may close the pop-up, but the device will continue the connection attempts in the background (to be fixed later within ME14-US40. Show informative error messages when collar returns an error during Wi-Fi setup).

The error message we have at the moment does not provide our users with enough information to understand what goes wrong and how they could resolve this issue. And there are no errors for the other steps, which could give the users an idea of what is wrong. Therefore it will be better to show specific error messages depending on which step the collar gets "stuck". Each error message should contain a link to an article with detailed instructions on how to fix the problem.

# Acceptance criteria

| AC | Description | Links / Designs | Text updates | New error messages | Poor Wi-Fi signal error |
|---|---|---|---|---|---|
| ME14-US36-AC07 | The following text updates should be done for the "Connecting to the \<Wi-Fi AP name\>" pop-up:"Configuring IP Address" step should be renamed to "Requesting IP address from router""Connecting to the internet" step should be renamed to "Confirming router internet access" | iOS |
| ME14-US36-AC01 | If an error occurs and the Wi-Fi setup process is automatically aborted on the "Connecting to the access point" step, the app should close the "Connecting to the \<Wi-Fi AP name\>" pop-up and show the M241 Unable to Connect to \<Network SSID\> message.Notes:we should not remove the invalid Wi-Fi error (see ME03-F03-AC34). The error should be shown each time the user enters an invalid password. this issue may occur due to a specific Wi-Fi router security setting. The AP may be configured to not allow the association with the collar (security or MAC filtering settings). | Appendix 3 – Error, Success, Warning Messages |
| ME14-US36-AC06 | Preconditions:the completion of any step from 3 - 5 takes \> than 5 secondsOR the connection process was restarted from the beginning at least onceIf one of the preconditions is true, and the user taps on the "Close" button on the "Connecting to the \<Wi-Fi AP name\>" pop-up, then the app should close the pop-up and display the corresponding error message. The error message should be displayed for the latest step the connection process gets to, during the current Wi-Fi setup attempt. The descriptions of the error messages are given in the acceptance criteria below.Examples:if the user initiates the connection process, and it is stuck on the 4th step for more than 5 seconds, and the user decides to abort the process (before the process is automatically restarted), then the app should show the error message for the 4th step.if the connection process fails on the 2nd step, restarts, goes up to the 5th step, fails again, restarts, and the user decides to abort the process on the 3rd step, then the app should show an error message for the 5th step. | - |
| ME14-US36-AC02 | The M240 Unable to request IP Address message should be used if the latest step the process got to is "Requesting IP address from router".Notes: this error may occur because there are no IP adresses avaiable in the WLAN . We can recommend our users to go to the Wi-Fi router settings and manually reserve an IP address for our collar. | Appendix 3 – Error, Success, Warning Messages |
| ME14-US36-AC03 | The M239 Unable to Connect to the Internet message should be used if the latest step the process got to is "Confirming router internet access".Notes: this error may also occur because ping protocol is blocked in the router settings (and the collar pings Google to test the internet connection). We can recommend our users to go to the router settings and unblock this protocol. | Appendix 3 – Error, Success, Warning Messages |
| ME14-US36-AC04 | The M238 Unable to Connect to Halo Secure Cloud Services message should be used if the latest step the process got to is "Connecting to Halo secure cloud services".Notes: this error may occur because either the Wi-Fi router blocks our ports 8883 and 443 (these 2 ports should be available and open) or because the IoT hub is down. | Appendix 3 – Error, Success, Warning Messages |
| ME14-US36-AC05 | If on the "Connect collar to your Wi-Fi network" screen the user selects a WiFi AP with a poor signal (see ME03-F01-AC46), then the app should show the M237 Weak Wi-Fi Signal pop-up message. | ME03-F03. Collar Wi-Fi setupME03-F01. Collars list |
