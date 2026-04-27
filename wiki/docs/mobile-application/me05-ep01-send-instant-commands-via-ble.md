---
title: "ME05-EP01 Send instant commands via BLE"
sidebar_label: "ME05-EP01 Send instant commands via BLE"
sidebar_position: 677
last_modified: "Apr 04, 2020"
author: "Nicolay Gavrilov"
---

| Document status | Document owners |
|---|---|
| APPROVED |
| Nicolay Gavrilov, Pavel Leonenko |General Description PoC To be defined Results of investigation MVP Solution Background scanning (or simply Scanning) Preliminary pairing Sending command Other Additional improvements (not included in the MVP scope)

# General Description

At the moment sending instant commands via LTE in the US takes too long (1 - 2 sec). This is not acceptable, both from the perspective of dog training (a dog will not understand why it is being corrected if there will be 1-2 seconds delay) and from the perspective pet safety (the dog may reach the dangerous/forbidden zone before the correction is being sent to the collar). To minimize the time between tapping on the correction button on the smartphone and applying the correction on the collar we need to send the corrections via BLE. At that, we may not solely rely on the BLE channel because it also has certain restrictions (the quality of BLE connection depends on the distance, obstacles, RF-interference etc.). Therefore the corrections should be sent via BLE and the internet in parallel. This approach leads to another problem: the collar should not apply a single correction twice. To avoid this, we may add ID (timestamp) to all corrections sent to the collar. The device should ignore a correction if it has a record of applied correction with the same ID.

# PoC

Click here to expand...## To be defined

- **Ensure that collars will be connected to the smartphone fast enough.**We most likely need a separate investigation/POC phase to make sure collars can connect to a smartphone quickly.
It may appear that it takes too long. As a result, we might need to rework the whole Collar - Smartphone BLE connection approach so as to maintain the constant BLE connection with the collars when they are in the range of smartphone Bluetooth.
- **Sending corrections in offline considering the current BLE security approach**(caching RC). This will mean that we'll have a limited number of instant commands for the offline state. After all the cached RC's are used the collar will stop accepting instant commands until it will go online again.
- **Instant commands for all pets via BLE.**Should we handle running instant commands for all pets (ME05-US24 Run instant command for all pets) via BLE? Or will it be OK to use only Wi-Fi/LTE channels for this case?
- **Returning errors via BLE.**Do we need to return errors via the BLE channel? E.g. for the case when commands are sent in the absence of internet connection on either the collar or smartphone?
- **Forbidding users to send too many corrections in the absence of the internet connection.**At the moment this is handled on BE side. But once we introduce an additional channel to deliver the corrections we might need to handle the problem with sending too many corrections on collar side for the situations when BE will be unavailable (no internet connection).

## Results of investigation

These results were gathered in good conditions: no other BLE/Wi-Fi devices around, no hindrances between the collar and the phone such as bushes, trees, etc., the distance between the collar and the phone was less than 2 meters.

Results can be not that good in worse conditions.

- If the app has not yet been paired with a collar since its startup, pairing will take much more than 1-2 seconds.
- If the app has already paired to a collar and remembered its advertising data, all future pairings will take about 0.55 second until the app is relaunched/shut down, sometimes more.
- Reading/writing a char for the first time after pairing takes about 1 second, sometimes more.
- All subsequent operations on chars are applied almost immediately - about 60 milliseconds.

# MVP Solution

Given that the very first pairing always takes too long we should perform it before user tries to apply an Instant Command. So in general the solution has three parts:

- **Background scanning:**the app tries to find all pets' collars and remember their advertising packages, so that it can connect to them quicker when needed.
- **Preliminary pairing:**the app starts connecting to and unlocking the collar as soon as the user opens Instant Command Card, so when the user fires the command, it can be sent almost immediately.
- **Sending command**:the command is sent via BLE if possible or via IoT Hub if not.

Here are more details on these points.

## Background scanning (or simply Scanning)

Background scanning means that:

