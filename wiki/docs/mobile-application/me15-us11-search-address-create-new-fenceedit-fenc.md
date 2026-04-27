---
title: "ME15-US11. Search address (Create new fence/Edit fence posts)"
sidebar_label: "ME15-US11. Search address (Create new fence/Edit fence posts)"
sidebar_position: 192
last_modified: "Jul 19, 2023"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED BY SQ |
| Galina Lonskaya Dmitry Kravchuk Nikita Krisko Siarhei Leushunou [X] Valeria Malets |
| HALO-10333 - MOB: ME15-US11. Search address (Create new fence/Edit fence posts) + ME04-US52. Move "blue bar" to the bottom of the screen (Create New Fence/Edit Fence Posts) and change the text Closed |
| Click here to expand...As of 31 Jan 2022 Galina Lonskaya created the initial story version As of 15 Feb 2022 Galina Lonskaya updated ME15-US11-AC04/AC05/AC13, added ME15-US11-AC14 |# Contents

User Story Acceptance criteria Implementation notes

# User Story

\> As a Halo App Account Owner, I want to search an address/place so that I can start the fence creation process without manual search on my map.

# Acceptance criteria

| AC | Description | iOS screen design/notes | Android screen design/notes |
|---|---|---|---|
| ME15-US11-AC01 | If there are no fence posts on Create New Fence/Edit Fence screens, then:"Search" bar with "Search" icon and "Search places and addresses" placeholder should be displayed. Note: blue bar is moved to the bottom within [Not impl.] ME04-US52. Move "blue bar" to the bottom of the screen (Create New Fence/Edit Fence Posts) story. | Zelplin Link | Zelplin Link |
| ME15-US11-AC02 | If I tap on "Search" bar, then "Search" modal window should be opened. | - | - |
| ME15-US11-AC03 | "Search" modal window (empty state) should consist of: "Search" field with:"Search" icon"Search places and addresses" placeholder"Cross" icon"Cancel" buttonKeyboard with Search button | Zeplin Link | Zeplin Link |
| ME15-US11-AC04 | "Search" button on the keyboard should be disabled, in case no characters are entered into "Search" field. Note: valid for iOS only | - | - |
| ME15-US11-AC05 | I cannot enter more than 100 characters into "Search" field. Note 1: the system doesn't allow it. Note 2: English characters are allowed only. | - | - |
| ME15-US11-AC06 | If at least one character is entered into "Search" field, then: autosuggested "Search" options should be displayed (the list of options can be scrollable). | Zeplin Link | Zeplin Link |
| ME15-US11-AC07 | If al least one character is entered into "Search" field, then: Cross icon should be displayed in "Search" field. | - | - |
| ME15-US11-AC08 | If I tap on the Cross icon, then: the Search field should be cleared. | - | - |
| ME15-US11-AC09 | If no results are found in accordance with the search request, then: the following error text should be displayed: "No address found". | Zeplin Link | Zeplin Link |
| ME15-US11-AC10 | If I tap on Search button and the Search request still isn't specific (more than 1 option is applicable (e.g. several shops with one name)), then: the list of auto-suggestions should be updated; no specials errors should be displayed.Note: the same behavior as in taxi-services | - | - |
| ME15-US11-AC11 | If I tap on the autosuggested option, then: the Search window should be closed; the required part of the map with corresponding zoom level should be displayed;the Search field with the search request and "Cross" icon should be displayed at the top of the screen.Note: appropriate zoom level should be identified by the system. | Zeplin Link | Zeplin Link |
| ME15-US11-AC12 | Precondition: Create new fence/Edit fence posts" screen is opened.If I tap on Cross icon and delete the search request, then: the search request should be removed;the placeholder should be displayed in the Search bar; "Cross" icon should not be displayed within the search field. | See pic in ME15-US11-AC01 | - |
| ME15-US11-AC13 | Precondition: Create new fence/Edit fence posts" screen is opened.If I add at least one fence post, then: the Search bar should be hidden. the red pin should be removed | - | - |
| ME15-US11-AC14 | The spinner should be displayed on "Search" modal window, in case the search requires some time. | - | - |## Implementation notes

| IN | Description |
|---|---|
| ME15-US11-IN01 | The following geocoder is planned to used for "Search" function: https://docs.mapbox.com/api/search/geocoding/ |
| ME15-US11-IN02 | Analytics event should be added: Compare how often the user creates a fence and use the search function with the number of the users who creates a fence, but doesn't use "Search" function. |
