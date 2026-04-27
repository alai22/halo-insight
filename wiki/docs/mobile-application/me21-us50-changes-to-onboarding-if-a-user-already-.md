---
title: "ME21-US50. Changes to Onboarding if a user already has a pet without assigned collars"
sidebar_label: "ME21-US50. Changes to Onboarding if a user already has a pet without assigned collars"
sidebar_position: 730
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue |
|---|---|---|
| APPROVED |
| Maria Shikareva [X]Maryia Paklonskaya [X] |
| HALO-14222 - MOB: ME21-US50. Changes to Onboarding if a user already has a pet without assigned collars Closed |# Contents

User story Acceptance criteria There are no pets without assigned collars in the account There are pets without assigned collars in the account

# User story

\> As a Halo business owner I want to have the screens for the 'Add Pet' flow updated so that they are ready to be included into the Onboarding flow.

# Acceptance criteria

| AC | Description | iOS screens designs | Android screens designs | Main flow | Onboarding |
|---|---|---|---|---|---|
| There are no pets without assigned collars in the account |
| ME21-US50-AC01 | Precondition: 'Assigning Your Halo Collar to Your Pet' is openedANDthere are no pets without assigned collars in the account.When a user taps the 'Add Pet' button, the app should open the 'Add Pet' screen (existing behaviour). | Link to Zeplin | Link to Zeplin |
| There are pets without assigned collars in the account |
| ME21-US50-AC02 | Precondition: 'Assigning Your Halo Collar to Your Pet' is openedANDthere are pets without assigned collars in the account.When a user taps the 'Add Pet' button, the app should open the 'Pair Collar With a Pet' screen with the following UI elements:Main flowOnboardingChanges:a question mark tappable icon at the right upper corner;When a user taps on a question mark icon, then the app should open the 'Need Help?' screen.'Done' button at the bottom of the screen.The button becomes active only in case a pet is selected.All other UI elements should not be changed!'Back' button;The button should navigate a user to the "Assigning Your Halo Collar to Your Pet" screen with video without any confirmation pop-up.'Pair Collar With a Pet' title;a question mark tappable icon at the right upper corner;When a user taps on a question mark icon, then the app should open the 'Need Help?' screen.'Please Choose Which Pet Should Use This Collar' subtitle;'Add New Pet' buttona list of Pets without Collars:Pet avatar or Paw icon (if pet avatar was not set)+ HALO ringPet's name;'Next' button at the bottom of the screen.The button becomes active only in case a pet is selected.no section with pets with collars (in onboarding only) | Changes:a question mark tappable icon at the right upper corner;When a user taps on a question mark icon, then the app should open the 'Need Help?' screen.'Done' button at the bottom of the screen.The button becomes active only in case a pet is selected.All other UI elements should not be changed! | 'Back' button;The button should navigate a user to the "Assigning Your Halo Collar to Your Pet" screen with video without any confirmation pop-up.'Pair Collar With a Pet' title;a question mark tappable icon at the right upper corner;When a user taps on a question mark icon, then the app should open the 'Need Help?' screen.'Please Choose Which Pet Should Use This Collar' subtitle;'Add New Pet' buttona list of Pets without Collars:Pet avatar or Paw icon (if pet avatar was not set)+ HALO ringPet's name;'Next' button at the bottom of the screen.The button becomes active only in case a pet is selected.no section with pets with collars (in onboarding only) | For Onboarding: Link to ZeplinMain Flow: Link to Zeplin | For Onboarding:Link to ZeplinMain Flow: Link to Zeplin |
| Changes:a question mark tappable icon at the right upper corner;When a user taps on a question mark icon, then the app should open the 'Need Help?' screen.'Done' button at the bottom of the screen.The button becomes active only in case a pet is selected.All other UI elements should not be changed! | 'Back' button;The button should navigate a user to the "Assigning Your Halo Collar to Your Pet" screen with video without any confirmation pop-up.'Pair Collar With a Pet' title;a question mark tappable icon at the right upper corner;When a user taps on a question mark icon, then the app should open the 'Need Help?' screen.'Please Choose Which Pet Should Use This Collar' subtitle;'Add New Pet' buttona list of Pets without Collars:Pet avatar or Paw icon (if pet avatar was not set)+ HALO ringPet's name;'Next' button at the bottom of the screen.The button becomes active only in case a pet is selected.no section with pets with collars (in onboarding only) |
| ME21-US50-AC03 | Content of this screen should be scrollable except the bottom part with the 'Done'/ 'Next' buttons. |
| ME21-US50-AC04 | When a user taps 'Next' button, then the app should:assign previously added collar to the selected pet;not show M189 Wait until the collar is synchronized (binding existing pet to a collar); - only for Onboardingnot show M188 Wait until the collar is synchronized (binding new pet to a collar); - only for Onboardingnavigate a user to the 'Connecting Your Halo Collar' screen (existing behavior).QA note: ME03-F04-AC08, ME03-F04-AC09 are changed. | - | - |
| ME21-US50-AC05 | Connection and communication errors should be handled according to ME14-F01 Unified errors handling. | - | - |
