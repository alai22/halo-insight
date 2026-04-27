---
title: "ME21-US68. Update FTUE/onboarding progress restoring logic"
sidebar_label: "ME21-US68. Update FTUE/onboarding progress restoring logic"
sidebar_position: 427
last_modified: "Jan 14, 2025"
author: "Galina Lonskaya"
---

Click here to expand...| Document status | Document owner | Link to JIRA issue | Changes history |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Timofey Burak [X] Dmitry Kravchuk |
| HALO-20582 - MOB: ME03-US68. Update FTUE Onboarding flow restoring logic Closed |
| Click here to expand...15 Jul 2024 draft user story is created by Galina Lonskaya |# Contents

User story Acceptance criteria Implementation notes

# User story

\> As a Halo app user I want my progress in the FTUE (~ First collar attach/Onboarding process) to be saved even if the app is closed so that I can resume FTUE (~ First collar attach/Onboarding process) where I left off without starting over.

# Acceptance criteria

| AC | Description | Handling of a new users who start onboarding process using the app version that supports new onboarding | Supposed FTUE progress restoration sequence after the app closing: | Logic for 2 smartphones | Handling of the users who started the onboarding process in an older version of the app | OLD Onboarding flow (screen name of last non completed step) | NEW FTUE/First collar attach/Onboarding flow (screen name of the step that should be shown after opening) |  |  | Handling of deep-link opening |
|---|---|---|---|---|---|---|---|---|---|---|
| ME21-US68-AC01 | If the app closes (e.g., crash, forced close, the session expired, etc.), then: my progress should be preserved up to the last not completed step when I reopen the app.Note: entered and not saved data is not cashed locally. |
| ME21-US68-AC02 | If FTUE Onboarding is completed, then:My Map screen should be opened. |
| ME21-US68-AC03 | Precondition: FTUE Onboarding is not completedIf there is no info about First Name OR no answer to 'Have your trained your dog before' question, then: Tell Us About Yourself (~new title: Welcome to the Halo Pack!) screen should be opened. |
| ME21-US68-AC04 | Precondition: FTUE Onboarding is not completed, First name and answers to 'Tell us about yourself' questions are providedIf there is no info about Permissions, then: 'Enable Permissions' screen should be opened. Note for QA: it might be without progress bar, it's OK discussed with Victor O |
| ME21-US68-AC05 | Precondition: FTUE Onboarding is not completed, the first name is provided and permissions are enabled/disabledIf there is no subscription:'Join the Pack' screen should be opened. |
| ME21-US68-AC13 | Precondition: FTUE Onboarding is not completed, the first name is provided, permissions are enabled/disabled, the collar is not addedIf the subscription is active for this account, then:'Adding Your Halo Collar' screen should be opened |
| ME21-US68-AC06 | Precondition: FTUE Onboarding is not completed, the first name is provided, permissions are enabled/disabled, the collar is added. If the pet is not linked to the collar, then: 'Set Up Your Pet’s Profile' screen should be opened. |
| ME21-US68-AC07 | Precondition: FTUE Onboarding is not completed, the first name is provided, permissions are enabled/disabled, the collar is added, the pet is addedIf Wi-Fi isn't skipped/set up, then: 'Connecting Your Halo to Wi-Fi' screen should be opened. |
| ME21-US68-AC08 | Precondition: FTUE Onboarding is not completed, the first name is provided, permissions are enabled/disabled, the collar is added, the pet is addedIf Wi-Fi is skipped/set up, then: 'Congratulations!' screen should be opened. |
| ME21-US68-AC09 | If I started 2 FTUE onboarding flows from 2 different smartphones using one Halo account and trying to add 2 different collars, then: I should be able to add two different collars to one account in parallel. |
| ME21-US68-AC10 | If I started 2 FTUE onboarding flows from 2 different devices using one Halo account and trying to add the same collar, then: I should be able to add the collar on one smartphoneNote: on the second smartphone I will not be able to add the same collar and for now will not see any error, this info will be added to the article by Halo team |
| ME21-US68-AC11 | When I open the updated app, then I should resume the onboarding process from the equivalent step in the new version that matches their last completed step in the old version (see the mapping table below)OLD Onboarding flow (screen name of last non completed step)NEW FTUE/First collar attach/Onboarding flow (screen name of the step that should be shown after opening)Tell Us About Yourself (first name is not added to the account)Tell Us About Yourself (~new title: Welcome to the Halo Pack!)Welcome to the Halo Pack!Enable Permissions'Halo Help' explanationEnable PermissionsEnable PermissionsEnable PermissionsDo You Have a Halo Collar?'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen Let's Get Started'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen Your Halo Collar Kit'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen 'Powering Up & Connecting' flow (added collar is not added to the account)'Adding Your Halo Collar' screen'Assign Your Halo Collar to Your Pet' flow (pet is not added to the account)'Adding Your Pet' screen (~new title: Set Up Your Pet’s Profile)'Connecting Your Halo Collar' flow (wi-fi not set/skipped)'Connecting Your Halo to Wi-Fi' screen'Halo Collar Updates' flow'Congratulations!' screen'Your Collar's GPS' flow'Congratulations!' screen'Using Halo Beacons' flow'Congratulations!' screen 'Using The Halo Collar App' screen'Congratulations!' screen Almost Ready The same screen, currently named 'Congratulations!'Start Halo Training'Congratulations!' screen Need Help?The same logic as previously: Depends on the screen from which it was initiated → therefore the last passed step should be opened after restoring (no need to save and show 'need Help?' screen).'Join Halo Pack' screen'Adding Your Halo Collar' OR 'Join Halo Pack', depending of the subscription 'Why Halo Collar?' screenMy Map screen 'Tour Halo App' screen My Map screen | Tell Us About Yourself (first name is not added to the account) | Tell Us About Yourself (~new title: Welcome to the Halo Pack!) | Welcome to the Halo Pack! | Enable Permissions | 'Halo Help' explanation | Enable Permissions | Enable Permissions | Enable Permissions | Do You Have a Halo Collar? | 'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen | Let's Get Started | 'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen | Your Halo Collar Kit | 'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen | 'Powering Up & Connecting' flow (added collar is not added to the account) | 'Adding Your Halo Collar' screen | 'Assign Your Halo Collar to Your Pet' flow (pet is not added to the account) | 'Adding Your Pet' screen (~new title: Set Up Your Pet’s Profile) | 'Connecting Your Halo Collar' flow (wi-fi not set/skipped) | 'Connecting Your Halo to Wi-Fi' screen | 'Halo Collar Updates' flow | 'Congratulations!' screen | 'Your Collar's GPS' flow | 'Congratulations!' screen | 'Using Halo Beacons' flow | 'Congratulations!' screen | 'Using The Halo Collar App' screen | 'Congratulations!' screen | Almost Ready | The same screen, currently named 'Congratulations!' | Start Halo Training | 'Congratulations!' screen | Need Help? | The same logic as previously: Depends on the screen from which it was initiated → therefore the last passed step should be opened after restoring (no need to save and show 'need Help?' screen). | 'Join Halo Pack' screen | 'Adding Your Halo Collar' OR 'Join Halo Pack', depending of the subscription | 'Why Halo Collar?' screen | My Map screen | 'Tour Halo App' screen | My Map screen |
| Tell Us About Yourself (first name is not added to the account) | Tell Us About Yourself (~new title: Welcome to the Halo Pack!) |
| Welcome to the Halo Pack! | Enable Permissions |
| 'Halo Help' explanation | Enable Permissions |
| Enable Permissions | Enable Permissions |
| Do You Have a Halo Collar? | 'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen |
| Let's Get Started | 'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen |
| Your Halo Collar Kit | 'Adding Your Halo Collar' OR in case no subscription, then 'Join Halo Pack' screen |
| 'Powering Up & Connecting' flow (added collar is not added to the account) | 'Adding Your Halo Collar' screen |
| 'Assign Your Halo Collar to Your Pet' flow (pet is not added to the account) | 'Adding Your Pet' screen (~new title: Set Up Your Pet’s Profile) |
| 'Connecting Your Halo Collar' flow (wi-fi not set/skipped) | 'Connecting Your Halo to Wi-Fi' screen |
| 'Halo Collar Updates' flow | 'Congratulations!' screen |
| 'Your Collar's GPS' flow | 'Congratulations!' screen |
| 'Using Halo Beacons' flow | 'Congratulations!' screen |
| 'Using The Halo Collar App' screen | 'Congratulations!' screen |
| Almost Ready | The same screen, currently named 'Congratulations!' |
| Start Halo Training | 'Congratulations!' screen |
| Need Help? | The same logic as previously: Depends on the screen from which it was initiated → therefore the last passed step should be opened after restoring (no need to save and show 'need Help?' screen). |
| 'Join Halo Pack' screen | 'Adding Your Halo Collar' OR 'Join Halo Pack', depending of the subscription |
| 'Why Halo Collar?' screen | My Map screen |
| 'Tour Halo App' screen | My Map screen |
| ME21-US68-AC12 | Precondition: FTUE onboarding is not completed and Halo app is either backgrounded or terminated. If I tap on a deep link that is intended to open some specific screen in Halo app, then: Halo app should be opened;the last not completed FTUE onboarding step should be opened. |# Implementation notes

| IN | Description |
|---|---|
| ME21-US68-IN01 | Supposed FTUE progress restoration sequence:If Onboarding status is 'partially completed' or 'fully completed' - redirect user to the 'My Map' screen;Otherwise, If User don't have 'first name filled' - start FTUE from 'Tell Us About Yourself' screen;Otherwise, if the App don't have all the permissions granted - start FTUE from 'Permissions' screen;Otherwise, if the user don't have required membership - start FTUE from the 'No Pack Membership' screen;Otherwise, if the user don't have any collars in the account - start FTUE from the 'Charging Your Collar' screen, start modal 'Add collar' flow from the beginning;Otherwise, if the user's collar don't have pet assigned - start FTUE from the 'Charging Your Collar' screen, start modal 'Add collar' flow from the pet assignment step. TBD: what to do if there are several collars in the account;Otherwise, if there is no 'Wi-Fi setup' step in the list of completed steps - start FTUE from the 'Charging Your Collar' screen, start modal 'Add collar' flow from the Wi-Fi-setup step;Otherwise, start FTUE from 'Congratulations' screen and mark the progress as 'fully completed'; |
