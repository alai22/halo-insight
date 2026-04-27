---
title: "[BL] ME03-US57. Deactivated collar errors on binding it to the user"
sidebar_label: "[BL] ME03-US57. Deactivated collar errors on binding it to the user"
sidebar_position: 151
last_modified: "Oct 05, 2021"
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED (SQ) |
| Maria Shikareva [X], Anastasia Brechko (QA), Timofey Burak [X] (MOB) |
| HALO-7484 - MOB: Handle deactivation on binding collar to user Closed Ballpark estimations:MOB 0,5SPQA 1SP |
| 28 Jun 2021 Maria Shikareva [X] ME03-US57-AC01 is updated (the error will be shown when the user taps on the 'Next' button → mobile app will know that the collar is deactivated only after this action). The link to Appendix 3 – Error, Success, Warning Messages is added.05 Oct 2021 Maria Shikareva [X] The story is marked as implemented and baselined. |# Contents

User story Acceptance criteria

# User story

\> As an owner I want to see an error message if my collar is deactivated so that to be notified about it.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME03-US57-AC01 | Precondition: the user has scanned QR code on the deactivated collar or entered a collar SN manually on the 'Add New Collar' scree while adding a collar to the account (see ME03-F00-AC04).When the user taps on the "Next" button, then the app should display M192 Deactivated collar. | - | - |
