---
title: "[BL] ME02-US16. Solvvy integration"
sidebar_label: "[BL] ME02-US16. Solvvy integration"
sidebar_position: 152
last_modified: "Apr 25, 2022"
author: "Maria Shikareva [X]"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Maria Shikareva [X] Pavel Leonenko (MOB) Valeria Malets(QA) |
| Click here to expand... HALO-7435 - MOB [NT]: [Investigation] Solvvy integration Closed HALO-7786 - BE: [Investigation] Solvvy integration Closed HALO-7137 - MOB [+BE]: ME02-US16. Solvvy integration Closed HALO-8216 - BE [+MOB]: ME02-US16. Solvvy integration Closed HALO-9321 - MOB+BE: ME02-US16. Solvvy integration Closed Ballpark estimations:BE: 0,5 SP (a standard task to add a link to config).MOB: 2-3SPQA: 2SP |
| Click here to expand...27 Sep 2021 Maria Shikareva [X] updated ME02-US16-AC08 based on the investigation results here: HALO-8568 - [GOAL] MOB [NT]: [Investigation] Solvvy: Clearing the stored data on iOS the same as on Android Closed .13 Oct 2021 Maria Shikareva [X] ME02-US16-AC01 - ME02-US16-AC05, ME02-US16-AC09 are crossed out; ME02-US16-AC06 is changed based on changes related to the new story: ME02-US25. Update the Settings screen tiled view to list view.29 Oct 2021 Maria Shikareva [X] The valid link is added (provided by Pavel Leonenko).12 Mar 2022 Maria Shikareva [X] Added Jira links.25 Apr 2022 Maria Shikareva [X] Marked the story as baselined (ME02-F00. View "Settings" screen). |# General information

At the moment a new AI-powered Q&A system called Solvvy is used on www.halocollar.com (it can be seen by clicking the floating "chat" icon in the lower right corner). It was integrated to improve user's self-help and to decrease the amount of requests to CSAs. And now it's already clear that it has a great effect on website: it's supposed to reduce the amount of created tickets to customer support; lower customer support costs; improve customer satisfaction and loyalty. Also Solvvy seems to be smarter than Zendesk. In this reference we likely want to add this to our Help solution in the Settings tab in the mobile application.

# Useful links

1. [https://solvvy.com/](https://solvvy.com/)
2. [https://www.halocollar.com/](https://www.halocollar.com/)(to see how it's implemented on web site)
3. [https://www.zendesk.com/apps/support/solvvy/](https://www.zendesk.com/apps/support/solvvy/)

# Discussed items

Click here to expand...## Apps which already uses Solvvy as a solution

|  | App name | Description | Notes |
|---|---|---|---|
| 1 | VSCO | only one button for getting help;no links to articles;there's an option to contact support via email if the answer is not found. |  |
| 2 | Calm | One common button for help and support;there're links to articles together with icon for Solvvy;there's an option to contact support via email if the answer is not found. |  |
| 3 | Scribd | One common button for FAQs and Support.On tapping the list of possible options is opened:FAQs → the same as 'Help' section in the Halo app;Ask a Question → opens a Solvvy form;My Tickets → the same as 'Feedback' section in the Halo app. |  |## MOB Ballpark estimations for different solutions:

1. use our own web-view:
  1. 1SP per both platforms*(note: this is the estimation for integration only a separate estimation should be done for updating the UI based on the defined solution → see the suggestions in the ACs below)*;

2. use existing SDK (for Xamarin):
  1. MOB: 5SP per both platforms;

3. create SDK (the same that was done for Zendesk integration):
  1. MOB: 5-8 SP per**each**platform.

## Completed questions

1. **Q:**Can we use Solvvy instead of Zendesk?
**A:**Currently Zendesk is used:
**Summary:**It's better to combine both solutions: Zendesk and Solvvy.Solvvy extends the opportunities of using Zendesk. Solvvy needs access to any knowledge base to analyze it and provide the best answer (and Zendesk works best for it).
  1. to store and provide the link to Help Center articles. Solvvy requires the access to any knowledge base or Zendesk to "learn" to answer the questions correctly;
  2. for Tickets management. Zendesk now provides a tool for the user to create a ticket for Customer Support, also it allows extracting logs for CSAs.

2. **Q:**Do we need the "Help" section at all?
**A:**At the moment we don't track how often the user taps on the "Help" button. We suggest leaving this section because it seems that Solvvy sometimes cannot provide the article for the customer's request (based on .csv data sent by Thomas). Therefore it's better to leave this section so the user will be able to search the required information.
3. **Q:**Do we need adding the Solvvy button to MyMap screen?
**A:**It's possible: Solvvy will be opened in a separate web-view with the 'Back' button. But it may seem for the users like we understand that something is not clear for them on MyMap so we've added this button.

# User story

\> As a user I want to have access to a smart tool to answer my questions so that not to search for the Help articles by myself.

# Acceptance criteria

| AC | Description | iOS screen design/ implementation status | Android screen design/ implementation status |
|---|---|---|---|
| ME02-US16-AC01 | A new "Support" button should be displayed on the "Settings" screen. | Pic ME02-US16-P01 "Settings" screenLink to Zeplin | The same as for iOS.Link to Zeplin |
| ME02-US16-AC02 | "Help" and "Feedback" buttons should be removed. | - | - |
| ME02-US16-AC03 | When the user taps on the 'Smart Help' button on the "Settings" screen, then the "Support" screen should be opened with the following UI elements:"Back" icon;"Support" title;"FAQs" option:an icon;'FAQs' title;'Find answers to common questions' note;Note: the "FAQs" option is used instead of "Help" button."Smart Help" option:an icon;'Smart Help' title;'Type any question and get answers interactively' note;"My Tickets" option:an icon;'My Tickets' title;'Report issues to Halo Support and see responses' note;Note: the "My Tickets" option is used instead of "Feedback" button. | Pic ME02-US16-P02 "Support" screenLink to Zeplin | The same as for iOS.Link to Zeplin |
| ME02-US16-AC04 | When the user taps on the "Back" icon, then the "Settings" screen should be opened. | - | - |
| ME02-US16-AC05 | When the user taps on the "FAQs" option, the Help Center should be opened (see ME02-F04. View "Help" screen (incl. integration with Zendesk and mobile logs)). | - | - |
| ME02-US16-AC06 | When the user taps on the "Smart help" button on the "Settings" screen, then a Solvvy WebView should be opened with the "Back" icon (see screen designs).The URL from the e-Commerce team is used.All info provided in the web-view depends on a third-party system "Solvvy".It's acceptable that Android and iOS screen UI can be different. | Similar to the Android design. |  |
| ME02-US16-AC07 | The link should be the following: https://cdn.solvvy.com/deflect/customization/halocollar/support.html | - | - |
| ME02-US16-AC08 | Precondition: Solvvy WebView is opened.When the user taps on the "Back" icon, then:the previous "Settings' screen should be opened;all stored data should be cleared (i.e. the history should not be saved; is the user taps "Smart Help" again, then they will not see their previous questions).See the investigation results in HALO-8568 - [GOAL] MOB [NT]: [Investigation] Solvvy: Clearing the stored data on iOS the same as on Android Closed | - | - |
| ME02-US16-AC09 | When the user taps on the "My Tickets" option, then the 'My Tickets' screen should be opened (see ME02-F05. View "Feedback" screen). | - | - |
