---
title: "ME01-F03. Add profile info after Sign Up"
sidebar_label: "ME01-F03. Add profile info after Sign Up"
sidebar_position: 596
author: "Galina Lonskaya"
---

| Document status | Test cases status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|---|
| TEAM REVIEW |
| NEED UPDATE as of 14 Oct 2022 |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko Valeryia Chyrkun [X] Maria Shikareva [X] |
| Click here to expand... HALO-2864 - MOB: ME01-US12. Add profile info after Sign Up (new UI design ) Closed HALO-6022 - Android: Add / edit user profile photo (dependency on Add/edit pet avatar) Closed HALO-10799 - BE+MOB: Add "last name" to the user account + update some related texts Closed HALO-12508 - MOB: Add note about "family membership" on "Create/edit account" screen Closed HALO-12516 - MOB: ME21-US02. Onboarding: Questionmark explanation screen Closed |
| Click here to expand...14 Oct 2022 Maria Shikareva [X] Baselined ME01-US27. Add note about "family membership" on "Create/edit account" screen; [Not impl.] ME21-US02. Onboarding: 'Questionmark' explanation screen |# Contents

User story Acceptance criteria 'Tell Us Your Name' screen Update Photo Remove Photo Take a Photo Choose From Gallery 'Family Membership' card 'Halo Support' screen

# User story

\> As an account owner I want to add profile info to my Halo account so that I can see my info in Halo app settings.

# Acceptance criteria

