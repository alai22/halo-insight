---
title: "(Native Apps) ME01-F04-US03. Auto Login"
sidebar_label: "(Native Apps) ME01-F04-US03. Auto Login"
sidebar_position: 494
last_modified: "Feb 26, 2025"
author: "Galina Lonskaya"
---

| Document owners | Link to JIRA/Linear Issue | History of changes |
|---|---|---|
| Galina Lonskaya, Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-413/[ios]-auto-login |
| 26 Feb 2025 draft is created by Galina Lonskaya |# Contents

User story Acceptance criteria Standard auto-login flow Allow logged-in users to continue using the app despite a communication issue

# User story

\> As Halo app account owner, I want to be automatically logged into the app without entering my credentials again, so that I can access my account quickly and seamlessly.

# Acceptance criteria

| AC | Description | Standard auto-login flow | Allow logged-in users to continue using the app despite a communication issue |
|---|---|---|---|
| ME01-F04-US03-AC01 | If:I launch the app,AND I have logged into the app at least once using the downloaded app,AND I was not logged out the previous time,then:The app should perform auto-login. |
| ME01-F04-US03-AC02 | Preconditions: the app has the cached version of the UserProfile dataIf during the login process, the app gets a communication error when downloading the abovementioned data, it should allow the user to proceed without showing any errors.Note: if the issue persists the users will see the communication errors on any operation involving sending requests to the BE. |
| ME01-F04-US03-AC03 | If during the login process, the app gets a communication error when trying to download:SubscriptionInfo dataor UserProfile data (and if there are no cached UserProfile data)it should NOT allow the user to proceed and display M113 popup Figma (see the old reference in Confluence M113 Network error). |
| ME01-F04-US03-AC04 | If during the login process, the app gets a communication error when trying to download:either AppConfig data it should NOT allow the user to proceed and display 'Unable to start app' screen, see Figma |
| ME01-F04-US03-AC05 | If during the login process, the app gets a communication error in response to one of the following requests:GetUserBeaconsBeaconMonitoringService.TrySendDataAsyncRefreshTileSetsget MapDatait should allow the user to proceed without showing any errors.Notes:if the issue persists the users will see the communication errors on any operation involving sending requests to the BE.if there is no UserBeacons data then the beacon name will not be displayed on the pet card and this is not an issue for this scenario. The name will appear when the communication error will be resolved. |Implementation details:

See StartDataService.InitializeDataManagersAsync()


