---
title: "ME04-US10. Create more than one fence"
sidebar_label: "ME04-US10. Create more than one fence"
sidebar_position: 653
last_modified: "Sep 16, 2019"
author: "Nicolay Gavrilov"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue |
|---|---|---|---|---|---|
| December Release |
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| APPROVED |
| Nicolay Gavrilov |
| HALO-1909 - ME04-US10. Create more than one fence Closed |# User story

\> As an owner I want to create more than one fence so that I can have multiple safe zones for my pets.

# Acceptance criteria

| AC | Text | Links |
|---|---|---|
| ME04-US10-AC01 | To create a new fence user taps on the corresponding button on 'My Fences' tab on 'My Map' section. | ME04. Fences#ME04-US06.Listoffences(Notapprovedwithoutdesign) |
| ME04-US10-AC02 | User places the first point of a new fence by tapping on any place on the map that is not occupied with other fences on 'Create New Fence' screen. | 'Create New Fence' screen in Zeplin |
| ME04-US10-AC03 | If a user tries to put a dot on the territory of an existing fence, the app should not allow this and show the toast message "Can't create overlapping fences". The dot remains on the previous coordinates. | N/A |
| ME04-US10-AC04 | If a user tries to put a dot so that the resulting border of the new fence crosses the area of another fence, the app should not allow this and show the toast message "Can't create overlapping fences". | N/A |
| ME04-US10-AC05 | User can see all fences created in his account on the map. | N/A |# Not doing

- Back-end app will not validate the fences for overlapping. In this case we will not be able to ensure that users will not be able to create overlapping fences. Overlapping fences may appear in such rare cases, as when multiple users will simultaneously create fences under the same account from different smartphones. Therefore the collars should support working overlapped fences.


