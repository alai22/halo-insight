---
title: "Non-catastrophic issues"
sidebar_label: "Non-catastrophic issues"
sidebar_position: 736
last_modified: "Jun 07, 2024"
author: "Kiryl Trafimau"
---

Note: As of 6 June 2024, users don't receive any information about non-catastrophic issues. Pending implementation.

## What is the non-catastrophic issue?

Non-catastrophic issues are the issues that don't require collar replacement. E.g. issues with some settings, software issues, or even the user's wrong behavior (when nothing is wrong with the collar, but the user uses it incorrectly). These issues don't require immediate attention, therefore we do not need behavior similar to catastrophic issues. Instead, we send weekly reports to the user to give them advice on how to deal with issues.

1. The query to check issues runs on a weekly basis: checks Daily Diagnostics data for all users to find issues.
2. If any of the issues are detected, Braze receives an[event](https://docs.google.com/document/d/1n-HYaKaMsnhYX2yJ15Kx8-FEuzaO1ttKJLZaYG5WAN4/edit)that specifies:
  - issue type;
  - collar id;
  - timestamp;
  - FW version;
  - last scan;
  - battery life.

3. According to the received event, Braze will send an email that provides advice for each issue type (e.g. update FW, restart the collar, etc.). There are email templates for each issue type and Braze will choose the proper template for email or combine a few templates in email (if 2+ issues are detected for the same user).

Non-catastrophic issue is an internal name for this category. We won't name them this way for end users.

## What do we do with non-catastrophic issues?

- Users can follow the advice from email. This is likely to help to resolve the issue.
- If users cannot deal with the issue themselves, they can contact support and provide CSA details from email.

## List of non-catastrophic issues:

Not implemented yet (we know how to detect):

(NI) ME03-US133 BE: Beam Healthcheck reports (Non-catastrophic issues)

#### Not implemented yet (we aren't sure yet how to detect):

(NI) ME03-US132 BE: Beam Healthcheck reports (Post-MRGP)

## Developers who have expertise in the feature

BE - Zakhar Makarevich

FW - Anton Tonkovich


