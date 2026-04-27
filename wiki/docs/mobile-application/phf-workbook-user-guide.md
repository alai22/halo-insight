---
title: "PHF Workbook User Guide"
sidebar_label: "PHF Workbook User Guide"
sidebar_position: 741
last_modified: "Jun 18, 2024"
author: "Victor Kozub"
---

## General

We have created a Workbook of Fence Events Analytics to track when users create/edit/delete their fences. We keep track of these events and store associated data (parameters used by users).

## How to access the Workbook

We have a copy of this Workbook on every environment (dev, stage, prod). As a CSA you will be working with real users, thus you need to access the production version of the report. Follow this link: https://portal.azure.com/#@idsmehrmangmail.onmicrosoft.com/resource/subscriptions/48cfe29e-ce4c-41f0-acb8-6c6ef906987f/resourceGroups/halo-prod/providers/microsoft.insights/workbooks/2d4d3a9e-419c-45ab-b9a4-acb4f17c6176/overview

Click on the Open Workbook button to open the Workbook. You can also check Linked Resource to make sure it's the production workbook (it should say halo-prod):

## Structure of the Workbook

Note that for the purpose of this guide a Workbook from the stage environment will be used because it has events in it. The prod version will have events after the release of PHF feature on prod.

The Workbook consists of the following elements (check the screenshot below):

1. Filters – you will most probably use the filter by**UserId**to show events of a specific user and the**Time Range**filter if needed.
2. Tabs – when you open a certain tab you will see corresponding event details. You will most probably use**Fence Creation Events**tab to see data related to new fences being created,**Fence Borders Edit Events**tab with data reflecting edits of already created fences, and**Fence Creation Cancelled Events**tab with data of fences that user abandoned during creation process or simply couldn't create because of some issue that should be investigated.
3. Tab data – when you select a specific tab you will see corresponding data in the table.
4. Export to Excel – a button you need to press to download data from currently opened table in Excel format. More on why you may need this below.
5. Edit – please,**do not press this button**, as it allows editing of the Workbook, and you may break it.

## How to reconstruct a fence

A typical use case would be to look at the fence user created or tried to create in order to find a problem with it. To do the latter you need to open the Fence Creation Cancelled Events tab, filter events by a specific UserId, and download export the data to Excel. Note that the last column in the table named FencePosts contains location data of the fence being selected, but you can copy this data from the column because of Workbook restrictions, you need to download the Excel first and then copy data from there:

You can use the following service to reconstruct the fence: https://www.gpsvisualizer.com/map_input?form=google

Paste the post data in the input box, but you need to delete semicolons and leave two coordinates per row like this:

Click on the Draw the map button to see the fence visualized:


