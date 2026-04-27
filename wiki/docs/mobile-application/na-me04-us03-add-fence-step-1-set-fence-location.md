---
title: "(NA) ME04-US03. Add Fence: Step 1. Set Fence Location"
sidebar_label: "(NA) ME04-US03. Add Fence: Step 1. Set Fence Location"
sidebar_position: 509
last_modified: "Apr 16, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-653/[ios]-add-fence-step-1-set-fence-locationAndroid: https://linear.app/fueled/issue/HALO-654/[android]-add-fence-step-1-set-fence-location |
| 24 Mar 2025 Mariya Kolyada created the initial version of a user story.15 Apr 2025 Dmitry Kravchuk added tech details. |# Contents

Contents User story Acceptance criteria Top Navigation Bar Map, General Map Controls, and Tutorial 'Fence Location Position' pin and Address Search

# User story

\> As Halo app account owner, I want to choose location of my fence creation, so the app autogenerate it where I need it.

# Acceptance criteria

| AC | Description | Design | Top Navigation Bar | Map, General Map Controls, and Tutorial | 'Fence Location Position' pin and Address Search | Create Fence |
|---|---|---|---|---|---|---|
| ME04-US03-AC01 | If I tap the 'Back' button, then the app should:Leave Fence creation.Display the previously opened screen. | Figma |
| ME04-US03-AC02 | If I tap the 'Questionmark' icon, then the app should:Open the 'Need Help?'The functionality should be implemented later within a separate user story: HALO-220 |
| ME04-US03-AC03 | The app should display the User location pin on the map (see (Native apps) ME15-F02. User location pin) |
| ME04-US03-AC04 | By default, the map should be centered on the user's device location pin.NoteIt means that the 'Fence Location Position' pin will be on the user's device location pin |
| ME04-US03-AC05 | The app should display the same 'Center on User Location' button as on the My Fences screen (see (Native Apps) ME15-F07. Center on User Location) |
| ME04-US03-AC06 | If I tap the 'Fence Tutorial' button, then the app should:Open Fence Tutorial (see (NA) ME04-F05. Fence tutorial) |
| ME04-US03-AC07 | The app should display/hide the same 'Compass' button as on the My Fences screen (see (Native Apps) ME15-F08. Map compass) |
| ME04-US03-AC08 | The app should always display the 'Fence Location Position' pin in the center of the screen and move the map underneath it (same as taxi apps). |
| ME04-US03-AC09 | If I tap the 'Address search field', then the app should:Expand the Address search card by sliding it up.Logic inside the expanded card is defined in (NA) ME04-US04. Add Fence: Step 1a. Search location by address. |
| ME04-US03-AC10 | Preconditions:There is an address in the 'Address search field'.If I drag the Map to place different from the location in the 'Address search field', then the app should:Clear the 'Address search field'. |
| ME04-US03-AC11 | If I tap the yellow part of the 'Fence Location Positioning' pin, then the app should behave the same as if the user taps the 'Create Fence' button. |
| ME04-US03-AC12 | If I tap the 'Create fence' button, then the app should:Check if:Location hovered with the 'Fence Location Position' pin is too zoomed out (less than 16th level).'Fence Location Position' pin is on the location of the existing fence.'Fence Location Position' pin is on the location of the extended road area (see (NA) ME04-US05. Add Fence: Step 2. Fence autogeneration attempt) | - |
| ME04-US03-AC13 | If the zoom scale on the map becomes less than 16, then the app should:Display the Zoom out error toast. | Figma |
| ME04-US03-AC14 | If I click the 'Create fence' button AND all validations mentioned above pass successfully, then the app should:Block the screen with a loader (see GUI-7 Full-screen loader)Trigger validations defined below in ME04-US03-AC15 and ME04-US03-AC16.If passed successfuly:Move to Step 2. Fence auto-generation process (see (NA) ME04-US05. Add Fence: Step 2. Fence autogeneration attempt)Get the updated list of the closest 20 existing fences in users account.NoteThe app should request the latest list of the closest 20 existing fences, so the app doesn't create the fence overlapping another fence if somebody created the fence at the same location using a different mobile device. | - |
| ME04-US03-AC15 | If the 'Fence Location Position' pin is on the location of the existing fence, then the app should:Display the Fence overlap error toast. | Figma |
| ME04-US03-AC16 | If the 'Fence Location Position' pin is on the location of the extended road area, then the app should:Didplay the Fence road intersection error toast | Figma |Tech details

After clicking on the “Create Fence” button, we should update the list of fences in case we don't have all the fences loaded.To do this, check that the number of fences in the list of already loaded fences is equal to geoFencesTotalCount. This value is returned in the geoFencesInfo model in GET /account/my/mapAfter that, we can check that the point is inside another fence

The AC15 criterion can only be verified once we have information about the objects on the map. This is described here - Auto-generate fences#Pre-generationchecks - item 1


