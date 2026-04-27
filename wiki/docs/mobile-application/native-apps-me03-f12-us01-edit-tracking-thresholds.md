---
title: "(Native apps) ME03-F12-US01. Edit Tracking Thresholds: 'Advanced Settings' screen"
sidebar_label: "(Native apps) ME03-F12-US01. Edit Tracking Thresholds: 'Advanced Settings' screen"
sidebar_position: 496
last_modified: "Mar 13, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links to Jira/Linear tickets | Changes history |
|---|---|---|
| Galina Lonskaya Dmitry Kravchuk |
| https://linear.app/fueled/issue/HALO-402/[ios]-edit-tracking-thresholds-unread-instruction-screen-state |
| 25 Feb 2025 draft story is created |# Contents

User story Acceptance criteria

# User story

\> As a Halo app account owner I want to see the instruction about GPS usage and GPS thresholds adjustment so that I can understand why GPS may work incorrectly and how I can fix it

# Acceptance criteria

| AC | Description |
|---|---|
| ME03-F12-US01-AC01 | If I tap on CTA on the 'Signal Analysis' screen, then: 'Advanced Settings' screen should be shown, see Figma |
| ME03-F12-US01-AC02 | Precondition: 'Advanced Settings' screen is shownIf I haven't opened 'Threshold adjustment' instruction previously, then:'Read Instruction' CTA should be highlighted visually, see Figma'checkbox' under CTA should not be displayed. |
| ME03-F12-US01-AC03 | The information that I have already opened the instruction about 'Threshold adjustment' should be stored on the mobile side. |
| ME03-F12-US01-AC04 | If I log in to another account from the same device, then:the information should about 'Threshold adjustment' should be deleted by the mob app. |
| ME03-F12-US01-AC05 | If I remove the Halo app from the device, then:the information should about 'Threshold adjustment' should be deleted by the mob app. |
| ME03-F12-US01-AC06 | If I tap on 'Read Instruction' CTA , then:the app should open Help Center article (https://support.halocollar.com/hc/en-us/articles/4423813191959) in the default mobile browser.Note: The links to the article should be stored on BE side. |
| ME03-F12-US01-AC07 | If I return back to the app after the instruction opening, then:the app should change the state of the Advanced Settings screen: see Figmathe checkbox should be checked by default |
| ME03-F12-US01-AC08 | If the checkbox is unchecked OR not displayed on the 'Advanced Settings' screen, then:the 'Edit Tracking Thresholds' button should be disabled. |
| ME03-F12-US01-AC09 | If the checkbox is checked, then:the 'Edit Tracking Thresholds' button button should be enabled. |
| ME03-F12-US01-AC10 | If all content doesn’t fit on the screen, the app should enable scrolling for the entire screen, except for the header. |Tech details

The article URL can be found in GET /configuration in Support.ManualGpsCalibrationArticleUrl field


