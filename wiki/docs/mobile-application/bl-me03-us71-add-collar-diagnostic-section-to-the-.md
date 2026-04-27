---
title: "(BL) ME03-US71. Add \"Collar Diagnostic\" section to the \"Collars list\""
sidebar_label: "(BL) ME03-US71. Add \"Collar Diagnostic\" section to the \"Collars list\""
sidebar_position: 205
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Alexei Zhukov Nikita Krisko Yuri Zhdanovich [X] Katherina Kaplina |
| HALO-10741 - [RI] BE+MOB: Add "Collar Diagnostic" section to the "Collars list" Closed Ballpark (for displaying only issues detected):MOB: 5SPBE: 5SPQA: 5SP |
| Click here to expand...20 Apr 2022 Maria Shikareva [X] Added links to Zendesk articles provided in "Halo | Articles for 'Collar Diagnostic'" email, Apr 18, 2022).21 Apr 2022 Maria Shikareva [X] Added ME03-US71-AC38 to handle cases if for some reason DD doesn't have data required for this feature.22 Apr 2022 Maria Shikareva [X] Updated several ACs due to moving them to a separate story as they require additional efforts and discussions):added a note to ME03-US71-AC23;crossed out 'Report the issue' button section and related ACs;updated texts for ME03-US71-AC25.22 Apr 2022 Maria Shikareva [X] Crossed out ME03-US71-AC21 as agreed on the 4/22/22 Tech call.26 Apr 2022 Maria Shikareva [X] Added ME03-US71-AC39, ME03-US71-AC40 (discussed with Timofey Burak [X] and Dmitriy Morozov [X]): it's better to add all numeric parameters to config.29 Apr 2022 Maria Shikareva [X] Corrected a design.04 May 2022 Maria Shikareva [X]Corrected a misprint in ME03-US71-AC06.Added a note to ME03-US71-AC24 for better consistency with ME03-US71-AC28.Rephrased ME03-US71-AC03 for more clarity.Corrected ME03-US71-AC11 (highlighted in blue): the data is outdated so it's OK to hide them as they have no value for the user.30 May 2022 Maria Shikareva [X] Marked the story as baselined (see ME03-F01. Collars list, ME03-F07. Collar Diagnostic, ME02-F00. View "Settings" screen). |# Contents

Contents General description User story Acceptance criteria 'My Collars' screen 'Collar Diagnostic' screen 'Last scan' section LTE section Wi-Fi section GPS section Compass section Battery section Processor section 'Report the issue' button Additional alerts 'Blue dot' on the 'Settings' tab and on "My Collars" option Alert on the 'My Collars' list

# General description

See the description in RI11. Collar Diagnostic in the Halo app.

# User story

\> As a Halo app account owner I want to be notified if my collar doesn't work and see tailored instructions to make improvements so that to observe results and know how to deal with that.

# Acceptance criteria

