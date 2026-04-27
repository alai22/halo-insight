---
title: "ME04-US50. Create a fence (mixed flow): add the Find Collar/Stop Sound buttons"
sidebar_label: "ME04-US50. Create a fence (mixed flow): add the Find Collar/Stop Sound buttons"
sidebar_position: 103
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue |
|---|---|---|
| REVISED |
| Galina Lonskaya |
| HALO-4732 - iOS: Create a fence (mixed flow): add the Find Collar button Closed |# User story

\> As an owner, I want to have access to the Find Collar button so that I can initiate the collar finding process by myself.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| ME04-US50-AC01 | Right after the "Find Collar - Confirmation" screen opening, the "Find the collar" request should NOT be sent to the collar automatically anymore. | ME04-US27-AC02 isn't valid anymore, see initial requirements in ME04-US27. Create a fence (mixed flow): confirm the correct collar pairing |
| ME04-US50-AC02 | The Find Collar screen UI and the text should be updated. The Find Collar button should be added and the new screen title should be used: Confirm Collar Choice. |  |
| ME04-US50-AC03 | If I tap on the Find Collar button, then: the "Find Collar" request should be sent to the collar; while request sending the spinner should be displayed at the button. |  |
| ME04-US50-AC04 | If the "Find Collar" request is sent to the collar successfully, then:the temporary toast message with the success message should be displayed: We found your collar. It should blink and play a sound for 10 sec.the collar should blink/beep for about 10 seconds;instead of the Find Collar button should be displayed the Stop Sound button for 10 seconds. After 10 seconds, the Find Collar text should be displayed again on the button. |  |
| ME04-US50-AC05 | If the "Find Сollar" request is failed due to the reason that the collar is not available (for instance, the collar is turned off or doesn't have Wi-Fi), then:the toast message with failure should be displayed for 4 sec: Your collar wasn't found. Try again. | See the same logic description for Find Collar/Stop Sound in ME03-US44. "Find Collar" at Collars list (logic update). |
| ME04-US50-AC06 | If I tap on the Stop Sound button and the request is sent successfully, then:the collar should stop blinking/beeping;instead of the Stop Sound button should be displayed on the Find Collar button. |
| ME04-US50-AC07 | If the "Stop Sound" request is failed due to the reason that the collar is not available (for instance, the collar is turned off or doesn't have Wi-Fi), then:then the toast message with failure should be displayed for 4 sec: Your collar wasn't found. Try again. |
| ME04-US50-AC08 | The unique sound should be used for the Find Collar command.Note: should be implemented on the FW side |
| ME04-US50-AC09 | The Find Collar sound should be increased incrementally.Note: should be implemented on the FW side |
