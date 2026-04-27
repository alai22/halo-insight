---
title: "[BL] ME03-US112. Level bar pin should be in disabled state if GPS level is low and pet pin should be ghosted"
sidebar_label: "[BL] ME03-US112. Level bar pin should be in disabled state if GPS level is low and pet pin should be ghosted"
sidebar_position: 318
author: "Ekaterina Dupanova"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Ekaterina Dupanova |
| HALO-16590 - MOB: Level bar pin should be in disabled state if GPS level is low and pet pin should be ghosted Closed |
| Click here to expand...As of: 01 Jun 2023 Ekaterina Dupanova created initial draft of the story16 Jan 2025 baselined to [BL] ME03-US85. Collar Details: GPS Signal Level Settings |# Contents

User story Acceptance criteria

# User story

As a Halo app user I want to be able to view GPS signal level pin in disabled state when the level is low so that I understand that something is wrong with the GPS level and I need to initialize the collar.

# Acceptance criteria

| AC | Description | Links, design |
|---|---|---|
| Entry point:Onboarding flow → Initializing GPS Add collar flow → Initializing GPSView GPS level (Advanced settings) |
| ME03-US112-AC01 | Precondition: GPS signal strength is in the Low rangeLevel Pin on the GPS level bar should be disabled. | Zeplin |
| ME03-US112-AC02 | Precondition:GPS signal strength is in the Low rangePet pin should be:DisabledHave a 'paused' pet pin badge |  |
