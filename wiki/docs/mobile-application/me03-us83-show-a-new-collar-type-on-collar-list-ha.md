---
title: "ME03-US83. Show a new collar type on Collar list: Halo 3"
sidebar_label: "ME03-US83. Show a new collar type on Collar list: Halo 3"
sidebar_position: 247
author: "Galina Lonskaya"
---

# Acceptance criteria

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada |
| HALO-11818 - MOB+BE: ME03-US83. Show a new collar type on Collar list: Halo 3 Closed |
| Click here to expand...As of 24 Jan 2023 Mariya Kolyada updated the US initial version created before. |# Contents

Acceptance criteria Contents User story Acceptance criteria Implementation notes

# User story

\> As Halo account owner I want to know which generation my collar belong to so that I could easily tell one collar from another in the list

# Acceptance criteria

| AC | Description | iOS screen designs/ implementation status | Android screen designs/ implementation status |  |
|---|---|---|---|---|
| ME03-US83-AC01 | PreconditionBoth following conditions are met:Some of my collars have a serial number with product type code (PP) == "H3" (see BR-10 Serial Number format).Example: 19-H352003-RTThe same collars have HardwareVersion = "3".If I open one of the following screens:"Adding Your Collar" screens;"Collars list" screen;"Assign a Collar" screen;"Confirm Collar Choice" screen;then the app should for the collars from precondition:Display the "Halo 3" label. | - | - |
| ME03-US83-AC02 | Image updates will be implemented in the separate US: https://portal.softeq.com/display/HALO/%5BNI%5D+ME03-US105.+Collars+images%2C+SN+and+version+updates |
| Note: this AC is already implemented, see HALO-11763 - MOB: Change wording for 'unsupported collar' Closed If for any reason Halo app didn't recognize a new collar type, then the app should:Display the "Unrecognized collar" label within the Collars list. |### Implementation notes

| IN | Description | Collar | Hardware | CollarType | Chip |
|---|---|---|---|---|---|
| ME03-IN83-AC01 | During mob estimation backward compatibility should be taken into the account. |
| ME03-IN83-AC02 | Collar types in DB: CollarHardware CollarTypeChipHalo 11version1lteQualcommHalo 21Version2QualcommHalo 2+2version2plusAirohaHalo 33version3Airoha | Halo 1 | 1 | version1lte | Qualcomm | Halo 2 | 1 | Version2 | Qualcomm | Halo 2+ | 2 | version2plus | Airoha | Halo 3 | 3 | version3 | Airoha |
| Halo 1 | 1 | version1lte | Qualcomm |
| Halo 2 | 1 | Version2 | Qualcomm |
| Halo 2+ | 2 | version2plus | Airoha |
| Halo 3 | 3 | version3 | Airoha |
