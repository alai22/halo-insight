---
title: "[Won't have] ME03-US67. Separate status for deactivated SIM card"
sidebar_label: "[Won't have] ME03-US67. Separate status for deactivated SIM card"
sidebar_position: 188
last_modified: "Jan 17, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Maria Shikareva [X] |
| HALO-9937 - MOB+BE: ME03-US67. Separate status for deactivated SIM card Closed |
| Click here to expand... |# User story

\> As a Halo app user I want to see that the SIM card of my collar is deactivated instead of having a common status "Paused. Currently using Wi-Fi" so that to be aware of this.

# Acceptance criteria

| AC | Description | Links/ Notes/ Wireframes |
|---|---|---|
| AE03-US69-AC | In this case we need a separate UI to show the status of SIM card - deactivated.We need to always display a separate status under My Collars → Cellular section if SIM card is deactivated (whether it's a fault/ was done intentionally + display a current state of a process (if we can do it): Pending/ waiting for reactivation.Reactivation pausedReactivation is in process/ reactivating. This can take some time. Reactivation failed. Consider contacting customer support.TBD links to Zoom/ Dog parkDeactivated:state from BE (last known status)if SIM card is activated from KORE → BE won't know about it (there's no synchronization process) | ME03-F01. Collars list#Network |
|  | Possible statuses on BE:scheduled;skipped - it was scheduled, but then the desired state changed, so the first request will be skippedcompleted - we received a successful response from KOREcancelled - when we get the corresponding status from KOREIf the status was "in progress" and then failed, it'll be re-scheduled.We can somehow highlight when "action required" label is in place, but at the moment it seems that this label isn't removed (when after "action required" CSA clicks "activate" button, another request is created in "scheduled", but the first one doesn't change the status and "action required" label isn't removed - was discussed with Zakhar but need to be confirmed during investigation task: HALO-9961 - BE [Investigate][NT]: KORE DB synchronization Closed ) |  |
| AE03-US69-AC06 | https://zpl.io/2Z1PMkq |  |
| AE03-US69-AC07 | The activation/deactivation request completion can take some time. In case of the failure the corresponded status will be displayed in the list of sim cards. | - |
| ME03-US23-AC06 | the standard popup message M180 SIM card activation time warning should be displayed above 'Bluetooth Devices - Successfully Paired with device' screen. | - |
