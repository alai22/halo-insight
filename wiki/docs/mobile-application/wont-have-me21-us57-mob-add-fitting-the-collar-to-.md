---
title: "[Won't have] ME21-US57. MOB: Add Fitting the Collar to Your Pet screen"
sidebar_label: "[Won't have] ME21-US57. MOB: Add Fitting the Collar to Your Pet screen"
sidebar_position: 345
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue |
|---|---|---|
| NEED UPDATE |
| Kiryl Trafimau |
| HALO-17859 - MOB, BE: Fitting the Сollar to Your Pet screen Closed |Acceptance criteria

User story

As an app user, I want to fit the collar as early as possible so that I can return it back without spending time on Onboarding

# Acceptance criteria

| AC# | Description | Comments, designs |
|---|---|---|
| ME21-US57-AC01 | Pre-condition: I am on 'Do you have a Halo Collar?' screenIF I selected 'Yes. I'm ready to set up my collar' optionWHEN I click NextTHEN I am redirected to the 'Fitting the Collar to Your Pet' screen |  |
| ME21-US57-AC02 | WHEN I am on the 'Fit the Collar to Your Pet' screenTHEN I can see:Step 1/2: Fitting Your Collar'Back' button, redirects to 'Do You Have a Halo Collar?' screen? button5 lines corresponding to the step of Onboarding process, 1st is highlighted'Fitting the Collar to Your Pet' title'If you haven't already sized your Halo collar to your dog, watch the video below to learn how.' text.VideoVideo file and subtitles https://vimeo.com/770767299 auto_generated_captions.vtt.srtPreview file Button'Skip' (secondary button) if video hasn't been watched yet'Next' (primary button) if video hasn't been watched yetBy click redirect the user to 'Charging your collar screen' | ADD VISUAL GRAPHICS |
| ME21-US57-AC03 | Pre-condition: Collar was already added (e.g. I added collar, did not add pet and then clicked 'back').WHEN I am on the 'Fit the Collar to Your Pet' screenTHEN I should not see 'back' buttonAND By click on Next I am redirected to the Adding your Pet screen |  |
