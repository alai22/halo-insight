---
title: "[BL] ME03-US05. Delete an offline collar"
sidebar_label: "[BL] ME03-US05. Delete an offline collar"
sidebar_position: 6
author: "Nicolay Gavrilov"
---

| Target release | Role | Epic | Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|---|---|---|
| December Release |
| Owner |
| ME03 As an Owner, I'd like to manage my collars to keep their info up to date. |
| REVISED |
| Nicolay Gavrilov |
| TBD |
| 07 Oct 2021 Maria Shikareva [X] The story is marked as baselined. |# User story

\> As an owner I want to delete an offline collar so that I could remove malfunctioned or lost devices from the list of collars in my app.

# Acceptance criteria

| AC | Text | Links |
|---|---|---|
| ME03-US05-AC01 | The user can delete a collar that is currently offline from his/her account. | N/A |
| ME03-US05-AC02 | Before deleting an offline collar the app displays a confirmation pop-up M23 Delete Collar.In case user confirms deleting, the app removes the device from user's account and BE makes corresponding updates in the device twin. The collar will be synchronized with device twin right after it goes online. No data that might be accumulated on the device in offline state is saved in the cloud in this case.In case user cancels deleting the app closes the pop-up. | Pop-ups:M23 Delete Collar |
