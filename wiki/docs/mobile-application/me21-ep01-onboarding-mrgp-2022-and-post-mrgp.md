---
title: "ME21-EP01. Onboarding MRGP 2022 and post MRGP"
sidebar_label: "ME21-EP01. Onboarding MRGP 2022 and post MRGP"
sidebar_position: 716
last_modified: "Sep 13, 2024"
author: "Galina Lonskaya"
---

# Contents

VISION Business needs & goals User goals Risks SCOPE Functional scope Tech risks OTHER Analytics Beta-testing Miro board flow Epic with User stories Onboarding idea General use case Delivery plan of Onboarding MRGP

| VISION | Element | Business needs & goals |  | Business needs & goals | Situation AS IS | Review sample (user voice) | How we understand the goal is achieved | BA notes | 1 | 2 | 3 | User goals | Risks |  | Risk | Metrics to analyze (how we can confirm event risk happened) | 1 | 2 | 3 | 4 | SCOPE | Functional scope | Tech risks | OTHER | Analytics | Beta-testing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Description |
| Business needs & goalsSituation AS ISReview sample (user voice)How we understand the goal is achievedBA notes1Decrease support Users often request support during set up of the system (% from Maria Kolyada):FW is outdated and some features do not work properly (TBD numbers)TBD Maria should make sure all metrics cover described casesWe need to check Zendesk tags related to tickets above.Need to understand when the real onboarding is completed GPS calibration is not performed (TBD numbers)Collar setup itself (find via BLE, set-up Wi-Fi) Beacon setup issues with set up (cannot find)basic_support__beacons_set-up tag (via search)2Decrease number of returns Users return collars due to unclear flow of system setup (TBD numbers). See the following reasons for return:gps_accuracy/weaktechnical_support___gps_not_accurate_/_weak_gpstoo_complextechnical_support___corrections__indoorweak_cellular/lte_coverage indoor_correctionstechnical_support___connectivityindoor_/in_fence_feedbackwarranties__only___gps_accuracy/weak (TBD)technical_support___beacons_-_not_workingwarranties__only___connectivityWe can compare % of returns based on the reasons.BA note: we need to check how the reason of returns is displayed on UI.3Increase loyalty Users write negative feedbacks about difficulties of set up (TBD numbers)No reviews related to Users feel not confident that they setup everything right and no reviews related to Users do not rely the system because initial setup was not clear (TBD reviews)We need additional time to calculate current number of the feedbacks and future. Not sure that we will do it during MRGP.Users request printed guides/additional information in order to understand how to set up system properly No reviews related to Users request printed guides/additional information in order to understand how to set up system properly (TBD numbers) | Decrease support | Users often request support during set up of the system (% from Maria Kolyada):FW is outdated and some features do not work properly (TBD numbers) |  | TBD Maria should make sure all metrics cover described cases | We need to check Zendesk tags related to tickets above.Need to understand when the real onboarding is completed | GPS calibration is not performed (TBD numbers) |  |  | Collar setup itself (find via BLE, set-up Wi-Fi) |  |  | Beacon setup issues with set up (cannot find)basic_support__beacons_set-up tag (via search) |  |  | Decrease number of returns | Users return collars due to unclear flow of system setup (TBD numbers). See the following reasons for return:gps_accuracy/weaktechnical_support___gps_not_accurate_/_weak_gpstoo_complextechnical_support___corrections__indoorweak_cellular/lte_coverage indoor_correctionstechnical_support___connectivityindoor_/in_fence_feedbackwarranties__only___gps_accuracy/weak (TBD)technical_support___beacons_-_not_workingwarranties__only___connectivity |  | We can compare % of returns based on the reasons. | BA note: we need to check how the reason of returns is displayed on UI. | Increase loyalty | Users write negative feedbacks about difficulties of set up (TBD numbers) |  | No reviews related to Users feel not confident that they setup everything right and no reviews related to Users do not rely the system because initial setup was not clear (TBD reviews) | We need additional time to calculate current number of the feedbacks and future. Not sure that we will do it during MRGP. | Users request printed guides/additional information in order to understand how to set up system properly |  | No reviews related to Users request printed guides/additional information in order to understand how to set up system properly (TBD numbers) |
| Decrease support | Users often request support during set up of the system (% from Maria Kolyada):FW is outdated and some features do not work properly (TBD numbers) |  | TBD Maria should make sure all metrics cover described cases | We need to check Zendesk tags related to tickets above.Need to understand when the real onboarding is completed |
| GPS calibration is not performed (TBD numbers) |  |  |
| Collar setup itself (find via BLE, set-up Wi-Fi) |  |  |
| Beacon setup issues with set up (cannot find)basic_support__beacons_set-up tag (via search) |  |  |
| Decrease number of returns | Users return collars due to unclear flow of system setup (TBD numbers). See the following reasons for return:gps_accuracy/weaktechnical_support___gps_not_accurate_/_weak_gpstoo_complextechnical_support___corrections__indoorweak_cellular/lte_coverage indoor_correctionstechnical_support___connectivityindoor_/in_fence_feedbackwarranties__only___gps_accuracy/weak (TBD)technical_support___beacons_-_not_workingwarranties__only___connectivity |  | We can compare % of returns based on the reasons. | BA note: we need to check how the reason of returns is displayed on UI. |
| Increase loyalty | Users write negative feedbacks about difficulties of set up (TBD numbers) |  | No reviews related to Users feel not confident that they setup everything right and no reviews related to Users do not rely the system because initial setup was not clear (TBD reviews) | We need additional time to calculate current number of the feedbacks and future. Not sure that we will do it during MRGP. |
| Users request printed guides/additional information in order to understand how to set up system properly |  | No reviews related to Users request printed guides/additional information in order to understand how to set up system properly (TBD numbers) |
| User is sure that they do all required steps in order the system works properly.User controls product setup flow.User learns how product works in one place. |
| See possible risks and how it can be measured in the table below:RiskMetrics to analyze (how we can confirm event risk happened)1Onboarding is to difficult to understand/ to perform (e.g. very technical, not clear, etc.)Users write negative reviews about OnboardingUsers go to support and ask how to perform setup/ ask any question about Onboarding flowUsers taps on Question mark icon (there will be a special analytics event)2Onboarding process is too long/ separate steps are too long Users return product because of the long onboarding/ because they don't have time to go through the flow/ they want to have a product ready as soon as possibleUsers write negative reviews about Onboarding duration3Onboarding is not 'skippable' (a user doesn't want to go through onboarding in general or right now)Users go to support and ask how to skip onboarding Users write negative reviews 4Users do not want to watch Onboarding videos (it's not convenient for them/ they want paper tutorial/ etc).Users skip watching video (there will be a special analytics event)Users write negative reviews | Onboarding is to difficult to understand/ to perform (e.g. very technical, not clear, etc.) | Users write negative reviews about OnboardingUsers go to support and ask how to perform setup/ ask any question about Onboarding flowUsers taps on Question mark icon (there will be a special analytics event) | Onboarding process is too long/ separate steps are too long | Users return product because of the long onboarding/ because they don't have time to go through the flow/ they want to have a product ready as soon as possibleUsers write negative reviews about Onboarding duration | Onboarding is not 'skippable' (a user doesn't want to go through onboarding in general or right now) | Users go to support and ask how to skip onboarding Users write negative reviews | Users do not want to watch Onboarding videos (it's not convenient for them/ they want paper tutorial/ etc). | Users skip watching video (there will be a special analytics event)Users write negative reviews |
| Onboarding is to difficult to understand/ to perform (e.g. very technical, not clear, etc.) | Users write negative reviews about OnboardingUsers go to support and ask how to perform setup/ ask any question about Onboarding flowUsers taps on Question mark icon (there will be a special analytics event) |
| Onboarding process is too long/ separate steps are too long | Users return product because of the long onboarding/ because they don't have time to go through the flow/ they want to have a product ready as soon as possibleUsers write negative reviews about Onboarding duration |
| Onboarding is not 'skippable' (a user doesn't want to go through onboarding in general or right now) | Users go to support and ask how to skip onboarding Users write negative reviews |
| Users do not want to watch Onboarding videos (it's not convenient for them/ they want paper tutorial/ etc). | Users skip watching video (there will be a special analytics event)Users write negative reviews |
| See ME21-EP01. Onboarding MRGP 2022 and post MRGP. |
|  |
| See the described tracked events in [NI] ME21-US13. Onboarding: mobile analytics. |
| Release this Onboarding feature to 10 % of the users See the plan Onboarding MRGP 2022. Alpha Testing |# Contents

VISION Business needs & goals User goals Risks SCOPE Functional scope Tech risks OTHER Analytics Beta-testing Miro board flow Epic with User stories Onboarding idea General use case Delivery plan of Onboarding MRGP

# Miro board flow

https://miro.com/app/board/o9J_l3oJd20=/?moveToWidget=3458764528014769609&cot=14

# Epic with User stories

ME21-EP01. Onboarding MRGP 2022 and post MRGP

# Onboarding idea

Before releasing the feature there were a lot of:

1. collar returns because of non-working collars.
  1. Some of them were not really working, but some weren't. Our assumption was that users don't understand how BLE/ Wi-Fi/ GPS works and therefore claim that the collars not working. Therefore one of the purposes was to teach a user to understand how the collar works, what the signals on the collar mean and give more understanding about the Halo system in general (incl. the collar, beacons, the app, etc.).

2. users' complaints that the system is hard to set up.
  1. Therefore one more purpose was to develop a step-by-step tutorial to help a user to get through the collar setup so that it becomes fully prepared to start working.

3. Other purposes (mostly from business perspective) can be found here:[ME21. FTUE (previously 'App User Onboarding')](156694582.mdx).

# General use case

1. A user enters the app.
2. The app sends a request to BE to check whether it's needed to restore user's Onboarding (Restoring onboarding is required when a user started onboarding but then left the app and entered again- in this case they should see Onboarding from the step where they stopped):
  1. if BE sends a flag "OnboardingCompleted = true", then
    1. the app should**not**restore onboarding and should allow a user to enter the app (based on current existing logic: My Map screen; previously opened screen, etc.)

  2. if BE sends a flag "OnboardingCompleted = false", then
    1. the app should check steps a user passed already and show the next**not**passed step.

3. The general idea of restoring can be found here:[NI] ME21-US43. Onboarding: user progress restoring.
4. Knowledge keepers:Dmitry Kravchuk,Alina Sharshun [X],Anton Zimin [X].

# Delivery plan of Onboarding MRGP

| Epic | User stories | InitialSP | FinalSP | Sprint | Summer 2022 | Autumn 2022 | 86 | 87 | 88 | 89 | 90 | 91 | 92 | 93 | 94 | 95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HALO-13044 - Onboarding MRGP: Get SN via BLE Closed | HALO-10493 - MOB+BE: Get SN via BLE when adding a new collar to the account (onboarding related) Closed Note: initially was created as an independent task. Then linked to onboarding MRGP. Note: initially was out of onboarding MRGP. | n/a | 8 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-12998 - Onboarding MRGP: 'beacon' flow Closed | HALO-11914 - MOB: Update 'Add beacon' flow (add extra steps with instructions) Closed Note: initially was created as an independent task. Then linked to onboarding MRGP. | n/a | 5 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-13002 - Onboarding MRGP: multi-permission screen Closed | HALO-12529 - MOB: ME21-US03. Multi-permission screen Closed | 3 sp | 5 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-13411 - MOB: ME21-US24. Onboarding: Multi-permission screen - unification of screen view for Android and iOS Closed - added by Valeryia Chyrkun [X] (I added this item as there's significant change of rules for displaying multi-permission screens) |  |  |  |  |  |  |  |  |  |  |  |  |
| HALO-13000 - Onboarding MRGP: Calibration step Closed | HALO-12505 - MOB: ME03-US85. Add Collar: Calibration Closed | 5 sp | 8 sp |  |  | Sergei |  |  |  |  |  |  |
| HALO-13001 - Onboarding MRGP: support Closed | HALO-12517 - MOB: ME21-US04. Support page 'Need Help?' Closed | 2 sp | 2 sp |  |  |  |  | Andrei? |  |  |  |  |  |
| HALO-12516 - MOB: ME21-US02. Onboarding: Questionmark explanation screen Closed | 2 sp | 2 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-12997 - Onboarding MRGP: FW update step Closed | HALO-12778 - MOB [NT]: Finalize solution for 'FW update' flow Closed | 4 sp | 4 sp? |  |  |  |  |  |  |  |  |  |  |
| HALO-12787 - MOB [NT]: Add SGEE status to GAP/GATT protocol (new telemetry version) Closed | 1 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-12701 - FW: Add SGEE status to telemetry Closed | - |  |  |  |  |  |  |  |  |  |  |
| HALO-12560 - MOB [+BE]: ME21-US07. Add FW update screens to 'Add Collar' flow Closed | 13 sp |  |  |  |  | Kirill or Siarhei? |  |  |  |
| HALO-13018 - Onboarding MRGP: Add collar step Closed | HALO-12759 - MOB: ME21-US25: Add 'Charge Your Halo Collar' screen to the 'Add Collar' step of the Onboarding process Closed | 1 sp | ? |  |  |  |  | Andrei? |  |  |  |  |  |
| HALO-13170 - Onboarding MRGP: Welcome to Halo app screen Closed | HALO-11914 - MOB: Update 'Add beacon' flow (add extra steps with instructions) Closed |  | 2sp |  |  |  |  | Dmitry? |  |  |  |  |  |
|  | HALO-11914 - MOB: Update 'Add beacon' flow (add extra steps with instructions) Closed Note: out of initial MRGP scope, added by Michael and Ken | 1-2 sp |  |  |  |  |  |  |  |  |  |  |  |
| HALO-12995 - Onboarding MRGP: main flow Closed | HALO-12994 - MOB [NT]: ME21-US20. Onboarding: stepper on the parent screens Closed | 5 sp | 5 sp |  |  |  |  | Siarhei ? |  |  |  |  |  |
| HALO-12561 - MOB+BE: ME21-US11. Onboarding: parent screens with video Closed Note: if it's necessary, we can release these screens within the Add collar adding from the collars list | 5 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-12562 - MOB: ME21-US12. Onboarding: general requirements (for exceptional and alternative cases) Closed | 0.5 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-13185 - MOB+BE: ME21-US43. Onboarding: user progress restoring Closed | 5 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-12521 - MOB [NT]: ME21-US16. Question mark icon requirements (related to Onboarding flow) Closed This story can be divided into several smaller ones, if it's necessary. | 2 SP |  |  |  |  |  |  |  |  |  |  |
| HALO-13038 - MOB+BE: ME21-US22. Onboarding: Add subtitles to onboarding video Closed | ? |  |  |  |  |  |  |  |  |  |  |
| HALO-13039 - MOB: ME21-US23. Onboarding: Add 'Watch full video' link to onboarding video screens Closed Assumption: Vimeo or YouTube link should be used | 1 SP |  |  |  |  |  |  |  |  |  |  |
| HALO-12899 - MOB [NT]: Add Firebase RemoteConfig support Ready for Development Note: initially was out of onboarding MRGP. | n/a | 3 SP |  |  |  | Kirill |  |  |  |  |  |  |
| HALO-12565 - MOB : Onboarding: Complete navigation Closed | 3 sp |  |  |  |  |  |  |  |  |  |  |  |
| HALO-12520 - MOB: ME21-US09. Onboarding: flow completion ('Almost Ready!' screen) Closed | 2 sp |  |  |  |  |  |  |  |  |  |  |  |
| HALO-12522 - MOB: ME21-US10. Onboarding: navigation to Training Closed | 3 sp |  |  |  |  |  |  |  |  |  |  |  |
| HALO-12518 - MOB: ME21-US05. User type choice screen Closed | 3 sp | 2 sp |  |  |  |  |  |  |  |  |  |  |
| HALO-12999 - Onboarding MRGP: add 2nd and subsequent collars Closed | HALO-12969 - MOB+BE: ME21-US14. Show Onboarding when a user adds a collar later Closed | 2 sp |  |  |  |  |  |  |  |  |  |  |  |
| HALO-10224 - Onboarding MRGP: other tasks Closed | HALO-12563 - MOB: ME21-US13. Onboarding: mobile analytics Closed | 3 sp |  |  |  |  |  |  |  |  |  |  |  |
| HALO-10224 - Onboarding MRGP: other tasks Closed | HALO-12508 - MOB: Add note about "family membership" on "Create/edit account" screen Closed | 1 sp | 2 sp |  | Kirill |  |  |  |  |  |  |  |  |
| HALO-10224 - Onboarding MRGP: other tasks Closed | HALO-12519 - MOB: Assign pet screen change Closed | 3 sp | 2 sp |  | Kirill |  |  |  |  |  |  |  |  |
| Configure necessary videos via configuration tool |  |  |  |  |  |  |  |  |  |  |  |  |  |
| BETA TESTING | IMPORTANT |  |  |  |  |  |  |  |  |  |  |  |  |
