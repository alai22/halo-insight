---
title: "[BL] ME21-US25. Onboarding: Charge Your Halo Collar"
sidebar_label: "[BL] ME21-US25. Onboarding: Charge Your Halo Collar"
sidebar_position: 259
author: "Maryia Paklonskaya [X]"
---

| Document status | Document owner | Link to JIRA Issue | History of changes | BA notes: | This story is mentioned on: |
|---|---|---|---|---|---|
| APPROVED |
| Maryia Paklonskaya [X] |
| HALO-12759 - MOB: ME21-US25: Add 'Charge Your Halo Collar' screen to the 'Add Collar' step of the Onboarding process Closed |
| 11 Aug 2022 screens are added for verification to the Action Items List 12 Aug 2022 draft version of the specification16 Aug 2022 specification is changed upon the comments from the customer09 Nov 2022 Maria Shikareva [X] Marked the story as baselined (see ME03-F00. Add collar). |
| add new screen to the https://miro.com/app/board/o9J_l3oJd20=/ send for verification by customerverified and approved texts, pictures, animation on the screen1verified and approved texts for the screen2 + cancel button behaviour |
|  |User story Acceptance criteria

Problem description

Now in the Onboarding flow there is no "Charge Your Halo Collar" screen. Thus, end users (especially first-time users) may not know how to safely charge their collars, what to avoid and what to expect from the collar.

# User story

As an app user, I want to add see how to charge my Halo Collar, so that I know the safest flow to charge it and aware of its behavior.

# Acceptance criteria

| AC# | Description | Comments, designs |
|---|---|---|
| ME21-US25-AC01 | Precondition: user has active subscription/planWhen I click 'Next' button on the 'Prepare Your Halo Collar' screen, then I see 'Charge Your Halo Collar'. | Zeplin Android; Zeplin iOS; |
| ME21-US25-AC02 | On the screen I see: "Close" button"Add collar" heading text"Charge Your Halo Collar" heading text"Plug in your Halo Collar using the Halo charging cord in a location where you expect to have Wi-Fi and/or LTE coverage." subheading textGif-animated picture with the cord and Halo CollarPicture of the cord + text "Use original Halo charging cord." Picture of the port + text "Make sure port is clean and has no water." Pictures of the battery and clock + text "Make sure the Battery Light on the collar blinks green when you plug it in."+ Text "Once it is charged (can take up to 2 hours) the Light will turn solid green."Information icon + text "NOTE: Do not unplug your collar if your collar is blinking any color other than green. This means an update is in progress."Button "Next" |
| ME21-US25-AC03 | When a user adds the second collar (see [Not impl.] ME21-US14. Onboarding: add the 2nd collar), then the app should display a screen "Charge Your Halo Collar" as well. |
| ME21-US25-AC04 | By clicking on the "Close/x" button while on the First Onboarding Collar - the parent screen should be shown "Prepare Your Halo Collar" |
| ME21-US25-AC05 | By clicking on the "Close/x" button while adding second+ collar - the previous screen should be shown |
| ME21-US25-AC06 | By clicking on the "Next" button - the screen "Link your Halo Collar to Your Account" (ME03-US72-AC05) should be displayed |
| ME21-US25-AC07 | The scroll should appear on the page if it does not fit the screen size. |
| ME21-US25-AC08 | Change texts on the next screen (Previous requirements ME03-US87-AC01)Heading text: "Link your Halo Collar to Your Account"instead of "select a halo collar to add"Text: "Quickly and firmly press and release the Power button on the front of the collar."instead of "Plug you Halo Collar into your Halo charging cord. Press and release the Power button on the front of the Halo Collar."Text with link should remain as is | Zeplin Android; Zeplin iOS; |
