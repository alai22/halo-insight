---
title: "(Native Apps) ME01-F04-US04. Post Login Navigation flow"
sidebar_label: "(Native Apps) ME01-F04-US04. Post Login Navigation flow"
sidebar_position: 495
last_modified: "Feb 26, 2025"
author: "Galina Lonskaya"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Galina Lonskaya, Pavel Leonenko |
|  |# Contents

User story Post-Login Navigation Flow

# User story

\> As an account owner, I want to log into my account so that I can proceed work with my Halo account.

| AC | Description | Post-Login Navigation FlowAfter successful authentication, the system should determine the next screen based on the user's status: |
|---|---|---|
| Onboarding Status Check |
| ME01-F04-AC | If Onboarding is not completed, the user should be redirected to the corresponding Onboarding step. |
| ME01-F04-AC | If Onboarding is completed, proceed to the next check. |
| Permissions Status Check |
| ME01-F04-AC | If the user has not previously accepted or denied the required permissions, they should be redirected to the Permissions screen, which displays the three required permissions. |
| ME01-F04-AC | If the user has already accepted or denied permissions, proceed to the next check. |
| Final Navigation Decision |
| ME01-F04-AC | If Onboarding is completed and permissions are accepted or denied, the user should be redirected to the My Fences tab.Link to Maria's user story |
