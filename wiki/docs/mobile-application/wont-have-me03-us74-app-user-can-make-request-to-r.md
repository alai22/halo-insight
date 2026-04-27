---
title: "(Won't have) ME03-US74. App user can make request to remove the collar from the other app"
sidebar_label: "(Won't have) ME03-US74. App user can make request to remove the collar from the other app"
sidebar_position: 209
author: "Valeryia Chyrkun [X]"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Valeryia Chyrkun [X] |
| HALO-11098 - MOB+BE: App user can make request to remove the collar from the other app user Ready for Development |
| Click here to expand... |# General description

Sometimes collar can be sold or gifted to another person, it will cause the issue when new owner cannot register the collar with their account because it is still associated with the previous owner. The pop-up which instructs user to ask the previous owner to remove the collar from account is a bad solution, because sometimes the new and previous owners have never even heard each other.

- For security reasons, Halo Customer Service team cannot delete a collar from an account without the explicit written permission of the original owner. (see the[article](https://support.halocollar.com/hc/en-us/articles/360062161853-Someone-gave-sold-me-a-collar-but-my-Halo-App-says-it-is-still-connected-to-their-account))

# User story

\> As an owner I want to be able to add/request ownership of the collar which is currently assigned to another user so I will be aware on what actions needed and original owner will not need to share their credentials for account.Ad a business owner I want minimize the involvement of CSAs in process of ownership change communication, so that their efforts can be focused on more important tasks.

# Acceptance criteria

| AC | Text | Screens | 'This collar is assigned to another account' pop-up |  | Email for removal |  | Push notifications after successful collar removal |  |
|---|---|---|---|---|---|---|---|---|
| General requirements |  |
| ME03-US74-AC01 | If I select a collar from the list under 'Assigned to Another Accounts' then the selected collar should not beep and blink. |  |
| ME03-US74-AC02 | If I select a collar from the list under 'Assigned to Another Accounts' then the 'Next' button doesn't become active. |  |
| ME03-US74-AC03 | Precondition: User is on the 'Add new collar-Select Halo Collar' screen and there's at least one collar under 'Assigned to Another Accounts' sectionWhen I click the collar located under 'Assigned to Another Accounts' , then I see the pop-up (M234) with the following elements:'This collar is assigned to another account' title'If you believe it belongs to you, you can request that the current owner to remove the collar from their account. ' text'Send request' button'Cancel' button |  |
| ME03-US74-AC04 | After user clicks 'Send Request' the pop-up is closed and the toast with the text 'The request is successfully sent.' is displayed. |  |
| ME03-US74-AC05 | If user clicks 'Cancel' then the 'This collar is assigned to another account' pop-up is closed. |  |
| ME03-US74-AC06 | User is allowed to send only 3 requests per day. When user clicks the 'Send Request' button for the 4th and more time then the pop-up (M233) is displayed:'The request is already sent' title'It may take some time for original owner to remove the collar from their account. You will be notified once the collar is permitted for adding to your account.' text'Ok' button. When I click the 'Ok' button, then the pop-ups are closed. |  |
| ME03-US74-AC07 | If I click 'Send Request' on the 'This collar is assigned to another account' pop-up, then the email is sent to the original owner with the following text:Subject: Security alert for your Halo collarBody: Halo blocked a user from assigning your Halo Collar \<Collar SN\> to their account.Someone just tried to assign one of your Halo collars to their account. Halo blocked them, but you should review what happened.If you no longer possess this collar and wish to permit this user to assign this Halo to their account, please tick the checkbox below and click the Submit button. This will remove this Halo from your account and permit them to take ownership of it. If you are still the owner of this Halo collar, you can ignore this email or visit the virtual Halo Dog Park for live, face-to-face assistance. Find the Halo Dog Park at www.halocollar.com/dogpark, or in the Halo App under Settings \> Live Support. I agree that collar \<Collar SN\> will no longer be assigned to my accountSubmit Best regards, Your Halo Security TeamWhere 'Submit' Button is inactive until user turns the checkbox 'I agree' 'I agree' checkbox is unchecked by default.\<Collar SN\> is a serial number of collar whose ownership was requested. | Text was changed |
| ME03-US74-AC08 | The 'Submit' link expires within 24 hours from the moment of the email sent date. |  |
| ME03-US74-AC09 | Precondition: Link is validWhen I click 'Submit', then I navigated to the web-page with the following elements:'Halo' icon'Great!' title'The collar was successfully removed from your Halo account' |  |
| ME03-US74-AC10 | Precondition: Link is invalidWhen I click 'Submit', then I navigated to the web-page with the following elements:'Halo' icon'Oh no!' title'The link has expired. Please press the button below to request a new link to remove the collar''Resend link' button |  |
| ME03-US74-AC11 | If user clicks 'Submit' and link is valid then the collar is removed from the original owner's account. |  |
| ME03-US74-AC12 | When the original owner successfully removes the collar from the account, then new owner receives notification:The collar \<Collar SN\> can be added to your account. |  |
| ME03-US74-AC13 | When the original owner successfully removes the collar from the account, then original owner receives notification:The collar \<Collar SN\> was removed from your account. |  |
