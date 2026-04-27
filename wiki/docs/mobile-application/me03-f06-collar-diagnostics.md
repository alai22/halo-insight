---
title: "ME03-F06. Collar Diagnostics"
sidebar_label: "ME03-F06. Collar Diagnostics"
sidebar_position: 627
last_modified: "Feb 04, 2025"
author: "Mariya Kolyada"
---

Existing App

- Collar Diagnostics screen should consist of the following sections:
  - Icon+Last scan status - ask Ryan
  - General information:
    - Collar Model
    - Collar Serial Number
    - Collar Color
    - Last scan data:
      - '\<time\> ago', where time value follows the rules BR-16
      - if last scan was more than 30 days ago - color it in red - ask Ryan

    - Overal Status:
      - TBD - ask Ryan

  - List of Collar Diagnostic Parameters + HW check status:
    - LTE
    - Wi-Fi
    - GPS
    - Compas - or Sensors?
    - Battery
    - Hardware

- HW check status:
  - Green circle + 'No issues' - if collar sent DailyDiagnostics AND corresponding parameter was normal
  - Orange circle + 'Issues Detected' - if collar sent DailyDiagnostics AND corresponding parameter has an issue
  - Red circle + 'Critical Issues Detected' - if collar sent DailyDiagnostics AND corresponding parameter has a catastrophic issue - ask Ryan if we need it

- App should hide the corresponding parameter in the List of Collar Diagnostic Parameters at all, if there is no Daily Diagnostics data for it.
- If the last scan was more than 30 days ago, the app should display:
  - Last scan status = 'No recent health data reported. Please, check your Halo's connectivity: use Halo Help to troubleshoot.'
    - Halo Help = https://cdn.solvvy.com/deflect/customization/halocollar/support.html?solvvyWF=1cb4c86a-7bd9-4c95-a498-5a63b84b7297
    - On Halo Help predefine question: Troubleshooting → Troubleshooting Guide.

  - Last scan data is colored in orange.
  - List of Collar Diagnostic Parameters is hidden.

- If there are some issues in the corresponding parameter of List of Collar Diagnostic Parameters, the the app should:
  - Display '\>' on the parameter.
  - Make the parameter tappable.
  - Display button Start Warranty Process?

- Action on Parameter tap - display pop-up explaining what kind of issue user has.
  - TBD


