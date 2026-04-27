---
title: "[Postponed] ME03-USXX. Send non-cat. issue if the contact tips lose contact with the skin several times throughout the day"
sidebar_label: "[Postponed] ME03-USXX. Send non-cat. issue if the contact tips lose contact with the skin several times throughout the day"
sidebar_position: 420
author: "Galina Lonskaya"
---

Page info| Document status | Document owners | Links to JIRA Issues | History of changes |
|---|---|---|---|
| DRAFT |
| Kiryl Trafimau Galina Lonskaya |
| HALO-20421 - FW+BE+MOB: Send non-cat. issue if the contact tips lose contact with the skin several times throughout the day Open |
| 30 May 2024 the draft user story is created |# User story

\> As Halo collar account owner I want to get notified when the there is an issue with the contact tips so that I can fix it

# Acceptance Criteria

| AC | Description | Notes |
|---|---|---|
| ME03-USXX-ACXX | IF at least 1 issue detected in DD during the last week according to validation rulesTHEN, the Event to Braze should be sent |  |
| ME03-USXX-ACXX | IF issue find in the last week DD according to validation rulesTHEN specific text for this the issue should be included in the email to the user |  |
| ME03-USXX-ACXX | IF any issue find in the last week DD according to validation rulesTHEN the following should be included in the end of the email to the user:Last scan [date time]Battery life (7 days average) [battery_life]FW version [version number] | expected to be done in the scope of (NI) ME03-US133 BE: Beam Healthcheck reports (Non-catastrophic issues) |# Validation rule

| Error name | Error validations | Text to tell the user about the issue (email). Managed on the Braze sideThis texts are suggestions, should be reviewed by Halo team. |
|---|---|---|
| Contact tips non-catastrophic issue | Counter 'skin contact test failed'\>XAND Counter 'skin contact test failed'\<=YNOTE: 2nd condition is to exclude those cases when this is a more serious catastrophic issue, which will be triggered if Counter \>Y | Our system has identified that your Halo Collar's contact tips may not be making proper contact with your dog's skin. This can affect the collar's performance and its ability to provide accurate feedback.To ensure the best performance and safety for your dog, please follow these steps:Check Fit and Placement:Ensure the collar is snug but not too tight. You should be able to fit two fingers comfortably between the collar and your dog's neck.Position the collar high on your dog's neck, close to the ears. This is typically the narrowest part of the neck, ensuring a more secure fit.Adjust Contact Tips:Make sure the contact tips are touching your dog's skin directly. If your dog has thick fur, you may need to trim the hair around the neck area where the contact tips rest.If your dog has long fur, consider using longer contact tips provided with the collar.Regular Checks:Regularly check the collar's fit and contact points, especially if your dog is very active. Adjust as necessary to maintain good contact.Comfort and Skin Care:Inspect your dog’s neck regularly for any signs of irritation or discomfort. If you notice any issues, adjust the collar's fit or contact tips accordingly and consult your veterinarian if needed.If you have any questions or need further assistance, please do not hesitate to contact our support team. |
