---
title: "[Won't have] ME03-US139. Charge Reminder"
sidebar_label: "[Won't have] ME03-US139. Charge Reminder"
sidebar_position: 321
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| CANCELED |
| Kiryl Trafimau |
| HALO-16705 - MOB, BE: Charge reminder Closed HALO-16770 - BE+FW: Method to receive charging status in real-time Resolved HALO-16771 - BE+FW: Update MQTT Closed HALO-16831 - FW: Send telemetry when collar starts charging In Progress |
|  |# User story

\> As an app user, I want to receive reminder to charge the collar battery So that my collars are always charged and functioning.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design |
|---|---|---|---|
| ME03-US139-AC01 | WHEN I am on the Settings screenTHEN I can see option Charge Reminder |  |  |
| ME03-US139-AC02 | IF I click Charge Reminder optionTHEN I redirected to the Charge Reminder screen:Screen title: 'Charge Reminder' TBD2. 'Back' button, navigation to Settings screen3. 'Done' button, appears if time changed or toggle changed,by click:-saves changes,-navigation to Settings screen4. Title: 'Get Your Collar Ready for Everyday' TBD5. 'Receive notifications that remind you tocharge your Halo collars if it is not set to the charger at a selected time' text. TBD6. 'Remind to charge my Halo collars' toggle, enabled by default. TBD7. 'Time' time selector, default value 8 PM.IF Interner error then display text "TBD" - as on beacon listIF BE not responding then display text "TBD" - as on beacon list | Remove tab bar, rename back to canceluse other control which selects by 15-30 mins, add text that time is approximate |
| ME03-US139-AC03 | IF collar did not send Telemetry for 2 days in the rowTHEN mark this collar as a 'Collar not in use'2. IF 'Collar not in use' sent Telemetry dataTHEN mark this collar as a 'Collar in use' |  |
| ME03-US139-AC04 | IF at least one 'Collar in use' is not on the charger according to the last telemetryWHEN Remind time THENIF this is not first notification for this userTHEN Send push-notification to the user:If 1 collar: '[Dog's Name 1] collar is not on the charger.' TBDIf 2 or more collars: '[Dog's Name 1], [Dog's Name 2], [Dog's Name N] collars are not on the charger.' TBDWhen tap on notification: open app on MyMap |  |
| ME03-US139-AC05 | IF at least one 'Collar in use' is not on the charger according to the last telemetryWHEN Remind time THENIF this is first notification for this userTHEN Send Event to Braze |  |
| ME03-US139-AC06 | IF all collars are on the charger according to the last telemetry OR only 'Collar not in use' are not on the chargerWHEN Remind time THEN Not send push-notification to the user |  |
| ME03-US139-AC07 | Notes:Track time according to the latest time received from any collar in the account2. If there are multiple mobile devices with Halo app with the same account-they all will receive push notifications. |  |  |
