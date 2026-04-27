---
title: "ME03-F06-US02. Collar Diagnostic updates after Automatic Warranty release"
sidebar_label: "ME03-F06-US02. Collar Diagnostic updates after Automatic Warranty release"
sidebar_position: 626
last_modified: "Feb 20, 2025"
author: "Mariya Kolyada"
---

| Document owners | Linear/Jira ticket | History of changes |
|---|---|---|
| Mariya Kolyada |
| iOS: https://linear.app/fueled/issue/HALO-341/[ios]-collar-diagnostic-updates-after-automatate-warranty-releaseAndroid: https://linear.app/fueled/issue/HALO-342/[android]-collar-diagnostic-updates-after-automatate-warranty-releaseBE: TBD |
| 11 Feb 2025 draft user story is created by Mariya Kolyada 20 Feb 2025 updated requirements by adding more cases proposed by Ryan and added the final version of the designs. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to initiate collar Warranty Replacement if my collar has catastrophic issues without leaving the app and login to ecom website so I can start teh process as quickly as possible. As Halo app account owner, I want to view Reported issues in addition to Detected by the collar on Collar Diagnostic so I make sure that Halo reported it.

# Acceptance criteria

All screen designs: Figma

Full-screen view example:

| AC | Description | New catastrophic issue | Condition | As is | To be | Condition | As is | To be | Condition | As is | To be | Condition | As is | To be | Replacement banner | Collas is on Warranty | Warranty Replacement has already been requested | As is | To be |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AC01 | Display the new catastrophic issue for the Hardware Parameter Collar Diagnostic:Appendix 14 - List of catastrophic and non-catastrophic issues (see collar issue type = 18) |
| AC02 | Update the 'Detailed Last scan status' at the top of the Collar Diagnostic screen:ConditionAs isTo beCollar Diagnostic has only issue(s) detected by the collar (all issue types except 18)FigmaCollar Diagnostic has only reported issue (issue type 18)Not supportedFigmaCollar Diagnostic has both reported issues and issue(s) detected by the collar Not supportedFigma | Collar Diagnostic has only issue(s) detected by the collar (all issue types except 18) | Figma | Collar Diagnostic has only reported issue (issue type 18) | Not supported | Figma | Collar Diagnostic has both reported issues and issue(s) detected by the collar | Not supported | Figma |
| Collar Diagnostic has only issue(s) detected by the collar (all issue types except 18) | Figma |
| Collar Diagnostic has only reported issue (issue type 18) | Not supported | Figma |
| Collar Diagnostic has both reported issues and issue(s) detected by the collar | Not supported | Figma |
| AC03 | Update the 'Diagnostic Status with a number of issues' on the Collar Diagnostic screen: ConditionAs isTo beCollar Diagnostic has only issue(s) detected by the collar (all issue types except 18)FigmaCollar Diagnostic has only reported issue (issue type 18)Not supportedFigmaCollar Diagnostic has both reported issues and issue(s) detected by the collar Not supportedFigma | Collar Diagnostic has only issue(s) detected by the collar (all issue types except 18) | Figma | Collar Diagnostic has only reported issue (issue type 18) | Not supported | Figma | Collar Diagnostic has both reported issues and issue(s) detected by the collar | Not supported | Figma |
| Collar Diagnostic has only issue(s) detected by the collar (all issue types except 18) | Figma |
| Collar Diagnostic has only reported issue (issue type 18) | Not supported | Figma |
| Collar Diagnostic has both reported issues and issue(s) detected by the collar | Not supported | Figma |
| AC04 | Update the 'Hardware section' on the Collar Diagnostic screen: ConditionAs isTo beCollar Diagnostic has only issue(s) detected by the collar (all issue types except 18)FigmaCollar Diagnostic has only reported issue (issue type 18)Not supportedFigmaCollar Diagnostic has both reported issues and issue(s) detected by the collar Not supportedFigma | Collar Diagnostic has only issue(s) detected by the collar (all issue types except 18) | Figma | Collar Diagnostic has only reported issue (issue type 18) | Not supported | Figma | Collar Diagnostic has both reported issues and issue(s) detected by the collar | Not supported | Figma |
| Collar Diagnostic has only issue(s) detected by the collar (all issue types except 18) | Figma |
| Collar Diagnostic has only reported issue (issue type 18) | Not supported | Figma |
| Collar Diagnostic has both reported issues and issue(s) detected by the collar | Not supported | Figma |
| AC05 | The app should open the following pop-ups by tapping on the 'Hardware section':ConditionAs isTo beCollar Diagnostic has only issue(s) detected by the collar (all issue types except 18)FigmaCollar Diagnostic has only reported issue (issue type 18)Not supportedFigmaCollar Diagnostic has both reported issues and issue(s) detected by the collar Not supportedSame as the pop-up with only reported issue, but both issue types should be listed at the bottom of the pop-up:HW - 18 - Customer Reported IssueHW - 15 - Processor Corruption | Collar Diagnostic has only issue(s) detected by the collar (all issue types except 18) | Figma | Collar Diagnostic has only reported issue (issue type 18) | Not supported | Figma | Collar Diagnostic has both reported issues and issue(s) detected by the collar | Not supported | Same as the pop-up with only reported issue, but both issue types should be listed at the bottom of the pop-up:HW - 18 - Customer Reported IssueHW - 15 - Processor Corruption |
| Collar Diagnostic has only issue(s) detected by the collar (all issue types except 18) | Figma |
| Collar Diagnostic has only reported issue (issue type 18) | Not supported | Figma |
| Collar Diagnostic has both reported issues and issue(s) detected by the collar | Not supported | Same as the pop-up with only reported issue, but both issue types should be listed at the bottom of the pop-up:HW - 18 - Customer Reported IssueHW - 15 - Processor Corruption |
| AC06 | Update the 'Replacement banner' on the Collar Diagnostic screen: Collas is on WarrantyWarranty Replacement has already been requestedAs isTo beNo-FigmaFigmaYesNoNot supportedFigmaYesYesNot supportedFigma | No | - | Figma | Figma | Yes | No | Not supported | Figma | Yes | Yes | Not supported | Figma |
| No | - | Figma | Figma |
| Yes | No | Not supported | Figma |
| Yes | Yes | Not supported | Figma |
| AC07 | If user taps one of the following banners:Collar is out of warranty,Warranty in Process,then the app should open the 'Dog Park Areas' screen.'Dog Park Areas' will be implemented later HALO-247, the placeholder screen should be shown for now. |
| AC08 | If user taps the banner when the Collar is on Warranty & Has not been requested yet, then the app should open the link generated by the BE via webview in the app.NoteThis link will open the screen with fields to enter the shipping address where the user will be already logged in to an account on ecom website. |
