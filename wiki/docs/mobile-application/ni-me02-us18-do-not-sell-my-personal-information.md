---
title: "[NI] ME02-US18. Do Not Sell My Personal Information"
sidebar_label: "[NI] ME02-US18. Do Not Sell My Personal Information"
sidebar_position: 160
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Maria Shikareva [X] |
| HALO-7933 - BE+MOB: ME02-US18. Do Not Sell My Personal Information Open |# General description

Halo and the third-party marketing partners may use the personal information the users send to us for the marketing purposes, to develop and display personalized content and advertising tailored to users' interests and/ or location and to measure its effectiveness. Under CCPA users have the right to opt-out from selling their personal information to third-parties.

According to CCPA the term "selling" means selling, renting, releasing, disclosing, disseminating, making available, transferring, or otherwise communicating orally, in writing, or by electronic or other means, a consumer’s personal information by the business to another business (e.g. an insurance company) or a third party for monetary or other valuable consideration. At the moment (as of 27 Aug 2021 Halo doesn't sell any personal information to third parties for a business or commercial purpose).

# User story

\> As a user I want to be able to make a request to opt-out of having my data sold to 3rd parties so that my personal data remains private.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| "Privacy and Terms" screen |
| ME02-US18-AC01 | The "Do Not Sell My Personal Information" option should be added to the "Privacy and Terms" screen (see screen designs). | ME02-US18-P01 "Privacy and Terms" screenUpdate the design (w/o delete option - as "delete' option is implemented separately)Link to Zeplin | Link to Zeplin |
| ME02-US18-AC02 | When the user taps on "Do No Sell My Personal Information" option on the "Accounts" screen, then the "Do No Sell My Personal Information" action sheet should be displayed with the following UI elements (see screen designs):"Do No Sell My Personal Information" title;"You're requesting to opt-out from selling your personal information to third parties. In this case you will not receive personalized advertisements, promotional messages, but you will still receive transactional messages from us regarding our Services. Please confirm your choice if you would like to opt-out of communications.";"Opt-out" button;"Close" button. | TBD designs | - |
| ME02-US18-AC03 | When the user taps "Close" button, then the action sheet should be closed with no requests sent. | - | - |
| ME02-US18-AC04 | When the user taps "Confirm" button, then the system sends a command to put the user's data to the "Black" list in Klaviyo (see ME02-US18-AC09 below). | - | - |
| ME02-US18-AC05 | If the command is sent successfully, then the system should display a success message MTBD Request sent:Title: Opt-out of communicationsBody: Your request to opt-out from selling your personal information to third parties is sent successfully. It may take up to 15 days to process it and to update our marketing preferences. We'll email to \<user email\> to notify you additionally when the request is successfully processed.Please note that the email may be in your Spam or Junk email folders.Buttons: OK, Learn more.TBD with Michael/ Heather: do we need to add an explanation "For more details on how to prevent this, tap "Learn more"? Cons: the pop-up text is already too long...TBD Think if we need to notify the user via emailQA note: when the user taps on the "OK" button in the error message, then the error pop-up should be closed.TBD add the text in Appendix 3 | - | - |
| ME02-US18-AC06 | When the user taps "Learn more" button, the link to the corresponding article should be opened in the mobile browser (see the detailed description in ME01-US16. Instructions to check spam folders on password recovery and email confirmation screens). | - | - |
| ME02-US18-AC07 | Precondition: the user has sent a request to opt-out.If the request failed, then the system should display an error message MTBD Request failed:Title: Request failedBody: Please try again later. If issue persists, please contact Halo customer support.Button: OKQA note: when the user taps on the "OK" button in the error message, then the error pop-up should be closed. |  |  |
| ME02-US18-AC08 | All the errors should be handled in accordance with ME14-F01 Unified errors handling. | - | - |
| ME02-US18-AC09 | Precondition: the command is successfully sent.The system should process the request:put the user's data to the "Black" list in Klaviyo (mark the user as excluded from all email);the EMTBD Opt-out of communications should be sent to the user:Title: Opt-out of communicationsBody: You have requested to opt-out from selling your personal information to third parties and your request is successfully processed. You will no longer receive personalized advertisements and promotional messages, but you will still receive transactional messages from us regarding our Services. Please note that you can opt in to the sale of your personal data anytime via Do Not Sell My Personal Information link.Have a good day!Your HALO teamNoteSee the Klaviyo details in https://apidocs.klaviyo.com/reference/lists-segments#exclude-globally. | - | - |
| ME02-US18-AC10 | "Do Not Sell My Personal Information" should be a link to the "Data Subject Access Request Form" on halocollar.com: https://app.termly.io/notify/2fc6550d-2a1c-4858-8a2f-bd3cd3b2021a. | - | - |
