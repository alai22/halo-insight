---
title: "(NA) ME04-US05. Add Fence: Step 2. Fence autogeneration attempt"
sidebar_label: "(NA) ME04-US05. Add Fence: Step 2. Fence autogeneration attempt"
sidebar_position: 510
last_modified: "Apr 16, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owner | Links to JIRA/Linear Issues | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada Dmitry Kravchuk |
| iOS: https://linear.app/fueled/issue/HALO-657/[ios]-add-fence-step-2-fence-autogeneration-attemptAndroid: https://linear.app/fueled/issue/HALO-658/[android]-add-fence-step-2-fence-autogeneration-attempt |
| 24 Mar 2025 Mariya Kolyada created the initial version of a user story. |# Contents

Contents User story Acceptance criteria

# User story

\> As Halo app account owner, I want the app autogenerate the fence for me so I spend less time on the fence creation.

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US05-AC01 | When the app autogenerates a fence, it should generate fence outline:initially based on registered property linesand then adjusting it by following the rules:-5 meters inside from the road.at least +(5 + \<warning zone\>) meters out from the building(s) inside the fence (if a registered property is not big enough and there is less than such a distance between the building and the registered property line)+\<warning zone\> meters out of registered property lines only in parts where there is no road nearby. |
| ME04-US05-AC02 | Distances from:road;building (without warning zone);should be manageable via config. |
| ME04-US05-AC03 | Warning zone should be manageable via config.The current value is 2 meters. |
| ME04-US05-AC04 | All implementation details related to the autogeneration algorithm can be found here: Auto-generate fences |
| ME04-US05-AC05 | All implementation details related to the map objects retrieving algorithm can be found here: Retrieving map objects |
| ME04-US05-AC06 | All implementation details related to the validation of fence intersection with hazards can be found here: Validation of intersections with objects on the map |
| ME04-US05-AC07 | After autogeneration the app should proceed with one of the following steps depending on the results of generation:(NA) ME04-US06. Add Fence: Step 3a. Simple square fence edit(NA) ME04-US07. Add Fence: Step 3b. Confirm Fence |Tech details

The logic on determining whether we can generate a fence or should make a simple square is also described here - Auto-generate fences


