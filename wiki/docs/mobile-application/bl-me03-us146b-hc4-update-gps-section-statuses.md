---
title: "(BL) ME03-US146b. HC4: Update GPS section statuses"
sidebar_label: "(BL) ME03-US146b. HC4: Update GPS section statuses"
sidebar_position: 480
last_modified: "Jan 30, 2025"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA issues | History of changes |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, |
| HALO-21212 - BE+MOB: ME03-US146. HC4: Update GPS intitialization statuses and notifications Closed |
| Click here to expand...As of 30 Jul 2024 Mariya Kolyadacreated the initial version of US.30 Jan 2025 baselined to ME03-F11 by Galina Lonskaya |# Contents

User Story Acceptance criteria

# User Story

\> As a Halo account owner I want view removed GPS initialization steps and simplified text related to it, and texts mentioning color of LED indicatiors that depend on my colalr generations so that I don't bother about tech details and can just define if my collar is ready for use or not.

# Acceptance criteria

| AC | Description | iOs design | Android design | Pet statuses | Collars list. GPS tile | Section/elememt | As is | To be | Element | Halo 1 - 3+ | Halo 4 - future generations |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ME03-US146-AC02 | Precondition: Collar requires initializationUpdate the Collars list by following the requirements below:Section/elememtAs isTo beSee ME03-US110. Redirect to Initializing GPS screen from Collar's list, Advanced Settings menu updatesCollar Photo on the top level of collar item in the listicon on pet avatar on top of the screenDisplay icon on the Collar Photo 'GPS' tile The 'GPS' tile should show:icon and 'Initialization required' text'Initialize' buttonUpon clicking on 'Initialize' button, the app redirects to 'GPS Initialization' flow that starts with this screen.Display:ElementHalo 1 - 3+Halo 4 - future generationsIconTextBring collar outside by hand until the GPS led blinks BLUE.Bring collar outside by hand until the GPS led blinks GREEN. | See ME03-US110. Redirect to Initializing GPS screen from Collar's list, Advanced Settings menu updates | Collar Photo on the top level of collar item in the list | icon on pet avatar on top of the screen | Display icon on the Collar Photo | 'GPS' tile | The 'GPS' tile should show:icon and 'Initialization required' text'Initialize' buttonUpon clicking on 'Initialize' button, the app redirects to 'GPS Initialization' flow that starts with this screen. | Display:ElementHalo 1 - 3+Halo 4 - future generationsIconTextBring collar outside by hand until the GPS led blinks BLUE.Bring collar outside by hand until the GPS led blinks GREEN. | Icon |  | Text | Bring collar outside by hand until the GPS led blinks BLUE. | Bring collar outside by hand until the GPS led blinks GREEN. | Halo 1-3 generations - iOSFigmaHalo 4+ generations - iOSFigma | Halo 1-3 generations - AndroidFigmaHalo 4+ generations - AndroidFigma |
| See ME03-US110. Redirect to Initializing GPS screen from Collar's list, Advanced Settings menu updates |
| Collar Photo on the top level of collar item in the list | icon on pet avatar on top of the screen | Display icon on the Collar Photo |
| 'GPS' tile | The 'GPS' tile should show:icon and 'Initialization required' text'Initialize' buttonUpon clicking on 'Initialize' button, the app redirects to 'GPS Initialization' flow that starts with this screen. | Display:ElementHalo 1 - 3+Halo 4 - future generationsIconTextBring collar outside by hand until the GPS led blinks BLUE.Bring collar outside by hand until the GPS led blinks GREEN. | Icon |  | Text | Bring collar outside by hand until the GPS led blinks BLUE. | Bring collar outside by hand until the GPS led blinks GREEN. |
| Icon |  |
| Text | Bring collar outside by hand until the GPS led blinks BLUE. | Bring collar outside by hand until the GPS led blinks GREEN. |
