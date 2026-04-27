---
title: "ME04-US99. Add fence posts in the fence edit and creation events in Azure AppInsights"
sidebar_label: "ME04-US99. Add fence posts in the fence edit and creation events in Azure AppInsights"
sidebar_position: 673
last_modified: "May 17, 2024"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] |
| HALO-20279 - MOB+BE: ME04-US99. Add fence posts in the fence edit and creation events in Azure AppInsights Closed |
| Click here to expand...As of 15 May 2024:Mariya Kolyadacreated the initial version of US. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo Product Owner I want to be able to download the fence posts position data from AppInsights so CSA could see what is wrong was with fence after specific fence creation or edit.

# Acceptance criteria

| AC | Description | As is | To be | As is | To be | As is | To be |
|---|---|---|---|---|---|---|---|
| ME04-US99-AC01 | Update the fence creation event in Azure App insights by adding new parameters:As isTo beDate+timeUser IDFence IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc)Date+timeUser IDFence IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc)Fences posts list (lat, lon)NoteIf possible, log posts in the following format:lat,lon\r\n39.32345,-109.35432\r\n39.32323,-109.35499\r\n…39.32345,-109.35432\r\nAdd the first post twice as the first one and the last one.The following service will be used for visualization:https://www.gpsvisualizer.com/map_input?form=data | Date+timeUser IDFence IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc) | Date+timeUser IDFence IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc)Fences posts list (lat, lon) |
| Date+timeUser IDFence IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc) | Date+timeUser IDFence IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc)Fences posts list (lat, lon) |
| ME04-US99-AC02 | Update the fence failed creation event in Azure App insights by adding new parameters:As isTo beDate+timeUser IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc)Date+timeUser IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc)Fences posts list (lat, lon) | Date+timeUser IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc) | Date+timeUser IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc)Fences posts list (lat, lon) |
| Date+timeUser IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc) | Date+timeUser IDFence auto-generation approach: Simple square/AutoOverlapping after autogeneration: None/Water/Road/Other fencesWere there any edits during creation after auto-generation? (yes/no)Location (address)Type of public place (none, beach, park, water, nature, etc)Fences posts list (lat, lon) |
| ME04-US99-AC03 | Update the fence borders edit event in Azure App insights by adding new parameters:As isTo beDate+timeUser IDFence IDList of viewed warnings/errors names with qty of seen timesDate+timeUser IDFence IDList of viewed warnings/errors names with qty of seen timesFences posts list (lat, lon) | Date+timeUser IDFence IDList of viewed warnings/errors names with qty of seen times | Date+timeUser IDFence IDList of viewed warnings/errors names with qty of seen timesFences posts list (lat, lon) |
| Date+timeUser IDFence IDList of viewed warnings/errors names with qty of seen times | Date+timeUser IDFence IDList of viewed warnings/errors names with qty of seen timesFences posts list (lat, lon) |
