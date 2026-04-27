---
title: "AE03-US106. Don't allow deleting user accounts with active subscription"
sidebar_label: "AE03-US106. Don't allow deleting user accounts with active subscription"
sidebar_position: 406
last_modified: "May 22, 2024"
author: "Nicolay Gavrilov"
---

| Document status | Document owners | Link to JIRA issue | Changes history |
|---|---|---|---|
| DRAFT |
| Nicolay Gavrilov |
| HALO-19943 - MOB [+BE]: AE03-US106. Don't allow deleting user accounts with active subscription Closed HALO-19773 - BE [+MOB]: Validate subscription existence in Stripe on user account deletion Closed |
| - |\> Acceptance criteria

| AC | Description | Notes, links, wire frames |
|---|---|---|
| AE03-US106-AC01 | FOR users with active subscription in Stripe AND no subscription on Halo BE sideWHEN they attempt to delete their accountTHEN they should see the M162 Unable to delete account due to an active subscription error message | ErrorCode.UserHasPurchasedSubscription |
| AE03-US106-AC02 | The text of the M162 Unable to delete account due to an active subscription error message should be updated as follows:Title: Unable to Delete Your AccountBody: Your Halo Collar(s) has an active Pack Membership plan. Please visit halocollar.com to cancel.Button: Ok | - |
| AE03-US106-AC03 | FOR users with multiple active subscriptions in Stripe and no no subscription in Halo DBWHEN they attempt to delete their accountTHEN they should see the M290 Unable to delete account due to multiple subscriptions in StripeNote: users can't do anything if they have multiple subscriptions in Stripe. Therefore we need to redirect them to Halo support team | ErrorCode.UserHasPurchasedSubscriptions |
| AE03-US106-AC04 | WHEN users attempt to delete their accountAND there no response is received from Stripe (UserSubscriptionStatusIsNotDetermined = 5103)THEN they should see the M17 Technical error message | ErrorCode.UserSubscriptionStatusIsNotDetermined |
