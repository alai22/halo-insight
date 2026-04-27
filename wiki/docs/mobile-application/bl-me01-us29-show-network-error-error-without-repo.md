---
title: "(BL) ME01-US29. Show \"Network error\" error without \"Report issue\" button in case of \"connection issue\" reason"
sidebar_label: "(BL) ME01-US29. Show \"Network error\" error without \"Report issue\" button in case of \"connection issue\" reason"
sidebar_position: 210
last_modified: "Oct 04, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| BASELINED in ME01-F00. App Launch (Splash Screen, Start Screen, Error Screen) by Galina Lonskaya on 04 Oct 2024 |
| Galina Lonskaya Nikita Krisko |
| HALO-11084 - MOB: Differentiate connection and communication issues within "Enter the system" flow Closed |
| Click here to expand...23 Mar 2022 story is created by Galina Lonskaya |# User story

\> As Halo Collar app account owner I want to see only relevant buttons within M113 Network error so that I can not send mobile logs in vain (when I just have connection issues)

# Acceptance criteria

| AC | Description | Links |
|---|---|---|
| ME01-US26-AC01 | "Report issue" button should not be displayed within M113 Network error, in case "connection" error is occurred. Note: "connection" error is an any error related to weak Internet connection or to the absence of Internet connection | ME14-F01 Unified errors handlingAppendix 3 – Error, Success, Warning Messages |
