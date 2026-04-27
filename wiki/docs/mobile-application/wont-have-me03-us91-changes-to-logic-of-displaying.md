---
title: "[Won't have] ME03-US91. Changes to logic of displaying article about GPS configuration when FW is outdated"
sidebar_label: "[Won't have] ME03-US91. Changes to logic of displaying article about GPS configuration when FW is outdated"
sidebar_position: 266
last_modified: "Sep 21, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Story owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| DRAFT |
| Maria Shikareva [X] Timofey Burak [X] Kirill Akulich [X] Dmitriy Morozov [X] Yekaterina Hovin |
| Click here to expand... HALO-13949 - BE: Update link in config Closed |
| Click here to expand... |# Contents

User story Acceptance criteria

# User story

\> As a Halo business owner I want to hide a link to Zendesk article about GPS configuration so that to force a user to update the collar and not show bypasses to initialize the collar's GPS.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | AS IS | TO BE |
|---|---|---|---|---|---|
| ME03-US91-AC01 | Precondition: the collar's FW doesn't support manual GPS initialization feature.The app should not show a right arrow on 'GPS Signal Level Settings'.The section should not be tappable → the app should not open a Zendesk article.QA note: ME03-F01-US66, ME03-F01-US67 are not relevant anymore. | See the screen in Zeplin | See the screen in Zeplin |
| ME03-US91-AC02 | The link to the article should be changed in BE config:AS ISTO BEhttps://support.halocollar.com/hc/en-us/articles/1500003312461-How-to-custom-configure-my-collar-s-indoor-outdoor-GPS-sensorhttps://support.halocollar.com/hc/en-us/articles/360048638273-How-to-update-the-firmware-on-my-Halo-CollarBA note: this should be done for the old apps to work correctly as a link will be deleted for new app versions only. | https://support.halocollar.com/hc/en-us/articles/1500003312461-How-to-custom-configure-my-collar-s-indoor-outdoor-GPS-sensor | https://support.halocollar.com/hc/en-us/articles/360048638273-How-to-update-the-firmware-on-my-Halo-Collar | - | - |
| https://support.halocollar.com/hc/en-us/articles/1500003312461-How-to-custom-configure-my-collar-s-indoor-outdoor-GPS-sensor | https://support.halocollar.com/hc/en-us/articles/360048638273-How-to-update-the-firmware-on-my-Halo-Collar |
