---
title: "[BL] ME03-US72. Get SN via BLE when adding a new collar to the account"
sidebar_label: "[BL] ME03-US72. Get SN via BLE when adding a new collar to the account"
sidebar_position: 207
last_modified: "Aug 12, 2022"
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] Dmitry Kravchuk Timofey Burak [X] Dmitriy Morozov [X] |
| HALO-10493 - MOB+BE: Get SN via BLE when adding a new collar to the account (onboarding related) Closed HALO-12836 - BE+MOB: Change link on the 'Halo is assigned to another account' screen collar?'link Closed HALO-12835 - MOB: ME03-US86. Add collar: link updates (rename one link, remove another) Closed |
| Click here to expand...30 Jun 2022 AC22-23 added by Valeryia Chyrkun [X]07 Jul 2022 removed reqs about check mark (AC12) 19 Jul 2022 Valeryia Chyrkun [X] updated design and text of 'You Need a Plan' at ME03-US72-AC21 |# General description

In general, we need to eliminate QR-code scan feature, so we will no longer need the QR-code on the box ( as currently we need to print special label for that and it adds the complexity). We also will no longer need the camera access. The possible solution is to implement getting the SN via Bluetooth (the same process as for Beacons search).

# User story

\> As an owner I want to be able to get the collar SN via Bluetooth so I will no longer face the challenge of scanning QR code on the collar covered by protective casing.

# Acceptance criteria

