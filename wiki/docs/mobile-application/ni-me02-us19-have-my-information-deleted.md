---
title: "[NI] ME02-US19. Have my information deleted"
sidebar_label: "[NI] ME02-US19. Have my information deleted"
sidebar_position: 161
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Maria Shikareva [X] + TBD |
| HALO-7979 - [RI] BE+MOB: ME02-US19. Have my information deleted Open |# General description

Under CCPA the user has the right to request that businesses delete personal information they collected from the user and to tell their service providers to do the same.

# User story

\> As a user I want to have an option to delete all my information that is collected by the Halo app so that to

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME02-US19-AC01 | The "Have My Information Deleted" option should be added to the "Privacy and Terms" screen (see screen designs). |  | Link to Zeplin |
| ME02-US19-AC02 | When the user taps on "Have My Information Deleted" option on the "Accounts" screen, then the "Have My Information Deleted" action sheet should be displayed with the following UI elements (see screen designs):"Have My Information Deleted" title;"You're requesting for the deletion of your personal information. In this case you have to delete your account, so all your data will be deleted from our active databases. Please keep a note that the full information deletion will happen in 30 days and this data cannot be restored.Please confirm your choice if you would like to delete your account.";"Delete account" button;"Close" button. | TBD design | - |
| ME02-US19-AC03 | When the user taps on the "Cancel" button, then the "Account" screen should be opened with no changes made. | - | - |
| ME02-US19-AC04 | When the user taps on the "Delete account" button, then the account deletion process should be initiated.For more details see:"Delete account" section ME02-US02. View "Edit Account" screen;ME19-US30. Subscription plans: deleting user account. | - | - |
|  | The user should be logged out from e-Commerce also.see the related bug: HALO-8366 - The user does not log out on the E-commerce site if the account is deleted through the app Open |  |  |
| ME02-US19-AC05 | Precondition: the user has initiated their account deletion.User's info should also be deleted from the Klaviyo list.For more details see https://apidocs.klaviyo.com/reference/lists-segments#exclude-globally.Note: acc. to CCPA - We should notify all third parties to whom the business has sold or shared the personal information to delete the consumer’s personal information (unless this proves impossible or involves disproportionate effort). | - | - |
| ME02-US19-AC06 | Precondition: the user has initiated their account deletion.User's info should also be deleted from the records of all service providers, incl.:Stripe billing info (incl. subscription history);At the moment when the user deletes an account, billing info is not deleted.account from e-Commerce should also be deleted;need to clarify what happens right now when the user deletes account where subscription was previouslyTBD what are our Service Providers?acc. to CCPA: we should notify any service providers or contractors to delete the consumer’s personal information from their records, | - | - |
| ME02-US19-AC07 | Precondition: the user has initiated their account deletion.User's info should also be deleted from logs.TBD Seems that logs are deleted in 30 days. According to CCPA businesses must respond to your request within 45 calendar days. Maybe we can add info to the text message that the full information deletion will happen in 30 days? | - | - |
| ME02-US19-AC08 | TBD with the teamAre there cases when information cannot be deleted? CCPA allows it if it's reasonably necessary for the business/ service provider/ contractor to maintain the consumer’s personal information in order to:Complete the transaction for which the personal information was collected, fulfill the terms of a written warranty or product recall conducted in accordance with federal law, provide a good or service requested by the consumer, or reasonably anticipated by the consumer within the context of a business’ ongoing business relationship with the consumer, or otherwise perform a contract between the business and the consumer - e.g. if the collar is not yet shipped; if the collar is under warranty; etc.If the subscription is cancelled when the collar is being shipped yet - TBDDebug to identify and repair errors that impair existing intended functionality.Detect security incidents, fraud, or illegal activity. | - | - |
|  | Can we send (and do we need it) an email that the data was deleted? |  |  |
