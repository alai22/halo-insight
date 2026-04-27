---
title: "(BL) ME03-US137 BE+MOB: Update popup when user clears cat. issues if there are no issues"
sidebar_label: "(BL) ME03-US137 BE+MOB: Update popup when user clears cat. issues if there are no issues"
sidebar_position: 320
last_modified: "May 15, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages | History changes |
|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-16693 - MOB: Update wordings for popup M271 Closed |
| The affected requirements:(BL) ME03-US121 BE+MOB: Ability to reset catastrophic issueAppendix 3 – Error, Success, Warning Messages#M271Therearenocatastrophicissues |
| 15 May 2024 Kiryl Trafimau Baselined to Appendix 3 – Error, Success, Warning Messages#M271Therearenocatastrophicissues |User Story Acceptance Criteria ME03-US137-AC03

# User Story

\> As a Halo account USER owner I want to reset catastrophic issue behavior if I think that issue on collar is fixed so that I can use the collar

# Acceptance Criteria

| ID | Acceptance criteria | Design |
|---|---|---|
| ME03-US137-AC03 | Precondition: previously Daily diagnostics reported that catastrophic issue was detected user opened Daily diagnostic screen, then issues were cleared from another device OR AAPIF 'clear issues' request is sent when there is no catastrophic issues deteceted, THEN return an error Appendix 3 – Error, Success, Warning Messages#M271TherearenocatastrophicissuesTitle: 'There are no issues'Body: 'The issue(s) has been cleared.'OK button, redirect to My collars screen |  |
