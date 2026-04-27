---
title: "(won't do) ME21-US94. Warning if pet age is more than 15 y.o. while adding pet"
sidebar_label: "(won't do) ME21-US94. Warning if pet age is more than 15 y.o. while adding pet"
sidebar_position: 366
last_modified: "Jan 29, 2024"
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related requirements |
|---|---|---|---|
| DRAFT |
| Kiryl Trafimau |
| HALO-18530 - MOB: Warning if pet age is more than 15 y.o. while adding pet Closed |
| ME21-US15. Assign pet |Acceptance criteria

User story

As an app user, I want to be prevented from making mistakes so that I provide correct information about the pet.

# Acceptance criteria

| AC# | Description | Comments, designs |
|---|---|---|
| ME21-US94-AC01 | Precondition: I am on the 'Adding Your Pet' screenIF I Select the Pet Birthday 15 years ago or earlierTHEN I can see popupTitle: Please, check the date TBDBody: According to your choice, your pet is 15 years old or older. TBDButton: OkBy click 'Ok' popup is closed |  |
| ME21-US94-AC02 | Precondition: I am on the 'Edit Pet Profile' screenIF I Select the Pet Birthday 15 years ago or earlierTHEN I can see popup Title: Please, check the date TBDBody: According to your choice, your pet is 15 years old or older. TBDButton: OkBy click 'Ok' popup is closed |  |
