---
title: "(Native Apps) ME01-FXX. Navigation after app launch"
sidebar_label: "(Native Apps) ME01-FXX. Navigation after app launch"
sidebar_position: 520
last_modified: "Mar 22, 2025"
author: "Galina Lonskaya"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| DRAFT |
| Mariya Kolyada, Dmitry Kravchuk |
|  |
|  |# Contents

Contents User story Acceptance criteria Scenario 1: Has subscription + Single Collar assigned to the account Scenario 2: Has subscription + Multiple Assigned Collars Scenario 3: Has subscription + Unassigned Pet Scenario 4: No subscription + Never had before Scenario 5: Lost subscription

# User story

\> As Halo app account owner, I want TBD

# Acceptance criteria

| AC | Description | Design | Scenario 1: Has subscription + Single Collar assigned to the account | Scenario 2: Has subscription + Multiple Assigned Collars | Scenario 3: Has subscription + Unassigned Pet | Scenario 4: No subscription + Never had before | Scenario 5: Lost subscription |
|---|---|---|---|---|---|---|---|
| ME01-FXX-AC | If I have subscription and 1 collar assigned to the pet in my account and I launch the app, then:My Fences tab should be opened. |  |
| ME01-FXX-AC | Precondition: I have subscription and 1 collar assigned to the pet in my accountIf the pet is inside fence at the moment, then My Fences should have the following state:my map should center on the fence, if the pet is inside fence at the momentthe Pet Card should be opened. | Figma |
| ME01-FXX-AC | Precondition: I have subscription and 1 collar assigned to the pet in my accountIf the pet is outside any fence at the moment, then My Fences tab should have the following state:my map should center on the pet pin, the Pet Card should be opened. |  |
| ME01-FXX-AC | If I have subscription and more than 1 collar assigned to the pets in my account, then:My Fences tab should be opened. |  |
| ME01-FXX-AC | Precondition: I have subscription and more than 1 collar assigned to the pets in my account My Fences should have the following state:The My Fences tab opens to the fence(s) containing the collarsadjusting the zoom to fit all collars in view and centering on the pet pins' centroid.The Pet Card is closed by default TBD with Mariya | Figma |
|  | If I have subscription and more than 1 collar assigned to the pets in my account, then:My Fences tab should be opened. |  |
|  | My Fences should have the following state:The My Fences tab opens to the fence(s) containing the collarsadjusting the zoom to fit all collars in view and centering on the pet pins' centroid.The Pet Card is closed |  |
|  |  |  |
|  |  |  |
|  |  |  |
