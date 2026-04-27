---
title: "(BL) ME03-US102 BE+FW: Actions on collar in case of catastrophic issue"
sidebar_label: "(BL) ME03-US102 BE+FW: Actions on collar in case of catastrophic issue"
sidebar_position: 300
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Link to JIRA Issue | BA processes | Estimates | Related pages | Change history |
|---|---|---|---|---|---|---|
| APPROVED |
| Maryia Paklonskaya [X] Kiryl Trafimau |
| HALO-15600 - BE+FW: ME03-US102 Actions on collar for catastrophic issues Closed HALO-15625 - FW: ME03-US102 Catastrophic issues: actions on collar Closed |
| create requirementsrefinementget final approval from the Halo LT finalised, ready for devadd to the baseline |
| BE: 1sp (without lost subscriptions)FW: 1 sprintQA: 3sp (without lost subscriptions) |
| MQTT Communication implemented on the back-end |
| 03 May 2024 Kiryl Trafimau Baselined to ME03-F07. Collar Diagnostic |# User Story

\> As a Business Owner I don't want users to keep using collars when there is a catastrophic issue with the collar

# Acceptance Criteria

| ID | Acceptance criteria |  | BE |  | FW | GIVEN | WHEN | THEN | GIVEN | WHEN | THEN | GIVEN | WHEN | THEN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME03-US102-AC01 | If during daily diagnostics the catastrophic issue was detected - BE should send trigger to TWIN about that so that collar started actions |
| ME03-US102-AC02 | Precondition: Collar received message that catastrophic issue was detectedIf the catastrophic issue was resolved - BE should send trigger to TWIN about that so that collar stopped actions |
| BE Technical Notes | Remove IsDisabled for the collar in twin if the collar's FirmwareVersion has been changed (otherwise the collar could not update to the new FW version) |
| ME03-US102-AC03 | Any catastrophic issueGIVENCollar got from the BE trigger (via TWIN) that any catastrophic issue except Compass (MEMS chip failure) happened ORCollar got from the BE trigger (via TWIN) that user has no longer subscription (and previously had)WHENThe collar is taken off from the charger AND started to move according to AccelerometerTHENActions should start on the collar:short vibration every secondswitch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light)Compass (MEMS chip failure)GIVENCollar got from the BE trigger (via TWIN) that catastrophic issue Compass (MEMS chip failure) happened WHENThe collar is taken off from the chargerTHENActions should start on the collar:switch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light)Any catastrophic issue+Compass (MEMS chip failure)GIVENCollar got from the BE trigger (via TWIN) that catastrophic issue Compass (MEMS chip failure) happenedAND Collar got from the BE trigger (via TWIN) that any catastrophic issue except Compass (MEMS chip failure) happenedWHENThe collar is taken off from the chargerTHENActions should start on the collar:switch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light)Actions will happen on the new versions of the FW only.Actions should stop when the collar is plugged in for charging. | Collar got from the BE trigger (via TWIN) that any catastrophic issue except Compass (MEMS chip failure) happened ORCollar got from the BE trigger (via TWIN) that user has no longer subscription (and previously had) | The collar is taken off from the charger AND started to move according to Accelerometer | Actions should start on the collar:short vibration every secondswitch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light) | Collar got from the BE trigger (via TWIN) that catastrophic issue Compass (MEMS chip failure) happened | The collar is taken off from the charger | Actions should start on the collar:switch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light) | Collar got from the BE trigger (via TWIN) that catastrophic issue Compass (MEMS chip failure) happenedAND Collar got from the BE trigger (via TWIN) that any catastrophic issue except Compass (MEMS chip failure) happened | The collar is taken off from the charger | Actions should start on the collar:switch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light) |
| Collar got from the BE trigger (via TWIN) that any catastrophic issue except Compass (MEMS chip failure) happened ORCollar got from the BE trigger (via TWIN) that user has no longer subscription (and previously had) |
| The collar is taken off from the charger AND started to move according to Accelerometer |
| Actions should start on the collar:short vibration every secondswitch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light) |
| Collar got from the BE trigger (via TWIN) that catastrophic issue Compass (MEMS chip failure) happened |
| The collar is taken off from the charger |
| Actions should start on the collar:switch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light) |
| Collar got from the BE trigger (via TWIN) that catastrophic issue Compass (MEMS chip failure) happenedAND Collar got from the BE trigger (via TWIN) that any catastrophic issue except Compass (MEMS chip failure) happened |
| The collar is taken off from the charger |
| Actions should start on the collar:switch colors RED and WHITE once every second on the Logo Lightshort blinking RED once every second (Battery/Charge Light and GPS/Bluetooth Light) |
| ME03-US102-AC04 | When collar gets from the BE that catastrophic issue is no longer trueOROnce the collar got from the BE that user has subscriptionTHENAll actions on collar should be stopped |
| ME03-US102-AC05 | IF actions on collar startedWHEN collar was rebootedTHEN actions on collar stopped until collar is taken from charger and moved again (just taken from charger for MEMS chip failure) |
