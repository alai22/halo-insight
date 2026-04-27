---
title: "ME01-US30. Add a new error during Login process in case device time is incorrect"
sidebar_label: "ME01-US30. Add a new error during Login process in case device time is incorrect"
sidebar_position: 604
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Nikita Krisko |
| HALO-11030 - MOB [ongoing monitoring]: "Login issue" review and fixes if necessary Closed |
| Click here to expand... |# User story

\> As a Halo app account owner I want to see specific errors during Login process so that I can understand the issue and easily fix it.

# Acceptance criteria

| AC | Description | Links |
|---|---|---|
| ME01-US30-AC01 | Precondition: user tries to Log inANDtime on the user's mobile phone is incorrect (i.e. it differs from the system time for more than 5 minutes).The mobile app should display a new error message instead of M113 Network error: M224. Check Your Device Time.Title: Login Security Issue: Device TimeBody: Please correct the date/time on your mobile device - or enable 'Set Automatically' in device settings. Then try logging in again. Button: OKButton: Report Issue | ME14-F01 Unified errors handlingAppendix 3 – Error, Success, Warning Messages |
