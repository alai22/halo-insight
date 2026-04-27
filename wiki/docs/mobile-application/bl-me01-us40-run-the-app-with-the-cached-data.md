---
title: "(BL) ME01-US40. Run the app with the cached data"
sidebar_label: "(BL) ME01-US40. Run the app with the cached data"
sidebar_position: 388
author: "Kiryl Trafimau"
---

| Document status | Document owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| BASELINED in ME01-F00. App Launch (Splash Screen, Start Screen, Error Screen) by Galina Lonskaya on 04 Oct 2024 |
| Kiryl Trafimau |
| HALO-19185 - MOB: Edge cases when launching the app Closed |
| 26 Jan 2024 a draft user story is created by Kiryl Trafimau |User story Acceptance criteria ME01-US40-AC01 ME01-US40-AC02 ME01-US40-AC03 ME01-US40-AC04 ME01-US40-AC05 ME01-US40-AC06

## User story

- As a Haloapp user, I want to use the app even without the internet, so that I can keep my dog safe at any time

## Acceptance criteria

| AC | Description |  |
|---|---|---|
| ME01-US40-AC01 | Pre-conditions:There is cached App configuration data (I opened the app with the internet previously).There is no internet.IF I start the Halo appTHEN Splash screen is displayed with "Your Phone Has No Internet Connection" bar |  |
| ME01-US40-AC02 | Pre-conditions:There is cached App configuration data (I opened the app with the internet previously).I am logged out the app previously.There is no internet.IF I start the Halo appWHEN Splash screen passedTHEN I am on the Start screenAND "Your Phone Has No Internet Connection" bar is displayed |  |
| ME01-US40-AC03 | Pre-conditions:There is no cached App configuration data.There is no internet.IF I start the Halo appTHEN I should see App startup failed screen (see ME01-F00-AC03) |  |
| ME01-US40-AC04 | Pre-conditions:There is internet.App received communication error from server while trying to load data.IF I start the Halo appTHEN I should see App startup failed screen (see ME01-F00-AC03) |  |
| ME01-US40-AC05 | Pre-condition: I am on the App startup failed screenIF Internet disappearedTHEN I should see "Your Phone Has No Internet Connection" bar |  |
| ME01-US40-AC06 | Pre-condition: I am on the Mandatory update screenIF Internet disappearedTHEN I should see "Your Phone Has No Internet Connection" bar |  |
