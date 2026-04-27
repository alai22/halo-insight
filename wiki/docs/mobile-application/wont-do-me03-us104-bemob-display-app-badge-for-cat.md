---
title: "(Won't do) ME03-US104 BE+MOB?: Display app badge for catastrophic issues"
sidebar_label: "(Won't do) ME03-US104 BE+MOB?: Display app badge for catastrophic issues"
sidebar_position: 303
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Estimates | Related pages |
|---|---|---|---|---|---|
| POSTPONED |
| Maryia Paklonskaya [X] |
| HALO-15149 - MOB+BE: [NT] Investigation of the App Icon Badge for catastrophic issues Closed HALO-15182 - MOB+BE: ME08-US39. App notifications badge Closed Won't do because app badge will be implemented within content cards for displaying number of conteте cards. |
| create requirementsrefinementget final approval from the Halo LT create investigations BE, MOBinvestigated of the BE side of the app badge implementation 0.5spinvestigated of the MOB side of the app badge implementation 0.5spfinalised, ready for devadded final designsadd to the baseline |
| BE:QA: |
| https://portal.softeq.com/display/HALO/%5BNot+implemented%5D+ME08-US36.+App+icon+badge+for+iOS#[NI] ME08-US37. Notification dots/number badge on Android |# User Story

\> As a Halo user I want to see on the app the badge so that I know without opening the app that some issue happened

# Acceptance Criteria

| AC # | Acceptance Criteria Description |
|---|---|
| ME03-US104-AC01 | Assumption: the App Badge is enabled for the app in the devices settingsThe mobile app should display a native app icon badge if at least 1 catastrophic issue was detected on at least 1 collar of the user. |
| ME03-US104-AC02 | The app badge should display number of affected collars, e.g.:if 1 collar has 2 catastrophic issues - the digit 1 should be displayed on the app badgeif 2 collars have 1 catastrophic issues each - then the digit 2 should be displayed on the app badge |
| ME03-US104-AC03 | The badge should disappear in the following cases:no catastrophic issues were detected for any collar in the account |
| ME03-US104-AC04 | Precondition: badge is displayed on the app icon.If the user kills the app and then restore it, then the app should still display the badge. |
| ME03-US104-AC05 | User would be able to set whether to display app badge for the app or not. Thus:if user in the device settings set that app badge should not be visible either for Halo app or for the all apps on the device - the app badge should not be displayed even if catastrophic issues happened. once user turned ON the visibility of the app badge for the app - the badge should appear (if catastrophic issue happened). |
