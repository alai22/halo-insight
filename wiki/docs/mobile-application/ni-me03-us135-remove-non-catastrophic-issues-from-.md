---
title: "(NI) ME03-US135. Remove non-catastrophic issues from Collar Diagnostic and Braze events"
sidebar_label: "(NI) ME03-US135. Remove non-catastrophic issues from Collar Diagnostic and Braze events"
sidebar_position: 413
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages | Change history |
|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau Mariya Kolyada |
| HALO-20276 - BE: ME03-US135. Remove non-catastrophic issues from Collar Diagnostic and Braze events Closed |
| The affected requirements:Appendix 14 - List of catastrophic and non-catastrophic issues |
| As of 15 May 2024 Kiryl Trafimau created draft.As of 24 Oct 2024 Mariya Kolyada updated the user story by adding the data what text should be deleted in teh app and how it is covered in the Weekly Health Check Report. |Acceptance Criteria Implementation note

\> As a Halo app account owner I want to stop viewing any non-catastrophic mentions on the Collar Diagnostic screen and recieve any emails triggered by Braze so that to observe results and know how to deal with that.

# Acceptance Criteria

| ID | Acceptance criteria | Screens |
|---|---|---|
| ME03-US135-AC01 | Precondition:Any non-catastrophic issue happens.If I open the Collar Diagnostic screen, then the app should:NOT display anything related to this issue on Collar Diagnostic screen:No orange '!' icon.No messages in sections related to part of system where the issue happened (see Implementation Notes bellow) |  |
| ME03-US135-AC02 | Precondition:Any non-catastrophic issue happens.The app should NOT trigger any non-catastrophic event sending to Braze (see https://docs.google.com/document/d/1n-HYaKaMsnhYX2yJ15Kx8-FEuzaO1ttKJLZaYG5WAN4/edit#heading=h.aezls5t9tzox) | - |
| ME03-US135-AC03 | Remove the non-catastrophic issues from the list of triggers for the orange triangle '!' icon on the Collars list screen → Collar's image. |  |For BA:

1. Remove mentioned issues fromAppendix 14 - List of catastrophic and non-catastrophic issues
2. Some AC on[ME03-F07. Collar Diagnostic](ME03-F07.-Collar-Diagnostic_156686937.mdx)should be updated (there are notes).

# Implementation note

|  | Section name---------------Error name | Error validations (trigger) | Collar Diagnostic text to be removed | Where it is covered in the Weekly Health Check Report |  | GPS |  |  |  |  | Battery |  |  |  |  | Other |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GPS chip failure 2 | GPS_err == 3 && Halo 1 or 2for 1 DailyDiagnostic | "GPS chip needs update. Tap here to learn how to fix this issue."Tap here = https://support.halocollar.com/hc/en-us/articles/13972076790807 | Issue_Group_3:"Your Halo collar may not be reporting GPS data frequently. To improve accuracy, open the Halo Collar app (Settings \> My Collars \> Select [Dog’s name collar]) and check diagnostics for next steps. If no issues are found, contact our support team for further assistance." |
| 2 | GPS chip failure 3 | GPS_fail == 1 && Halo 2+for 1 DailyDiagnostic |
| 3 | Battery charging issue 1 | at least 1 of 3 days 0\<ChargeCurr\<100ANDother days in a 3-days range could be ChargeCurr == 0___________________________________Battery charge amperage range is from 0 to 500. | "An issue was detected with the battery. Tap here to review our warranty and Protection Plans or contact support for further instructions"Tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103contact support = Dog Park (https://halocollar.page.link/open-halo-app-dog-park) | Issue_Group_16:"We noticed [Dog's Name]'s collar is charging slower than usual. Use the Halo cable and a USB-C adapter for optimal speed. See our charging guide for details." |
| 4 | Battery Daily Diagnostics | The app should indicate that there's an issue with battery when:battery_health \<70% AND \> 0%Implementation note: we need the lower byte for battery_health=toint(MsgBody. battery_health) % 256.for 1 DailyDiagnostic | 'Your battery's maximum capacity has fallen below 70%. Contact support about replacing the battery.'Contact support = Dog Park (https://halocollar.page.link/open-halo-app-dog-park) | Issue_Group_15:"We noticed a potential issue with [Dog's Name]'s Halo collar battery. Open the Halo Collar app (Settings \> My Collars \> Select [Dog’s Name] collar) and check diagnostics for next steps. Contact our support team if nothing shows." |
| 5 | Processor Daily DiagnosticsThis indicates a lot of collar reboots, approximately 10 seconds each reboot. Cannot be fixed by user. | The app should indicate that there's at least 1 issue:Counters.HF_Resets = 255ORCounters.SW_Resets = 255ORCounters.WDG_Resets \>= 10for 1 DailyDiagnostic | Possible processor corruption. Tap here to review our warranty and Protection Plans or contact support for further instructions. Tap here = https://support.halocollar.com/hc/en-us/articles/5575769230103contact support = Dog Park (https://halocollar.page.link/open-halo-app-dog-park) | Issue_Group_13:"Your collar may need a firmware update. Open the Halo Collar app (Settings \> My Collars \> [Dog’s Name] collar \> Collar Update). If your collar is up-to-date, check for a potential hardware issue. Open the Halo Collar app (Settings \> My Collars \> Select [Dog’s Name] collar) and check diagnostics for next steps. If no issues are found, contact our support team for further assistance. Contact Support if issues persist." |