- the app scans in background for all the collars which are assigned to pets and haven't been discovered yet since the app launch;
- and remembers advertising packages of discovered collars.

For MVP version Scanning is started as soon as we get all pets' collars, and it ends only when all these collars are discovered. Scanning is paused in cases when the app begins to scan for other set of devices in foreground: e.g. in adding collar flow, or Wi-Fi setup flow, or choosing a collar for fence creation, etc.

Later we can think of improving Scanning process. Here are some of options:

- Perform Scanning only while Pet Card is opened,
- Or perform not all the time but by intervals - this will decrease battery usage (see point 1 of Additional Improvements section below).

Q: Does that mean that Bluetooth permission will be requested on My Map?

A: For MVP - yes, if the user installs the app and logs in the account with already created pets with collars. Later we can delay Bluetooth permission prompting (see point 4 of Additional Improvements section below).

## Preliminary pairing

Preliminary pairing means that the app connects to a collar and unlocks it.

It is done as soon as the user opens Instant Command Card. It can be performed only for collars which have already been discovered by Background scanning. Otherwise the app does not pair with the collar on Instant Command Card opening.

The app disconnects from the collar when the user closes Instant Command Card. Thus we will need to perform Preliminary pairing again later.

## Sending command

Sending command over BLE is performed only if the app is paired to the collar AND the collar is unlocked. Otherwise, the command will be sent via the Internet.

The timeout for sending via BLE is 1 second. If for some reason the app could not send a command within 1 second, the app cancel sending the command over BLE and sends it over the Internet.

IoT Hub is used instantly if:

- Bluetooth is turned off;
- Background scanning has not yet discovered the collar we need;
- The collar is not unlocked, or the app is not paired with the collar.

BLE only is used if there is no internet connection.

In case there is no internet and BLE is off we show the M133 error.

In order to send a command via BLE,

- We subscribe to the Instant Command char (to be added on collar side) which notifies us about the result.
- After subscribing we write a command number to the Instant Command char.
- The Instant Command char should support Write and Notify, its length should be 1 byte for Write and 2 bytes for Notify.
- The Instant Command char should have command index (1-6) for Write;andcommand tran-code (a rotating 1-byte value - 0-255)+ command indexfor Notify response. The mechanism is similar to unlocking collar.

## Other

- Collar must add incoming commands to logs.

# Additional improvements (not included in the MVP scope)

1) Time intervals for background scanning (~ 2 SP). When the app is launched, it scans for the collar for only 30 seconds. If not all collars were discovered during this time, the scanning is performed 2 more times with 1 minute delay between attempts. Also we run the scanning in case a user tried to send a command to a collar which has not been found during these 3 initial scannings. MVP solution presumes that we'll scan without timeouts until we find all the collars. This may increase iPhone battery usage.

2) Caching all available devices which are found during foreground scanning (~ 2 SP). For MVP we will pause background scanning when foreground scanning is started - e.g. when user opens a list of collars to choose one to create fence using it. This feature will allow us to remember all devices found by this foreground scan and add them to the list of devices which have been remember during background scanning.

3) Allow discovering the newly added devices on the fly (~ 2 SP). This will allow us to add newly added collars as targets for background scanning as soon as we know that such collars has appeared. E.g. if a user assigned a collar to a pet on the device A, we will try to find this collar on the device B as soon as the app on the device B will receive this collar on My Map or on Collars List.

4) Delaying Bluetooth permission prompting (1-2 SP). This is to avoid asking for Bluetooth permission right after the first launch of the app on MyMap screen when the users has no collar added to the account.

5) Automatic retry for pairing errors (~ 1SP). In case Preliminary pairing fails, we retry this operation to increase a chance of using BLE for sending a command next time.

6) Automatic reconnecting if the collar disconnects after the pairing (~ 1SP). In case Preliminary pairing was successful but then the collar disconnected for some reason, we will try to reconnect to it and unlock it one more time.

7) Additional custom errors for the user (if needed). For MVP only one general error message will be shown if sending a command fails. We could customize it. Anyway we log any errors in MVP so that's not a must have.


