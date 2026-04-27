---
title: "(BL) ME03-US143. BE: Display valid name of the network"
sidebar_label: "(BL) ME03-US143. BE: Display valid name of the network"
sidebar_position: 326
last_modified: "Jun 07, 2024"
author: "Kiryl Trafimau"
---

| Document status | Story owners | Links to JIRA Issues | Related requirements | Change History |
|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-15449 - BE: MNC API and/or table lookup to report current carrier by Operator name (vs. by MNC) on Cellular Status UI Closed |
| [BL] ME07-US146. MOB, BE: Display Cellular network name on the Pet Card |
| 07 Jun 2024 Kiryl Trafimau Baselined to ME03-F07. Collar Diagnostic |# Contents

User story Acceptance criteria

# User story

\> As an owner I want to view the cellular network name so that I can understand the cellular data provider.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| ME03-US143-AC01 | Precondition: Wi-Fi is not configured for collar AND according to the last received telemetry the collar is using cellularIF user opens My collars and expands this collarTHEN Cellular tile displays the Brand name of the cellular provider according to the Lookup table |  | The same design as for iOS. |
| ME03-US143-AC02 | Precondition: Wi-Fi is configured for the collar, BUT according to the last received telemetry the access point is not available AND cellular is used currentlyIF user opens My collars and expands this collarTHEN Cellular tile displays the Brand name of the cellular provider according to the Lookup table |  | The same design as for iOS. |
| ME03-US143-AC03 | IF BE receives the correct name (not only numbers and spaces) then display it. 2. IF BE receives only numbers and spaces then display the name according to the Lookup tablemcc-mnc.csv2a. IF BE received mcc mnc which not present in the table, then display mcc mnc.2b. IF BE received mcc mnc which does not have operator name in the table, then display mcc mnc. |  |  |
