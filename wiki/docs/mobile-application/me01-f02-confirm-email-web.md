---
title: "ME01-F02. Confirm email (web)"
sidebar_label: "ME01-F02. Confirm email (web)"
sidebar_position: 40
author: "Galina Lonskaya"
---

| Document type | Document status | Document owners | Link to JIRA Issue |
|---|---|---|---|
| Baseline story (checked by dev team) |
| APPROVED |
| Galina Lonskaya, Anastasia Brechko |
| BE: HALO-2861 - BE: ME01-US11. Confirm email (new UI design) Closed , HALO-4881 - BE: [Android] ME01-F02. Confirm email (web) Closed |# User story

\> As an account owner, I want to confirm my email address so that I can log into my Halo account first time.

| AC | Description | UI design / impl-n status |
|---|---|---|
| ME01-F02-AC01 | If I press the "Confirm Email Address" button in the email EM001 Confirm Your Halo Account and the link is valid, then:the app user's email should acquire "confirmed" status;a web screen with a success message should be displayed. See the screen design.for iOS: a toast message "Open this page in Halo?" with the Cancel and Open button should be displayed. See the continuation in ME01-F02-AC02. for Android: Halo Collar app should be opened without a toast message displaying as in the iOS app. | IOS DONE ANDROID TO DOLink to Zeplin |
| ME01-F02-AC02 | Precondition: AC is valid for iOS only. A toast message "Open this page in Halo?" with the Cancel and Open button is displayed on the screen design above with the info about successful email confirmation. If I tap on the Open button, then the Halo Collar app should be opened.If I tap on the Cancel button, then the toast message should be closed. | IOS DONE ANDROID TO DO |
| ME01-F02-AC03 | If I press the "Confirm Email Address" button in the email EM001 Confirm Your Halo Account and the link is not valid anymore, then:a web screen with the info about failed email confirmation due to the link expiration should be displayed. See the screen design. | IOS DONE ANDROID TO DOLink to Zeplin |
| ME01-F02-AC04 | Precondition: the screen design "Web screen with the info about failed email confirmation due to the link expiration" is displayed. If I press the Resend Confirmation button and the email isn't confirmed, then:the EM001 Confirm Your Halo Account should be sent again;a web screen with a success message should be displayed. See the screen design. | IOS DONE ANDROID TO DOLink to Zeplin |
| ME01-F02-AC05 | Precondition: the screen design "Web screen with the info about failed email confirmation due to the link expiration" is displayed.If I press the Resend Confirmation button and the email is confirmed, then:a web screen with a success message should be displayed. See the screen design.the mobile app should be launched according to ME01-F02-AC01 and ME01-F02-AC02 | IOS DONE ANDROID TO DO |
