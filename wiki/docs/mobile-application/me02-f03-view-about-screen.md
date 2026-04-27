---
title: "ME02-F03. View \"About\" screen"
sidebar_label: "ME02-F03. View \"About\" screen"
sidebar_position: 97
author: "Galina Lonskaya"
---

| Document status | Test cases status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| REVISED |
| UPDATED as of 15 Feb 2022 (by Alexandr Tsarikov [X]) |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko |
| HALO-3240 - MOB+BE: ME02-US11. View About screen Closed HALO-4651 - Android: ME02-F03. View "About" screen Closed HALO-9925 - MOB: Change "copyright" from "2021" to "2022" Closed |
| Click here to expand...02 Sep 2022 Maria Shikareva [X] Baselined [BL] ME01-US23. MOB: Change year from "2021" to "2022" on Splash/Start/About screens.07 Jun 2024 Kiryl Trafimau Baselined:(BL) ME01-US36. MOB: Add register mark to the Halo name(BL) ME01-US37. MOB: Update Halo logo |# Contents

User story Acceptance criteria Privacy Policy Terms of Service Data Providers Software License Location Information App Release Notes Firmware Release Notes

# User story

\> As a user I want to view About screen so that I can be aware of app legal info.

# Acceptance criteria

| AC | Description | iOS screen design / implementation statusIOS DONE | Android screen design/implementation statusANDROID DONE | Privacy Policy | Terms of Service | Data Providers | Software License | Location Information | App Release Notes |
|---|---|---|---|---|---|---|---|---|---|
| ME02-F03-AC01 | Precondition: Settings screen is opened.If I tap on the About button, then the About screen should be opened.The screen consists of:Back icon"About" titleHalo Logo + Halo label"Version" + \<app version number\>"Ⓒ \<current year\> Halo® by Protect Animals With Satellites, LLC""Terms of Service" tile"Privacy Policy" tile"Data Providers" tile"Software License" tile"Location Information" tile"App Release Notes" tileFirmware Release NotesTab barNote: List of tiles should be scrollable if it doesn't fit. | The screen consists of:Back icon"About" titleHalo Logo + Halo label"Version" + \<app version number\>"Ⓒ \<current year\> Halo® by Protect Animals With Satellites, LLC""Terms of Service" tile"Privacy Policy" tile"Data Providers" tile"Software License" tile"Location Information" tile"App Release Notes" tileFirmware Release NotesTab bar | Link to Zeplin | Link to Zeplin |
| The screen consists of:Back icon"About" titleHalo Logo + Halo label"Version" + \<app version number\>"Ⓒ \<current year\> Halo® by Protect Animals With Satellites, LLC""Terms of Service" tile"Privacy Policy" tile"Data Providers" tile"Software License" tile"Location Information" tile"App Release Notes" tileFirmware Release NotesTab bar |
| ME02-F03-AC02 | All links from this screen should be saved on BE. | - | - |
| ME02-F03-AC12 | 'Halo' logo icon and 'Halo' label should be displayed in one line.Note: decided internally by dev team, reason: to display all menu options within one screen (iPhone 8) | - | - |
| ME02-F03-AC03 | If I tap on the Privacy Policy link, then web-view with Privacy policy should be opened.web-view header consists of:Back icon"Privacy Policy" titleSee link: https://app.termly.io/document/privacy-policy/2fc6550d-2a1c-4858-8a2f-bd3cd3b2021a | - | - |
| ME02-F03-AC04 | If I tap on the Terms of service link, then web-view with Terms of Service should be opened.web-view header consists of:Back icon"Terms of Service" titleSee link: https://app.termly.io/document/terms-of-use-for-ecommerce/02d81772-7c46-4ce0-9149-aca6a49fba8e | - | - |
| ME02-F03-AC05 | If I tap on the Data Providers link, then the web page with Data Providers should be opened. | - | - |
| ME02-F03-AC06 | "Data Providers" web page should have a similar UI design:Note: this page is prepared by Softeq | - | - |
| ME02-F03-AC07 | If I tap on the Software License link, then the web page with Software License should be opened. | - | - |
| ME02-F03-AC08 | "Software License" web page should have the following UI design → see sample in ME02-F03-AC06.Note: this page is prepared by Softeq | - | - |
| ME02-F03-AC09 | If I tap on the Location Information link, then the web page with Location Information should be opened.web-view header consists of:Back icon"Location Information" title | - | - |
| ME02-F03-AC10 | "Location Information" web page should have the following UI design → see sample in ME02-F03-AC06.Note: this page is prepared by Softeq | - | - |
| ME02-F03-AC11 | If I tap on Release Notes, then Halo App Store Page should be opened.See App Store link: https://apps.apple.com/app/id1476830649See Google Play link: TBD | - | - |
| Firmware Release Notes |
| ME02-F03-AC12 | If I tap on 'Firmware Release Notes' button, then:'https://support.halocollar.com/hc/en-us/articles/1500004830041-Firmware-Update-Release-Notes' link should be opened in default browser. | - | - |

