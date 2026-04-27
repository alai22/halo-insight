---
title: "[Postponed] ME01-F09. Walk-trough for new users and new feature announcements"
sidebar_label: "[Postponed] ME01-F09. Walk-trough for new users and new feature announcements"
sidebar_position: 95
author: "Nicolay Gavrilov"
---

| Document status | Document owners | Links to JIRA Issues |
|---|---|---|
| DRAFT |
| Nicolay Gavrilov |
| TBD |# User story

We need a system to walk the new users through the main features of the app and announce new features to existing users

# Acceptance criteria

| AC | Description | iOs Design / Implementation status | Android Design / Implementation status |
|---|---|---|---|
| ME01-F09-AC01 | New feature announcement/user embedded web frames shown on login:shown on an embedded web-frame; the content is created in a CMS,the links to web-pages and applied app versions are managed via admin portal (optionally via REST API),the tutorials are marked as read on BE and never shown again for a specific user and a version of the app (optionally 'Remind me later' button to show the tutorial on the next login)Pros: users won't miss them, potentially saves time and efforts in case you plan to announce changes and new features more frequently, does not require rebuilding the appCons: dev. efforts, relies on the internet connectionPriority: this should be done before October (when we have training updates)an acceptable solution, provided:it'll look good.If we lose internet connection, in the middle of the walk trough (e.g. on the 2nd step). What will happen? Is it possible to load all of the walk-trough content to avid such problems?The solution may be used both for new users walk-trough and new feature announcements.In addition to CMS, we should also consider using Zendesk. We can create articles and add links to them to the app. The mobile app will take data from the article and present it on the mobile screen. The article will be composed according to certain rules (e.g. only one image and limited number of characters). Naming conventions should allow linking articles to versions.Preferable CMS is WordPressMichael suggested to check WalkMe.com - an off the shelf tool for walkthroughs. Dev. team should check it. This tool could also be used for subscription upgrade prompts.How exactly the system will define if we need to show the 'What's new' screens? Some sort of 'unseen' flag for each user for each new mobile app version (iOs and Android)?Dismiss / Remind me later (on the next login) buttons2020-07-29 Meeting notes: BA+UX callhttps://www.trychameleon.com/blog/how-to-announce-new-featureshttps://www.nngroup.com/articles/mobile-instructional-overlay/ | IOS TO DO | ANDROID TO DO |
