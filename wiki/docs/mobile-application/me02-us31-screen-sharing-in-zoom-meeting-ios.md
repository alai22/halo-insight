---
title: "ME02-US31. Screen sharing in Zoom meeting (iOS)"
sidebar_label: "ME02-US31. Screen sharing in Zoom meeting (iOS)"
sidebar_position: 183
last_modified: "Dec 17, 2021"
author: "Ekaterina Dupanova"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-9629 Closed |
| As of 01 Dec 2021 Ekaterina Dupanova created requirements for screen sharing on iOS |# User Story

\> As Halo Collar app account owner I want to be able to share my screen when I am in a Live Support meeting so that I can show screens in my Halo app and demonstrate what issue I have faced.

# Acceptance criteria

| AC | Description | iOS UI design |
|---|---|---|
| ME02-US31-AC01 | PreconditionZoom meeting screen is in maximized viewIf I click on the "Share" button in a Zoom meeting and choose the "Screen" option, then the app should:Display M213 Allow screen sharing (iOS) pop-up.This behavior applies to iOS versions 12+. Not available for iOS 11. To initiate screen sharing for iOS 11 please refer to ME02-US31-AC11. | The screen UI is managed by ZoomSDK |
| ME02-US31-AC11 | PreconditionZoom meeting screen is in maximized viewIf I click on the control center and choose "Record" option, the app shows Halo screen share options and other screen sharing apps available. | The screen UI is managed by ZoomSDK |
| ME02-US31-AC02 | PreconditionUser has clicked "Start Broadcast" andTimer has startedThe app should open the screen with 2 buttons: Share Device Audio (on/off), Stop Share. | The screen UI is managed by ZoomSDK |
| ME02-US31-AC03 | PreconditionZoom meeting screen is in maximized viewIf I click on the "More" button and choose the "Minimize Meeting " option, then the app should:open the Zoom meeting in a minimized view | The screen UI is managed by ZoomSDK |
| ME02-US31-AC06 | The app should allow to exit minimized view of the Zoom meeting and open the Zoom meeting in maximized view:by clicking on the minimized Zoom meeting by clicking on Live Support on the settings screen | The screen UI is managed by ZoomSDK |
| ME02-US31-AC07 | PreconditionUser has started screen sharingThe app should allow the user to display and click on elements of the screens inside the Halo app and outside the Halo app | The screen UI is managed by ZoomSDK |
| ME02-US31-AC08 | If I drag the Zoom meeting in a minimized view, the app allows moving the Zoom window across the edges of the screen. | The screen UI is managed by ZoomSDK |
| ME02-US31-AC09 | PreconditionUser has clicked "Start Broadcast" The app should start timer that indicates how much time the screen sharing has been going on. | The screen UI is managed by ZoomSDK |
| ME02-US31-AC10 | PreconditionScreen sharing is in progressandUser has clicked on status bar on top of the screenThe app should display M214 Stop screen sharing (iOS) pop-up. | The screen UI is managed by ZoomSDK |