| AC | Description | iOS UI design | Android UI design |
|---|---|---|---|
| 'Tell Us Your Name' screen |
| ME01-F03-AC01 | Precondition: a user hasn't added a name to their Halo account.When a user logs into the app, then the app should display the "Tell Us Your Name" screen with the following UI elements:'Done' button;Avatar placeholder;'Update Photo' button;'Tell Us Your Name' title;'We will use your name for email and other communications' text;'First Name' text field (see ME01-F03-AC02 below);'Last Name' text field (see ME01-F03-AC03 below)'Plan to share the Halo app with your family? Tap here to learn how.' text.Where 'Tap here' is a button to show 'Family Membership' card. | Link to Zeplin | Link to Zeplin |
| ME01-F03-AC02 | 'First Name' text field should have the following parameters:mandatory field;max length is 20 characters.The app should forbid to enter the 21st character or space. |
| ME01-F03-AC03 | 'Last Name' text field should have the following parameters:optional field;max length is 20 characters.The app should forbid to enter the 21st character or space. |
| ME01-F03-AC04 | Precondition: "Tell Us Your Name" screen is opened.The app should display a cross icon in the Name field while editing. | The link to Zeplin | - |
| ME01-F03-AC05 | When a user taps on the Cross icon, the app should clear the field. |
| ME01-F03-AC06 | Precondition: "Tell Us Your Name" screen is opened.When a user taps on the 'Done' button, but the Name field is empty, then the app should:display M263 Enter name error;display fields underlined. | Link to Zeplin | Link to Zeplin |
| ME01-F03-AC07 | Precondition: "Tell Us Your Name" screen is opened.When a user taps on the 'Done' button AND the First Name is entered AND the name and photo are saved successfully, then the app should open the 'Halo Support' screen (see exception in ME01-F03-AC08 below). | - | - |
| ME01-F03-AC08 | "Halo Support' should be shown to the user only after registration and should not be shown after each launch of the app. | - | - |
| ME01-F03-AC09 | Precondition: "Tell Us Your Name" screen is opened.When a user taps the 'Done' button AND the First Name is entered BUT data isn't saved successfully, then the app should display connection/communication errors (see ME14-US01. Unified errors handling). | - | - |
| Update Photo |
| ME01-F03-AC10 | Precondition: "Tell Us Your Name" screen is opened.When a user taps on the 'Update Photo' button or the photo placeholder, then the app should display the "Update Photo" action sheet with the following UI elements:'Remove Photo' button;'Take a Photo' button;'Choose From Gallery' button;'Close' button. | Link to Zeplin | Link to Zeplin |
| ME01-F03-AC11 | When a user taps 'Close' button, then the app should close the action sheet. |
| Remove Photo |
| ME01-F03-AC12 | When a user taps on the 'Remove Photo' button, then the app removes the photo form the user's avatar. | - | - |
| Take a Photo |
| ME01-F03-AC13 | Precondition: a user doesn't grant nor restrict access to the Camera.When a user taps on the 'Take a Photo' button, then the app requests access to the camera: M154 Camera access request. | - | - |
| ME01-F03-AC14 | Precondition: M154 Camera access request is displayed.When a user allows Camera usage, then the app opens a standard camera view screen to take a photo. | - | - |
| ME01-F03-AC15 | When a user taps on the "Capture" icon, the app should display the standard screen with "Retake" or "Use Photo" buttons. | - | - |
| ME01-F03-AC16 | When a user taps 'Retake' button, then the app opens a standard camera view screen again to take a new photo. | - | - |
| ME01-F03-AC17 | When a user taps 'Use Photo' button, then the app opens the “Move and Scale” screen (iOS) or "Crop" screen (Android) to select the photo area to display. | - | - |
| ME01-F03-AC18 | A user should be able scale a photo on the screen within a circle frame pinching in/out. | - | - |
| ME01-F03-AC19 | When a user submits the chosen photo, then the app should set the new profile picture as the user's avatar at the "Tell Us About Yourself!". | - | - |
| ME01-F03-AC20 | Precondition: M154 Camera access request is displayed.When a user doesn't allow Camera usage, then the app notifies the user that access is restricted, see the message M59. Camera permissions denied | - | - |
| Choose From Gallery |
| ME01-F03-AC21 | Precondition: a user doesn't grant nor restrict access to the Camera Roll.When a user taps on the 'Choose From Gallery' button, then the app requests access to the gallery: M152 Photo access request. | - | - |
| ME01-F03-AC22 | Precondition: M152 Photo access request is displayed.When a user allows Camera usage, then the app opens the screen with all app photos. | - | - |
| ME01-F03-AC23 | When a user taps on the photo from the list, then:a selected photo becomes selected;the app displays the screen “Move and Scale”. | - | - |
| ME01-F03-AC24 | A user should be able scale a photo on the screen within a circle frame pinching in/out. | - | - |
| ME01-F03-AC25 | The image should meet size and format requirements, see R-6 and R-7. | - | - |
| ME01-F03-AC26 | If users try to set images with invalid extension, then the app should show pop up with corresponding M14 Invalid image message. | - | - |
| ME01-F03-AC27 | When a user taps on the "Done" button, then the app should set the new profile picture as the user's avatar at the "Tell Us About Yourself!" screen. | - | - |
| ME01-F03-AC28 | Precondition: M152 Photo access request is displayed.When a user doesn't allow Camera usage, then then app notifies the user that access is restricted, see the message M64. Photo permissions denied. | - | - |
| ME01-F03-AC29 | If a user tries to upload a photo and something goes wrong, the app should display connection/communication errors (see ME14-US01. Unified errors handling). | - | - |
| 'Family Membership' card |
| ME01-F03-AC30 | If I tap on 'Tap here', then I see 'Family Membership' card with the following elements:Title: Family MembershipBody: When you create an account in the Halo App and connect to that account, only that specific account can be used to access that collar. Therefore, if there are multiple people in your family who need access to the collar, you must share the same login credentials. We strongly recommend that each individual who is accessing the Halo Collar through the app goes through User Training before taking responsibility for a dog that is using the collar.Button: Close | iOS | Android |
| ME01-F03-AC31 | When a user taps the 'Close' button, then the app should close the 'Family Membership' card. |
| ME01-F03-AC32 | 2 events for gathering analytics should be added: View_family_membership_cardCreate_user_account | - | - |
| 'Halo Support' screen |
| ME01-F03-AC33 | The 'Halo Support' screen should have with following elements:'?' icon (not tappable on this screen);'If you need a help during onboarding , tap on this icon and select one of the preferred options below.' text;'Halo Help' section:'Halo Help' icon;'Halo Help' subtitle;'The easiest and quickest way to get answers to your Halo product questions.' text;'Halo Dog Par' section:Halo Dog Park TM icon'Halo Dog Park TM' subtitle;'Join a live Zoom session during open hours for: customer support, sales questions, training and events.' text;'If you need the support later during your everyday app usage, please go to the Settings tab.' text;'Next' button. | Link to Zeplin | Android |
| ME01-F03-AC34 | When a user taps the 'Next' button, then the app should navigate a user to the 'Enable Permissions' screen. |
| ME01-F03-AC35 | Content of the screen should be scrollable except the bottom part of screen with the 'Next' button. |
