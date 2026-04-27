---
title: "ME01-US25 Let users run the app in case they are logged in but encounter a Communication exception"
sidebar_label: "ME01-US25 Let users run the app in case they are logged in but encounter a Communication exception"
sidebar_position: 602
last_modified: "Feb 18, 2022"
author: "Nicolay Gavrilov"
---

| Document status | Document owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| APPROVED(SQ) |
| Nicolay Gavrilov Nikita Krisko |
| HALO-10280 - MOB: ME01-US25 Let users run the app in case they are logged in but encounter a Communication exception Closed |
| Click here to expand...11 Feb 2022 updated ME01-US25-AC01, ME01-US25-AC02, and ME01-US25-AC0316 Feb 2022 updated ME01-US25-AC01 and ME01-US25-AC0218 Feb 2022 added ME01-US25-AC04, corrected ME01-US25-AC01, ME01-US25-AC02, and ME01-US25-AC03 |# User story

\> As a user I want to be able to use the app even if I encounter a communication error during the login so that I could at least use the features that rely on Bluetooth communication channel.

# Acceptance criteria

| AC | Description | Links |
|---|---|---|
| ME01-US25-AC01 | Preconditions:the app has the cached version of the UserProfile dataIf during the login process, the app gets a communication error when downloading the abovementioned data, it should allow the user to proceed without showing any errors.Note: if the issue persists the users will see the communication errors on any operation involving sending requests to the BE. | - |
| ME01-US25-AC02 | If during the login process, the app gets a communication error when trying to download:SubscriptionInfo dataor UserProfile data (and if there are no cached UserProfile data)it should NOT allow the user to proceed and display the M113 Network error. | ME14-F01 Unified errors handling |
| ME01-US25-AC04 | If during the login process, the app gets a communication error when trying to download:either AppConfig data it should NOT allow the user to proceed and display the Application Startup failed screen | - |
| ME01-US25-AC03 | If during the login process, the app gets a communication error in response to one of the following requests:GetUserBeaconsBeaconMonitoringService.TrySendDataAsyncRefreshTileSetsget MapDatait should allow the user to proceed without showing any errors.Notes: if the issue persists the users will see the communication errors on any operation involving sending requests to the BE.if there is no UserBeacons data then the beacon name will not be displayed on the pet card and this is not an issue for this scenario. The name will appear when the communication error will be resolved. | - |
