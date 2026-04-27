---
title: "[BL] ME03-US68. Android: show the \"Location and Bluetooth permission denied\" message when adding a collar"
sidebar_label: "[BL] ME03-US68. Android: show the \"Location and Bluetooth permission denied\" message when adding a collar"
sidebar_position: 189
author: "Nicolay Gavrilov"
---

| Document status | Document owner | Link to JIRA Issue | Changes history |
|---|---|---|---|
| DRAFT |
| Nicolay Gavrilov |
| HALO-9860 - [Android] ME03-US68 Show M143 "Bluetooth permission denied" message when adding a collar Closed |
| Click here to expand... |# User story

\> As an owner I want see the correct error when I add a collar to my account and the Location permission is not granted on my Android smartphone so that I can understand what exactly I need to do to fix the issue

# Acceptance criteria

| AC | Text |
|---|---|
| ME03-US68-AC01 | Preconditions:the Android app is usedthe Location permission is not grantedWhen the user scans a QR code or enters the collar serial number manually, the app should show the M217 "Location and Bluetooth permission denied" message |
