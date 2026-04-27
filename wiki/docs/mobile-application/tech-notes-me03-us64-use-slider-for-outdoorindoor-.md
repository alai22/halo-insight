---
title: "Tech notes: ME03-US64. Use slider for outdoor/indoor threshold adjustment"
sidebar_label: "Tech notes: ME03-US64. Use slider for outdoor/indoor threshold adjustment"
sidebar_position: 170
last_modified: "Oct 22, 2021"
author: "Maria Shikareva [X]"
---

# Contents

General description Terminology Problem Solution (and main implementation notes)

# General description

This page is created to describe the whole implementation logic and communication between different components.

See the initial description in the business requirements here: [Not implemented] ME03-US64. Use slider for outdoor/indoor threshold adjustment.

# Terminology

Metrics: current GPS accuracy level. The greater it is, the more accurate GPS coordinates are.

GPS Status: can be Indoor, Hybrid GPS, and Outdoor based on Metrics values. Indoor means Metrics is low; Outdoor = Metrics is high; Hybrid means Metrics is somewhere in between.

Boundaries (lower and upper, BL and BU): values which are actually used to calculate GPS Status:

- Metrics \< BL → Indoor
- Metrics \> BU → Outdoor
- BL \<= Metrics \<= BU → Hybrid.

Limits (lower and upper, LL and LU): values which are used to calculate Boundaries. Limits are stored on collars internally, and they are reported to Twin. At the moment (as of 20 Oct 2021 ) BE doesn't handle these Limits in Twin.

In currently existing FW next formulas are used:

- BL = LL + (LU - LL) * 0.4
- BU = LL + (LU - LL) * 0.6, or = LU - (LU - LL) * 0.4

This is the same as

- BL = 0.6 * LL + 0.4 * LU
- BU = 0.4 * LL + 0.6 * LU

# Problem

We need to allow a user to tweak Boundaries using the slider, so that the mobile app can calculate hypothetic GPS Status instantly without saving these Boundaries on the collar and getting real GPS Status.

On the other hand the mobile app needs to save Limits on the collar instead of Boundaries (as the collar operates 'limits' parameter). It means that the mobile app needs to calculate Limits based on Boundaries chosen by the user. If we do this, we will have to update the algorithm every time it's changed on FW side (i.e. 40/60 ratio).

# Solution (and main implementation notes)

1. "Manual GPS calibration" feature should be supported only by**new FW**.
  1. Note: Mobile app will tell usersthey must update collar FW in case it doesn't support Boundaries only (seeME03-US64-US03).

2. It's required to create a new FW version which will use Boundaries directly and which will allow to save Boundaries got from BE (see[HALO-7880](https://jira.softeq.com/browse/HALO-7880?src=confmacro)-FW: Manual GPS calibration (improved logic for Indoor/Outdoor determination)Closed).
  1. FW also needs Limits, they should not be removed. FW uses limits to definitely define that the collar is outdoor/ indoor even when the collar is not moving around, i.e. when the collar reaches limits, it's clear that the collar is outdoor/ indoor.

3. Mobile app will send these Boundaries to the collar and get them from the collar**via BE**(not to/ from the collar directlyvia BLE) asBE must be source of trust.
4. Mobile app will only know about Boundaries (not Limits): download them from BE, show them to user and allow him/ her to change them, and then send Boundaries to BE.
  1. In order to show currently used Boundaries on the slider, the app should use the values provided by BE and display them**without additional calculations**.

5. BE saves new Boundaries in the desired TWIN,so that the collar can restore these values after formatting.
  1. When a collar needs values to be re-synchronized after resetting, then is should happen via Configuration Session sync with C2D direct method for setting values instead of putting raw numbers to desired TWIN section.

6. BE should include "Manual GPS calibration" settings into a part of Configuration Sync process, so they'll have a relevant status whether the changes are synchronized with the collar or not.
  1. Existing Configuration Sync Status will be used for this feature;**no need in splitting it**for "manual GPS calibration"*(so it's OK if the GPS settings are already synchronized, and when the user changes settings for pet mode, "synchronizing" status will be displayed for GPS settings as well)*.

7. BE can have**no**Current Boundaries (e.g. when BE didn't get the latest Boundaries from the collar and didn't save it to database).
  1. When a user defines new Boundaries in the app, Current Boundaries are initialized by these values sent by the user - BE doesn't wait until it gets Boundaries from the Reported Twin.

8. FW will calculate Limits itself based on the received Boundaries (so if the math is changed, then we need to only update FW). We need to have this logic in one place, the collar can now update its own limits, so it's better to have this calculation logic on FW,**not**BE.
  1. If we have a new formula in the future, it'll just depend on what version of FW you're running.

9. FW will send all 4 parameters to the reported TWIN:
  1. Limitsof automatic calibration;
  2. Boundaries of manual calibration.

10. Automatic calibration mechanism (a comment from Michael): the new one that's now in testing is not effective.We MAY want to leave the other 'walk-around' method, but I tend to think we should remove it.


