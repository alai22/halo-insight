---
title: "ME21-US32. Onboarding: Updates for 'Add Collar' flow"
sidebar_label: "ME21-US32. Onboarding: Updates for 'Add Collar' flow"
sidebar_position: 269
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Timofey Burak [X] Dmitry Kravchuk Yekaterina Hovin |
| Click here to expand... HALO-14140 - MOB: ME21-US32. Onboarding: Updates for 'Add Collar' flow Closed |
| Click here to expand...08 Nov 2022 Maria Shikareva [X] Crossed out ME21-US32-AC09 as discussed with Siarhei Leushunou [X] (this logic is already implemented).23 Nov 2022 Maria Shikareva [X] Updated ME21-US32-AC05 to give more details about iOS/ Android behavior differences.25 Nov 2022 Maria Shikareva [X] Updated 'Halo Collar Has Been Securely Added to Your Account' section (it turned out that in the main flow 'Done' button was already renamed to 'Next'). |# Contents

User story Acceptance criteria 'Power Up & Connect' screen 'Charge Your Halo Collar' screen 'Link Your Halo Collar to Your Account' screen 'Halo Collar Has Been Securely Added to Your Account' screen 'This Halo Collar Is Assigned to Another Account' screen Add a question mark icon Other changes Subscription related restrictions Implementation notes

# User story

\> As a Halo business owner I want to have the screens for the 'Add Collar' flow updated so that they are ready to be included into the Onboarding flow.

# Acceptance criteria

