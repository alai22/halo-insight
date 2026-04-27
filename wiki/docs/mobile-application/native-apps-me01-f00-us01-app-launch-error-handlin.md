---
title: "(Native Apps) ME01-F00-US01. App Launch Error Handling"
sidebar_label: "(Native Apps) ME01-F00-US01. App Launch Error Handling"
sidebar_position: 492
last_modified: "Apr 16, 2025"
author: "Galina Lonskaya"
---

Page info| Task owners | Link to JIRA/Linear Issue | Changes history |
|---|---|---|
| Galina Lonskaya Pavel Leonenko |
| https://linear.app/fueled/issue/HALO-410/[ios]-app-launch-error-handling |
| 26 Feb 2024 draft is created by Galina Lonskaya |# Contents

User Story Acceptance criteria

# User Story

\> As Halo App Account Owner, I want the app to launch smoothly with clear feedback during the startup process, so that I understand that the app is loading and can be informed if something goes wrong.

# Acceptance criteria

| AC | Precondition | iOS UI design | Android UI design | App Launch: Mandatory Update Check | App Launch: Сonnection/Communication/cache data check |  | Preconditions | UI for the user | Displayed screen | Internet connection issue | Any other issue except connection issue (communication, etc.) | Refresh Token presents | Has cached config data |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ME01-F00-US01-AC01 | If I launch the app and a mandatory update is required, then: 'Update Required' screen should be opened, see Figma. | - | - |
| ME01-F00-US01-AC02 | If no IC, then 'No Internet Connection' bar should be shown, see Figma |  |  |
| If the mandatory update is not required and an error happens during Halo app launch process, then see how the different errors should be handled in the following table: PreconditionsUI for the userDisplayed screenInternet connection issueAny other issue except connection issue (communication, etc.)Refresh Token presentsHas cached config dataME01-F00-US01-AC03n/a'Unable to Start App' screen, see FigmaME01-F00-US01-AC07n/aWelcome screen, see FigmaME01-F00-US01-AC04n/adoesn't matter'Unable to Start App' screen, see FigmaME01-F00-US01-AC08 the error during configuration downloading doesn't matterdoesn't matter'Unable to Start App' screen, see FigmaME01-F00-US01-AC05n/a (session expired error) (expired refresh token →the user logged out)doesn't matterWelcome screen, see FigmaME01-F00-US01-AC06 any error except the error during configurationdownloading and the session expired errordoesn't matterWelcome screen, see Figma OR perform auto-login, see(Native Apps) ME01-F04-US03. Auto Login | ME01-F00-US01-AC03 |  | n/a |  |  | 'Unable to Start App' screen, see Figma | ME01-F00-US01-AC07 |  | n/a |  |  | Welcome screen, see Figma | ME01-F00-US01-AC04 |  | n/a |  | doesn't matter | 'Unable to Start App' screen, see Figma | ME01-F00-US01-AC08 |  | the error during configuration downloading | doesn't matter | doesn't matter | 'Unable to Start App' screen, see Figma | ME01-F00-US01-AC05 |  | n/a (session expired error) | (expired refresh token →the user logged out) | doesn't matter | Welcome screen, see Figma | ME01-F00-US01-AC06 |  | any error except the error during configurationdownloading and the session expired error |  | doesn't matter | Welcome screen, see Figma OR perform auto-login, see(Native Apps) ME01-F04-US03. Auto Login |
| ME01-F00-US01-AC03 |  | n/a |  |  | 'Unable to Start App' screen, see Figma |
| ME01-F00-US01-AC07 |  | n/a |  |  | Welcome screen, see Figma |
| ME01-F00-US01-AC04 |  | n/a |  | doesn't matter | 'Unable to Start App' screen, see Figma |
| ME01-F00-US01-AC08 |  | the error during configuration downloading | doesn't matter | doesn't matter | 'Unable to Start App' screen, see Figma |
| ME01-F00-US01-AC05 |  | n/a (session expired error) | (expired refresh token →the user logged out) | doesn't matter | Welcome screen, see Figma |
| ME01-F00-US01-AC06 |  | any error except the error during configurationdownloading and the session expired error |  | doesn't matter | Welcome screen, see Figma OR perform auto-login, see(Native Apps) ME01-F04-US03. Auto Login |Implementation details:

The logic of logging in and opening the proper screen should be implemented in a shared class, and reused here and in two more places. Please see StartScreenManager.TryNavigateToProperScreenAsync().

Also, since we store access token in KeyChain on iOS, we have to check at startup whether it's the first launch or not. If it is, we need to delete the access/refresh tokens if they exist - otherwise the previous user will be logged in after app reinstallation.


