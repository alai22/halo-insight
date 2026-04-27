---
title: "ME02-US32. Replace technical error pop-up when user cannot join a meeting"
sidebar_label: "ME02-US32. Replace technical error pop-up when user cannot join a meeting"
sidebar_position: 610
last_modified: "Jan 20, 2022"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada |
| HALO-9745 - [MOB]: ME02-US32. Replace technical error pop-up when user cannot join a meeting Closed |
| As of 06 Dec 2021 Mariya Kolyada created the initial version of US. |# User Story

\> As Halo Collar app account owner I want to get suggestion to use other support options in case of some technical error so that I won't be confused by suggestion to use support when I'm currently trying to use it.

# Acceptance criteria

| AC | Description | iOS UI design | Android UI design |
|---|---|---|---|
| ME02-US32-AC01 | PreconditionThe Settings screen is openedIf I click on the Live support option and some unexpected technical error has happened, the app should: Display custom M215 Error Accessing Dog Park instead of general M17 Technical error.NoteAn unexpected technical error can be for example in one of the following cases: internet loss, smth wrong with meeting token, ZoomSDK error, etc. | - | - |
