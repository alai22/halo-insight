---
title: "[BL] ME02-US11. View \"About\" screen"
sidebar_label: "[BL] ME02-US11. View \"About\" screen"
sidebar_position: 47
author: "Galina Lonskaya"
---

| Role | Epic | Document status | BA story owner | QA story owner | DEV story owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|---|---|---|
| Owner |
| ME02 Settings |
| APPROVED |
| Galina Lonskaya |
| Anastasia Brechko |
| Siarhei Leushunou [X], Eugene Paseka |
| HALO-3240 - MOB+BE: ME02-US11. View About screen Closed |
| 15 Feb 2022 Maria Shikareva [X] Marked the story as baselined. |# User story

\> As a user, I want to view About screen so that I can be aware of app legal info.

Acceptance criteria

| AC | Description | Privacy Policy | Terms of Service | Data Providers | Software License | Location Information | Release Notes |
|---|---|---|---|---|---|---|---|
| ME02-US11-AC01 | Precondition: Settings screen is opened.If I tap on the About icon, then the About screen should be opened:The screen consists of:Back icon"About" titleHalo Logo"Version" + \<app version number\>"Ⓒ 2020 Halo by PAWS, LCC""Terms of Service" tile"Privacy Policy" tile"Data Providers" tile"Software License" tile"Location Information" tile"Release Notes" tileTab barNote: List of tiles should be scrollable if it doesn't fit. |  | The screen consists of:Back icon"About" titleHalo Logo"Version" + \<app version number\>"Ⓒ 2020 Halo by PAWS, LCC""Terms of Service" tile"Privacy Policy" tile"Data Providers" tile"Software License" tile"Location Information" tile"Release Notes" tileTab bar |
|  | The screen consists of:Back icon"About" titleHalo Logo"Version" + \<app version number\>"Ⓒ 2020 Halo by PAWS, LCC""Terms of Service" tile"Privacy Policy" tile"Data Providers" tile"Software License" tile"Location Information" tile"Release Notes" tileTab bar |
| ME02-US11-AC02 | All links from this screen should be saved on BE. |
| ME02-US11-AC03 | If I tap on the Privacy Policy link, then web-view with Privacy policy should be opened.Web-view header consists of:Back icon"Privacy Policy" titleSee link: https://app.termly.io/document/privacy-policy/2fc6550d-2a1c-4858-8a2f-bd3cd3b2021a |
| ME02-US11-AC04 | If I tap on the Terms of service link, then web-view with Terms of Service should be opened.Web-view header consists of:Back icon"Terms of Service" titleSee link: https://app.termly.io/document/terms-of-use-for-ecommerce/02d81772-7c46-4ce0-9149-aca6a49fba8e |
| ME02-US11-AC05 | If I tap on the Data Providers link, then the WEB page with Data Providers should be opened. |
| ME02-US11-AC06 | "Data Providers" WEB page should have a similar UI design:Note: this page is prepared by Softeq |
| ME02-US11-AC07 | If I tap on the Software License link, then the WEB page with Software License should be opened. |
| ME02-US11-AC08 | "Software License" WEB page should have the following UI design → see sample in ME02-US11-AC06. Note: this page is prepared by Softeq |
| ME02-US11-AC09 | If I tap on the Location Information link, then the WEB page with Location Information should be opened.Web-view header consists of:Back icon"Location Information" title |
| ME02-US11-AC10 | "Location Information" WEB page should have the following UI design → see sample in ME02-US11-AC06. Note: this page is prepared by Softeq |
| ME02-US11-AC11 | If I tap on Release Notes, then HALO App Store Page should be opened.See link: https://apps.apple.com/app/id1476830649Note: At that moment the link doesn't work as we haven't released the app in App Store |