| AC | Text | Screens | 'Pressing button' screen | Bluetooth pairing screen | Find and Choose Collar: Choose Halo Collar |
|---|---|---|---|---|---|
| ME03-US72-AC01 | Precondition: Collar list or 'Assign a collar' screen is opened. User has active subscription.If a user taps on the "Add Collar" button, then:the 'Add a New Collar' screen should be opened. (see ME03-US72-AC05) |  |
| ME03-US72-AC02 | Precondition: Bluetooth is not turned on the smartphoneIf a user taps on the "Add Collar" button, then M178 Disabled Bluetooth (Wi-Fi setup, Add Beacon) pop-up should be displayed. |  |
| ME03-US72-AC21 | Precondition: Collar list or 'Assign a collar' screen is opened. User doesn't have active subscription.If a user taps on the "Add Collar" button, then 'You need a plan' screen should be opened (see the design) with the following elements'You Need a Plan' titleThe set of UI elements described in ME19-US16 Subscription plan upgrade prompting screen. |  |
| ME03-US72-AC03 | If I tap on 'Add Collar' button and Bluetooth is turned on my smartphone, then:'Add New Collar' screen should be opened;Bluetooth scanning process for collars should be started automatically.The 'Add New Collar' screen should be shown before at least one collar which met the rues (ME03-US72-AC04) is found The scanning of collars should be real-time |  |
| ME03-US72-AC04 | The rules for showing the collar/(s) found via Bluetooth scanning:If there's a collar found with new firmware (no matter assigned or available) and Button is not pressed, then this collar will not be displayed If there's a single collar with new firmware and Button pressed found, and the collar is not assigned to any account, and there's an active subscription for collar or user, then 'Connecting over Bluetooth' screen (see ME03-US72-AC08) is automatically shown skipping the step of showing the list of found collars. If there's only one collar with new firmware and Button pressed found, and there's an active subscription for collar or user, and the collar is assigned to another account, then 'Add New Collar-Assigned to Another Account' screen is shown (see ME03-US72-AC11) If there's a collar/(s) with old firmware (no matter available or assigned), then 'Select collar to add' screen is shown (see ME03-US72-AC12)If there's a combination of collars of both old and new firmware is found and there's no collar with new FW and button pressed between them then 'Select collar to add' screen is shown (see ME03-US72-AC12) |  |
| ME03-US72-AC05 | 'Add New Collar- Select a Collar to Add' screen should consist of:Cancel/'x' button. When I click this button, then I modal window is closed.'Add New Collar' title'Select a Halo Collar to Add' subtitle'Press and release the Power button on the front of the Halo.' text 'Why don't I see my collar?' linkImage of finger pressing the Power button | iOS Android |
| ME03-US72-AC06 | If Collar advertisement package is bitten/corrupted then it should not be displayed in the list of Collars and cannot be added |  |
| ME03-US72-AC07 | When I click the button on the the collar that is already assigned to my account, then I nothing happens and I don't see my collar in the list of found collars. |  |
| ME03-US72-AC22 | When connection error occur after user clicks 'Add Collar' button and the process of scanning has started, then I see toast message N31. |  |
| ME03-US72-AC23 | When communication error occur after user clicks 'Add Collar' button and the process of scanning has started, then I see M126, after I click Cancel button scanning process resumes. |  |
| ME03-US72-AC08 | The following elements should be added to the animation on 'Connecting over Bluetooth' screen:\<Collar model\> icon \<Collar SN\>\<Collar type\> | iOS Android |
| ME03-US72-AC09 | The following changes should be made on 'Collar has been securely added to your account' screen:The following elements should be added to collar's imagery:\<Collar model\> icon \<Collar SN\>\<Collar type\>The text should be added:'Collar can have only one account owner at a time. You can find details about your collar on 'My account' page on our web site.' where 'My account' is a link to halocollar.com The 'Done' button should be renamed to 'Next' - After user clicks the 'Next' button, then the flow resumes on Choosing a Wi-fi network screen. | iOS Androidadd_collar-pairing-bluetooth.mp4 need to remove back arrow |
| ME03-US72-AC10 (TBD - can be implemented later as improve) | For collars shipped by IPDD: The color of collar on the imagery should be the same as a real collar user has purchased.If the collar was not shipped by IPDD and we doesn't have the information about it's color then we display the default ivory model image. |  |
| ME03-US72-AC11 | If the collar found via Bluetooth scan has:has new FW,Power button is pressed, collar is assigned to another account, then 'Add New Collar - Select Collar to Add' screen is displayed with the following elements:'Back' button'Add New Collar' title'This Halo Collar is Assigned to Another Account' subtitleThe found collar with:\<Collar model\> icon \<Collar SN\>\<Collar type\>'The Halo Collar belongs to another account, it must be removed from the previous account before you can add it.' text 'Done' button'Why don't I see my Halo Collar' link | iOS Android need to make some changes |
| ME03-US72-AC12 | If all found collar(s) has the old FW or there's combination of collars with old FW and collar with new FW assigned to another account (button pressed),then 'Add New Collar - Select Collar to Add' screen should consist of: For ios - 'Close' button, for android - 'X', 'Add New Collar' title'Select a Halo Collar to Add' subtitle 'Why don't I see my Halo Collar' linkThe list of the found collars: \<Collar model\> icon \<Collar SN\>\<Collar type\>'Assigned to Another Account' subtitle'The Halo collars listed below belong to another account, they must be removed from the previous account before you can add them.' text The list of the found collars:\<Collar model\> icon \<Collar SN\>\<Collar type\> | need to remove'next' buttoniOS Android |
| ME03-US72-AC13 | The 'Assigned to Another Account' section should not be visible if there's no collars assigned to another accounts on the list |  |
| ME03-US72-AC14 | If I click 'Next' on 'Add New Collar - Select Collar to Add' screen and neither user nor collar have active subscription, then 'You need a plan' screen should be opened (see the design) with the following elements'You need a plan' titleThe set of UI elements described in ME19-US16 Subscription plan upgrade prompting screen. |  |
| ME03-US72-AC15 | If I have a list of collars displayed on 'Add New Collar - Select Collar to Add' screen and then the collar with new firmware and button pressed is found then I automatically redirected to 'Connecting over Bluetooth' screen displaying the data of the collar with pressed button. |  |
| ME03-US72-AC16 | If the collar is assigned to another account, then it should be displayed under 'Assigned to Another Account' section on the list. The collar assigned to another user cannot be selected. |  |
| ME03-US72-AC17 | If I tap on 'Why don't I see my Halo Collar' link, then the following page should be opened using the default browser: https://support.halocollar.com/hc/en-us/articles/5082602354583 |  |
| ME03-US72-AC18 | I can select a collar from the list via a tap on the collar tile (relates only to the collars with old FW). When I tap on the collar in the list then I see 'Connecting over Bluetooth' screen |  |
| ME03-US72-AC19 | Precondition: collar is deactivated, is displayed in general list of collar (not under 'Assigned to Another Account' section)If I tap the collar tile then the app should display M192 Deactivated collar.Note: If deactivated collar has new FW version, then it will not be displayed anywhere during the process of adding collar via Bluetooth. HALO-12823 - MOB: ME03-US88. Handling deactivated collar with new FW while adding to the account Closed Need to discuss the improve for deactivated accounts. |  |
| ME03-US72-AC20 | In case Bluetooth on smartphone is turned off during the collar scanning, then:M178 Disabled Bluetooth (Wi-Fi setup, Add Beacon) popup should be displayed.After Bluetooth connection resumes at the same screen where it was interrupted |  |
| ME03-US72-AC24 | If Bluetooth is turned off when the collar is added to the account then nothing happens and I will not see 'Bluetooth is Disabled' screen. |  |
| ME03-US72-AC25 | 'Bluetooth is Disabled' empty state screen should have the following elements:Title: Add CollarButton: arrow icon for iOS and 'x' for AndroidSubtitle: Bluetooth Is DisabledText: Please turn Bluetooth ON in your device settings to continue. Bluetooth is needed to pair your Halo collar and connect it to the app. | ios |### Diagram


