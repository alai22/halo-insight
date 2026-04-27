---
title: "ME04-US44. Highlight the first fence post and add a tip how to close a fence"
sidebar_label: "ME04-US44. Highlight the first fence post and add a tip how to close a fence"
sidebar_position: 664
last_modified: "May 11, 2020"
author: "Galina Lonskaya"
---

| Role | Epic | Document status | BA story owner | QA story owner | DEV story owner | Link to JIRA Issue |
|---|---|---|---|---|---|---|
| Owner |
| ME04 Create fence |
| APPROVED |
| Galina Lonskaya |
| Anastasia Brechko |
| Vadim Pylsky [X] |
| HALO-3709 - MOB: ME04-US44. Highlight the first fence post and add a tip how to close a fence Closed |# User story

\> As owner, I want to view the first fence post with different UI and special tip so that I can easy understand which fence post to tap to close a fence.

# Acceptance criteria

| AC | Text | Links / Notes/ UI Design / Wireframes |
|---|---|---|
| ME04-US44-AC01 | Precondition: "Create New Fence" screen is opened.If at least 3 fence posts are added and the fence outline still hasn't been closed, then:the first fence post should be animated, see animation.the animation continues till I close a fence or less than 3 fence posts are left on My Map. | See source user stories: ME04-EP03 Create a fence with a collarNote: If I remove fence posts and only 1 or 2 fence posts left, then the first fence post should not be animated. |
| ME04-US44-AC02 | Precondition: "Create New Fence" screen is opened. If I add a fence post, the number of dots becomes 3 and the fence outline hasn't been closed, then:the standard iOS popup message M139 Great job with the fence creation should be displayed. | - |
| ME04-US44-AC03 | Precondition: "Create New Fence" screen is opened, unclosed fence with 3 or more fence posts is displayed. If I remove fence posts, only 1 or 2 fence posts left and I add the 3rd fence post, then: the popup M139 Great job with the fence creation should be displayed again, see ME04-US44-AC02. | - |
| ME04-US44-AC04 | If the 3rd point is added via a tap on Undo/Redo, then:the popup M139 Great job with the fence creation should not be displayed again. | - |
