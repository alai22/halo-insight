---
title: "ME21-US75. Send 'collar_attached_first_use' event to Braze (required for 'Go Outside' IAM)"
sidebar_label: "ME21-US75. Send 'collar_attached_first_use' event to Braze (required for 'Go Outside' IAM)"
sidebar_position: 433
last_modified: "Jan 16, 2025"
author: "Galina Lonskaya"
---

Page info| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya Dmitry Kravchuk |
| HALO-20804 - MOB: ME21-US75. Send 'collar_attached_first_user' event to Braze (required for 'Go outside' IAM) Closed |
| 19 Jul 2024 the draft user story is created |Table of Contents

User story Acceptance criteria Implementation notes

# User story

\> As Halo app account owner I want to know how to complete the collar setup properly so that my collar will work properly after FTUE Collar attach flow completion.

# Acceptance criteria

| AC | Description | UI design |
|---|---|---|
| ME21-US75-AC01 | Precondition: I go through FTUE onboarding, attach 1st collar, gets to the congrats screenIf I tap on the CTA to go outside, then:My Map screen should be opened. A trigger should be be sent to Braze to send in-app messageBraze in-app message should be shown + UI design of in-app message- \> Out of Softeq responsibility zone (will be a separate ticket for testing when Tristan prepares campaign) | - |
| ME21-US75-AC02 | Precondition: I go through FTUE onboarding, attach 1st collar, gets to the congrats screen, click to add another collar, attach 2nd collar, get to congrats screenIf I tap on the CTA to go outside, then:My Map screen should be opened. A trigger should be sent to Braze to send in-app messageBraze in-app message should be shown + UI design of in-app message- \> Out of Softeq responsibility zone (will be a separate ticket for testing when Tristan prepares campaign) | - |# Implementation notes

|  | Description |
|---|---|
| ME21-IN75-AC01 | A trigger sent to send in-app message: 'collar_attached_first_use' |
