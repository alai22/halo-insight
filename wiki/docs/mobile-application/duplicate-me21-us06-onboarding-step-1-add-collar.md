---
title: "[Duplicate] ME21-US06. Onboarding: Step 1: Add collar"
sidebar_label: "[Duplicate] ME21-US06. Onboarding: Step 1: Add collar"
sidebar_position: 235
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | History of changes |
|---|---|---|---|
| DRAFT |
| Valeryia Chyrkun [X] |
| HALO-12565 - MOB : Onboarding: Complete navigation Closed |
| 05 Oct 2022 Maria Shikareva [X] Marked the story as 'Duplicate' because another page is created for this step: [NI] ME21-US32. Onboarding: Updates for 'Add Collar' flow. |+ need to change texts for the main flow also (not only Onboarding)

# General description

Note: when the user doesn't have a subscription, try scan QR code, then the prompting screen will be displayed. The user should be able to get back to the role choice from this screen

# User story

\> As an app user, I want to add my Halo to the app to proceed with the Onboarding process.

# Acceptance criteria

| AC | Description | Links, design |
|---|---|---|
| ME21-US06-AC01 | Precondition: user doesn't have active subscription/planWhen I click 'Next' button on the 'Prepare Your Halo Collar' screen, then I see 'You need a plan' screen (see the reqs here). |  |
| ME21-US06-AC02 | When I close 'You need a plan' screen then I navigated to 'Do you have a Halo Collar?' screen. |  |
| ME21-US06-AC13 | Precondition: user has active subscription/planWhen I click 'Next' button on the 'Prepare Your Halo Collar' screen, then I see 'Charge Your Halo Collar'. | https://miro.com/app/board/o9J_l3oJd20=/ Need to verify texts + animation? |
| ME21-US06-AC03 | Precondition: user has active subscription/planWhen I click 'Next' button on the 'Charge Your Halo Collar' screen, then I see 'Select a Halo Collar to Add' (see the requirements here). |  |
| ME21-US06-AC04 | 'Change your mind? Back to Start' text should be added to the 'Select a Halo Collar to Add' screen on the User Onboarding. |  |
| ME21-US06-AC05 | Where 'Back to Start' is a link to 'Do you have a Halo Collar?' screen. |  |
| ME21-US06-AC06 | When I tap 'Done' button on 'Halo Collar Has Been Securely Added to Your Account' then I see 'Assign you Halo to you Dog' screen. |  |
| ME21-US06-AC07 | When I tap 'Done' button on 'Halo Collar Has Been Securely Added to Your Account' then I see 'Assign you Halo to you Dog' screen (see ME21-US15. Assign pet) |  |
| ME21-US06-AC07 | When I click 'Wi-Fi Setup' on 'Assign you Halo to you Dog' screen then I see 'About the Halo Collar Connections' page. |  |
| ME21-US06-AC07 | When I click 'Next' button on 'About the Halo Collar Connections' page, then I navigated to 'Connect your Halo to Wi-Fi'. See the requirements on ME03-F03. Collar Wi-Fi setup. |  |
| ME21-US06-AC08 | 'Setup Wi-fi Later' button should be added to the bottom of 'Connect your Halo to Wi-fi' screen. |  |
| ME21-US06-AC09 | When I click 'Setup Wi-fi Later' button, then I see 'Connect Your Halo To Wi-Fi' pop-up with the following elements (TBD -add popup#):Title: Connect Your Halo To Wi-FiText: It is important to connect your Halo collar to Wi-Fi to download and apply firmware updates to receive new features.Button: Setup Wi-FiContinue With LTE |  |
| ME21-US06-AC09 | When I connection to Wi-fi successfully finished on 'Connect your Halo to Wi-Fi' then I navigated to 'Firmware Update' screen (see [BL] ME21-US07. Add FW update screens to 'Add Collar' flow). |  |
