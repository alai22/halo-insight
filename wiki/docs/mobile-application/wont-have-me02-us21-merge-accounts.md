---
title: "[Won't have] ME02-US21. Merge accounts"
sidebar_label: "[Won't have] ME02-US21. Merge accounts"
sidebar_position: 165
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Maria Shikareva [X] |
| HALO-7852 - SSO: Need to provide a way for the user to merge accounts for e-commerse and mobile app Closed |# User story

\> As a user ...Use case 1: the user has a Halo account with all the data (dogs, collars, history, etc.). Currently we have 20000 users. After subscriptions release they will have to log in to halocollar.com and buy a subscription. Many user don't know their email address which is used in the current Halo app or they have a new address and want to use it. So they sign up to halocollar.com with another address, buy a subscription, then log into the current Halo app and see no info about subscription (have no access to premium features). We need to think about the way how to merge two accounts into 1.Use case 2: the user wants to give their dog to someone with Halo app also and wants to share all the dog's data (history an so on). So it can be also helpful to merge dog's data into another account with the user's permission form the old account.

# Possible solutions

1. Subscription account - an newly created account with the bought subscription (the account was created via halocollar.com).
2. Existing account - a Halo app account with all the info in it (dogs, collars, history, etc.).

|  | Solution | Description |  |  |
|---|---|---|---|---|
| Initiate migration from the mobile appThe user has a Halo app account with all info in it.The user creates a new account and buys a subscription.Then the user opens the app:with old credentials and sees no subscription;with new credentials and sees no pet info.The user goes to Account page in any account and initiates account merging.Provides info about the account that has to be migrated.Confirms accounts migrating via email (enters the code from the app). |
| 1 | Migrate the subscription account into the existing account | All info from the subscription account should be merged into the previous account (i.e. the user continues using the existing account).TBDNeed to check what info is saved in Stateset/ E-commerce.How difficult is to change the email in Stateset/ E-commerce? | There is less data to merge.It's more user friendly to allow the user to do this themselves via the app (then via AAP). | Seems to be more complex as soon as subscription account is linked to a lot of places (Stateset/ E-commerce). |
| 2 | Migrate the existing account into the subscription account | All info from the existing account should be merged into the subscription account (i.e. the user continues using the existing account). | Seems to be less complex as all the data is only saved on our side.It's more user friendly to allow the user to do this themselves via the app (then via AAP). |  |
| 2.1 | The user can initiate the process from the existing account |  | More likely that the user will be logged into the existing account (because their credentials are already saved), so it can be more correct to allow doing it from the existing account. | The user will be logged out after the migration is finished. |
| 2.1 | The user can initiate the process from the subscriptions account |  | Pulling the data from the existing account seems less easier.The user will not be logged out. |  |
| 3 | Make it possible from AAP | The user contacts Customer Support, and then CSA initiates this merging. | No need in mobile efforts. | CSA has to know somehow that both accounts are owned by this one person. |
| 4 | Create a ticket to Zendesk from the mobile | The user creates a ticket, then CSA initiates account merging. | No need in mobile efforts. | CSA has to know that both accounts are owned by this one person |
| 5 | Tell the user to cancel the subscription from the new account and buy again from the old account |  | No efforts for development. | This will impact billing and so on, and this can be annoying for the user. |# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME02-US21-AC | We should not allow to merge accounts if there are collars/ pets in both of them (this can be rather complex if the user has collars/ pets in both accounts).TBD what if the user has subscriptions on both accounts? Is it the possible case and do we need to handle such situations? Why the user can buy subscriptions on both accounts and then wants to merge them? |  |  |
| ME02-US21-AC | Need to know exactly that this is the right user (some confirmation process):the user provides the email associated with another account that has to be merged;gets a confirmation email with a code;enters the code in the mobile app. |  |  |
| ME02-US21-AC | Need to take into consideration:One of the account should be cleared out.The user will see: "Email is not found" message? Or it will be possible for the user to enter the same account using both emails?Need to take into consideration User ID changing (also).If some personal info differs in both accounts (e.g. last name) - what should be used? Info from the account into which info is merged? |  |  |
| ME02-US21-AC |  |  |  |
| ME02-US21-AC |  |  |  |
| ME02-US21-AC |  |  |  |
