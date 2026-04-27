---
title: "[Postponed] ME04-US88. Log fence images to Azure Blob storage"
sidebar_label: "[Postponed] ME04-US88. Log fence images to Azure Blob storage"
sidebar_position: 385
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED (SQ) |
| Mariya Kolyada, Dmitry Kravchuk , Anton Zimin [X] , Svyatoslav Luzin |
| HALO-19064 - MOB+BE: ME04-US88. ME04-US68. Log fence images to Azure Blob storage Open |
| Click here to expand...As of 16 Jan 2024 :Mariya Kolyadacreated the initial version of US by moving requirements related to the image to this separate US for PHF Post-MRGP scope. |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo Product Owner I want to be able to view the fence images in addition to fence geo data so that I can better understand how teh current fences look like and analyse this data for futher hipothesis generation.

# Acceptance criteria

| AC | Description |
|---|---|
| ME04-US88-AC01 | Save fence images named with Fence image ID to the Azure Blob Storage.Development notesBE and FE developers should decide what is a better way of implementation: one endpoint or two separate for fence data and fence image.Concern: if we have 2 separate endpoints - we can have a situation in which data is added, but the image is not added.Other notes:The image is about 100 KB. |
| ME04-US88-AC02 | If user deletes fence, then the system should:Delete the fence image from Blob Storage. |
| ME04-US88-AC03 | The solution should be expandable for future UI implementation in AAP.So that CSAs can open user's fences images in AAP UI. |
