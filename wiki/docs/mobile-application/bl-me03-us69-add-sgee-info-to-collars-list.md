---
title: "[BL] ME03-US69. Add SGEE info to \"Collars\" list"
sidebar_label: "[BL] ME03-US69. Add SGEE info to \"Collars\" list"
sidebar_position: 191
author: "Maria Shikareva [X]"
---

| Document status | Story owners | Links to JIRA Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Valeryia Chyrkun [X] Kirill Akulich [X] Aleksei Pay Alexandr Tsarikov [X]Dmitriy Morozov [X] |
| HALO-10256 - BE+MOB: Add SGEE info to "Collars" list Closed As of 01/31/2022 - Ballpark estimation: 2-3SP (BE), 2SP with scale implementation and 3SP without scale (Mobile), 3SP (QA) |
| Click here to expand...As of 31 Jan 2022 Renaming ‘GPS accuracy’ to ‘Satellite position data’ Changing information on Advanced Setting page adding information about how many days left before the next update and to add in parenthesis when the last update took place (today/yesterday/this week). All the information is shown on the Advanced settings screen and the only case when we will need the additional screen is when the data is outdated. Deleted link to Help Center with the article on how to fix the issue As of 25 Feb 2022 Added data format (MM.DD.YYYY) to ME03-US69-AC01Added description of warning icon to ME03-US69-AC0502 Mar 2022 corrected ME03-US69-AC01 |# Contents

General description User story Acceptance criteria Advanced settings page - up-to-date data (normal flow) Advanced settings page - outdated files (alternative flow) Connection and communication errors Implementation notes

# General description

As of 19 Jan 2022 This information can be helpful for the users to understand the level of collar's GPS accuracy.

As of 24 Jan 2022 discussion: Absence of SGEE info on Halo app is number 1 issue for final customers, usually they call to support and say 'Something wrong with my GPS, it's not accurate' and the most common reason is that the collar didn't download SGEE data (GPS update) due to any reason (some houses are not equipped with Wi-fi router, some has a bad LTE signal on the home area or when they have a LTE/Wi-fi connection they're not plugged in, etc.).

Note: To download the SGEE update a collar should be plugged in and simultaneously connected to LTE/ Wi-Fi.

But at the moment of calling no one can tell what is the reason of issue because neither customer nor the CSA can see the data regarding GPS update. SGEE is currently stored on daily diagnostics which is hidden from all the users except Michael, even tech support cannot see that data. Rather then bothering CSA each time customers face the issue with GPS accuracy it's better to give them option to see the SGEE data themselves or give them visibility of probable reasons of issues with a link to the article with recommendation on what to do without forcing customers to download the SGEE data.

# User story

\> As a Halo app owner I want to see the state of the GPS accuracy on Halo app and to fix the GPS issues by myself so that I will not have to call to support for reporting the GPS issue and requesting recommendations on how to fix that.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ Implementation status | Advanced settings page - exceptional flow (Collar doesn't support the SGEE feature) | Advanced settings page - outdated files (alternative flow) | Connection and communication errors |
|---|---|---|---|---|---|---|
| Advanced settings page - up-to-date data (normal flow) |
| ME03-US69-AC01 | Precondition: GloExp/GpsEXP date is more than Today date.A new section should be added to the "Advanced Settings" screen under 'Indoor/ Outdoor' settings:'Satellite position data' title; '\<number of days till SGEE file expiration\> days remaining' ( Last update: \<date\>)' , text (TBD), e.g. '7 days remaining (Last update: 01.01.2022)' .The number should be rounded upwardAnd the date format is MM.DD.YYYY | Pic 1See the screen in Zeplin | Pic 1See the screen in Zeplin |
| ME03-US69-AC02 | Where \<number of days till SGEE file expiration\> = \<GloExp/GpsEXP\> - \<Today date\>,where GloExp/GpsEXP are expiration date received from the collar on Daily Diagnostics, |  |  |
| ME03-US69-AC03 | where \<Today date\> is a local date of app user |  |  |
| ME03-US69-AC04 | Where \<date\> is a date of uploading of SGEE file that are currently used by collar |  |  |
| ME03-US69-AC05 | Precondition: the collar's FW doesn't support SGEE feature.If user opens "Advanced Settings" screen, then the system displays the following items:'Satellite position data' title;'For the greatest location accuracy, please upgrade the firmware of your collar. If your firmware status indicates ‘up-to-date’, please notify Customer Support.' text; | Zeplin Link | Zeplin Link |
| ME03-US69-AC05 | Precondition: GloExp/GpsEXP date is less than Today date. SGEE data on the collar is outdatedIf user opens "Advanced Settings" screen, then the system displays the following items:'Satellite position data' text +Warning icon( ) title; 'No satellite position data on collar. Make sure your collar has Wi-Fi or LTE connectivity while it is charging - and do not turn if off.', text | Zeplin Link | Zeplin Link |
| ME03-US69-AC06 | Connection and communication errors are handled according to ME14-US69 Unified errors handling | - | - |
|  |  |  |  |
|  |  |  |  |# Implementation notes

| IN | Description |
|---|---|
| ME03-US69-IN01 | Expiration date of SGEE file should be extracted from the Daily Diagnostics sent by the collar itself. |
|  |  |
