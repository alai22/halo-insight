---
title: "ME03-US105. Collars images, SN and version updates"
sidebar_label: "ME03-US105. Collars images, SN and version updates"
sidebar_position: 304
author: "Mariya Kolyada"
---

# Acceptance criteria

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| HALO-15684 - MOB+BE: ME03-US105. Collars images, SN and version updates Closed |
| Click here to expand...As of 15 Feb 2023 Mariya Kolyada updated the US initial version created before.As of 16 Mar 2023 Mariya Kolyada added ME03-US105-AC07. |# Contents

Acceptance criteria Contents User story Acceptance criteria Implementation notes

# User story

\> As Halo account owner I want to see my pet image instead of collar or image with version if there is no assigned pet so that I can imediately inderstand what pet is assigned to the collar and what version it has.

# Acceptance criteria

| AC | Description | iOS screen designsDon't pay attention that serial number doesn't meet collar version. Designs just show where SN is displayed. | Android screen designs | Add collar | As is | To be | Collars list | Assign collar | Confirm collar choice |  | Condition | Displaying rules | As is | To be | As Is | To Be | As Is | To Be | Create fence | As Is | To Be | GPS initialization |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME03-US105-AC01 | Replace the collar image on the steps:“Connecting Over Bluetooth” "Your Halo Collar Has been Added To Your Account""This Halo Collar Is Assigned to Another Account"according to the following requirements:As isTo beDisplay collar image depending on collar versionDisplay collar image with “Yellow halo” (image from step “Linking Your Halo Collar to Your Account”) | Display collar image depending on collar version | Display collar image with “Yellow halo” (image from step “Linking Your Halo Collar to Your Account”) | “Connecting Over Bluetooth” screenZeplin "Your Halo Collar Has been Added To Your Account" screen"This Halo Collar Is Assigned to Another Account" screen | The same as iOsZeplin |
| Display collar image depending on collar version | Display collar image with “Yellow halo” (image from step “Linking Your Halo Collar to Your Account”) |
| ME03-US105-AC02 | Replace the current images of the collars according to the requirements below:ConditionDisplaying rulesAs isIf FE has access to BE.Display the collar image according to the Halo version.If FE has NO access to BE.Display the default "Collar Placeholder" image.To beIf I have an assigned pet to the collarDisplay this pet's image.NoteIf Pet has NO image - display the default paw (the same as on the Pet Card).If I have NO assigned pet to the collarDisplay the "Halo version" image according to the requirements in ME03-US105-AC03 below.If FE has no access to BEDisplay default "Collar Placeholder" imageNote: as we do it now, no changes here. | If FE has access to BE. | Display the collar image according to the Halo version. | If FE has NO access to BE. | Display the default "Collar Placeholder" image. | If I have an assigned pet to the collar | Display this pet's image.NoteIf Pet has NO image - display the default paw (the same as on the Pet Card). | If I have NO assigned pet to the collar | Display the "Halo version" image according to the requirements in ME03-US105-AC03 below. | If FE has no access to BE | Display default "Collar Placeholder" imageNote: as we do it now, no changes here. | "Collars list" screen"Assign collar" screen"Confirm collar choice" screen | The same as iOs |
| If FE has access to BE. | Display the collar image according to the Halo version. |
| If FE has NO access to BE. | Display the default "Collar Placeholder" image. |
| If I have an assigned pet to the collar | Display this pet's image.NoteIf Pet has NO image - display the default paw (the same as on the Pet Card). |
| If I have NO assigned pet to the collar | Display the "Halo version" image according to the requirements in ME03-US105-AC03 below. |
| If FE has no access to BE | Display default "Collar Placeholder" imageNote: as we do it now, no changes here. |
| ME03-US105-AC03 | The "Halo version" image should consist of the:"Yellow Paw" icon;H\<Halo version\>.Examples:H1, H2, H2+, H3 | The same as iOs |
| ME03-US105-AC04 | Move the Halo version to the collar list item’s TitleAs IsTo Be\<Pet Name\>’s HaloHalo \<Halo version\>Example:Buddy’s HaloHalo 2+\<Pet Name\>’s Halo \<Halo version\>Example:Buddy’s Halo 2+ | \<Pet Name\>’s HaloHalo \<Halo version\>Example:Buddy’s HaloHalo 2+ | \<Pet Name\>’s Halo \<Halo version\>Example:Buddy’s Halo 2+ | The same as iOs |
| \<Pet Name\>’s HaloHalo \<Halo version\>Example:Buddy’s HaloHalo 2+ | \<Pet Name\>’s Halo \<Halo version\>Example:Buddy’s Halo 2+ |
| ME03-US105-AC05 | Add label before the Serial number on the collar list itemAs IsTo Be\<Serial number\>Example:19-H152003-RTSN: \<Serial number\>Example:SN: 19-H152003-RT | \<Serial number\>Example:19-H152003-RT | SN: \<Serial number\>Example:SN: 19-H152003-RT | The same as iOs |
| \<Serial number\>Example:19-H152003-RT | SN: \<Serial number\>Example:SN: 19-H152003-RT |
| ME03-US105-AC06 | Update the Collar pin image according to the requirements from ME03-US105-AC02. | "Create fence" screen | The same as iOs |
| ME03-US105-AC07 | Add the Halo version to the Currently Using Pet on the 'Create Fence' screenAs IsTo BeCurrently Using \<Pet Name\>’s HaloExample:Currently Using Buddy’s HaloCurrently Using \<Pet Name\>’s Halo \<Halo version\>Example:Currently Using Buddy’s Halo 2+ | Currently Using \<Pet Name\>’s HaloExample:Currently Using Buddy’s Halo | Currently Using \<Pet Name\>’s Halo \<Halo version\>Example:Currently Using Buddy’s Halo 2+ | TBD"Create fence" → "Currently Using Pet" screenZeplin |  |
| Currently Using \<Pet Name\>’s HaloExample:Currently Using Buddy’s Halo | Currently Using \<Pet Name\>’s Halo \<Halo version\>Example:Currently Using Buddy’s Halo 2+ |
| ME03-US105-AC08 | Update the Collar pin image according to the requirements from ME03-US105-AC02. | "GPS initialization" screen | The same as iOs |### Implementation notes

| IN | Description |
|---|---|
| ME03-IN105-AC01 | During BE estimation backward compatibility should be taken into the account. |
| ME03-IN105-AC02 | BE side should store default images that depend on the Halo versionZenlin link |
