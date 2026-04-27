---
title: "(Native Apps) ME02-F04. Map Settings"
sidebar_label: "(Native Apps) ME02-F04. Map Settings"
sidebar_position: 507
last_modified: "Mar 07, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| READY |
| Mariya Kolyada, Dmitry Kravchuk |
| iOS: TBDAndroid: TBD |
| As of 05 Mar 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria Map View Setting Map Setting Storing

# User story

\> As Halo app account owner, I want to view Map Setting on More screen so I can change my map settings to be always used by the app.

# Acceptance criteria

| AC | Description | Design | Map View Setting | Keep Screen Awake Setting | Keep Map Facing North Setting | Map Setting Storing |
|---|---|---|---|---|---|---|
| ME02-F04-AC01 | If I tap Map Settings on the More screen, then the app should:Open the Map Settings screen. | Screen default stateFigma |
| ME02-F04-AC02 | By default, the Satellite map style should be selected. |
| ME02-F04-AC03 | Only one map type can be chosen at a time. |
| ME02-F04-AC04 | If I change the map style (Satellite\<-\>Standard), then the app should:Change the value of the selected style on the Map Settings screen.Load all app screens with the map having this map style until the user changes it to the opposite. |
| ME02-F04-AC05 | By default, 'Keep Screen Awake' = ON. |
| ME02-F04-AC06 | If I change 'Keep Screen Awake' to ON, then the app should for all app screens with the map:Keep the screen active unless the user locks the screen or leaves the app (smartphone system awakeness setting should be overridden). |
| ME02-F04-AC07 | If I change 'Keep Screen Awake' to OFF, then the app should for all app screens with the map:Keep the screen following the corresponding smartphone system awakeness setting. |
| ME02-F04-AC08 | By default, 'Keep Map Facing North' = OFF. |
| ME02-F04-AC09 | If I change 'Keep Map Facing North' to ON, then the app should for app screens with the map that do NOT have custom logic:Block map orientation change on user rotation gestures.Never display the compass button? Or always display??Keep the map always facing north. |
| ME02-F04-AC10 | If I change 'Keep Map Facing North' to OFF, then the app should for app screens with the map that do NOT have custom logic:Unblock map orientation change on user rotation gestures.Display the compass button if the map orientation faces other than north. |
| ME02-F04-AC11 | The app should store the Map Settings values for my account locally on the mobile device). This means that if I open my app account using another device, then the default map settings (or previously applied settings for my account on that device) will be applied. |
| ME02-F04-AC12 | Map Settings values can be cleared for the account used on the specific mobile device in the following cases only after I:Removed the app from the mobile device;Logged out and logged into a different account using the same mobile device. |
