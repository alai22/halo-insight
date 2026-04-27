---
title: "(NA) ME05-FE01-US02: Sound Bar Slider"
sidebar_label: "(NA) ME05-FE01-US02: Sound Bar Slider"
sidebar_position: 572
last_modified: "May 02, 2025"
author: "Galina Lonskaya"
---

| Document owners | Links | History of changes |
|---|---|---|
| Galina Lonskaya, Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-881/ios-sound-bar-slider |
| 05/01/2025 draft is created by Galina Lonskaya |### User story

\> n/a

Content

User story Acceptance criteria

### Acceptance criteria

| AC | Text | UI Design | Sound Bar | 'Adjust Volume Carefully' popup |
|---|---|---|---|---|
| AC01 | The minimum value of the sound bar should be 1. | Figma |
| AC02 | The maximum value of the sound bar should be 15. |
| AC03 | The volume value displayed in the header should update dynamically to reflect the current volume, based on the thumb's position on the slider. |
| AC04 | The slider should be controlled either by tapping and dragging the thumb, or by tapping on the track to "jump" to the desired position. |
| AC05 | The slider should have 15 invisibly spaced tick marks along the track. The thumb should snap to these tick marks as it is dragged, ensuring that it only stops at these specific increments. |
| AC06 | While dragging the thumb along the slider and passing through the tick marks, a haptic effect should be applied for each incremental change in volume. |
| AC07 | The active portion of the slider should change color (e.g., yellow) to visually indicate the current volume level. |  |
| AC08 | If I increase the volume by 3 or more increments in a single adjustment, then: the following popup message should be shown. | Figma |
| AC09 | If I tap on the Got It, then: the popup should be closed. | - |
| AC10 | If I tap on the Don't show this again, then: the popup should not be shown anymore. Note: the info about popup viewing should be saved locally (only on mob side) | - |
