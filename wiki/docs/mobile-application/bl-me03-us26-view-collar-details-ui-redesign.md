---
title: "[BL] ME03-US26. View Collar details (UI redesign)"
sidebar_label: "[BL] ME03-US26. View Collar details (UI redesign)"
sidebar_position: 56
author: "Galina Lonskaya"
---

| Role | Epic | Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|---|
| Owner |
| ME03 Manage collars |
| REVISED |
| Galina Lonskaya |
| HALO-3106 - MOB: ME03-US26. View Collar details (UI redesign) Closed |
| 07 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As an owner, I want to view the collars list with the improved UI/UX design so that I can get better UX out of the interaction with the collars list app functionality.

| AC | Description | Collar cards opening logic | Expanded collar card functionality description | "Pet" tile | "Last heard" tile | "Find My Collar" button | "Wi-Fi" tile | "LTE" tile | "Collar Update" tile | Remove collar |
|---|---|---|---|---|---|---|---|---|---|---|
| ME03-US26-AC01 | I can see minimized and expanded info about the collar by tapping the list item with a collar.Down icon illustrates that expanded view will be opened and the Up icon will collapse expanded view. |
| ME03-US26-AC02 | I can open/hide expanded info at any collar. Only one collar could have expanded view at a time. |
| ME03-US26-AC03 | The app should hide the expanded info when I tap the minimized card of this collar or another collar. |
| ME03-US26-AC04 | If I expand the collar tile, then the following data should be displayed:Pic - Collars list with the expanded collarcard (with the gotten telemetry)Pic - Collars list with the expanded collarcard (without the gotten telemetry) | Pic - Collars list with the expanded collarcard (with the gotten telemetry) | Pic - Collars list with the expanded collarcard (without the gotten telemetry) |
| Pic - Collars list with the expanded collarcard (with the gotten telemetry) | Pic - Collars list with the expanded collarcard (without the gotten telemetry) |
| ME03-US26-AC05 | If the pet is linked to the collar, then:\<Pet Photo\> + HALO ring in color of pet + "Currently linked to" text + \<Pet's name\> + Right arrow button" should be displayed. |
| ME03-US26-AC06 | If the pet isn't linked to the collar, then:"Not linked to a pet" text + "Right Arrow" icon should be displayed. |
| ME03-US26-AC08 | Precondition: The collar is linked to the pet.If I tap on the Pet tile, then see the continuation in ME03-US27. View "Link Pet /Disconnect Collar from the Pet" action sheet (UI redesign) |
|  | Precondition: The collar isn't linked to any pet.If I tap on the Pet tile, then see the continuation in ME03-US30 Add Collar (UI redesign) Pair collar with a pet. |
| ME03-US26-AC09 | If there is the gotten telemetry related to the "last heard", then:"Last heard" text + \<last heard timestamp\> + "Find My Collar" button should be displayed. |
| ME03-US26-AC10 | If there is no gotten telemetry related to the "last heard", then:"Last heard" text + "No data" text + "Find My Collar" button should be displayed. |
| ME03-US26-AC11 | If I tap on Find My collar, then the following warning message should be displayed: Title: WarningBody: This is not recommended if your dog is wearing the Halo collar. Find now anyway?Button: Find → see ME03-US26-AC12Button: Cancel → popup should be closed. |
| ME03-US26-AC12 | If I tap on the Find button, then while the collar answer isn't got, the spinner should be displayed instead of the Find My Collar button. |
| ME03-US26-AC13 | If I tap on the Find My collar button and there is no answer from BE, then the toast message with failure should be displayed.Text: Your collar wasn't found. Try again.Note: Toast message is displayed temporarily. |
| ME03-US26-AC14 | If I tap on the Find My collar button and the collar receives the "Find My Collar" command, then the toast message with success should be displayed.Text: We found your collar. It should blink and play a sound for 10 sec.Note 1: Toast message is displayed temporarily.Note 2: The collar plays an audible tone once and blinks LEDs for 10 seconds. The tone should be unique and not used for any other pet commands. |
| ME03-US26-AC15 | The cellular tile should have the same UI as in Zeplin.See the functionality description in ME03-US19. Update Wi-fi/LTE connection status / signal strength displaying at the Collars List. |
| ME03-US26-AC16 | I can initiate a WiFi network changing from this screen. See continuation in ME03-US03. Connect WiFi Network. |
| ME03-US26-AC17 | The cellular tile should have the same UI as in Zeplin.See the functionality description in ME03-US19. Update Wi-fi/LTE connection status / signal strength displaying at the Collars List. |
| ME03-US26-AC18 | If the collar has "Up to date" FW, then:"Up to date" text + "(" + "version" text + \<XX.XX.XX\> + ")" should be displayed (if the version is known) |
| ME03-US26-AC19 | If the collar doesn't have "Up to date" FW, then:"Version" text + \<version number XX.XX.XX\> + "is available" text should be displayed at the Collar Update tile"Exclamation mark" near the collar photo should be displayed. |
| ME03-US26-AC20 | If I initiate collar deletion by tapping "Remove This Device", then: the app should show M23 Delete Collar message to confirm this action and initiate deletion. |
| ME03-US26-AC21 | If I submit deletion, then:the collar should be deleted;the updated collars list should be displayed. |
