---
title: "(Native apps) ME03-F12-US06. Edit Tracking Thresholds: Revert to Default Settings"
sidebar_label: "(Native apps) ME03-F12-US06. Edit Tracking Thresholds: Revert to Default Settings"
sidebar_position: 499
last_modified: "Mar 13, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links to Jira/Linear tickets | Changes history |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-407/[ios]-edit-tracking-thresholds-revert-to-default-settings |
| 27 Feb 2025 draft is created by Galina Lonskaya |# Contents

User story Acceptance criteria

# User story

\> As a Halo app account owner I want to be able to return the MIN and MAX GPS threshold thumbs to the default values so that the GPS can have settings suggested by the system.

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-F12-US06-AC01 | If 'Low and High GPS' values displayed on the 'Edit Tracking Thresholds' screen are equal to the default values, then:the 'Restore Defaults' button should be disabled, see Figma. |
| ME03-F12-US06-AC02 | If 'Low and High GPS' value displayed on 'Edit Tracking Thresholds' screen are different from the default values, then:the 'Restore Defaults' button should be enabled, see Figma. |
| ME03-F12-US06-AC03 | If the user taps 'Restore Defaults' button, then:'Low and High GPS' sliders should be automatically moved to the default values;the 'Restore Defaults' button should become disabled. |
| ME03-F12-US06-AC04 | The default thresholds are configurable on BE side. |Tech details

Default LowerBoundary and UpperBoundary come in the configuration - GET /configuration ManualGpsCalibration.DefaultLowerBoundary and ManualGpsCalibration.DefaultUpperBoundary fields


