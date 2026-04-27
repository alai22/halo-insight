---
title: "ME04-US38. Do not change map state after opening/closing Create New Fence/Edit Fence Posts screen"
sidebar_label: "ME04-US38. Do not change map state after opening/closing Create New Fence/Edit Fence Posts screen"
sidebar_position: 120
last_modified: "Dec 21, 2020"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| APPROVED |
| Galina Lonskaya, Pavel Leonenko, Anastasia Brechko |
| HALO-5544 - ME04-US38. IMPORTANT Do not change map state after opening/closing Create New Fence/Edit Fence Posts screen Closed |# User story

\> As an account owner, I want to have the same map state after transition from My Map to the fence creation/editing so that I will not need to adjust my map state after "Create New Fence"/"Edit Fence Posts" screen opening.

# Acceptance criteria

| AC | Description | iOS implementation / UI designIOS TO DO | Android/ implementation / UI designANDROID TO DO | My Map → Create New Fence | Create New Fence → My Map | My Map → Edit Fence Posts | Edit Fence Posts → My Map |
|---|---|---|---|---|---|---|---|
| See the source requirements in ME04-F00. Add fence without GPS (should be updated after the story implementation) |
| ME04-US38-AC01 | If I initiate the Create New Fence screen view, then the map state should not be changed:zoom level should be the same as on My Map, if it's equal or more than 16;orzoom level should be 16, if on my map it's less than 16;map type(satellite/standard) should be the same as on My Map;the same map area should be visible as on My Map (at the moment my map centered on my location). | - | - |
| ME04-US38-AC02 | If I complete/cancel the Fence creation, then:My Map should be opened with the last used map type that was used within the fence creation flow. | - | - |
| ME04-US38-AC03 | If I initiate the Edit Fence Posts screen view, then:map type should be the same as on My Map.Note: within the fence editing flow, my map should be centered on the created fence as it was before (no changes) | - | - |
| ME04-US38-AC04 | If I complete/cancel the Fence editing, then:My Map should be opened with with the last used map type that was used within the fence editing flow. | - | - |
