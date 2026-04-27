---
title: "ME03-F08. Delete Collar"
sidebar_label: "ME03-F08. Delete Collar"
sidebar_position: 630
last_modified: "Jan 31, 2025"
author: "Mariya Kolyada"
---

User Story: As a user, I want to be able to delete a collar from my account so that I don't see it if I don't use it anymore and someone who might use it can add it to their account.

Acceptance Criteria:

- If User taps the 'Delete Collar' button, then the app should displayM23 confirmation pop-up (Existing App:M23)
www.figma.com
- If User confirms deletion, the app should:
  - Display the More screen with the updated My Devices section.
  - Remove collar from user account.

- BE should:
  - Make corresponding updates in the device twin.
  - Deactivate SIM card of the collar.
*Note: there is no need to notify the app user about SIM card deactivation using the mobile app interface, the same statement is valid for CSA/SA.*

- If the collar is offline, the device will be synchronized right after it goes online. No data that might be accumulated on the device in the offline state is saved in the cloud in this case.
- If the SIM card deactivation is failed (e.g. "canceled" status is received from KORE), then:
  - SA/СSA should be informed about the failure, see AE03-US47. Deactivate/activate SIM card from the list of the SIM cards


