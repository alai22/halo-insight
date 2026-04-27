---
title: "ME21-US88. Send 'daily_map_view_no_collar' SDK event to Braze"
sidebar_label: "ME21-US88. Send 'daily_map_view_no_collar' SDK event to Braze"
sidebar_position: 454
last_modified: "Jan 16, 2025"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Kirill Akulich |
| HALO-21352 - MOB: ME21-US88. Send SDK event daily_map_view_no_collar to Braze Closed |
| 16 Sep 2024 the draft user story is created |Table of Contents

User story Acceptance criteria Implementation notes

# User story

\> n/a, the events are required for Halo Marketing team

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| ME21-US88-AC01 | If:I open the app for the first time on a given day (= first time during last 24 hours)ANDNo collars are currently linked to the user’s account, AND Onboarding is completedTHEN:SDK event: 'daily_map_view_no_collar' should be sent to Braze. | - |
| ME21-US88-AC02 | The 'daily_map_view_no_collar' event may be sent repeatedly as many times as necessary if all the sending conditions are met. | - |
| ME21-US88-AC03 | IF:Event has NOT been delivered successfully to Braze.THEN:The app should try to send it again until it is successfully delivered. |  |# Implementation notes

| IN | Implementation notes |
|---|---|
| ME21-IN88-AC01 | Kiryl's suggestion that was approved by Adrian in 'Daily Map View No Collar Event for Halo Users Exiting Onboarding Without Collar' email. Kiryl: We will store on the mobile side the last time the event was sent and the user viewed a map without a collar in the account; If the current date is greater than the "daily map view without collar" date more than 24hrs -\> we will send a new event and remember it in the local store. Disadvantages of this solution:1. If a user uses multiple devices then each of them will use its own local memory -\> as a result events will be sent on each device every day. I think this is ok, but I would like to point it out to you to consider when configuring the campaign in Braze. We can also discuss whether we need to configure this time span between events. If so, we will need additional BE work to provide this value for mobile.Adrian: I think it will be quite unlikely that a user will have multiple devices each with collar-less Halo mobile app installed, so lets accept that risk.I do not foresee us changing the time span, so I think it's OK to leave it at 24 hours.Adrian: No info about subscription is required to be included into event |
| ME21-IN88-AC02 | Implementation of the case with the deleted collar :Collar added to the app → When the app is opened, the current date is saved.Collar removed from the app → No specific actions taken after collar removal.App is minimized: → No specific actions are triggered.App is opened again:Check the stored date.If more than 24 hours have passed since the last saved date:Trigger an event.Save the current date.If less than 24 hours have passed, no action is taken. |
