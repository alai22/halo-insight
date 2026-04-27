---
title: "(Won't do) ME03-US96 BE+MOB+FW: An ability of the end user to rescan the collar"
sidebar_label: "(Won't do) ME03-US96 BE+MOB+FW: An ability of the end user to rescan the collar"
sidebar_position: 294
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Estimates | Related pages |
|---|---|---|---|---|---|
| CANCELLED |
| Maryia Paklonskaya [X] |
| HALO-15599 - BE+MOB+FW: ME03-US96 An ability of the end user to rescan the collar Closed Was decided with Michael, Ken and Anton Tonkovich not to do.FW accumulates data during 24 hours. Implementing manual rescan requires rewriting FW business logic of diagnosis-very big scope. |
| create requirementsrefinementget final approval from the Halo LT finalised, ready for devadded final designsadd to the baselinenew article about what should you do when catastrophic issue happens (similar to https://support.halocollar.com/hc/en-us/articles/5575769230103)add changes about the lights blinking colours to the existing articles e.g. https://support.halocollar.com/hc/en-us/articles/360044743313-What-Do-the-LED-Lights-on-the-Collar-Mean- |
| BE: MOB: QA: FW: |
| Hardware issues detection ME03-F07. Collar Diagnostic[BL] ME03-US71. Add "Collar Diagnostic" section to the "Collars list" MQTT Communication implemented on the back-end |# User Story

\> As a USER I want to get notified when the collar is broken so that I do not use it for dog's protection

# Acceptance criteria

| ID | Acceptance criteria | Design |
|---|---|---|
| ME03-US96-AC01 | Add an ability of the end user to run the Diagnostic from the mobile app:Add button to the Daily Diagnostics screen "Rescan the Collar"By clicking on the button - the diagnostics of the collar should happenUpdate of the MQTT is needed here - will be done within LINKBE would send to the FW a trigger to re-scan the collar + get the updates + re-calculate all the issues ==\> update the "last seen" + issues of the collar | Android; iOS |
