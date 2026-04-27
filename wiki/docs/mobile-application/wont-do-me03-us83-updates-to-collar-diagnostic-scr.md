---
title: "(Won't do) ME03-US83. Updates to \"Collar Diagnostic\" screen (feedback after Sprint 83 Demo)"
sidebar_label: "(Won't do) ME03-US83. Updates to \"Collar Diagnostic\" screen (feedback after Sprint 83 Demo)"
sidebar_position: 224
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED Was fully covered in the scope of other stories - see references on the AC |
| Maria Shikareva [X] Timofey Burak [X] Dmitriy Morozov [X] Katherina Kaplina Alexei Zhukov |
| HALO-11813 - MOB+BE: Updates for "Collar Diagnostic" screen (feedback after Demo: texts, Solvvy links, minor UI updates) Closed |
| Click here to expand... |# Contents

General description User story Acceptance criteria 'Collar Diagnostic' screen: general improvements 'Battery' section improvements

# General description

This US contains improvements for the 'Collar Diagnostic' section in the app discussed during 2022-05-12 Meeting notes: Sprint 83 Demo and 2022-05-16 Meeting notes: BA call (Monday).

# User story

\> As a Halo app account owner I want to see more details about my Halo collar's hardware performance so that to better understand what's happening on the collar and what are the possible issues.

# Acceptance criteria

| AC | Description | iOS screen designs/ implementation status | Android screen designs/ implementation status | AS IS | TO BE | AS IS | TO BE | AS IS | TO BE | AS IS | TO BE | AS IS | TO BE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 'Collar Diagnostic' screen: general improvements |
| ME03-US83-AC01 was done in scope of ME03-US101-AC09 (point 7) | 'Last scan' format should be changed:AS ISTO BE\<time\> is displayed in the format: HH:MM AM/PM \<date\> is displayed in the format: MM/DD/YYYY.The system should display "\<time\> ago" using BR-16 Passed time format.QA note: ME03-US71-AC06 is changed. | \<time\> is displayed in the format: HH:MM AM/PM \<date\> is displayed in the format: MM/DD/YYYY. | The system should display "\<time\> ago" using BR-16 Passed time format. | Pic ME03-US83-P01 "Collar Diagnostic" screenLink to Zeplin | The same as for iOS.Link to Zeplin |
| \<time\> is displayed in the format: HH:MM AM/PM \<date\> is displayed in the format: MM/DD/YYYY. | The system should display "\<time\> ago" using BR-16 Passed time format. |
| ME03-US83-AC02 was done in scope of ME03-US101-AC09 (point 4) | The app should not display "(reports every 24 hours)" text in any case.BA note: it was decided to remove it as it can be confusing for the user if the collar reported last time more than 24 hours ago. We'll highlight it in the text above (see ME03-US83-AC05 below). | - | - |
| ME03-US83-AC03 was done in scope of ME03-US101-AC09 (point 1) | The name of the 'Processor' section should be changed:AS ISTO BEProcessorOtherBA note: we need this change as this section can include issues with not processor, but with audio chip, motion sensor, etc. | Processor | Other | - | The same as for iOS.Link to Zeplin. |
| Processor | Other |
| ME03-US83-AC04 was changed and done in scope of Catastrophic and non-catastrophic issues of the collar | Precondition: there's an issue with OtherThe app should display an updated text for the issue:AS ISTO BEAn issue is detected with the collar's processor. Tap here to review our warranty and Protection Plans.An issue is detected with some collar's hardware components. Tap here to review our warranty and Protection Plans.Note: 'tap here' should remain a link as described in ME03-US71-AC30. | An issue is detected with the collar's processor. Tap here to review our warranty and Protection Plans. | An issue is detected with some collar's hardware components. Tap here to review our warranty and Protection Plans. | - | - |
| An issue is detected with the collar's processor. Tap here to review our warranty and Protection Plans. | An issue is detected with some collar's hardware components. Tap here to review our warranty and Protection Plans. |
| ME03-US83-AC05 was changed and done in scope of ME03-US101-AC09 (point 6) | Precondition: no issues detected.If the user opens the 'Collar Diagnostic' screen, the app should display changed text for the header:AS ISTO BEBelow are the latest self-diagnostics reported daily by your Halo collar \<Collar serial number\>.Below are the latest self-diagnostics reported daily by your Halo collar \<Collar serial number\> via LTE or Wi-Fi.No diagnostic issues have been detected. If you're still having issues, please make sure you have the latest Halo app and your collar firmware is up-to-date. For additional troubleshooting please use Halo Help.BA note: we need this change to help the user if the issue is not with HW. E.g. LTE is not working, a user will see that LTE module is working properly, so they will be able to go through the troubleshooting flow and try to find another reason. | Below are the latest self-diagnostics reported daily by your Halo collar \<Collar serial number\>. | Below are the latest self-diagnostics reported daily by your Halo collar \<Collar serial number\> via LTE or Wi-Fi.No diagnostic issues have been detected. If you're still having issues, please make sure you have the latest Halo app and your collar firmware is up-to-date. For additional troubleshooting please use Halo Help. | - | - |
| Below are the latest self-diagnostics reported daily by your Halo collar \<Collar serial number\>. | Below are the latest self-diagnostics reported daily by your Halo collar \<Collar serial number\> via LTE or Wi-Fi.No diagnostic issues have been detected. If you're still having issues, please make sure you have the latest Halo app and your collar firmware is up-to-date. For additional troubleshooting please use Halo Help. |
| ME03-US83-AC06 was done in scope of ME03-US101-AC09 (point 6) | \<Collar serial number\> should be highlighted in bold. | - | - |
| ME03-US83-AC07 was done in scope of ME03-US101-AC09 (point 6) | Halo app should be a link to the new version of the mobile application in AppStore/ Play Market. | - | - |
| ME03-US83-AC08 was done in scope of ME03-US121-AC14 | Precondition: the collar didn't send DailyDiagnostics for more than 30 days.If the user opens the 'Collar Diagnostic' screen, the app should display changed text for the last scan issue:AS ISTO BENo recent health data reported. Check collar connectivity.No recent health data reported. Please, check your Halo's connectivity: use Halo Help to troubleshoot. | No recent health data reported. Check collar connectivity. | No recent health data reported. Please, check your Halo's connectivity: use Halo Help to troubleshoot. | Pic ME03-US83-P02 "Collar Diagnostic" screen with no recent dataLink to Zeplin | Link to Zeplin |
| No recent health data reported. Check collar connectivity. | No recent health data reported. Please, check your Halo's connectivity: use Halo Help to troubleshoot. |
| ME03-US83-AC09was done in scope of ME03-US121-AC15 | 'Halo Help' should be a tappable link.Link: https://cdn.solvvy.com/deflect/customization/halocollar/support.html?solvvyWF=1cb4c86a-7bd9-4c95-a498-5a63b84b7297When a user taps on it, the app should initiate 'Halo Help' opening with predefined question typed: Troubleshooting → Troubleshooting Guide. |  | - |
| 'Battery' section improvements |
| ME03-US83-AC10 was done in scope of ME03-US101-AC09 (point 5) | If the collar reports "battery_life" ≤ 0, then the app should not display the "Last reported battery life" section.BA note: we can face such situation when the collar reports DD for the first time and doesn't have this information yet (so to avoid displaying "0 hours"). | - | - |
