---
title: "[Duplicate] ME21-US17. Onboarding: Step 4: Сollar update"
sidebar_label: "[Duplicate] ME21-US17. Onboarding: Step 4: Сollar update"
sidebar_position: 250
last_modified: "Oct 05, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
|  |
| Add new ticket |
| Click here to expand...05 Oct 2022 Maria Shikareva [X] Marked the story as 'Duplicate' because another page was created: [NI] ME21-US35. Onboarding: Updates for 'Collar Update' flow. |# Need to revisit requirements for Onboarding - these are just copied from the main flow

# Contents

Need to revisit requirements for Onboarding - these are just copied from the main flow Assumptions User story Acceptance criteria Both Collar's FW and SGEE data are Up-to-Date Collar's FW and/ or SGEE data are Outdated Errors handling Implementation notes

# Assumptions

1. This story will be released as a next step for 'Add collar' flow after Wi-Fi setup.
2. Video screen will not be implemented within this story.
3. An 'info' icon will be added to all screens within a separate story.
4. A stepper will be added to all screens within a separate story.
5. The collar starts FW updates/ SGEE downloading immediately as soon as all conditions are met.
6. Turning the collar OFF during the flow will be described within a separate story.
7. The collar will send FW update statuses to BE:
  1. if the collar is online, then immediately;
  2. if the collar is offline, then right after the collar becomes online → it will send all missed statuses.

8. If the FW package is deleted:
  1. during downloading phase - it's impossible, BE doesn't delete files;
  2. during applying phase - in this case TWIN won't be updated and the collar will try to download this file again.

9. When FW update is started/ completed, the user will receive a push-notification and if they tap on it, nothing happens → the app won't open a 'Notifications' tab (see the existing requirements inME08-US19-AC05)
10. There's no priority in updating FW/ downloading SGEE manifest/ downloading SGEE tar files.
11. It's OK to use "Collar Update" wording instead of "Firmware Update" → this is more clear to the users.
12. If connection is lost during FW update, the the collar waits for the same interface for 12 hours:
  1. if the connection appears using the same interface, then the collar starts FW update again;
  2. if connection doesn't appear, the the collar puts FW update to the queue to download it via any interface.

# User story

