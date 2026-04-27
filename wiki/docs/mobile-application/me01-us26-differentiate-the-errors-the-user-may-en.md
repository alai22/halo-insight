---
title: "ME01-US26 Differentiate the errors the user may encounter during \"login\" process"
sidebar_label: "ME01-US26 Differentiate the errors the user may encounter during \"login\" process"
sidebar_position: 194
last_modified: "May 26, 2022"
author: "Nicolay Gavrilov"
---

| Document status | Document owners | Links to JIRA Issues | Change history |
|---|---|---|---|
| APPROVED (SQ) |
| Nicolay Gavrilov Nikita Krisko |
| HALO-10284 - MOB: ME01-US26 Differentiate the errors the user may encounter during "login" process Closed |
| Click here to expand... |# User story

\> As a user I want to know the exact reason why I can't login to the app so that I understand if I can do anything to fix the problem.

# Acceptance criteria

| AC | Description | Links | As is | To be | As is | To be |
|---|---|---|---|---|---|---|
| ME01-US26-AC01 | Preconditions:the user is on the "Application startup failed" screen As isTo beIf after tapping on the "Retry" button a connection error occurs, the app displays the M113 Network error pop-up.If after tapping on the "Retry" button a connection error occurs, the app should display the M125 Connection error.And if the user taps "Try again" on the M125 pop-up 4 times in the row and the internet connection is not restored the app should show the M113 Network error. | If after tapping on the "Retry" button a connection error occurs, the app displays the M113 Network error pop-up. | If after tapping on the "Retry" button a connection error occurs, the app should display the M125 Connection error.And if the user taps "Try again" on the M125 pop-up 4 times in the row and the internet connection is not restored the app should show the M113 Network error. | ME14-F01 Unified errors handlingAppendix 3 – Error, Success, Warning Messages |
| If after tapping on the "Retry" button a connection error occurs, the app displays the M113 Network error pop-up. | If after tapping on the "Retry" button a connection error occurs, the app should display the M125 Connection error.And if the user taps "Try again" on the M125 pop-up 4 times in the row and the internet connection is not restored the app should show the M113 Network error. |
| ME01-US26-AC02 | Preconditions:the user is on the "Application startup failed" screen As isTo beIf after tapping on the "Retry" button a communication error occurs, the app displays the M126 Communication error pop-up. After the pop-up is closed the user is logged out and is forwarded to the login screen.If after tapping on the "Retry" button a communication error occurs, the app displays the M126 Communication error pop-up. After the pop-up is closed the user should remain logged in and should stay on the "Application startup failed" screen. | If after tapping on the "Retry" button a communication error occurs, the app displays the M126 Communication error pop-up. After the pop-up is closed the user is logged out and is forwarded to the login screen. | If after tapping on the "Retry" button a communication error occurs, the app displays the M126 Communication error pop-up. After the pop-up is closed the user should remain logged in and should stay on the "Application startup failed" screen. | Appendix 3 – Error, Success, Warning Messages |
| If after tapping on the "Retry" button a communication error occurs, the app displays the M126 Communication error pop-up. After the pop-up is closed the user is logged out and is forwarded to the login screen. | If after tapping on the "Retry" button a communication error occurs, the app displays the M126 Communication error pop-up. After the pop-up is closed the user should remain logged in and should stay on the "Application startup failed" screen. |
