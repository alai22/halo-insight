---
title: "ME04-US49. Remove the possibility to activate/deactivate fences and filter them on my map"
sidebar_label: "ME04-US49. Remove the possibility to activate/deactivate fences and filter them on my map"
sidebar_position: 86
last_modified: "Aug 12, 2020"
author: "Galina Lonskaya"
---

| Role | Epic | Document status | BA story owner | DEV, QA story owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| Owner |
| ME04 Manage fences |
| APPROVED |
| Galina Lonskaya |
| Pavel Leonenko, Anastasia Brechko, Eugene Paseka |
| HALO-4429 - BE + MOB: Remove the possibility to activate/deactivate fences and filter them on my map Closed |# Intro

\> The update was described by Halo team in the email: "Fences On/Off Confusion" (June 16). "We would like to reduce the complexity for users, so Michael and Ken and I have discussed removing the "active/inactive" toggle switch for all fence cards, and force all fences to always be active. We don't really need this feature anymore. Since we do not allow overlapping fences, and we also do not currently have the "snap to shared boundary" feature, there is no reason to ever deactivate a fence. A user could simply switch the fence mode."

# User story

\> As owner, I don't want to make fence active or inactive because in order to turn off/on the fences I use "Fences on / Fences off" button at the pet's card.

# Acceptance criteria

| AC | Text | New UI design | Map Settings update (the update is valid for My Map and Create New Fence) | Map Settings (an update is valid for Creat New Fence / Edit Fence Posts screen ) |  | Text updates |
|---|---|---|---|---|---|---|
| ME04-US49-AC01 | By default, all fences should be created as active and displayed as active all time. Note: we don't use "active/inactive" terms anymore. | - |
| ME04-US49-AC02 | "Activate/Deactivate fence" toggle, the toggle title, and the tip under the toggle should be removed from the fence card. | Pic 1 - Fence card |
| ME04-US49-AC03 | "Active/Inactive" label and the icon should be removed from the fence card. |
| ME04-US49-AC04 | "Fences" label should be used instead of the "Fence Types" | Pic 2 - Map Settings |
| ME04-US49-AC05 | "Show" option be enabled by default (fences are visible). | - |
| ME04-US49-AC06 | Precondition: "Show" ("Hide") button is selected.If I tap on the Show (Hide) button, then nothing changes (the Show(Hide) button should be still selected).Note for developers: the tapping effect should happen. | - |
| ME04-US49-AC07 | Precondition: "Show" button is enabled. If I tap on the Hide button, then:the Hide button and subtitle should be selected;the Show button and subtitle should be deselected;the fences should be invisible. | - |
| ME04-US49-AC08 | Precondition: "Hide" button is selected.If I tap on the Show button, then:the Show button and subtitle should be selected;the Hide button and subtitle should be deselected;the fences should be visible (if they exist). | - |
| ME04-US49-AC09 | While creating/editing a fence, the Fence filter should not be available.Note: the tappable effect isn't applied. Buttons are disabled (65% opacity). | Pic 3 Map settings, while creating-editing a fence |
| ME04-US49-AC10 | I should always see all fences on the screen when creating or editing a fence. |
| ME04-US49-AC11 | M43 Fence On error text is updated. | - |
| ME04-US49-AC12 | M87 Automatic Fences Off text is updated. | - |
| ME04-US49-AC13 | M83 Fences Off notice text and trigger is updated. | - |
| ME04-US49-AC14 | M82 Updates for the last fence text and trigger is updated. | - |# Implementation notes

| AC | Text | Links/Wireframes/Notes |
|---|---|---|
| ME04-US49-IN01 | Active/inactive fences logic should NOT be removed from the BE side. | - |
| ME04-US49-IN02 | Existed inactive fences should be deleted. | - |
