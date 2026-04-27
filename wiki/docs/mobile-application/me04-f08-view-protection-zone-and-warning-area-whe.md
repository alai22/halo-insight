---
title: "ME04-F08. View Protection Zone and Warning Area when the fence is selected"
sidebar_label: "ME04-F08. View Protection Zone and Warning Area when the fence is selected"
sidebar_position: 651
last_modified: "Dec 07, 2020"
author: "Galina Lonskaya"
---

| Document type | Document status | Story owners | Link to JIRA Issue |
|---|---|---|---|
| Baseline story |
| APPROVED |
| Galina Lonskaya, Anastasia Brechko, Pavel Leonenko, Eugene Paseka |
| HALO-5156 - iOS: Warning area + Protection zone displaying on My Map. Closed HALO-5407 - Android: Warning area + Protection zone displaying on My Map. Closed |# User story

\> As an account owner, I want to view Protection Zone and Warning Area when the fence is selected so that I can understand where my pet(s) get(s) Warning, Boundary and Emergency Feedback.

# Acceptance criteria

| AC | Text | iOS implementation status / NotesIOS DONE | Android implementation status / NotesANDROID DONE |
|---|---|---|---|
| ME04-F08-AC01 | If the fence is selected and the fence card is up (in both minimized and default view), then:the selected fence should be displayed with its Protection Zone;the selected fence should be displayed with its Warning Area.Note 1: the calculation logic for both the Protection zone and Warning Area is implemented on the BE side, see tech description in Geofence Zone Calculation.Note 2: see the source story with the fence card description: ME04-F01. Fence card. | Pic 1 - Selected fence with Protection Zone and Warning Area + default fence cardPic 2 - Selected fence with Protection Zone and Warning Area + minimized fence card | Pic 1 - Selected fence with Protection Zone and Warning Area + default fence card | Pic 2 - Selected fence with Protection Zone and Warning Area + minimized fence card | See Pic 1 for Android;See Pic 2 for Android |
| Pic 1 - Selected fence with Protection Zone and Warning Area + default fence card | Pic 2 - Selected fence with Protection Zone and Warning Area + minimized fence card |
| ME04-F08-AC02 | The following legend should be added both to the minimized and default fence card:Circle contained the pattern of Warning Area+ "Warning Area" labelCircle contained the pattern of Protection Zone+ "Protection Zone" label | See pic 1,2 above. | - |
| ME04-F08-AC03 | The Questionmark button should be added to the fence card for both default and minimized view. | See pic 1,2 above. | - |
| ME04-F08-AC04 | If I tap on the Questionmark button, then:the Fence Legend sheet should be opened (a similar sheet as used for Instant Feedback, see ME05-FE00. Instant feedback).The Fence Legend sheet consists of: Circle with Warning Area pattern + "Warning Area" label"Warning and Boundary Feedback will only occur while your dog is inside this area + heading toward the boundary." textCircle with Protection Zone pattern + "Protection Zone" label"In the Protection Zone, your dog only receives Emergency Feedback while moving away from the boundary. When your dog stops moving OR heads home, Emergency Feedback stops and Encouragement Feedback begins. Beyond the Protection Zone, your dog’s Halo enters Lost Mode." text "Close" button for iOS; "Cross" icon for Android. | Pic 3 - Fence Legend sheet | See Pic 3 for Android |
| ME04-F08-AC05 | If I tap outside the "Fence legend" sheet or tap on the Close button (for iOS)/ the Cross icon (for Android), then:the Fence Legend sheet should be closed. | - | - |
| ME04-F08-AC06 | Protection Zone can be overlapped by other fences, if they intersect.Note: It was agreed within the dev team, BA and UI/UX that the white border of the Protection Zone can lay above other fence outlines, since it's hard to display it under the outline from the dev perspective. | See pic 1,2 above. | - |
| ME04-F08-AC07 | Warning Area UI, while the creation or editing of the fence, is different from the Warning Area displayed, when the fence is selected. Instead of the dashed line, the solid line should be used, when the fence is selected. Note 1. The initial requirements for Warning Area, see in ME04-F07. Warning Area. | - | - |
