---
title: "[BL] ME03-US23. SIM card activation/deactivation after the collar binding/unbinding"
sidebar_label: "[BL] ME03-US23. SIM card activation/deactivation after the collar binding/unbinding"
sidebar_position: 122
author: "Galina Lonskaya"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| APPROVED |
| Galina Lonskaya, Alexei Zhukov, Anastasia Brechko, Pavel Leonenko |
| HALO-5882 - BE: [SMRGP II] ME03-US23. Sim-card activation/deactivation on the collar binding/unbinding Closed - this ticket is merged to HALO-6286 HALO-6286 - BE: [SMRGP II]: Sim card activation/ deactivation for plan changes/ on the collar binding/unbinding (part 1) Closed HALO-6361 - MOB: [SMRGP II] ME03-US23. Sim-card activation/deactivation on the collar binding/unbinding Closed |
| 05 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |User story Acceptance criteria BE part Mobile part Diagram 1 Sim card statuses

# User story

\> As the product owner, I want to have an automatic SIM card activation/deactivation after the collar binding/unbinding to the app user account so that I will not be forced to pay for SIM cards of the collars not added to the app user account.

# Acceptance criteria

| AC | Text | iOS implementation status/ UI designTO DO | Android implementation status/ UI design TO DO | BE part | Mobile part |
|---|---|---|---|---|---|
| ME03-US23-AC01 | Precondition: the collar isn't added to any user account at the moment and the SIM card of the collar is deactivated and not in 'test state' (see Note 1 below).If I add the collar to the my account, then:in addition to the already implemented logic described in ME03-F00. Add collar, the following step should be performed after the successful completion of the collar addition flow (the flow may include or may not include pet assigning): SIM card should be activated, by default Halo Collar 5 MB plan should be applied.Note 1 (from Michael): All units ship with the SIM 'active', but in a special 'test state' that incurs no charges until data starts being sent. We do NOT need to actively ACTIVATE these SIMs when they FIRST get associated to their FIRST user account.Note 2: Integration with KORE is required for SIM card activation/deactivation.Note 3: See Diagram 1 Sim card statuses: state machine diagram below. | - | - |
| ME03-US23-AC02 | If SIM card activation is being performed and 'Halo Collar 5 MB plan' isn't available in KORE (PrismPro) by any reason, then:the first plan within the list of the available plans should be applied. | - | - |
| ME03-US23-AC03 | Precondition: the collar isn't added to any user account at the moment and SIM card of the collar is activated and/or in special 'test state'.If I add the collar to my account, then:then no changes described in ME03-US23-AC01 should be applied within the collar addition flow. | - | - |
| ME03-US23-AC04 | Precondition: the collar is added to any user account at the moment and the SIM card of the collar is activated or in 'test state';If the collar is deleted from my account, then:in addition to the already implemented logic described in ME03-F01. Collars list (see the section: Delete collar), AE03-US30. Delete collar from the app user account, ME02-US02. View "Edit Account" screen (see the section: Delete account) the following step should be performed after the successful deleting: SIM card of the collar should be de deactivated.Note: there is no need to notify the app user about SIM card deactivation using mobile app interface, the same statement is valid for CSA/SA. | - | - |
| ME03-US23-AC05 | If the SIM card activation/deactivation is failed (e.g. "canceled" status is received from KORE), then:SA/СSA should be informed about the failure, see AE03-US40. View the list with the failed SIM card activation/deactivations.the alert/email should be sent to L2 engineer. Removed, agreed on the tech call (3/23/21) | - | - |
| ME03-US23-AC06 | Precondition: 'Bluetooth Devices - Successfully Paired with device' screen is displayed; SIM card of the collar can be in any status.In addition to the already implemented logic described in ME03-F00. Add collar, the following step should be performed after the tap on 'Done' button at 'Bluetooth Devices - Successfully Paired with device' screen and further successful completion of the collar binding:the standard popup message M180 SIM card activation time warning should be displayed above 'Bluetooth Devices - Successfully Paired with device' screen. Note: In case the collar binding isn't completed successfully, M180 SIM card activation time warning should not be displayed. | - | - |
| ME03-US23-AC07 | Precondition: M180 SIM card activation time warning is displayed above 'Bluetooth Devices - Successfully Paired with device' screen.If I tap on 'OK' button at M180 SIM card activation time warning,then ME03-F03. Collar Wi-Fi setup flow should be started. | - | - |
| Note 1: Within this story we are not going to perform bulk SIM card deactivation of "unassigned" collars (IMPORTANT: but not collars in a special 'test state'). This PBI has been added to the Product Backlog and will be performed later (as on 1/18/21 PBI has Low 4 priority). Note 2: See the state machine diagram created by BE team: Sim Card Activation/Deactivation | - | - |#### Diagram 1 Sim card statuses


