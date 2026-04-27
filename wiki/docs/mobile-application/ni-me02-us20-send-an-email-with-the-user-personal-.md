---
title: "[NI] ME02-US20. Send an email with the user personal data (under CCPA)"
sidebar_label: "[NI] ME02-US20. Send an email with the user personal data (under CCPA)"
sidebar_position: 163
author: "Maria Shikareva [X]"
---

| Document status | Document owner | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Maria Shikareva [X], TBD BE + QA |
| HALO-7983 - [RI] BE: [NT] [Investigate] User's personal data request (under CCPA) (Part 2) Ready for Development HALO-8003 - [RI] BE: ME02-US20. Send an email with the user personal data (under CCPA) Open Ballpark estimations:BE: min 8SP (if a separate job is required → it's required to take info from logs)QA BE: 5SP (if info from logs is required, otherwise 3SP) |General description User story Acceptance criteria

# General description

CCPA (California Consumer Privacy Act) is a state-wide data privacy law that regulates how businesses all over the world are allowed to handle the personal information (PI) of California residents. The effective date of the CCPA is January 1, 2020. It is the first law of its kind in the United States.

# User story

\> As a user I want to receive my personal data under my request so that I know what information is being collected from me in the HALO app.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME02-US20-AC | Precondition: the user has tapped on the "Send Request" button in the "Request My Personal Data" action sheet on the "Account" screen.When the request is successfully sent, the system should start a job (TBD the frequency with Eugene) which generates a .CSV file (TBD while development) with the following user's personal data:all data from the database (excl. PetStatistics);TBD how the User Photo/ Pet Photo will be sent? via links? Clarify how long they can be available for the user?TBD if we store history for collars/ users geolocation data OR just one, current/last known locationall data from logs;TBD if possible: payment data (credit card number, purchase history, invoices, billing addresses, security code associated with credit card).https://stripe.com/privacyIf you are a Customer of a Stripe User, please direct your requests directly to the User. For example, if you are making, or have made, a purchase from a merchant using Stripe as a payment processor, and you have a request that is related to the payment information that you provided as part of the purchase transaction, then you should address your request directly to the merchant.https://stripe.com/privacy-center/legal#your-rights-and-choicesNote: PetStatictics is not considered to be user's personal data, it's not mentioned in the Privacy Policy and will not be included into the file. Anyway this info can be sent later under the user's separate request to Customer Support. | Need to update the design of the email | - |
| ME02-US20-AC | When the file is ready, the EM010 File with the user personal data should be sent to the user:Title: Personal Data RequestBody: You have requested a file with your personal data. This link will work only for 4 days (TBD with Eugene) after we send it. Because it may contain personal information, be sure to keep the link private and only download the file to your own computer. Have a good day!Your HALO team"Link to the file". |  |  |
| ME02-US20-AC | When the user clicks on the link in the EM010 File with the user personal data, the file downloading should be initiated via browser. |  |  |
| ME02-US20-AC | A .CSV file should have the following format: CSV format.xlsx TBD Instagram suggests HTML format or JSON | - | - |
| ME02-US20-AC | A file should have the following name format: \<username_date\>. Example: mariashikareva_07142021. | - | - |
| ME02-US20-AC | If the user clicks on the link in the email after 4 days (i.e. when the link is expired), then the web screen with "Resend data" button should be opened with the following UI elements:'HALO' icon;"Oh no!" text"The link we sent has expired as it works for 4 days only. You can request another copy of your data." text;"Resend data" button. | Prepare screen designs |  |
| ME02-US20-AC | When the user clicks on the "Resend data" button, then:the system should generate a new file as described from ME02-US20-AC13;the following web screen with "Resend data" button should be displayed with the following UI elements:'HALO' icon;"Data requested" title;"We've started creating a file of all data that you've shared with the Halo app and we'll email to \<user email\>. It may take up to 24 hours to collect this data and send it to you. Please note that the email may be in your Spam or Junk email folders. For more details on how to prevent this, click here."Click here" should be a link to the corresponding article (see the detailed description in ME01-US16. Instructions to check spam folders on password recovery and email confirmation screens). | Prepare screen designs |  |
| ME02-US20-AC | Need to remember: every time when new data appears add them to CCPA data list. |  |  |
