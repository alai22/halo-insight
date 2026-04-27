---
title: "[BL] ME04-US85. Prompting screen for Add Fence"
sidebar_label: "[BL] ME04-US85. Prompting screen for Add Fence"
sidebar_position: 381
last_modified: "Jun 07, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owners | Links to JIRA Issues | Related requirements |
|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-18979 - MOB: Prompt to upgrade if user exceeds fence limit Closed HALO-19068 - BE: Prompt to upgrade if user exceeds fence limit Closed |
| M58 Fence restrictionM288 Fence restriction |## User story

\> As a Halo Collar account owner I want to be able to see the prompt to upgrade screen having button that send email with magic link so that I can easily upgrade my plan and add more fences.

## Acceptance criteria

| AC | Description | Design |
|---|---|---|
| ME04-US85-AC01 | Pre-conditions:I am a user with No plan (never had a plan)I have less than 5 fences in my account.IF I click "Add fence"THEN I should see 'Create New Fence' screen |  |
| ME04-US85-AC02 | Pre-conditions:I am a user with No plan (never had a plan)I have 5 fences or more in my account.IF I click "Add fence"THEN I should see popup M288 Fence restrictionTitle: 'No collar'Body: 'You need to have a Halo Collar to add more than 5 fences'. (5 is configurable)Button: "Ok", by click close popup |  |
| ME04-US85-AC03 | Pre-conditions:I am a Bronze plan member (including temporary access to plan).I have less than 5 fences in my account.IF I click "Add fence"THEN I should see 'Create New Fence' screen |  |
| ME04-US85-AC04 | Pre-conditions:I am a Bronze plan member (including temporary access to plan).I have 5 fences or more in my account.IF I click "Add fence"THEN I should see prompting screen ME19-US39. Replace prompting screens having video with screen having magic link#ME19-US39-AC03 |  |
| ME04-US85-AC05 | Pre-conditions:I am a Silver plan member (including temporary access to plan).I have 20 fences or more in my account.IF I click "Add fence"THEN I should see prompting screen ME19-US39. Replace prompting screens having video with screen having magic link#ME19-US39-AC03 |  |
| ME04-US85-AC06 | Pre-conditions:I am a Silver plan member (including temporary access to plan).I have less than 20 fences in my account.IF I click "Add fence"THEN I should see 'Create New Fence' screen |  |
| ME04-US85-AC07 | Pre-conditions:I am a Gold plan member (including temporary access to plan).I have more than 20 fences in my account.IF I click "Add fence"THEN I should see 'Create New Fence' screen (remove 20 fences limitation popup) |  |
| ME04-US85-AC08 | Pre-conditions:I am a Gold plan member (including temporary access to plan).I have 1000 fences in my account.IF 1001st fence is being savedTHEN I should see Appendix 3 – Error, Success, Warning Messages#M17Technicalerror M126 Communication error HALO-19405 - MOB: error for 1000 fences Closed |  |
| ME04-US85-AC09 | Pre-conditions:I am a user with No plan.I previously had a plan.IF I click "Add fence"THEN I should see prompting screen ME19-US39-AC09 |  |
