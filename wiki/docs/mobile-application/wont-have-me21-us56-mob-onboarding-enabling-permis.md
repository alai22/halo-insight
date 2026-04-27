---
title: "(Won't have) ME21-US56. MOB: Onboarding: Enabling Permissions screen rework"
sidebar_label: "(Won't have) ME21-US56. MOB: Onboarding: Enabling Permissions screen rework"
sidebar_position: 344
last_modified: "May 10, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA issue |  |
|---|---|---|---|
| DRAFT |
| Kiryl Trafimau |
| HALO-17857 - MOB: Enable permissions rework Closed |
|  |# User story

\> As Halo app account owner, I want to view list of permissions required for Halo app so that I can manage permissions required for Halo app

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME21-US56-AC01 | WHEN I am on the 'Enable Permissions' screenTHEN I see the title 'Enabling Permissions' |  |
| ME21-US56-AC02 | AS IS:WHEN I am on the 'Enabling Permissions' screenTHEN I can see:-'Select' button on the Location Access card-'Select' button on the Bluetooth Access card-'Select' button on the Push Notifications cardTO BE:WHEN I am on the 'Enable Permissions' screenTHEN I can see:-'Enable' button on the Location Access card-'Enable' button on the Bluetooth Access card-'Enable' button on the Push Notifications card |  |
| ME21-US56-AC03 | Pre-condition: I am on the 'Enabling Permissions' screenAS IS:IF At least one 'Enable' button is displayed on the screenTHEN I can see disabled 'Next' button in the bottom of the screenTO BE:IF At least one 'Enable' button is displayed on the screenTHEN I can see 'Enable All' button in the bottom of the screen (not disabled) |  |
| ME21-US56-AC04 | Pre-conditions: I am on the 'Enabling Permissions' screenAll 'Enable' buttons are displayed on the screen (for Location Access, for Bluetooth Access, for push-notifications)WHEN I click 'Enable All' buttonTHEN Permission is requested for all permissions AND Pop-ups should be displayed one-by-one in the order permissions mentioned (Location-\>Bluetooth-\>Push-notifications) |  |
| ME21-US56-AC05 | Pre-conditions: I am on the 'Enabling Permissions' screenNot all 'Enable' buttons are displayed on the screen (for Location Access, for Bluetooth Access, for push-notifications) = at least for one of the permissions ON or OFF already displayed.WHEN I click 'Enable All' buttonTHEN Permission is requested for all permissions, for which 'Enable' button is displayedAND Pop-ups should be displayed one-by-one in the order permissions mentioned (Location-\>Bluetooth-\>Push-notifications) without permissions which was already requested |  |
| ME21-US56-AC06 | Pre-condition: I am on the 'Enabling Permissions' screenIF There is no any 'Enable' button displayed on the screen (for Location Access, for Bluetooth Access, or for push-notifications)THEN I can see 'Next' button in the bottom of the screen (not disabled) |  |
| ME21-US56-AC07 | WHEN I am on the 'Enabling Permissions' screenTHEN I can see 'Help for Halo Collar setup' tip near the ? button for 3 seconds after screen openedAND I should not see 'Help for Halo Collar setup' tip after 3 seconds passed |  |
| ME21-US56-AC08 | WHEN I am on the 'Enabling Permissions' screen AND Onboarding has been already passedTHEN I should not see 'Help for Halo Collar setup' tip |  |### Implementation Notes

| IN | Description |
|---|---|
|  |  |
