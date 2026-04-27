---
title: "[BL] ME21-US38. Changes for 'Automatic Halo Collar Updates' screen logic (telemetry = null)"
sidebar_label: "[BL] ME21-US38. Changes for 'Automatic Halo Collar Updates' screen logic (telemetry = null)"
sidebar_position: 275
last_modified: "Oct 28, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Timofey Burak [X] Siarhei Leushunou [X] Milana Vasilionak [X] |
| HALO-14049 - MOB: Collar offline is displayed for a few seconds Closed HALO-14189 - ME21-US38. Changes for 'Automatic Halo Collar Updates' screen logic (telemetry = null) Closed |
| Click here to expand...07 Oct 2022 Maria Shikareva [X] Added Jira links + updated designs.10 Oct 2022 Maria Shikareva [X] Added a precondition to ME21-US38-AC01 as discussed with Siarhei Leushunou [X]: we don't need to show an 'Initializing...' status if we get information that the FW is up-to-date.28 Oct 2022 Maria Shikareva [X] Marked the story as baselined (ME03-F09. Collar Updates). |# Contents

General description User story Acceptance criteria

# General description

As of 07 Oct 2022 : if the collar is added to the account, Wi-Fi is set up, but the collar is new (i.e. has never sent telemetry), then for a few seconds a user can see that the collar is offline though in fact the collar is online but a new telemetry hasn't been sent yet (see HALO-14049 - MOB: Collar offline is displayed for a few seconds Closed for detailed description). We need to handle this case somehow.

# User story

\> As a Halo app user I want to see a separate status on the 'Automatic Halo Collar Updates' screen when I'm adding a totally new collar so that not to be confused that the collar is offline.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | Icon | SGEE status in the app | GPS light meaning image/ animation | Collar update status in the app(regardless of version) | Battery light meaning image/ animation |
|---|---|---|---|---|---|---|---|---|
| ME21-US38-AC01 | Preconditions:a user entered the 'Automatic Halo Collar Updates' screenANDtelemetry = nullANDthe latest data about current FW version is NOT up-to-date.The app should display a new statuses both for 'Satellite Position Data' and 'Collar Update Status' sections:IconSGEE status in the appGPS light meaning image/ animationCollar update status in the app(regardless of version)Battery light meaning image/ animationInitializing your Halo Collar. Please wait.an image with pink LEDInitializing your Halo Collar. Please wait.an image with green LED |  | Initializing your Halo Collar. Please wait. | an image with pink LED | Initializing your Halo Collar. Please wait. | an image with green LED | Link to Zeplin | Link to Zeplin |
|  | Initializing your Halo Collar. Please wait. | an image with pink LED | Initializing your Halo Collar. Please wait. | an image with green LED |
| ME21-US38-AC02 | New status should not be displayed on the Collars list. | - | - |
