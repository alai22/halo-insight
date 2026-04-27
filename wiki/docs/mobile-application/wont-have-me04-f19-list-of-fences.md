---
title: "[Won't have] ME04-F19. List of fences"
sidebar_label: "[Won't have] ME04-F19. List of fences"
sidebar_position: 74
last_modified: "Nov 24, 2020"
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Document owner | Link with Jira | Revision history |
|---|---|---|---|---|---|
| Owner |
| ME04 As an Owner, I'd like to manage my fences to keep safe/unsafe zones up to date. |
| DRAFT |
| Diana Aladina |
|  |
|  |User story

As a user, I would like to view the list of available fences so that I can view what fences are available for me in one place.

### Acceptance criteria

| AC | Text |
|---|---|
| ME04-US06-AC01 | A user can initiate list view on "My Map" screen by tapping list icon and selecting "My Fences" option. |
| ME04-US06-AC02 | The fences are sorted in order of creation (new on top).A user should have an option to "Create New Fence" |
| ME04-US06-AC03 | Each item in the list should have 2 view option:shortexpanded |
| ME04-US06-AC04 | Each short description in the list should contain:Fence nameFence iconFence status (Active vs. Inactive)City, State, CountryArrow to open expanded view |
| ME04-US06-AC05 | Each expanded description in the list should contain:Fence nameFence iconFence status (Active vs. Inactive)"Fence Status is \<STATUS\>" with toggle switcher to change the state"Fence Boundaries. Edit fence posts and safe areas" and button "Edit""Fence Details. Edit fence name" and button "Edit"Arrow to hide expanded view |
| ME04-US06-AC06 | Each item line must be clickable and initiates short/expanded viewAll fences show only short info by defaultOnly one fence can have expanded view at a timeThe app should hide the expanded info when a user taps short info line of this fence or another fence |
| ME04-US06-AC07 | If a user has 0 fences, list view should have button "Create New Fence" and a tip "No fences to display" |
| ME04-US06-AC08 | If any change has been applied and it will affect a pet with a collar, the app should start sync with it automatically. |
| ME04-US06-AC09 | If it was unable to sync fence updates with some collars due to availability issues, the app should show:M37 Offline Changes (one collar is offline)M38 Offline Changes (multiple collars)Changes should be synced next time, when a collar is available and online. |
| ME04-US06-AC10 | Fence Boundaries. Edit fence posts and safe areas. After tapping "Edit", the app should focus the map on selected fence with editable dots. See ME04-US04. Edit a fenceFence Details. Edit fence name. After tapping "Edit", the app should show the screen "Edit Fence" TBD |
| ME04-US06-AC11 | When a user taps fence icon, the app should open Map view with centered selected zone (zoomed in close enough) and show a card with details. |
| ME04-US06-AC12 | My Map should be selected in the Tab Bar. |
| ME04-US06-AC13 | A user can use pull-to-refresh to update the state of the screen. |### Screen ME04-5 - List of fences

TBD


