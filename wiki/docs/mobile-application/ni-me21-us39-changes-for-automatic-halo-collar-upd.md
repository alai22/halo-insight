---
title: "[NI] ME21-US39. Changes for 'Automatic Halo Collar Updates' screen logic (updated SGEE is enough to go further)"
sidebar_label: "[NI] ME21-US39. Changes for 'Automatic Halo Collar Updates' screen logic (updated SGEE is enough to go further)"
sidebar_position: 276
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Maria Shikareva [X] |
|  |
| Click here to expand... |# Contents

General description User story Acceptance criteria

# General description

As of 07 Oct 2022 : if the collar is added to the account, Wi-Fi is set up, but the collar is new (i.e. has never sent telemetry), then for a few seconds a user can see that the collar is offline though in fact the collar is online but a new telemetry hasn't been sent yet (see HALO-14049 - MOB: Collar offline is displayed for a few seconds Closed for detailed description). We need to handle this case somehow.

1. polling?
2. we need to make sure EPO happens first and when it happens, we should allow the user to move further even if the collar isn't updated. The process can look like: FW update is in progress → collars knows that SGEE is available → stop uploading FW and start loading SGEE. Having SGEE up-to-date is more important on this step because on the next step (GPS initialization) we need to have an updated EPO for better experience.
3. There's no priority in updating FW/ downloading SGEE manifest/ downloading SGEE tar files.

# User story

\> As a Halo app user I want to see a separate status on the 'Automatic Halo Collar Updates' screen when I'm adding a totally new collar so that not to be confused that the collar is offline.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
|  | polling?we need to make sure EPO happens first and when it happens, we should allow the user to move further even if the collar isn't updated. The process can look like: FW update is in progress → collars knows that SGEE is available → stop uploading FW and start loading SGEE. Having SGEE up-to-date is more important on this step because on the next step (GPS initialization) we need to have an updated EPO for better experience.There's no priority in updating FW/ downloading SGEE manifest/ downloading SGEE tar files. |  |  |
