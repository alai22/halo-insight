---
title: "(NI) ME21-US58. Add 'No Pack Membership' handling after 'Enable Permissions' screen"
sidebar_label: "(NI) ME21-US58. Add 'No Pack Membership' handling after 'Enable Permissions' screen"
sidebar_position: 354
author: "Kiryl Trafimau"
---

Page info| Document status | Document owner | Link to JIRA Issue | Related requirements | History of changes |
|---|---|---|---|---|
| APPROVED |
| Galina Lonskaya |
| HALO-17860 - MOB: [Logic] ME21-US58. Add 'No Pack Membership' handling after 'Enable Permissions' screen Closed HALO-20638 - MOB: [UI] ME21-US58. Add 'No Pack Membership' handling after 'Enable Permissions' screen Closed |
| ME01-US31. Catch users without subscription#ME01-US31-AC05ME01-US31. Catch users without subscription#ME01-US31-AC06 |
| 12 Dec 2023 Kiryl Trafimau has created a draft user story 02 Jul 2024 Galina Lonskaya has updated the user story in accordance with new UI design |Table of Contents

User story Acceptance criteria 'Pack Membership Plan' screen description 'Send instructions' sub flow 'Сontinue using the app without a collar' sub flow 'Log in to another account' sub flow Implementation Notes

# User story

As a Halo account owner I want to see the options available to me if it is discovered during the onboarding process that my email is not associated with a subscription, so that I can continue to use the product according to the intended subscription level.

# Acceptance criteria

| AC# | Description | Comments, designs | 'Pack Membership Plan' screen description | 'Send instructions' sub flow | 'Сontinue using the app without a collar' sub flow | 'Log in to another account' sub flow |
|---|---|---|---|---|---|---|
| ME21-US58-AC01 | Precondition: I don't have a subscription plan (including temporary)If I tap on Next button on 'Enable Permissions' screen (see the details in ME01-F10. Enable Permissions), then:'Join the Pack' screen should be opened. | See Figma |
| ME21-US58-AC02 | 'Join the Pack' screen should consist of:Screen title: 'Join the Pack' Text: copy the text from Figma, note: the email of the user account owner should be shown in this textImageSubtitle: Benefits of Joining: Text: copy the text from FigmaButton #1: 'Send Sign Up Instructions' Button #2 should consist of: Icon 'Continue using app without collar' title'Functionality will be limited.' subtitleRight arrow icon Button #3Icon 'Log in using another account' title 'Click here to try a different login.' Right arrow icon 'Have a plan already? Refresh' text, where 'Refresh' is a link |
| ME21-US58-AC03 | 'Join the Pack' screen should become scrollable, if the content doesn't fit into the screen. Note: it was discussed with Victor and Ryan that 'Have a plan already? Refresh' should be pinned to the bottom of the screen | - |
| ME21-US58-AC04 | Precondition: 'Join the Pack' is displayed. If I tap on 'Send Sign Up Instructions' button, then:'Check Your Email' card should be opened, see the detailed description in next AC'Benefits of Joining:' title should be changed to 'Instructions have been sent'Text under 'Benefits of Joining:' title should be changed to: copy the text from Figma, text should contain 'contact support' link 'Send Sign Up Instructions' should be changed to 'Resend Instructions' button.The email should be sent automatically to the current email of the user with "magic link" to the eCommerce siteOnce the link is clicked - the eCommerce site is opened AND user is already logged in AND the plan options are displayedthe text of the email: Appendix 7 - Email messages#EM048Messagewithmagiclinktobuysubscription (note: already implemented) | Immediately after user clicked 'Send instructions':See Figma |
| ME21-US58-AC05 | 'Check Your Email' card should consist of:Icon;'Check Your Email' title'An email with next steps was sent to [user's email address]' text'Open Email App' linkafter a tap - the default email application should open on the device'Close' buttonNote: the similar same card without button is implemented within ME01-US31. Catch users without subscription |
| ME21-US58-AC06 | Precondition: 'Join the Pack' with 'Resend Instructions' button is displayed. If I tap on 'contact support' link, then:'Need Help?' screen should be opened. | - |
| ME21-US58-AC07 | If I tap on 'Resend Instructions' button, then the same behavior should be applied as described in ME21-US58-AC03. | - |
| ME21-US58-AC08 | If something goes wrong after a tap on 'Send Sign up Instructions' / 'Resend instructions' button, then: unified error handling mechanism should be applied. | - |
| ME21-US58-AC09 | Precondition: 'Join the Pack' screen is opened If I tap on Refresh button, then: see all logic and error handling in ME19-US160. Refresh user's subscription to make sure there is no mismatch between Stripe and BE with one exception: after mismatch resolving 'Charging Your Collar' screen should be displayed. |  |
| ME21-US58-AC10 | 'Question mark' should be added to the right upper corner with the standard 'support' functionality: 'Need Help?' screen should be opened. | See Figma |
| ME21-US58-AC11 | Precondition: 'Join the Pack' is displayed. If I tap on 'Continue using the app' link, then:'Let's Get a Head Start' screen should be opened. Note 1: 'Let's Get a Head Start' has been implemented within ME21-US28. Onboarding: video screens (User Choice + App Tour)Note 2: 'Why Halo Collar?' screen will be removed and 'Let's Get a Head Start' screen will be updated within a separate story: (NI) ME21-US76. Update 'Let's get a head start' screen within 'Continue w/o collar' flow | See Figma |
| ME21-US58-AC12 | Precondition: 'Join the Pack' is displayed. IF I tap on 'Log In to another account' button, then:the Switch account сard should be opened. Note: this popup has been implemented within ME01-US31. Catch users without subscription | See Figma |# Implementation Notes

| IN | Description |
|---|---|
| ME21-IN58-AC01 | Technical details from Timofey:this task includes logic of checking subscription after finishing with permissions and selecting next screen ("Charging Your Collar" or "No Pack Membership"). Also, it includes returning to the "Charging Your Collar" when subscription is updated;we might need to use a version of subscription endpoint with Stripe synchronization to check subscription from this screen, just to make sure it is up-to-date. |
| ME21-IN58-AC02 | When a user initiates a request by tapping on a screen element, a standard blue spinner must appear if the processing time exceeds 0,5 TBD second, and remain visible until the processing is complete. |
