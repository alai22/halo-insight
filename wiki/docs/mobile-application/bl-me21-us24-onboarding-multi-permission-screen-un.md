---
title: "[BL] ME21-US24. Onboarding: Multi-permission screen - unification of screen view for Android and iOS"
sidebar_label: "[BL] ME21-US24. Onboarding: Multi-permission screen - unification of screen view for Android and iOS"
sidebar_position: 258
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owner | Link to JIRA issue | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Valeryia Chyrkun [X] |
| HALO-13411 - MOB: ME21-US24. Onboarding: Multi-permission screen - unification of screen view for Android and iOS Closed |
| Click here to expand...14 Oct 2022 Maria Shikareva [X] Marked the story as baselined (see ME01-F10. Enable Permissions). |# General description

We do not want to 'hide' any setting that is always 'ON' based on the OS; rather, we should always show all three permissions sections. For ones that are ON by definition, we should just show them already in the ON state. There is another important element to this screen, which is to 'teach' the customer what the interactions are between the mobile app and the collar/phone.

# User story

\> As Halo app account owner, I want to view list of permissions required for Halo app so that I can manage permissions required for Halo app and be informed about which permissions are needed for Halo to work properly.

# Acceptance criteria

| AC | Description | iOS | Android |
|---|---|---|---|
| ME21-US24-AC01 | The set of sections for Android and iOS devices regardless of what permissions are needed by device should be the same. (See ME21-US03-AC01 for iOS) | Zeplin |  |
| ME21-US24-AC02 | If version of OS or device type doesn't support/ask for certain permission type, then this permission should have 'ON' state and be disabled by default. |  |  |
| ME21-US24-AC03 | For iOS 13 the Bluetooth permission should have "ON" state and be disabled by default. |  |  |
| ME21-US24-AC04 | For Android only: If I click 'Allow' on Bluetooth permission, then Location permission should also change state to 'ON'. If I click 'Don't allow' on Bluetooth permission, then Location permission should also change its state to 'OFF'. |  |  |
| ME21-US24-AC05 | For Android only: If I click 'Allow' on Location permission, then Bluetooth permission should also change state to 'ON'. If I click 'Don't allow' on Location permission, then Bluetooth permission should also change its state to 'OFF'. |  |  |
