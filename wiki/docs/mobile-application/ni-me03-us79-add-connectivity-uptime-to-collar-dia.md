---
title: "(NI) ME03-US79. Add connectivity uptime to \"Collar Diagnostic\" screen"
sidebar_label: "(NI) ME03-US79. Add connectivity uptime to \"Collar Diagnostic\" screen"
sidebar_position: 226
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Maria Shikareva [X] |
| HALO-11876 - MOB+BE+FW: Add connectivity uptime to "Collar Diagnostic" screen Open |
| Click here to expand... |# Contents

Contents General description User story Acceptance criteria LTE section Wi-Fi section GPS section Compass section Processor section

# General description

This US contains improvements for the 'Collar Diagnostic' section in the app discussed during 2022-05-12 Meeting notes: Sprint 83 Demo and 2022-05-16 Meeting notes: BA call (Monday).

# User story

\> As a Halo app account owner I want to see more details about my Halo collar's hardware performance so that to better understand what's happening on the collar and what are the possible issues.

# Acceptance criteria

| AC | Description | iOS screen designs | Android screen designs |
|---|---|---|---|
| ME03-US85-AC01 | The app should display a new 'Connectivity Uptime' section with the following UI elements:Total Connection Time: 5h 18m from 24 hours (OnTime parameter, already in DD).Wi-Fi connected: 2h 00m/ better for userLTE connected: 3h 18mIt doesn't mean that the collar was connected all the time, the time can overlap??? it depends on FWShow this info in % - relation to OnTime value.WiFi connection time = WiFiOnTime/ OnTime *100%.Is it informative for the user? Maybe it's better display it in hours?Halo Server connected: 80%. Ideally this time should be equal to the sum of WiFi+LTE. Check with BE how easy for them it can be to calculate.TBD what if data for LTE/ WiFi and Azure differs? Do we need to highlight it somehow/ give a link to troubleshooting? Need to exclude time when the collar was powered off/ dead - we should not consider this as a problem. - it should be solved by using OnTime parameter.Reconnections amount - we can display this as an issue?:WiFi reconnects: 1LTE reconnects: 3Azure reconnects: 0Need to think what to display if the amount is too big/ send the user to troubleshooting flowTBD Do we need a new section OR we can somehow combine it with existing LTE/ WiFi?Maybe we should not show this section if no data was received for the latest 24 hours? |  |  |
| ME03-US85-AC02 |  |  |  |
|  | Wi-Fi sectionWi-Fi reconnects (how many connections was done) - counters for Wi-Fi reconnectsConnection time |  |  |
|  | Would also be good if they could “start logging” and go recreate the problem they are having. |  |  |
|  |  |  |  |
|  | Add more useful details about WiFi router, type of manufacturer, whether it's roaming or not, etc. - less priority. |  |  |
|  |  |  |  |
| ME03-US83-AC06 | 'LTE' section:LTE icon;'LTE' title;check icon (see ME03-US83-AC07 below);instructions (if applicable);'Wi-Fi' section:Wi-Fi icon;'Wi-Fi' title;check icon (see ME03-US83-AC07 below);instructions (if applicable);'GPS' section:GPS icon;'GPS' title;check icon (see ME03-US83-AC07 below);instructions (if applicable);'Compass' section:Compass icon;'Compass' title;check icon (see ME03-US83-AC07 below);instructions (if applicable);'Battery' sectionBattery icon;'Battery' title;check icon (see ME03-US83-AC07 below);instructions (if applicable); | Link to Zeplin | The same as for iOS. |
|  |  |  |  |
| ME03-US83-AC38 | If the collar sent Daily Diagnostic without fields required to define an issue (i.e. it's impossible to say whether the collar has an issue or not), the app should hide the section at all. | - | - |
| LTE section |
| ME03-US83-AC12 | The app should indicate that there's an issue with LTE module when:LTE_Init_Fails \> 0 ANDLTE_FW = 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row.Note: if LTE is off/ not connected, this should not affect DailyDiagnostics data, i.e. the collar sends it anyway. | - | - |
| ME03-US83-AC13 | Precondition: there's an issue with LTE module.The app should display the following text: 'LTE module is not working properly and the collar needs to be replaced. Tap here to review our warranty and Protection Plans'. | - | - |
| ME03-US83-AC14 | 'Tap here' should be a link to the Zendesk article on how the user can initiate collar replacement.The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/5575769230103. | - | - |
| Wi-Fi section |
| ME03-US83-AC15 | The app should indicate that there's an issue with Wi-Fi module when:RSI_Init_Fails \> 10ANDWIFI_FW_Version": nullANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row. | - | - |
| ME03-US83-AC16 | Precondition: there's an issue with Wi-Fi module.The app should display the following text: 'Wi-Fi module is not working properly and the collar needs to be replaced. Tap here to review our warranty and Protection Plans'. | - | - |
| ME03-US83-AC17 | 'Tap here' should be a link to the Zendesk article on how the user can initiate collar replacement.The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/5575769230103. | - | - |
| GPS section |
| ME03-US83-AC18 | The app should indicate that there's an issue with GPS module when:GPS_fail \> 0 ANDGPS_msg_cnt = 0ANDOnTime is not 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row. | - | - |
| ME03-US83-AC19 | Precondition: there's an issue with GPS module.The app should display the following text: 'GPS module is not working properly. Tap here to learn how to fix this issue.' | - | - |
| ME03-US83-AC20 | 'Tap here' should be a link to the Zendesk article on how the user can reprogram collar GPS chip.The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/5455274593431. | - | - |
| Compass section |
| ME03-US83-AC22 | The app should indicate that there's an issue with compass when:CollarTelemetry.CompassBadCnt =\> 35ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row. | - | - |
| ME03-US83-AC23 | Precondition: there's an issue with compass.The app should display the following text: 'Compass is not working properly. Please perform compass calibration from Advanced Settings.Note: we need to have an ability to redirect the user to the 'Advanced Settings' screen but it'll be implemented within a separate story as it requires additional efforts (see [Not implemented] ME03-US81. UX improvements for "Collar Diagnostic" screen). | - | - |
| Processor section |
| ME03-US83-AC28 | The app should indicate that there's at least 1 issue:Counters.HF_Resets = 255ORCounters.SW_Resets = 255ORCounters.WDG_Resets = 10Notes: we can start with max value for the counter (255) and later define the max applicable number of such resets;it's enough to have such values in 1 DailyDiagnostics (not 3 DD in a row). | - | - |
| ME03-US83-AC29 | Precondition: there's an issue with processor.The app should display the following text: 'An issue is detected with the collar's processor. Tap here to review our warranty and Protection Plans.' | - | - |
| ME03-US83-AC30 | 'Tap here' should be a link to the Zendesk article on how the user can initiate collar replacement.The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/5575769230103. | - | - |