\> As a Halo app user I want to have my collar ready-to-go with updated FW and up-to-date satellite data so that to be sure that I have the latest performance improvements and the most accurate location data.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| Preconditions: a user has successfully configured Wi-FiORa user skipped configuring Wi-Fi and tapped 'Continue Without Wi-Fi' button. |
| ME21-US07-AC01 | The app should:check whether FW update and satellite data are up-to-date;open a 'Collar Update' screen with a spinner. | - | - |
| ME21-US07-AC02 | A 'Collar Update' screen should have the following UI elements:'Collar Update' title;spinner. | - | - |
| ME21-US07-AC03 | Connection and communication errors are handled according to ME14-F01 Unified errors handling, where "Collar Updates data is" wording should be used instead of \<items\>.For BA: Need to update ME14-F01-AC08 and ME14-F01-AC09. | - | - |
| Both Collar's FW and SGEE data are Up-to-Date |
| ME21-US07-AC04 | The app should display 'Your Halo Collar and Satellite Data Are Up-To-Date' screen with the following elements:'Your Halo Collar and Satellite Data Are Up-To-Date' title;'Halo continuously improves the performance of your Halo collar(s) - updates come every month! Your Halo collar will automatically download and then apply the latest version and satellite data while charging and connected to the Internet.' text;an image "Collar is on charge, LED is green"'Done' button. | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US07-AC05 | When the user taps 'Done' button, then the app:should close the "Your Halo Collar and Satellite Data Are Up-To-Date" screen;redirect the user to the Collar List (see ME03-F01. Collars list).Note: in the 'Onboarding' flow the app should open the next step as described in ME21-US08. Onboarding: GPS calibration screens. | - | - |
| Collar's FW and/ or SGEE data are Outdated |
| Preconditions: Wi-Fi isn't configuredANDthere's no LTE on the collar. |
| ME21-US07-AC06 | The app should display 'Halo Collar and Satellite Data Updates' screen with the following elements:'Halo Collar and Satellite Data Updates' title;'It's important to keep your Halo collar upgraded for better performance and more accurate and precise location. Though the collar will continue to work properly when not up-to-date, we highly recommended updating at your earliest convenience. Your Halo collar will automatically download and then apply the latest version and satellite data while charging and connected to the Internet.' text;an image "Collar is on charge, LED is green"'Done' button.Note: as soon as we can't say definitely that the FW and SGEE are outdated because the collar is offline, it's better to show a note explaining the importance of such updates. | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US07-AC07 | When the user taps 'Done' button, then the app:should close the "Your Halo Collar and Satellite Data Are Outdated" screen;redirect the user to the Collar List (see ME03-F01. Collars list).Note: in the 'Onboarding' flow the app should open the next step as described in ME21-US08. Onboarding: GPS calibration screens. | - | - |
| Preconditions: Wi-Fi isn't configured AND there is LTE on the collarORWi-Fi is configuredANDthe collar isn't plugged. |
| ME21-US07-AC08 | The app should display 'Your Halo Collar Is Not Plugged In' screen with the following elements:'Your Halo Collar Is Not Plugged In' title;'For the safety of your dog, your Halo collar will only upgrade if it's charging and has a minimum level of charge. Please plug in your Halo now to continue.'an image "Collar is on charge";'Have trouble updating?' text;'Use the wired update method.' link.'Continue Without Update' button.It should appear after 5 minutes of displaying this screen.'Next' button.TBD with Michael: internally we discussed that as soon as the text will be the same on the next screen and usually it's more convenient for the user to see next steps automatically, so it's better not to display this 'Next' button.BA note: the user should not be able to skip this step. | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US07-AC09 | The video should be animated.Dev note (as confirmed with Margarita Yasinskaya): vector graphic won't work for this animation as we have real photos of the collar, therefore it's more likely to be a gif animation. | - | - |
| Preconditions: Wi-Fi isn't configured AND there is LTE on the collarORWi-Fi is configuredANDthe collar is pluggedANDbattery level ≤ 20%. |
| ME21-US07-AC10 | The app should display 'Please Charge Your Halo Collar to Continue' screen with the following elements:'Please Charge Your Halo Collar to Continue' title;'For the safety of your dog, your Halo collar will only upgrade if it's charging and has a minimum level of charge. Please wait a while longer while it charges.' text;Charging status:charging battery icon;current battery level\> %'(waiting for 20% charge)' textan image "Collar is on charge, LED is green";'Have trouble updating?' text;'Use the wired update method.' link.'Continue Without Update' button.It should appear after 5 minutes of displaying this screen.TBD with Michael: we'd like to display this button in advance if we definitely know that the collar won't be able to charge to 20%. E.g. if the current % is less than 15%.TBD with Michael: what should be done with a link? Assumption: we should hide it.Dev note: the app should be able to get the updated data from BE as soon as possible so that to show relevant statuses to a user. | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US07-AC11 | The app should display 'Please Charge Your Halo Collar to Continue' screen until:the battery is charged to 20%ORthe user taps 'Continue Without Update' button. | - | - |
| Preconditions: Wi-Fi isn't configured AND there is LTE on the collarORWi-Fi is configuredANDthe collar is pluggedANDbattery level \>20%. |
| ME21-US07-AC12 | The app should display 'Your Halo Collar Update' screen with the following elements:'Your Halo Collar Update' title;'For the safety of your dog, your Halo collar will only upgrade if it's plugged in. Please leave your Halo plugged in while it is upgrading.' text;Updating status with a number of a step with a progress bar.'Can take about 5 minutes'. note;Assumption: it's OK to display here 5 minutes though FW update via LTE can take about 10 minutes.an image "Collar is on charge, LED is red";'Have trouble updating?' text;'Use the wired update method.' link. | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US07-AC13 | Possible updating statuses (applicable for FW update only):Downloading;Verifying;Applying. | - | - |
| ME21-US07-AC14 | Progress bar should be divided into 3 parts and depend on the updating status: the app should fulfill the progress bar right after the previous step is completed.Note: as of 06 Jul 2022 the collar doesn't send info about the progress of FW update, but there's a task for future: HALO-12792 - MOB: Update GAP/GATT protocol about Firmware Update Progress Open . | - | - |
| ME21-US07-AC15 | Precondition: collar FW update AND SGEE downloading are successfully completed.The app should display 'Your Halo Collar and Satellite Data Are Up-To-Date' screen (see ME21-US07-AC02).Dev note: the app should be able to get the updated data from BE as soon as possible so that to show relevant statuses to a user. | - | - |
| ME21-US07-AC16 | Precondition: collar FW update is successfully completedANDthere's no info about SGEE downloading (as soon as the collar doesn't report if the SGEE downloading started OR SGEE was downloaded before FW update and the collar didn't report "completed' status because of Outdated FW).The app should display 'Your Halo Collar Is Up-To-Date' screen: the same as described in ME21-US07-AC02 with the only difference:'Your Halo Collar Is Up-To-Date' title.'If your Halo Collar GPS LED is blinking pink, it means that the collar is downloading satellite position data. Please wait up to 5 minutes until the LED remains off.' text. | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US07-AC17 | 'Use the wired update method' should be a link to a Zendesk article and should be opened in the mobile browser: https://support.halocollar.com/hc/en-us/articles/360055259994-How-to-apply-a-wired-firmware-update-to-your-collar.Note: if the user starts updating FW using wired method and turns the collar OFF, then the app will display a "Continue Without Update" button after 5 minutes. | - | - |
| ME21-US07-AC18 | If the user unplugs the collar during collar update (any step), then the app should display "Your Halo Collar Is Not Plugged In" screen (see ME21-US07-AC06).Dev note: the app should be able to get the updated data from BE as soon as possible so that to show relevant statuses to a user. | - | - |
| Errors handling |
| ME21-US07-AC19 | Precondition: 'Your Halo Collar Update' screen is displayed.If the update continues for more than 5 minutes, then the app should display another state of "Your Halo Collar Update" with the following elements:'Your Halo Collar Update' title;'For the safety of your dog, your Halo Collar will only upgrade if it's charging and has a minimum level of charge. Please leave your Halo plugged in while it is upgrading.' text;Updating status with a progress bar.'Seems like it might take longer than expected. You can wait some more or update later'. note;an image "Collar is on charge, LED is red.'Continue Without Update' button. TBD with Michael that a link will be hidden. | Link to Zeplin | The same as for iOS.Link to Zeplin |
| ME21-US07-AC20 | Precondition: Connection is lost during downloading FW update.The app should display "Connection Lost" screen with the following elements:'Connection Lost' title;'Your Halo Collar will automatically download and then apply the latest version and satellite data while charging and connected to the Internet again.' text;an alert icon;"Download Failed" status;an image "Collar is on charge, LED is red";'Continue Without Update' button.Note: the app will be able to know this info only if the collar has 2 connection types (Wi-Fi and LTE) and for now one of them is lost (using which FW update is downloading). If there was only 1 connection type available and now it's lost, then we'll never know 100% exactly that connection is lost, the collar just stops reporting, therefore the app will show a 'Continue Without Update' button after 5 minutes waiting. | Update the |  |
| ME21-US07-AC21 | Precondition: FW update downloading/ verifying/ applying failed.The app should display "Collar Update Failed" screen with the following elements:'Collar Update Failed' title;'Your Halo Collar will automatically download and then apply the latest version and satellite data while charging and connected to the Internet again.' text;an alert icon;failed status;an image "Collar is on charge, LED is red";'Continue Without Update' button. |  |  |
| ME21-US07-AC22 | Possible failed statuses:download failed;verify failed;apply failed.Note: this only applicable for FW update because the collars doesn't report the same statuses for SGEE downloading. | - | - |
| ME21-US07-AC23 | When a user taps on a 'Continue Without Update' button, then the app should:display a MTBD pop-up:Title: "Continue Without Update"Body: "It's important to have an updated collar to receive new features and performance improvements. Your Halo Collar will automatically download and then apply the latest version and satellite data while charging and connected to the Internet."Buttons: 'Continue Update', 'Update Collar Later'Add to Appendix 3 – Error, Success, Warning Messages. | Update the | - |
| ME21-US07-AC24 | Precondition: MTBD is opened.When the user taps on 'Continue Update' button, the app should:close the pop-up;keep the previous screen opened. | - | - |
| ME21-US07-AC25 | Precondition: MTBD is opened.When the user taps on 'Update Collar Later' button, the app should:close the pop-up and the screen;redirect the user to the Collar List (see ME03-F01. Collars list).Note: in the 'Onboarding' flow the app should perform actions as described in ME21-US08. Onboarding: GPS calibration screens. | - | - |
| ME21-US07-AC26 | '5 minutes' should be a configurable value. |  |  |# Implementation notes

| IN | Description |
|---|---|
| ME21-US07-IN01 | FW feature is required for reporting this state |
