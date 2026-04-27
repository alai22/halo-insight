---
title: "[Postponed] ME04-US07. Create a fence, that has a common border with another one"
sidebar_label: "[Postponed] ME04-US07. Create a fence, that has a common border with another one"
sidebar_position: 73
last_modified: "Jun 05, 2020"
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Document owner | Link with Jira | Revision history |
|---|---|---|---|---|---|
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| DRAFT |
| Diana Aladina |
|  |
|  |## ME04-US07. Create a fence, that has a common border with another one

### User story

As a user, I would like to create a fence and connect its border with an existing fence, so that I have several zones with common borders.

### Acceptance criteria

| AC | Screens | Text |
|---|---|---|
| ME04-US07-AC01 |  | Precondition: a user has at least one existing fence on the map. A user can't create a fence that overlaps territory of another one. But a user should be able to create a fence, that shares a border with another zone. |
| ME04-US07-AC02 | Screen ME04-11- Create Common Border | Types of dots placement regarding another fence:a user taps a dot that doesn't affect another fence → the dot remains on the specified positiona user taps a dot that is on the border of another fence, without crossing other sides → the dot remains on the specified positiona user taps a dot inside another fence (only 1 side of the polygon is involved) → the dot is moved to the border of existing fence along the trajectory towards the nearest side of the zonea user taps a dot inside another fence (2+ sides of the polygon are involved) → the dot is moved to the border of existing fence along the trajectory towards the nearest side of the zone, new dots are automatically placed on the other sides and corners of future common border to surround existing fence and exclude overlappinga user taps a dot outside existing fence, but a new line will cross that fence border(s) → the dot remains on the specified position, existing fence is surrounded with addition dots on the border from the system to exclude overlapping |
| ME04-US07-AC03 |  | When a user creates/edits a fence and next dot will lead to intersection of different fences areas, the system should automatically go around the existing border with dots along the previous trajectory.the system should move dots to the border along the trajectory, if a user puts it inside existing fencethe system should add additional dots itself, when the line tends to cross more than 1 side of existing fencethe system should add dots on the corner(s) of the sides, when the line tends to cross more than 1 side of existing fence |
| ME04-US07-AC04 |  | When a user taps a dot that will be moved to the border or will lead to adding extra dots on the border → the app should show a message: "Fence was adjusted because safe zones can't overlap". This message a user sees every time this situation happens. |
| ME04-US07-AC05 |  | "Common Border" does not refer to single points which are shared (i.e. if only one point has been "snapped" to another fence, this does not create a shared border because a pet cannot safely move through one single point). Common borders require a minimum of one shared line segment (two dots).If there are no ways to close a fence without overlapping another one, the app should show a message on the screen: "Impossible to create a fence without overlaying others. Try to create another shape" → last attempt to tap a dot is failed, it is not placed om the map |
| ME04-US07-AC06 |  | If 2 active fences have a common border, a pet should cross it both ways without any corrections.If two fences have a common border and one of them becomes inactive → "paused" warning area should become active. The same case when a user deletes a fence, that had a common border with another one. |
| Warning area |
| ME04-US07-AC07 |  | When a user confirms drawn fence and goes to the next step "Warning Area", they should see special animation. This animation will explain the logic of corrections and common borders.Animation logic:Animation should show a user an example of two generic fences with a common border. Fence #1 is the preexisting fence, Fence #2 is the newly-created fence. Fence #1 starts with active status, then switches to inactive. Fence #2 starts with "paused" warning area. While Fence #1 switches to inactive, Fence #2 warning area "fills in" to show a normal warning areaAnimation should include tip text with message: "You have created fences that share a common border. When both fences are active, your pet can safely move between both fences without being warned or corrected"Tip text area should have "Got It" button; User must confirm their understanding with "Got It" button in order to stop animationAnimation continues on an infinite loop until user confirmsAfter a user taps "Got it", user returns to normal warning area screen and sees their own fences |
| ME04-US07-AC08 |  | Warning area that is not active due to common a border should be marked differently on Warning area screen. |
| Created fence with common border |
| ME04-US07-AC09 |  | All fences with common borders should have same appearance with rounded corners as other fences. Dots should not move from original location in order to round the corners. |
| ME04-US07-AC10 | Screen ME04-12- Common border, active fences | Created fence that has a common border with another one should have an icon on the map that user can tap. It will appear on top of the shared border. Icon will provide information about shared border.Icon should appear on top of any location where fences have common borders. If Fence #2 shares common borders with 3 other fences, this icon should appear in 3 different locations on all 3 borders that are shared with other fencesUser's and pet's pins should have a priority over this icon |
| ME04-US07-AC11 | Screen ME04-13- Common border with inactive fence | When a user taps information icon, information appears in standard "card" location on-screen. Message can have two options:When both fences are active: "These two fences are both active and share a common border. Your pet(s) can safely move between both fences without warnings or corrections while they are both active"When one fence is inactive and the other is active: "These two fences share a common border, but only one is active. Your pet(s) will receive warnings and corrections normally from the active fence. Your pet(s) cannot move between these two fences unless both fences are active"Small preview of animation from warning area screen from fence creation appears in "card" body for both optionCard behaves normally and disappears when user taps anywhere else on the screenIcon should disappear, when both fences, that have a common border, are inactive. |