| AC | Description | iOS screens designs | Android screens designs | Main flow | Onboarding flow | AS IS | TO BE | AS IS | TO BE | AS IS | TO BE | Main flow | Onboarding flow | AS IS | TO BE | Main flow | Onboarding flow | AS IS | TO BE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 'Power Up & Connect' screen |
| ME21-US32-AC01 | Entry points (only within Onboarding):a user tapped 'Next' on the 'What's in Your Halo Collar Kit' screen ORa user tapped 'Watch Later' button in the M262 Please Watch the Video! on the 'What's in Your Halo Collar Kit' screen. | Link to Zeplin | Link to Zeplin |
| ME21-US32-AC02 | 'Return to Start' button should be added to the 'Power Up & Connect' screen. |
| ME21-US32-AC03 | When a user taps on the 'Add Collar' button OR 'Watch Later' button in the M262 Please Watch the Video!, then the app navigates them to the 'Charge Your Halo Collar' screen (with Subscription restriction described in ME21-US32-AC21 below). |
| ME21-US32-AC04 | When a user taps on the 'Return to Start' button, then the app navigates them to the 'Do You Have a Halo Collar?' screen.Note: see ME21-US32-IN01 below. |
| 'Charge Your Halo Collar' screen |
| ME21-US32-AC05 | Main flowOnboarding flowWhen 'Charge Your Halo Collar' screen is opened from the app not within Onboarding flow (e.g. when a user adds a second collar), the app should display a 'Cancel'/ 'x' button (leave as is).'Cancel'/ 'x' button should be changed to '\<' when 'Charge Your Halo Collar' screen is opened within Onboarding flow, which navigates a user to the "Power Up & Connect" screen with video. | When 'Charge Your Halo Collar' screen is opened from the app not within Onboarding flow (e.g. when a user adds a second collar), the app should display a 'Cancel'/ 'x' button (leave as is). | 'Cancel'/ 'x' button should be changed to '\<' when 'Charge Your Halo Collar' screen is opened within Onboarding flow, which navigates a user to the "Power Up & Connect" screen with video. | Link to Zeplin | Link to Zeplin |
| When 'Charge Your Halo Collar' screen is opened from the app not within Onboarding flow (e.g. when a user adds a second collar), the app should display a 'Cancel'/ 'x' button (leave as is). | 'Cancel'/ 'x' button should be changed to '\<' when 'Charge Your Halo Collar' screen is opened within Onboarding flow, which navigates a user to the "Power Up & Connect" screen with video. |
| 'Link Your Halo Collar to Your Account' screen |
| ME21-US32-AC06 | The title should be changed to match capitalization rules (see GUI-6 Style for buttons, links and screen titles):AS ISTO BELink your Halo Collar to Your AccountLink Your Halo Collar to Your Account | Link your Halo Collar to Your Account | Link Your Halo Collar to Your Account | Link to Zeplin | Link to Zeplin |
| Link your Halo Collar to Your Account | Link Your Halo Collar to Your Account |
| ME21-US32-AC07 | The placeholder picture should be changed (to match new design with a yellow Halo label):BA note: we don't change a picture on the 'Connecting over Bluetooth' screen and in the list of found collars because here the app shows a user's real collar taken from BE. |
| ME21-US32-AC08 | The tile with found collars should be changed (updates are highlighted in blue):AS ISTO BE\<Collar model\> icon \<Collar SN\>\<Collar type\>\<Collar model\> icon \<Collar SN\>\<Collar type\>a right arrow icon.QA note 1: ME03-FE00-AC57 isn't relevant anymore.QA note 2: the best way to test this screen is to try to add a collar with old FW.QA note 3: further behavior should remain as is:Preconditions: the user tapped on the found collarANDall validations are successful.1. The app should navigate the user to the next screen: 'Connecting over Bluetooth' screen.2. 'Next' button should not appear, checkmark should not appear. | \<Collar model\> icon \<Collar SN\>\<Collar type\> | \<Collar model\> icon \<Collar SN\>\<Collar type\>a right arrow icon. | Link to Zeplin | Link to Zeplin |
| \<Collar model\> icon \<Collar SN\>\<Collar type\> | \<Collar model\> icon \<Collar SN\>\<Collar type\>a right arrow icon. |
| ME21-US32-AC09 | Preconditions: the user tapped on the found collarANDall validations are successful.The following changes should be made:AS ISTO BEThe selected collar should be displayed with a checkmark.'Next' button is displayed.When a user tap on the 'Next' button, then the app opens the 'Connecting over Bluetooth' screen.The app should navigate the user to the next screen: 'Connecting over Bluetooth' screen.'Next' button should not appear, checkmark should not appear.QA note: ME03-FE00-AC62 isn't relevant anymore. | The selected collar should be displayed with a checkmark.'Next' button is displayed.When a user tap on the 'Next' button, then the app opens the 'Connecting over Bluetooth' screen. | The app should navigate the user to the next screen: 'Connecting over Bluetooth' screen.'Next' button should not appear, checkmark should not appear. |
| The selected collar should be displayed with a checkmark.'Next' button is displayed.When a user tap on the 'Next' button, then the app opens the 'Connecting over Bluetooth' screen. | The app should navigate the user to the next screen: 'Connecting over Bluetooth' screen.'Next' button should not appear, checkmark should not appear. |
| 'Halo Collar Has Been Securely Added to Your Account' screen |
| ME21-US32-AC10 | Main flowOnboarding flow'Next' button should remain as is.'Done' button should be renamed to the 'Next' button. | 'Next' button should remain as is. | 'Done' button should be renamed to the 'Next' button. | Link to Zeplin | Link to Zeplin |
| 'Next' button should remain as is. | 'Done' button should be renamed to the 'Next' button. |
| ME21-US32-AC11 | 'Next' button should be moved to the bottom. |
| ME21-US32-AC12 | Content of this screen should be scrollable except the bottom part with the 'Next' buttons. |
| ME21-US32-AC13 | When a user taps 'Next' button, then the app should navigate a user to 'Assign Your Halo Collar to Your Dog' screen.Note: on tapping 'Done' the logic shouldn't be changed. |
| 'This Halo Collar Is Assigned to Another Account' screen |
| ME21-US32-AC14 | The title should be changed to match capitalization rules (see GUI-6 Style for buttons, links and screen titles):AS ISTO BEThis Halo Collar Is Assigned To Another AccountThis Halo Collar Is Assigned to Another Account | This Halo Collar Is Assigned To Another Account | This Halo Collar Is Assigned to Another Account | Link to Zeplin | Link to Zeplin |
| This Halo Collar Is Assigned To Another Account | This Halo Collar Is Assigned to Another Account |
| ME21-US32-AC15 | 'Done' button should be moved to the bottom.BA note: it's OK to have a 'Done' button here (not 'Next' because tapping on this button ends a flow of adding a collar). |
| ME21-US32-AC16 | Content of this screen should be scrollable except the bottom part with the 'Done' button. |
| ME21-US32-AC17 | Main flowOnboarding flowIf opened not within Onboarding, then the flow should remain as is (as described in ME03-F00-AC70).When a user taps 'Done' button, then the app should navigate a user to the 'Power Up & Connect' screen. | If opened not within Onboarding, then the flow should remain as is (as described in ME03-F00-AC70). | When a user taps 'Done' button, then the app should navigate a user to the 'Power Up & Connect' screen. |
| If opened not within Onboarding, then the flow should remain as is (as described in ME03-F00-AC70). | When a user taps 'Done' button, then the app should navigate a user to the 'Power Up & Connect' screen. |
| Add a question mark icon |
| ME21-US32-AC18 | A question mark tappable icon should be displayed at the left upper corner on the following screens (both opened within the main flow and Onboarding):'Power Up & Connect' screen;'Charge Your Halo Collar' screen;'Link Your Halo Collar to Your Account' screen;'Bluetooth Is Disabled' screen;'Connecting Over Bluetooth' screen;'Halo Collar Has Been Securely Added to Your Account' screen;'This Halo Collar Is Assigned to Another Account' screen. | - | - |
| ME21-US32-AC19 | When a user taps on a question mark icon, then the app should open the 'Need Help?' screen. | - | - |
| Other changes |
| ME21-US32-AC20 | The text of M192 Deactivated collar should be changed:AS ISTO BETitle: ErrorBody: This collar is deactivated. Please contact Halo customer support.Button: OKTitle: This Halo Collar Is Assigned to Another AccountBody: This collar was previously used and was deactivated for security reasons. To learn more, please contact us at the Halo Store in the Halo Dog Park™. Or, select and add another Halo Collar to your account.Button: OK | Title: ErrorBody: This collar is deactivated. Please contact Halo customer support.Button: OK | Title: This Halo Collar Is Assigned to Another AccountBody: This collar was previously used and was deactivated for security reasons. To learn more, please contact us at the Halo Store in the Halo Dog Park™. Or, select and add another Halo Collar to your account.Button: OK | - | - |
| Title: ErrorBody: This collar is deactivated. Please contact Halo customer support.Button: OK | Title: This Halo Collar Is Assigned to Another AccountBody: This collar was previously used and was deactivated for security reasons. To learn more, please contact us at the Halo Store in the Halo Dog Park™. Or, select and add another Halo Collar to your account.Button: OK |
| Subscription related restrictions |
| ME21-US32-AC21 | Precondition: a user doesn't have active subscription (i.e. has 'No plan').When a user taps 'Add Collar' button on 'Power Up & Connect' screen OR 'Watch Later' button in the M262 Please Watch the Video!, then the app should display a prompting screen video.BA note: new info about subscriptions will be received only on bringing the app to foreground - this is an existing logic through the whole app. There's an epic with related task for future: HALO-9645 - WebSockets Kaizen Open | - | - |
| ME21-US32-AC22 | Precondition: a prompting screen video is displayed.When a user taps on a 'Close' button, the app should:close a prompting screen;leave 'Power Up & Connect' screen opened. | - | - |# Implementation notes

| ID | Description |
|---|---|
| ME21-US32-IN01 | Implementation notes: on returning back to start it's needed to refresh navigation stack. |