| AC | Description | iOS screen designs/ implementation status | Android screen designs/ implementation status | Icon | Value | Description |
|---|---|---|---|---|---|---|
| 'My Collars' screen |
| ME03-US71-AC01 | A new section "Collar Diagnostic" should be added to the "My Collars" screen under "Cellular" section. | - | - |
| ME03-US71-AC02 | Preconditions: the collar supports 'Collar Diagnostic" feature (i.e. the collar sends DailyDiagnostics)ANDthere's at least 1 sent DailyDiagnosticsANDall parameters are checked and correct (see ME03-US71-AC05 below).A new section "Collar Diagnostic" should have the following elements:'Collar Diagnostic' title;'No issues detected' status with the corresponding icon;right arrow icon. | Pic ME03-US71-P01 "Collar Diagnostic" section, no issues detectedLink to Zeplin | Zeplin |
| ME03-US71-AC03 | Preconditions: the collar supports 'Collar Diagnostic" feature (i.e. the collar sends DailyDiagnostics)ANDthere's at least 1 sent DailyDiagnosticsANDall parameters are checked and at least one group of conditions for any section isn't met (see ME03-US71-AC07 below)OR when the collar didn't report DailyDiagnostics for a month (see ME03-US71-AC08 below).A new section "Collar Diagnostic" should have the following elements:'Collar Diagnostic' title;'Issues detected' status with the corresponding icon;right arrow icon. | Pic ME03-US71-P02 "Collar Diagnostic" section, issues detectedLink to Zeplin | The same as for iOS.Zeplin |
| ME03-US71-AC04 | Preconditions: the collar supports 'Collar Diagnostic" feature (i.e. the collar sends DailyDiagnostics)ANDthere's no DailyDiagnostics data.A new section "Collar Diagnostic" should have the following elements:'Collar Diagnostic' title;'No data reported yet' status with the corresponding icon. | Pic ME03-US71-P03 "Collar Diagnostic" section, no dataLink to Zeplin | The same as for iOS. |
| ME03-US71-AC05 | Precondition: the collar doesn't support "Collar Diagnostic" feature (i.e. the collar doesn't send DailyDiagnostics).A new section "Collar Diagnostic" should have the following elements:'Collar Diagnostic' title;'Collar Diagnostic is not supported. Please upgrade your collar.' text. |  | The same as for iOS. |
| 'Collar Diagnostic' screen |
| ME03-US71-AC06 | When the user taps on the "Collar Diagnostic" section, then the app should open the "Collar Diagnostic" screen with the following UI elements:'Collar Diagnostic' title;'Back' icon;'Below are the latest self-diagnostics reported daily by your Halo collar \<Collar serial number\>.' text;'Last scan: \<time\> \<date\>' (reports every 24 hours), where:\<time\> is displayed in the format: HH:MM AM/PM \<date\> is displayed in the format: MM/DD/YYYY.'LTE' section:LTE icon;'LTE' title;check icon (see ME03-US71-AC07 below);instructions (if applicable);'Wi-Fi' section:Wi-Fi icon;'Wi-Fi' title;check icon (see ME03-US71-AC07 below);instructions (if applicable);'GPS' section:GPS icon;'GPS' title;check icon (see ME03-US71-AC07 below);instructions (if applicable);'Compass' section:Compass icon;'Compass' title;check icon (see ME03-US71-AC07 below);instructions (if applicable);'Battery' sectionBattery icon;'Battery' title;check icon (see ME03-US71-AC07 below);instructions (if applicable);'Processor' section:Processor icon;'Processor' title;check icon (see ME03-US71-AC07 below);instructions (if applicable). | Link to Zeplin | The same as for iOS. |
| ME03-US71-AC07 | Possible values for the check icon:IconValueDescription Checked - correctcollar sent DailyDiagnostics ANDa parameter was normalChecked - issuescollar sent DailyDiagnosticsANDthere was an issue |  | Checked - correct | collar sent DailyDiagnostics ANDa parameter was normal |  | Checked - issues | collar sent DailyDiagnosticsANDthere was an issue | - | - |
|  | Checked - correct | collar sent DailyDiagnostics ANDa parameter was normal |
|  | Checked - issues | collar sent DailyDiagnosticsANDthere was an issue |
| ME03-US71-AC08 | The system should analyze data from DailyDiagnostics using the specific criteria described below and save the results.Note: as of 15 Mar 2022 a collar reports DailyDiagnostics once a day and BE saves the data without analyzing.Note: the mobile app should get this data from BE (not from the collar itself). | - | - |
| ME03-US71-AC09 | If the user taps "Back" icon, then the mobile app should open "My Collars" list with the selected collar expanded. | - | - |
| ME03-US71-AC10 | All content should be scrollable except the header with 'Collar Diagnostic' title and 'Back' icon. | - | - |
| ME03-US71-AC38 | Requirement not supported after implementation of (BL) ME03-US101 BE+MOB: Catastrophic issues: calculation and displaying of the issue in appIf the collar sent Daily Diagnostic without fields required to define an issue (i.e. it's impossible to say whether the collar has an issue or not), the app should hide the section at all.Example18 Apr 2022 - DD was sent entirely; LTE issue exists19 Apr 2022 - DD was sent entirely; LTE issue exists20 Apr 2022 - DD was sent w/o info about LTE OR LTE values were sent partially (LTE_Init_Fails or LTE_FW)As a result: LTE section should be hidden on the app.21 Apr 2022 - DD was sent entirely again; the app should display a section with no issue (even if there's any because it wasn't sent for 3 days in a row). | - | - |
| ME03-US71-AC39 | \<24\> hours should be a configurable value. | - | - |
| 'Last scan' section |
| ME03-US71-AC11 | If the collar hasn't sent DailyDiagnostics for more than 30 days, then the app should additionally: highlight 'last scan' title with red color;display 'No recent health data reported. Check collar connectivity.' text with a warning icon;not display '(reports every 24 hours)' text;not display the list with sections.grey out the list with sections. | Pic ME03-US71-P04 "Collar Diagnostic" screen - no recent dataLink to Zeplin | Zeplin |
| ME03-US71-AC40 | \<30\> days should be a configurable value. | - | - |
| LTE section |
| ME03-US71-AC12 | The app should indicate that there's an issue with LTE module when:LTE_Init_Fails \> 0 ANDLTE_FW = 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row.Note: if LTE is off/ not connected, this should not affect DailyDiagnostics data, i.e. the collar sends it anyway. | - | - |
| ME03-US71-AC13 | Precondition: there's an issue with LTE module.The app should display the following text: 'LTE module is not working properly and the collar needs to be replaced. Tap here to review our warranty and Protection Plans'. | - | - |
| ME03-US71-AC14 | 'Tap here' should be a link to the Zendesk article on how the user can initiate collar replacement.The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/5575769230103. | - | - |
| Wi-Fi section |
| ME03-US71-AC15 | The app should indicate that there's an issue with Wi-Fi module when:RSI_Init_Fails \> 10ANDWIFI_FW_Version": nullANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row. | - | - |
| ME03-US71-AC16 | Precondition: there's an issue with Wi-Fi module.The app should display the following text: 'Wi-Fi module is not working properly and the collar needs to be replaced. Tap here to review our warranty and Protection Plans'. | - | - |
| ME03-US71-AC17 | 'Tap here' should be a link to the Zendesk article on how the user can initiate collar replacement.The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/5575769230103. | - | - |
| GPS section |
| ME03-US71-AC18 | The app should indicate that there's an issue with GPS module when:GPS_fail \> 0 ANDGPS_msg_cnt = 0ANDOnTime is not 0 ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row. | - | - |
| ME03-US71-AC19 | Precondition: there's an issue with GPS module.The app should display the following text: 'GPS module is not working properly. Tap here to learn how to fix this issue.' | - | - |
| ME03-US71-AC20 | 'Tap here' should be a link to the Zendesk article on how the user can reprogram collar GPS chip.The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/5455274593431. | - | - |
| ME03-US71-AC21 | The app should also indicate if GPS calibration required (the same triggers as used for NT34 GPS calibration required (assigned collar)): GPS Calibration Required. Please bring Halo outdoors until the GPS led blinks BLUE. | - | - |
| Compass section |
| ME03-US71-AC22 | The app should indicate that there's an issue with compass when:CollarTelemetry.CompassBadCnt =\> 35ANDthe collar reports abovementioned parameters in 3 DailyDiagnostics in a row. | - | - |
| ME03-US71-AC23 | Precondition: there's an issue with compass.The app should display the following text: 'Compass is not working properly. Please perform compass calibration from Advanced Settings.Note: we need to have an ability to redirect the user to the 'Advanced Settings' screen but it'll be implemented within a separate story as it requires additional efforts (see [Not implemented] ME03-US81. UX improvements for "Collar Diagnostic" screen). | - | - |
| Battery section |
| ME03-US71-AC24 | The app should indicate that there's an issue with battery when:battery_health \<70%.Implementation note: we need the lower byte for battery_health=toint(MsgBody.battery_health) % 256.Example for reference: "battery_health":605 is equal to 93%.Note 1: it's enough to have such values in 1 DailyDiagnostics (not 3 DD in a row) because it cannot increase in further DD if received once.TBD for developers: Double check formula with Michael | - | - |
| ME03-US71-AC25 | Precondition: there's an issue with battery.The app should display the following text: 'Your battery's maximum capacity has fallen below 70%. Contact support about replacing the battery.' | - | - |
| ME03-US71-AC26 | 'Report the issue' should be a clickable link. | - | - |
| ME03-US71-AC27 | 'Last reported battery life' should contain the value from DailyDiagnostics: "battery_life" using the following rounding rules:if the battery life is \>1 hour, it should be shown in "H h MM m" format;if the battery life is \<1 hour, it should be shown in "MM m" format.Note: 'battery_life' field should always be in DD (i.e. there are no cases when the collar sends DD, but 'battery_life' field doesn't exist in it). | - | - |
| Processor section |
| ME03-US71-AC28 | The app should indicate that there's at least 1 issue:Counters.HF_Resets = 255ORCounters.SW_Resets = 255ORCounters.WDG_Resets = 10Notes: we can start with max value for the counter (255) and later define the max applicable number of such resets;it's enough to have such values in 1 DailyDiagnostics (not 3 DD in a row). | - | - |
| ME03-US71-AC29 | Precondition: there's an issue with processor.The app should display the following text: 'An issue is detected with the collar's processor. Tap here to review our warranty and Protection Plans.' | - | - |
| ME03-US71-AC30 | 'Tap here' should be a link to the Zendesk article on how the user can initiate collar replacement.The link should be opened in the mobile browser.Link: https://support.halocollar.com/hc/en-us/articles/5575769230103. | - | - |
| 'Report the issue' button |
| ME03-US71-AC31 | When the user taps on "Report the issue" link, then the app should open the default email sender with the draft "Issue with \<issue\>" email. | - | - |
| ME03-US71-AC32 | The "Issue with \<issue\>" email should consist of: Subject: [HALO-APP] Collar Diagnostic: Battery issue OR [HALO-APP] Collar Diagnostic: Processor issueEmail recipient: support@halocollar.zendesk.comEmail body: Attachment: file with the mobile logsNote 1 : the sender's email can differ from the email that is used in Halo account.Note 2: email body should be empty. | - | - |
| ME03-US71-AC33 | When the user sends an email, the app should open "Collar Diagnostic" screen. | - | - |
| Note: Softeq doesn't control the following behavior, but it's assumed to be performed: In case support@halocollar.zendesk.com is chosen as the email recipient, then after the email sending Zendesk request should be created and CSAs should be able to view it in https://halocollar.zendesk.com/agent/dashboard. |
| Additional alerts |
| 'Blue dot' on the 'Settings' tab and on "My Collars" option |
| ME03-US71-AC34 | When any parameter has an error (i.e. 'Issues found' label is displayed), then a 'Blue dot' indicator should be displayed:on the 'Settings' tab;next to "My Collars" section. | Pic ME03-US71-P05 "Settings" screen with blue dotsLink to Zeplin | The same as for iOS. |
| ME03-US71-AC35 | Precondition: 'Blue dot' indicator is displayed on the 'Settings' tab/ next to "My Collars' option.A 'Blue dot' indicator should disappear from both places when: a new DailyDiagnostics is sent ANDno issues are detected.QA Note: the blue dot should stay in place for another notifications (if applicable). | - | - |
| Alert on the 'My Collars' list |
| ME03-US71-AC36 | Precondition: the app displays "Issues detected" status.The app should also display an alert icon next to the collar icon in the collars list both in the expanded and minimized views. | See Pic ME03-US71-P02 "Collar Diagnostic" section, issues detected above | The same as for iOS. |
| ME03-US71-AC37 | The alert should disappear from both places when: a new DailyDiagnostics is sent ANDno issues are detected. | - | - |
