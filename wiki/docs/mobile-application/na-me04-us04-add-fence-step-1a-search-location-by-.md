---
title: "(NA) ME04-US04. Add Fence: Step 1a. Search location by address"
sidebar_label: "(NA) ME04-US04. Add Fence: Step 1a. Search location by address"
sidebar_position: 521
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-655/[ios]-add-fence-step-1a-search-location-by-addressAndroid: https://linear.app/fueled/issue/HALO-656/[android]-add-fence-step-1a-search-location-by-address |
| 24 Mar 2025 Mariya Kolyada created the initial version of a user story.11 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want to search an address/place so that I can place the fence location without manual map pan.

# Acceptance criteria

| AC | Description | Design iOS |
|---|---|---|
| ME04-US04-AC01 | The expanded 'Address search' card on opening should have:Search fieldLeaving button:Back - AndroidCancel - iOSOpened keyboard with the Search button | Figma |
| ME04-US04-AC02 | For iOS only, the app should display the 'Search' button on the keyboard in a disabled state, in case no characters are entered yet. |
| ME04-US04-AC03 | The app should forbid entering more than 100 characters in the Search field. |
| ME04-US04-AC04 | If the 'Search' field has at least one character both in the expanded 'Address search' card and 'Set Fence Location' screen, then the app should: Display the Cross button inside the field. |
| ME04-US04-AC05 | If I tap on the Cross button, then the app should: Clear the 'Address search' field. |
| ME04-US04-AC06 | Each time user enters a new character into the 'Search' field, the app should: Search for addresses relevant to the entered characters.Display GUI-7 Full-screen loader below underneath the 'Search' field and an opened keyboard while forming the list of options (only if it takes some time). |
| ME04-US04-AC07 | Precondition'Search' field has at least one character.If I tap the 'Search' button on the keyboard, then the app should behave the same as if after entering each new symbol. |
| ME04-US04-AC08 | If the app found relevant options to the entered characters in the 'Search' field, then the app should: Display the search results below the 'Search' field. |
| ME04-US04-AC09 | The app should add a scroll if the search results do NOT fit on the screen. |
| ME04-US04-AC10 | If I tap one of the search results, then the app should:Put this option inside the 'Search' field + 'Cross' icon.Collapse the expanded 'Address search' card by sliding down.Zoom in/out to the 18th zoom level.Move the center of the map to the selected address. | Figma |
| ME04-US04-AC11 | If the app found NO relevant options to the entered characters in the 'Search' field, then the app should display that no address was found. | Figma |Tech details

The backend is not currently used for address search.The current application uses https://docs.mapbox.com/api/search/geocoding/ for address search.However, since Google and Apple Maps are used, it might make sense to use tools from Apple (MKLocalSearch) and Google (Places API). There is no specific requirement, but we do have a key for the Mapbox API onlyThe search request is executed after input with a half-second delay to reduce the number of requests


