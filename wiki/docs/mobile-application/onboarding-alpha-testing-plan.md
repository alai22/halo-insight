---
title: "Onboarding. Alpha Testing Plan"
sidebar_label: "Onboarding. Alpha Testing Plan"
sidebar_position: 738
author: "Maria Shikareva [X]"
---

# Contents

General information Instruction (detailed description) Instruction (short for beta-testers) Before starting Start Onboarding Feedback surveys KPIs for iteration results measurement Results analysis Feedbacks

# General information

| Parameter | Value | Goals | Roles | Entry points for beta testing | Number of iterations | Duration of beta testing (per 1 iteration) | Duration of results analysis(per 1 iteration) |
|---|---|---|---|---|---|---|---|
| Check if Onboarding steps are clear enough for end users.Define possible steps where a user can stuck for some time.Understand how much time Onboarding takes.Define steps where a user needs support.Check if CSRs are ready to support users during Onboarding flow (since there's an option to contact DP directly during Onboarding).Gather user feedback.Find areas of improvement for MRGP scope.Define scope for Post-MRGP phase (Onboarding MRGP II).Define level of criticality of any bugs found during beta testing. |
| Beta testersHalo Team: CSRs.Softeq Team:BAsQAssome other team members not involved into the onboarding development processResults reviewersSofteq BA |
| The Halo app:Android iOS |
| At least 1, but the final number depends on KPIs results after each iteration |
| 1 business day ( 16 Nov 2022 / 17 Nov 2022 ) |
| 2 business days ( 17 Nov 2022 - 18 Nov 2022 ) |# Instruction (detailed description)

1. You need to have a real collar**with cable**.
  1. *Assumption: we want to test only the first flow with adding a real collar.*
  2. Environment: the collar can be on any environment; it's easier for the mobile team to have several builds for specific environments.
  3. *Note: there's an option to test using Vysor for those users who don't have a real collar. Idea: a user 1 with a collar connects the app to Vysor, a user 2 can pass Onboarding on their own device completing the steps from user 1 device. Cons: a user 1 has to communicate with a collar (charge if required, press on the button, etc).*

2. Mob team should add Apple IDs/ email addresses to TestFlight/ AppCenter so that everybody can download a build.
3. You need to download the specific build from:
  1. TestFlight → for iOS
    1. The iOS version ([1.57.542](https://appstoreconnect.apple.com/apps/1476830649/testflight/ios/a96134e1-b19f-43c0-b975-2aed7b338033))

  2. AppCenter → for Android
    1. The Android version ([1.46.288](http://https//appcenter.ms/orgs/PAWSCollar/apps/HALO-Android-Production/distribute/releases/3))

4. You need to have a plan.
  1. You can use AAP to grant temporary access for your collar.

5. To see Onboarding you can select one of 2 ways:
  1. **Recommended:**use a new account.
    1. Unassign a collar from the previous account (this step is optional: you can skip it if you have another collar that is not assigned to any account).
    2. Download required build.
    3. Create a new account.

  2. Possible: use existing account.
    1. Unassign the collar from the existing account.
    2. Delete the app.
    3. Re-install the app using the required build.
    4. Log In using credentials from existing account.
    5. We DO NOT recommend using this flow because in this case the Onboarding will start from 'Permissions' screen, not from the very beginning (since you already have an account and your name provided).

6. Please note that you should pass Onboarding without leaving the app - as of17 Nov 2022this process is continuous.
7. Ideally you should have an Indoor beacon not added to the account (but it's OK not to have it because adding a beacon is a skippable step in the Onboarding).
8. On the 'Do You Have a Halo Collar?' screen you should choose the first option ('I have my Halo Collar').
  1. You can select any option, but mostly we're interested in your experience with adding a real collar.

9. Please mark the time required to complete the Onboarding.
10. You should pass the Onboarding making notes about some things that aren't unclear, confusing, etc.
  1. Please mark the name of the screen on which you needed help.

11. Please fulfill the survey after completing the Onboarding: we need to know your general experience about the flow.
  1. If you have some notes/ comments about any step, you can provide us with it via the same survey.

# Instruction (short for beta-testers)

## Before starting

1. You need to have a real collar looking on production environment**with cable**.
  1. If your collar looks on any other environment, please, notify us BEFORE starting the Onboarding so that we can build specific version for your environment.

2. You should provide your Apple IDs/ email addresses to the Softeq mobile team so that you will be added to TestFlight/ AppCenter and be able to download a build.
3. You need to download the specific build from (only after you're added there):
  1. TestFlight → for iOS
    1. The iOS version ([1.57.542](https://appstoreconnect.apple.com/apps/1476830649/testflight/ios/a96134e1-b19f-43c0-b975-2aed7b338033))

  2. AppCenter → for Android
    1. The Android version ([1.46.288](http://https//appcenter.ms/orgs/PAWSCollar/apps/HALO-Android-Production/distribute/releases/3))

4. You need to have a plan on your account.
  1. If you don't have a plan, you can use AAP to grant yourself temporary access for Gold for 1-2 days.

5. To see Onboarding you can select one of 2 ways:
  1. **Recommended:**use a new account.
    1. Unassign a collar from the previous account (this step is optional: you can skip it if you have another collar that is not assigned to any account).
    2. Download required build.
    3. Create a new account.

  2. Possible: use existing account.
    1. Unassign the collar from the existing account.
    2. Delete the app.
    3. Re-install the app using the required build.
    4. Log In using credentials from existing account.
    5. We DO NOT recommend using this flow because in this case the Onboarding will start from 'Permissions' screen, not from the very beginning (since you already have an account and your name provided).

6. Ideally you should have an Indoor beacon not added to the account (but it's OK not to have it because adding a beacon is a skippable step in the Onboarding).
7. Please note that you should pass Onboarding without leaving the app - as of17 Nov 2022this process is continuous.
8. You will have to go outside for GPS initialization.

## Start Onboarding

1. Open the app.
2. Create a new account (reminder: you should have a Plan on it).
3. Proceed with other steps.
4. On the 'Do You Have a Halo Collar?' screen you should choose the first option ('I have my Halo Collar').
  1. You can select any option, but mostly we're interested in your experience with adding a real collar.

5. Please mark the time required to complete the Onboarding.
6. You should pass the Onboarding making notes about some things that aren't unclear, confusing, etc.
  1. Please mark the name of the screen on which you needed help.

7. Please fulfill the survey after completing the Onboarding: we need to know your general experience about the flow.
  1. If you have some notes/ comments about any step, you can provide us with it via the same survey.

# Feedback surveys

https://forms.gle/SLeSgzdCTLug2NP57

# KPIs for iteration results measurement

| KPI | Results analysis (who is responsible for measurement and analysis) |
|---|---|
| The CSAT metric for User | Softeq BAs |
| The CES metric for User | Softeq BAs |
| The number and criticality level of found bugs | Softeq BAs and QAsMichael, Ken |# Results analysis

Onboarding. Alpha testing results report

# Feedbacks

Schedule a meeting after beta testing where end users are going to share their feedback: what was good, what was bad, what needs to be improved.


