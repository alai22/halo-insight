---
title: "ME21-US51. Eliminate assigning first collar from Feedback testing"
sidebar_label: "ME21-US51. Eliminate assigning first collar from Feedback testing"
sidebar_position: 731
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Updates | Link to JIRA Issue |
|---|---|---|---|
| APPROVED |
| Maryia Paklonskaya [X] Dmitry Kravchuk |
| 03 Feb 2023 updated due to new input from the development team |
| HALO-15360 - [MOB] ME21-US51: Eliminate assigning first collar from Feedback testing Closed |# Contents

Acceptance criteria

# Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME21-US49-AC01 | If a pet does not have an assigned collar - the app should not display the 'Test On Collar' button at all. | - |
| ME21-US49-AC02 | M79 No collar for testing error message should be deleted.QA note: ME05-FE05-AC02 is changed. |  |
| ME21-US49-AC03 | In case the "Test on collar" was pressed for already deleted collar - the common technical issue should be displayed |  |
