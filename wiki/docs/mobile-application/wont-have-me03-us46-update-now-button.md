---
title: "[Won't have] ME03-US46. 'Update now' button"
sidebar_label: "[Won't have] ME03-US46. 'Update now' button"
sidebar_position: 118
author: "Nicolay Gavrilov"
---

| Document status | Document owner | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Nicolay Gavrilov |
| TBD |# User story

\> Users find it confusing that they cannot take action on their firmware updates. I think it would be helpful to add a button that says "Update now"

# Acceptance criteria

| AC | Description | iOS impl-n | Android impl-n |
|---|---|---|---|
|  | Decided to try updating the text of FW update statuses instead (see 2020-12-09 Meeting notes: BA call |  |  |
| ME04-US46-AC01 | Add a button that says "Update now". The button should available only when an update is pending. Add screen which says "please plug your Halo Collar in to charge and connect it to Wi-Fi to update your firmware"When connected → next screen: saying 'keep the collar plugged in and connected until you see .... led or something'. | IOS TO DO | ANDROID TO DO |
|  |  |  |  |
|  | The message text "Firmware update failed. Please contact support." does not provide much information for the user about why it failed, or how to prevent it. We should change this text, but we need to look at the underlying causes the update the message |  |  |
