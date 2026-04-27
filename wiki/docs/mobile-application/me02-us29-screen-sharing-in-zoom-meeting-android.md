---
title: "ME02-US29. Screen sharing in Zoom meeting (Android)"
sidebar_label: "ME02-US29. Screen sharing in Zoom meeting (Android)"
sidebar_position: 180
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-9488 Closed |
| As of 12 Nov 2021 Mariya Kolyada created the page for future requirements.As of 24 Nov 2021 Ekaterina Dupanova created requirements for screen sharing/minimizing for Android only |# User Story

\> As Halo Collar app account owner I want to be able to share my screen when I am in a Live Support meeting so that I can show screens in my Halo app and demonstrate what issue I have faced.

# Acceptance criteria

| AC | Description | Android UI design |
|---|---|---|
| ME02-US29-AC01 | PreconditionZoom meeting screen is in maximized viewIf I click on the "Share" button in a Zoom meeting and choose the "Screen" option, then the app should:Display M212 Allow screen sharing (Android) pop-up. | The pop-up window is managed by the Android system |
| ME02-US29-AC02 | PreconditionZoom meeting screen is in maximized viewIf I click on the "More" button and choose the "Minimize Meeting " option, then the app should:open the Zoom meeting in a minimized view | The screen UI is managed by ZoomSDK |
| ME02-US29-AC03 | PreconditionUser has started screen sharingandZoom meeting screen is in minimized viewThe app should:show an open side panel. | The screen UI is managed by ZoomSDK |
| ME02-US29-AC08 | PreconditionUser has started screen sharingandZoom meeting screen is in maximized viewThe app should:show side panel in an open state for 3-4 seconds and then close it. | The screen UI is managed by ZoomSDK |
| ME02-US29-AC04 | The app should allow to exit minimized view of the Zoom meeting and open the Zoom meeting in maximized view:by clicking on the minimized Zoom meeting by clicking on Live Support on the settings screen by clicking on the zoom notification in the push notification | The screen UI is managed by ZoomSDK |
| ME02-US29-AC09 | PreconditionUser has never shared Halo app screen beforeandUser has initiated screen sharingIf I click the "Start Share" button, the app should open the menu with the list of other apps of the device (for Android 10, 11; for Android 8 the app skips this step and open the next page).If I choose "Halo", the app opens the screen with the toggle "Allow display over other apps". | The screen UI is managed by ZoomSDK |
| ME02-US29-AC05 | PreconditionUser has started screen sharingandUser has provided consent to display content over other appsThe app should allow the user to display and click on elements of the screens inside the Halo app and outside the Halo app | The screen UI is managed by ZoomSDK |
| ME02-US29-AC06 | If I drag the Zoom meeting in a minimized view, the app allows to move the Zoom window across the edges of the screen. | The screen UI is managed by ZoomSDK |
| ME02-US29-AC07 | PreconditionUser has started screen sharingandUser has minimized the Zoom meeting firstandUser has maximized the Zoom meeting backIf I Stop screen sharing, the app should make the minimize screen option available in the menu again (More→ Share screen). | The screen UI is managed by ZoomSDK |
