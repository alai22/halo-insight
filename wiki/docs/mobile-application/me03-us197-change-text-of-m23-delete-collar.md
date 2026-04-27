---
title: "ME03-US197. Change text of M23 Delete Collar"
sidebar_label: "ME03-US197. Change text of M23 Delete Collar"
sidebar_position: 639
last_modified: "Dec 19, 2023"
author: "Kiryl Trafimau"
---

| Document status | Document owners | Link to JIRA Issue | Change history |
|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-18646 - MOB: Warn the app user to go to CS when he/she removes the collar from the app Closed |
| - |# General Description

Sometimes users delete a collar with some issue (e.g. BLE module issue) and then they cannot add it back to the account. This causes issue with the Warranty replacement process. We also lose the ability to pull logs from the collar as it is not connected to Wi-Fi once off the account.

# User Story

As a user, I want the text of M23 Delete Collar to be changed so that I am warned not to delete a collar from my account contacting support.

# Acceptance criteria

| AC | Description |  | AS IS | TO BE |
|---|---|---|---|---|
| ME03-US197-AC01 | The text of M23 Delete Collar should be changed as follows:AS ISTO BETitleDelete CollarCaution BodyDeleting your collar from your account should only be performed if you are returning or giving away your collar. Please confirm that you want to delete this collar.Only delete your collar from your account if you're returning or giving it away. For any collar issues, visit the Halo Dog Park for customer support first.ButtonCancelCancelButtonDeleteDelete Collar | Title | Delete Collar | Caution | Body | Deleting your collar from your account should only be performed if you are returning or giving away your collar. Please confirm that you want to delete this collar. | Only delete your collar from your account if you're returning or giving it away. For any collar issues, visit the Halo Dog Park for customer support first. | Button | Cancel | Cancel | Button | Delete | Delete Collar |
| Title | Delete Collar | Caution |
| Body | Deleting your collar from your account should only be performed if you are returning or giving away your collar. Please confirm that you want to delete this collar. | Only delete your collar from your account if you're returning or giving it away. For any collar issues, visit the Halo Dog Park for customer support first. |
| Button | Cancel | Cancel |
| Button | Delete | Delete Collar |
