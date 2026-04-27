---
title: "ME03-US128. Show a new collar type Halo 4 in Collars list (mob app)"
sidebar_label: "ME03-US128. Show a new collar type Halo 4 in Collars list (mob app)"
sidebar_position: 368
author: "Galina Lonskaya"
---

# Acceptance criteria

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-19524 - MOB: Show a new collar type on Collar list: Halo 4 (May 2024) Closed |
| Click here to expand... |# Contents

Acceptance criteria Contents User story Acceptance criteria Implementation notes

# User story

\> As Halo account owner I want to know which generation my collar belong to so that I could easily tell one collar from another in the list

# Acceptance criteria

| AC | Description | iOS screen designs/ implementation status | Android screen designs/ implementation status |
|---|---|---|---|
| ME03-US128-AC01 | PreconditionBoth following conditions are met:Some of my collars have a serial number with product type code (PP) == "H4" (see BR-10 Serial Number format).Example: 19-H452003-RTIf I open one of the following screens:"Adding Your Collar" screens;"Collars list" screen;"Assign a Collar" screen;"Confirm Collar Choice" screen;then the app should for the collars from precondition:Display the "Halo 4" label. | - | - |
| ME03-US128-AC02 | Display H4 image for Halo 4. | See Zeplin. | The same as for iOS |### Implementation notes

| IN | Description | Collar | Hardware | CollarType | Chip |
|---|---|---|---|---|---|
| ME03-IN128-AC01 | During mob estimation backward compatibility should be taken into the account. |
| ME03-IN128-AC02 | Collar types in DB: CollarHardware CollarTypeChipHalo 11version1lteQualcommHalo 21Version2QualcommHalo 2+2version2plusAirohaHalo 33version3AirohaHalo 33version3finalAirohaHalo 4 4version4Airoha | Halo 1 | 1 | version1lte | Qualcomm | Halo 2 | 1 | Version2 | Qualcomm | Halo 2+ | 2 | version2plus | Airoha | Halo 3 | 3 | version3 | Airoha | Halo 3 | 3 | version3final | Airoha | Halo 4 | 4 | version4 | Airoha |
| Halo 1 | 1 | version1lte | Qualcomm |
| Halo 2 | 1 | Version2 | Qualcomm |
| Halo 2+ | 2 | version2plus | Airoha |
| Halo 3 | 3 | version3 | Airoha |
| Halo 3 | 3 | version3final | Airoha |
| Halo 4 | 4 | version4 | Airoha |
