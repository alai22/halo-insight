---
title: "ME14-US40. Show informative error messages when collar returns an error during Wi-Fi setup"
sidebar_label: "ME14-US40. Show informative error messages when collar returns an error during Wi-Fi setup"
sidebar_position: 714
last_modified: "May 18, 2022"
author: "Nicolay Gavrilov"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| DRAFT |
| Nicolay Gavrilov, Kirill Akulich [X] |
| TBDFW dependency to fix the issue with infinite connection attempts |
| Click here to expand... |# Contents

General Description Acceptance criteria

# General Description

At the moment when a user configures a Wi-Fi AP for the collar, during the process of connecting the collar to the configured AP the app shows the progress on the "Connecting to the \<Wi-Fi AP name\>" pop-up:

If an error occurs on steps 2 - 4 ("Connecting to the access point", "Configuring IP address", "Connecting to the internet" and "Connecting to Halo secure cloud services"), the collar restarts the connection process from the 2nd step. The collar gives up the connection process and displays the “Move closer to access point or try again” error on the 5th failed attempt to complete this process (regardless of on which steps it fails).

This error message does not provide our users with enough information to understand what goes wrong and how they could resolve this issue. Therefore it will be better to show a specific error message for each failed attempt depending on which step the collar gives up the whole process. Each error message should contain a link to an article with detailed instructions on how to fix the problem.

# Acceptance criteria

| AC | Description | Links |
|---|---|---|
| ME14-US36-AC01 | If an error occurs and the Wi-Fi setup process is aborted on the "Connecting to the access point" step, the app should close the "Connecting to the \<Wi-Fi AP name\>" pop-up and show the M241 Unable to Connect to \<Network SSID\> message.If the user taps on the "Close" button, the app should close the error pop-up.If the user taps on the "Detailed information" button, the app should open the following link in the web browser: https://support.halocollar.com/hc/en-us/articles/5303874858647Notes:we should not remove the invalid Wi-Fi error (see ME03-F03-AC34). The error should be shown each time the user enters an invalid password. this error may occur due to a specific Wi-Fi router security settings. The AP may be configured to not allow the association with the collar (security or MAC filtering settings).it is irrelevant which on which steps during the previous 4 attempts the collar got an error. The app should display the error message depending on which step the 5th attempt failed. | Appendix 3 – Error, Success, Warning Messages |
| ME14-US36-AC02 | If an error occurs and the Wi-Fi setup process is aborted on the "Configuring IP address" step, the app should close the "Connecting to the \<Wi-Fi AP name\>" pop-up and show the M240 Unable to Configure IP Address message.If the user taps on the "Close" button, the app should close the error pop-up.If the user taps on the "Help" button, the app should open the following link in the web browser: https://support.halocollar.com/hc/en-us/articles/5304101322263Notes: this error may occur because there are no IP adresses avaiable in the WLAN . We can recommend our users to go to the Wi-Fi router settings and manually reserve an IP address for our collar. | Appendix 3 – Error, Success, Warning Messages |
| ME14-US36-AC03 | If an error occurs and the Wi-Fi setup process is aborted on the "Connecting to the internet" step, the app should close the "Connecting to the \<Wi-Fi AP name\>" pop-up and show the M239 Unable to Connect to the Internet message.If the user taps on the "Close" button, the app should close the error pop-up.If the user taps on the "Help" button, the app should open the following link in the web browser: https://support.halocollar.com/hc/en-us/articles/5304434289431Notes: this error may also occur because ping protocol is blocked in the router settings (and the collar pings Google to test the internet connection). We can recommend our users to go to the router settings and unblock this protocol. | Appendix 3 – Error, Success, Warning Messages |
| ME14-US36-AC04 | If an error occurs and the Wi-Fi setup process is aborted on the "Connecting to Halo secure cloud services" step, the app should close the "Connecting to the \<Wi-Fi AP name\>" pop-up and show the M238 Unable to Connect to Halo Secure Cloud Services message.If the user taps on the "Close" button, the app should close the error pop-up.If the user taps on the "Help" button, the app should open the following link in the web browser: https://support.halocollar.com/hc/en-us/articles/5304672359447Notes: this error may occur because either the Wi-Fi router blocks our ports 8883 and 443 (these 2 ports should be available and open) or because the IoT hub is down. | Appendix 3 – Error, Success, Warning Messages |
| ME14-US36-AC05 | If on the "Connect collar to your Wi-Fi network" screen the user selects a WiFi AP with a poor signal (see ME03-F01-AC46), then the app should show the M237 Weak Wi-Fi Signal pop-up message.If the user taps on the "Cancel" button, the app should close the error pop-up.If the user taps on the "Continue" button, the app should open the Wi-Fi password pop-up (see ME03-F03-AC13) | ME03-F03. Collar Wi-Fi setupME03-F01. Collars list |
