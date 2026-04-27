---
title: "[NI] ME02-US06. Request My Personal Data"
sidebar_label: "[NI] ME02-US06. Request My Personal Data"
sidebar_position: 35
last_modified: "Mar 14, 2024"
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | Change history |
|---|---|---|---|
| DRAFT |
| Galina Lonskaya, Maria Shikareva [X], Pavel Leonenko (MOB), Eugene Paseka (BE), Anastasia Brechko (QA) |
| HALO-6086 - [RI] MOB: ME02-US06. Request My Personal Data Open HALO-7967 - [RI] BE: ME02-US06. Request My Personal Data Open Ballpark estimations:MOB: 3-5SP (1SP for changes to "Account" screen + 2SP for "Privacy and Terms" screen + 1-2SP for custom action sheet)QA MOB: 3SP (1SP for changes to "Account" screen + 2SP for "Privacy and Terms" screen). |
| 15 Jul 2021 Maria Shikareva [X] The document is updated due to changed requirements during the time. |General description Useful links User story Acceptance criteria "Account" screen "About" screen "Privacy and Terms" screen

# General description

CCPA (California Consumer Privacy Act) is a state-wide data privacy law that regulates how businesses all over the world are allowed to handle the personal information (PI) of California residents. The effective date of the CCPA is January 1, 2020. It is the first law of its kind in the United States.

# Useful links

1. [https://oag.ca.gov/privacy/ccpa](https://oag.ca.gov/privacy/ccpa)
2. [https://ccpacompliancechecklist.com/](https://ccpacompliancechecklist.com/)
3. [https://www.morganlewis.com/-/media/files/document/2019/california-consumer-privacy-act-checklist.ashx?la=en&hash=0A8A3C710055C4F888204D0D58B3CC89E7FBB41C](https://www.morganlewis.com/-/media/files/document/2019/california-consumer-privacy-act-checklist.ashx?la=en&hash=0A8A3C710055C4F888204D0D58B3CC89E7FBB41C)
4. [https://app.termly.io/notify/2fc6550d-2a1c-4858-8a2f-bd3cd3b2021a](https://app.termly.io/notify/2fc6550d-2a1c-4858-8a2f-bd3cd3b2021a)
5. [https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201720180AB375](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201720180AB375)
6. [https://www.esrb.org/privacy-certified-blog/ccpa-california-consumer-privacy-act-5-steps-for-mobile-app-developers/](https://www.esrb.org/privacy-certified-blog/ccpa-california-consumer-privacy-act-5-steps-for-mobile-app-developers/)

# User story

\> As a user I want to have an ability to request my personal data so that I know what information is being collected from me in the HALO app.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| "Account" screen |
| ME02-US06-AC01 | A new "Privacy and Terms" section should be added to the "Account" screen under the Settings tab (see screen designs). | ME02-US06-P01 "Account" screenLink to Zeplin | The same as for iOS.Link to Zeplin |
| ME02-US06-AC02 | When the user taps on the "Privacy and Terms" section, then the "Privacy and Terms" screen should be opened with the following elements (see screen designs):"Privacy and Terms" title;"Request My Personal Data" option;For more details see ME02-US06. Request My Personal Data."Terms of Service" link;For more details see ME02-US11. View "About" screen."Privacy Policy" link;For more details see ME02-US11. View "About" screen."Back" icon. | ME02-US06-P02 "Privacy" screenLink to Zeplin | The same as for iOS.Link to Zeplin |
| ME02-US06-AC03 | When the user taps on the "Back" button, then the "Account" screen (see ME02-US06-P01) should be opened with no changes made. | - | - |
| "About" screen |
| ME02-US06-AC04 | The following rows should be deleted from the "About" screen under the "Settings" tab:"Terms of Service""Privacy Policy". | - | - |
| "Privacy and Terms" screen |
| ME02-US06-AC05 | When the user taps on "Request My Personal data" on the "Account" screen, then the "Request My Personal Data" action sheet should be opened with the following UI elements (see screen designs):"Request My Personal Data" title;"We'll email you a link to a file with your personal information to \<user_email\>. It may take up to 24 hours to collect this data and send it to you.";"Send Request" button;"Close" button. | ME02-US06-P03 "Personal Data Request" screenLink to Zeplin | The same as for iOS.Link to Zeplin |
| ME02-US06-AC06 | When the user taps "Close" button, then the action sheet should be closed with no requests sent. | - | - |
| ME02-US06-AC07 | When the user taps "Send Request" button, then the request should be sent. | - | - |
| ME02-US06-AC08 | Precondition: the user has requested their personal data.If the request is successful, then:the system should display a success message M196 Data requested:Title: Data requestedBody: We've started creating a file of all data that you've shared with the Halo app and we'll email to \<user email\>. It may take up to 24 hours to collect this data and send it to you. Please note that the email may be in your Spam or Junk email folders.Buttons: OK, Learn more.TBD with Michael/ Heather: do we need to add an explanation "For more details on how to prevent this, tap "Learn more"? Cons: the pop-up text is already too long...2. further actions should be performed as described in [NI] ME02-US20. Send an email with the user personal data (under CCPA).QA note: when the user taps on the "OK" button in the error message, then the error pop-up should be closed.TBD update text in Appendix 3 | ME02-US06-P04 "Data Requested successfully" screenLink to Zeplin | - |
| ME02-US06-AC09 | When the user taps "Learn more" button, the link to the corresponding article should be opened in the mobile browser (see the detailed description in ME01-US16. Instructions to check spam folders on password recovery and email confirmation screens). | - | - |
| ME02-US06-AC10 | Precondition: the user has requested their personal data.If the request failed, then the system should display a success message M197 Data request failed:Title: Data request failedBody: Please try again later. If issue persists, please contact Halo customer support.Button: OKQA note: when the user taps on the "OK" button in the error message, then the error pop-up should be closed. | - | - |
| ME02-US06-AC11 | All the errors should be handled in accordance with ME14-F01 Unified errors handling. | - | - |
| ME02-US06-AC12 | '24 hours' should be a configurable value. |  |  |
