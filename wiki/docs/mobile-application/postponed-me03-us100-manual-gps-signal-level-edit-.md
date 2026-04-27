---
title: "[Postponed] ME03-US100. 'Manual GPS Signal Level edit' popup"
sidebar_label: "[Postponed] ME03-US100. 'Manual GPS Signal Level edit' popup"
sidebar_position: 298
author: "Ekaterina Dupanova"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Ekaterina Dupanova |
| HALO-15541 - MOB: 'Manual GPS Signal Level edit' popup Ready for Estimation |
| Click here to expand...As of: 02 Feb 2023 Ekaterina Dupanova created initial draft of the story22 Feb 2023 Ekaterina Dupanova finalized the US |# Contents

User story Acceptance criteria

# User story

As a Halo app user I want to be able to open an article about overriding calculated GPS signal level thresholds to be aware of the the risks.

# Acceptance criteria

| AC | Description | Links, design |
|---|---|---|
| 'Edit GPS Signal Levels' popup |
| ME03-US100-AC01 | Precondition:User clicks Edit button in View mode the 'GPS Signal Level settings' screen (see [NI] ME03-US98. View/Edit GPS level bar (Advanced Settings -\> 'GPS signal levels' screen))The app opens the 'Edit GPS Signal Levels' popup with the following elements:icon'Edit GPS Signal Levels' title'Before editing GPS Signal Levels please read the article to understand the risks of overriding the default settings' text'Read The Article' button 'Cancel' button |  |
| ME03-US100-AC02 | When the user clicks on 'Read The Article' button, then the app should open Help Center article in the default mobile browser. |  |
| ME03-US100-AC03 | The link to the article: https://support.halocollar.com/hc/en-us/articles/4423813191959. |  |
| ME03-US100-AC04 | If the app knows that the user has previously opened the article, then the actions described in ME03-US100-AC06 should be performed. |  |
| ME03-US100-AC05 | Info that the user has already opened the article should be saved on the mobile side (the mobile app should delete this info when account is changed). |  |
| ME03-US100-AC06 | When the user returns back to the app after reading the article, the app should:display another state of 'Edit GPS Signal Levels' popup (see UI design):icon'Edit GPS Signal Levels' title'Continue' button |  |
| ME03-US100-AC07 | Precondition:The user clicks Continue in the 'Edit GPS Signal Levels' popup The app opens 'Advanced GPS settings' screen in Edit mode (Edit mode is described in [NI] ME03-US98. View/Edit GPS level bar (Advanced Settings -\> 'GPS signal levels' screen)) |  |
| ME03-US100-AC08 | Precondition:The user clicks Cancel in the 'Manual GPS Signal Level edit' popupThe app closes the popup and opens the screen in the View mode. |  |
