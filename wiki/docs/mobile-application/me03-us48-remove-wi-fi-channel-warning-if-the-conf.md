---
title: "ME03-US48. Remove 'Wi-Fi channel warning' if the conflicting networks are from the same AP"
sidebar_label: "ME03-US48. Remove 'Wi-Fi channel warning' if the conflicting networks are from the same AP"
sidebar_position: 312
last_modified: "May 27, 2024"
author: "Galina Lonskaya"
---

| Document status | Story owners | Link to JIRA Issue |
|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya |
| HALO-16197 - MOB: Remove 'Wi-Fi channel warning' if the conflicting SSIDs are from the same AP Closed |# User story

\> As a Halo account owner I do not want to see 'Wi-Fi channel warning' when the conflicting networks are from the same access point so that I will not be misled by 'Wi-Fi channel warning' when actually Wi-Fi network can be used. More context: This is a common scenario for customers who enable a ‘Guest’ network - the same AP offers two SSID’s on the same RF that don’t actually conflict - but use two SSIDs.

# Acceptance criteria

| AC | Text | Link |
|---|---|---|
| ME03-US48-AC01 | If the assumed conflicting networks are from the same access point (see how to understand it in ME03-US48-IN01), then: Wi-Fi network should not be considered as not recommended for the usage and 'Wi-Fi channel warning' label and 'i' icon should not be displayed under the name of these networks on the Setting Up Wi-Fi screen. | See the initial requirement: ME03-F03-AC49 |# Implementation notes

| IN | Text |
|---|---|
| ME03-US48-IN01 | The system should be able to tell by the BSSID that some conflicting SSIDs from one AP. |
