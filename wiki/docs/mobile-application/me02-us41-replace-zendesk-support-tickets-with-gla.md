---
title: "ME02-US41. Replace Zendesk support tickets with Gladly and move logs attachment to a separate support item"
sidebar_label: "ME02-US41. Replace Zendesk support tickets with Gladly and move logs attachment to a separate support item"
sidebar_position: 614
last_modified: "Jan 22, 2025"
author: "Mariya Kolyada"
---

| Document status | Document owners | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Mariya Kolyada, Dmitry Kravchuk , Katherina Kaplina |
| HALO-22224 - MOB+BE: ME02-US41. Replace Zendesk support tickets with Gladly and move logs attachment to a separate support item Closed |
| As of 14 Jan 2025:Mariya Kolyada created the initial version of US. |# User Story

\> As a Halo accout owner I want to able to view updated My Tickets element and added Send Diagnostics so that I can reach the new Gladly system for support tickets and send logs as a separate feature because it is impossible automatically attach them to Gladly.

# Acceptance criteria

| AC | Description | iOs design | Android design | Element | Value |
|---|---|---|---|---|---|
| ME02-US41-AC01 | Remove My Tickets on the following screens:Settings Screen: Support Need Help Screen | OUTDATEDFigma 1 | Figma 2 | The same as iOs |
| ME02-US41-AC02 | Remove the 'My Tickets' button from Guide and Video Tutorials screen managed by ZendeskSDK. |
| ME02-US41-AC03 | Add the following new support item below 'Halo Dog Park' on the:Settings Screen: Support Need Help ScreenElementValueTitleSend App DiagnosticsSubtitleEmail system logs to support team.Action on tapBehave according to requirements described in ME14-US33. Start email sending to Halo from the Halo App. | Title | Send App Diagnostics | Subtitle | Email system logs to support team. | Action on tap | Behave according to requirements described in ME14-US33. Start email sending to Halo from the Halo App. |
| Title | Send App Diagnostics |
| Subtitle | Email system logs to support team. |
| Action on tap | Behave according to requirements described in ME14-US33. Start email sending to Halo from the Halo App. |
| ME02-US41-AC04 | Put the following values in the draft email for the 'Send App Diagnostics':Recipient: support@halocollar.com;Subject: Log Submission;Body: empty;Attachments: App logs (the same that the app attaches now to Zendesk tickets). |## Mobile analytics

Log the following 'Clicked CTS' events to Amplitude:

| Event ID | CTA name | Event Properties: Screen Name |
|---|---|---|
| ME02-US41-MA01 | Halo Help | 'Settings' or 'Need help?' |
| ME02-US41-MA02 | Halo Dog Park |
| ME02-US41-MA3 | Send App Diagnostics |
| ME02-US41-MA04 | Guide and Video Tutorials |
