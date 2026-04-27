---
title: "[BL] ME04-US55. Update text below Warning Area and Protection Zone on the Fence Card"
sidebar_label: "[BL] ME04-US55. Update text below Warning Area and Protection Zone on the Fence Card"
sidebar_position: 287
last_modified: "Oct 03, 2024"
author: "Ekaterina Dupanova"
---

| Document status | Story owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-14484 Closed |
| Click here to expand...As of 04 Nov 2022 Ekaterina Dupanova created initial version of the U |# User story Acceptance criteria

# User story

As a Halo app account owner I want to see more specific explanation for Warning Area and Protection Zone on the Fence Card so as to understand better what happens in each of these areas.

# Acceptance criteria

| AC | Description | iOS screen design | Android screen design | As Is (below Warning Area) | To Be (below Warning Area) | As Is (below Protection Zone) | To Be (below Protection Zone) |
|---|---|---|---|---|---|---|---|
| ME04-US55-AC01 | Precondition: a user taps on the Questionmark buttonThe system opens the Fence Legend sheet should be opened (a similar sheet as used for Instant Feedback, see ME05-FE00. Instant feedback)As Is (below Warning Area)To Be (below Warning Area)Warning and Boundary Feedback will only occur while your dog is inside this area + heading toward the boundary. Warning and Boundary Feedback will occur only while your dog is inside this area and moving toward the fence line. Feedback stops if your dog stops or turns around.As Is (below Protection Zone)To Be (below Protection Zone)In the Protection Zone, your dog only receives Emergency Feedback while moving away from the boundary. When your dog stops moving OR heads home, Emergency Feedback stops and Encouragement Feedback begins. Beyond the Protection Zone, your dog’s Halo enters Lost Mode.In the Protection Zone, your dog will receive Emergency Feedback, along with Warning and Boundary feedback, while moving further away from the fence line. When your dog stops moving OR heads back home, Preventions stop and the Return Whistle is used to guide your dog to safety. Beyond the Protection Zone, your dog’s Halo enters Lost Mode and only uses the Return Whistle periodically. | Warning and Boundary Feedback will only occur while your dog is inside this area + heading toward the boundary. | Warning and Boundary Feedback will occur only while your dog is inside this area and moving toward the fence line. Feedback stops if your dog stops or turns around. | In the Protection Zone, your dog only receives Emergency Feedback while moving away from the boundary. When your dog stops moving OR heads home, Emergency Feedback stops and Encouragement Feedback begins. Beyond the Protection Zone, your dog’s Halo enters Lost Mode. | In the Protection Zone, your dog will receive Emergency Feedback, along with Warning and Boundary feedback, while moving further away from the fence line. When your dog stops moving OR heads back home, Preventions stop and the Return Whistle is used to guide your dog to safety. Beyond the Protection Zone, your dog’s Halo enters Lost Mode and only uses the Return Whistle periodically. | Link to Zeplin |  |
| Warning and Boundary Feedback will only occur while your dog is inside this area + heading toward the boundary. | Warning and Boundary Feedback will occur only while your dog is inside this area and moving toward the fence line. Feedback stops if your dog stops or turns around. |
| In the Protection Zone, your dog only receives Emergency Feedback while moving away from the boundary. When your dog stops moving OR heads home, Emergency Feedback stops and Encouragement Feedback begins. Beyond the Protection Zone, your dog’s Halo enters Lost Mode. | In the Protection Zone, your dog will receive Emergency Feedback, along with Warning and Boundary feedback, while moving further away from the fence line. When your dog stops moving OR heads back home, Preventions stop and the Return Whistle is used to guide your dog to safety. Beyond the Protection Zone, your dog’s Halo enters Lost Mode and only uses the Return Whistle periodically. |
