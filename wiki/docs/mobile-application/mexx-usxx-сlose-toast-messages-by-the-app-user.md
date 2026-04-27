---
title: "MEXX-USXX. Сlose toast messages by the app user"
sidebar_label: "MEXX-USXX. Сlose toast messages by the app user"
sidebar_position: 227
last_modified: "Aug 29, 2023"
author: "Galina Lonskaya"
---

| Document status | Story owners | Link to JIRA Issue |
|---|---|---|
| DRAFT |
| Galina Lonskaya |
| HALO-11945 - MOB: Сlose toast messages by the app user Ready for Development |# General description

While developing a new concept of Instant Feedback redesign has become obvious that mandatory 4 sec displaying of the toast message doesn't give enough flexibility for the end user. Since he/she can read the toast message quicker than during 4 sec and want to have access to the functionality lying underneath. So, it was decided to add ability to close the toast messages by the app user.

# User story

\> As a Halo account owner, I want to be able to close a toast message so that I can see another toast message or have access to more space on my map.

# Acceptance criteria

| AC | Text | iOS | Android |
|---|---|---|---|
| ME0X-USXX-ACXX | "Cross" icon should be displayed on all toast messages within the app. Note 1: the list of all toast messages can be found here: Appendix 10 – Toast Notifications | Zeplin | ADD SCREEN |
| ME0X-USXX-ACXX | If I tap on the Cross icon, then:the currently displayed toast message should be closed; a toast queuing should be shown (if exist). | - | - |# Implementation notes

| IN | Description |
|---|---|
| ME0X-USXX-INXX | iOS toasts have in-built functionality of the toast closing. Dev team just need to enable it. Note: discussed Timofey Burak [X] |
