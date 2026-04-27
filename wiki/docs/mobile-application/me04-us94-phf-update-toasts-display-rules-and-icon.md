---
title: "ME04-US94. PHF. Update toasts' display rules and icons"
sidebar_label: "ME04-US94. PHF. Update toasts' display rules and icons"
sidebar_position: 407
last_modified: "May 02, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-19982 - MOB: ME04-US94. PHF. Update toasts' display rules and icons Closed |
| As of 17 Apr 2024 :Mariya Kolyada created the initial version of US.As of 18 Apr 2024 Mariya Kolyada added criteria related to toasts' icons |# User Story

\> As a Halo accout owner I want to view only up-to-date fence error tosts/warnings relevant to current fence posts state so that I understand what I need to fix.

# Acceptance criteria

| AC | Description | Toast message | Icon As Is | Icon To Be |
|---|---|---|---|---|
| ME04-US94-AC01 | Trigger Zoom In validation on the fence change using the fence itself or Undo/Redo/Delete in the bottom navigation bar:Forbid to add/delete posts until the zoom level is fixed.Move the post back to the previous state on the post's move attempt. |
| ME04-US94-AC02 | PreconditionAny fence error toast is displayed on the screenIf I change the fence somehow using the fence itself or Undo/Redo/Delete, then the app should:Clear the displaying toasts and any toasts in a queue to be displayed (if any).Hide displaying toast.Display the new error toasts relevant to the current fence state if it has any issues.Exception:If road/water/building intersection or fence overlap hasn't been fixed - the app doesn't display toast again. But if user fixes it and produces it later again - they will see toast again, because it is considered a new issue. |
| ME04-US94-AC03 | PreconditionAny fence error toast is displayed on the screenIf I click the 'Save' button, then the app should:Clear the displaying toasts and any toasts in a queue to be displayed (if any).Hide displaying toast.Validate the fence on overlapping with other fences:If this validation is passed - proceed with other existing validations and save following existing rules.If this validation is NOT passed - display the Overlapping fences toast instead of cleared ones. |
| ME04-US94-AC04 | Changing the map view to standard should NOT clear other displaying toast. |
| ME04-US94-AC05 | Update the icons of the listed toast messages following the rules:Toast messageIcon As IsIcon To BePlease zoom in to place a fence post accuratelyYour fence must have at least \{0\} fence postsPlease make sure fence posts are at least 6 feet apart | Please zoom in to place a fence post accurately |  |  | Your fence must have at least \{0\} fence posts | Please make sure fence posts are at least 6 feet apart |  |
| Please zoom in to place a fence post accurately |  |  |
| Your fence must have at least \{0\} fence posts |
| Please make sure fence posts are at least 6 feet apart |  |
