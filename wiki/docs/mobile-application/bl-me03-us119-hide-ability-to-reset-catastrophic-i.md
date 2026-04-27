---
title: "(BL) ME03-US119 Hide Ability to reset catastrophic issue"
sidebar_label: "(BL) ME03-US119 Hide Ability to reset catastrophic issue"
sidebar_position: 391
last_modified: "May 03, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related pages | Change history |
|---|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-19313 - MOB: Hide option to reset cat.issues on mobile+wording update Closed |
| (BL) ME03-US121 BE+MOB: Ability to reset catastrophic issue |
| 03 May 2024 Kiryl Trafimau Baselined to ME03-F07. Collar Diagnostic |User Story Acceptance Criteria ME03-US119-AC01 ME03-US119-AC02

# User Story

\> As a Halo business owner I want users not to reset catastrophic issue without contact support so that we make sure they will claim warranty replacement

# Acceptance Criteria

| ID | Acceptance criteria | Design |
|---|---|---|
| ME03-US119-AC01 | If there is catastrophic issue was detected on collar (no matter if firmware feature for action on collar is supported)THEN User should see on the 'Collar diagnostics' screen of the collar that has an issue a section with:a. Title: 'We've detected an issue with your collar that requires a replacement.'b. Grey text: 'We want to help correct this right away and get a replacement collar on your dog. We just need you to confirm your shipping information [hyperlink to magic link] to start the warranty process.'[hyperlink to magic link]-blue, should initiate popup ME03-US119-AC02 | Zeplin: iOS | Android |
| ME03-US119-AC02 | IF user clicked hyperlink THEN Send email with the Magic link to the user (as is, no changes for popup and logic behind magic link)AND Popup should appear:Title: 'Check Your Email'Text: 'An email with next steps was sent to [email address].CTA link: 'Open mail app', opens default email app on the deviceClose button: closes popup |  |
