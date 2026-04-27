---
title: "[BL] ME03-US88. Handling deactivated collar with new FW while adding to the account"
sidebar_label: "[BL] ME03-US88. Handling deactivated collar with new FW while adding to the account"
sidebar_position: 255
last_modified: "Sep 23, 2022"
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Valeryia Chyrkun [X] Dmitry Kravchuk Timofey Burak [X] Yekaterina Hovin |
| HALO-12823 - MOB: ME03-US88. Handling deactivated collar with new FW while adding to the account Closed |
| Click here to expand...12 Sep 2022 Maria Shikareva [X]Changed a title from '...old FW' to ... 'new FW' because the story describes behavior for the deactivated collars with new FWs (see "Question: Adding deactivated collar to the account" email, Jul 22, 2022).Updated ME03-US88-AC04 (the existing behavior is confirmed with Mariya Kolyada). |# General description

During testing we noticed some inconsistency in processing cases when user tries to add the deactivated collar. See email thread 'Question: Adding deactivated collar to the account' for details

# User story

\> As an app user I want to be see the screen which informs me that my collar is deactivated and cannot be added to the account so I am not frustrated by nothing happening when I press the by button on the collar.

# Acceptance criteria

| AC | Text | Screens |
|---|---|---|
| ME03-US88-AC01 | Precondition: user adds the collar to the account and this collar is deactivated (with a new FW version)When I press the button on the collar, then I see the screen with the following elements:Button: arrow icon (Back)Button: DoneTitle: Add CollarSubtitle: This Collar is DeactivatedCollar's image (see ME03-US72-AC08 for details)Text: This collar was previously used and was deactivated for security reasons. To learn more, please contact us at the Halo Store in the Halo Dog Park TM. Or, select and add another Halo Collar to your account. | Zeplin |
| ME03-US88-AC02 | When I click 'Back' button, then I navigated to 'Add New Collar- Select a Collar to Add' screen (ME03-US72-AC05). |  |
| ME03-US88-AC03 | Where 'Halo Store' is a link to Dog Park (Halo Store section). (see ME20-US02-AC01). |  |
| ME03-US88-AC04 | When user navigates to the Dog Park, then after user returning back from the area section they will see first 'Welcome to the Halo Dog Park' screen; after one more tap back - the 'This Collar Is Deactivated' screen (ME03-US88-AC01). |  |
| ME03-US88-AC05 | When I click 'Done' button, then the adding collar flow is closed and I will see the entry point screen (see ME03-US72-AC01). |  |
| ME03-US88-AC06 | Precondition: there are another collars with old FW found via BLE scanning (user is on Select a Halo Collar to Add screen - see ME03-US72-AC12)When I press the button on deactivated collar with New FW, then I see 'This Collar Is Deactivated' screen. When I click 'Back' button on that screen then I see 'Add New Collar- Select a Collar to Add' screen (ME03-US72-AC05) |  |### Diagram


