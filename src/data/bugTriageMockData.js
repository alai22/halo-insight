/**
 * Mock bug/issues data for Bug Triage Copilot prototype.
 * No Jira dependency; used for UX and triage flow only.
 */

export const PLATFORMS = ['iOS', 'Android', 'Backend', 'Other'];
export const COMPONENTS = ['Auth', 'Payments', 'Onboarding', 'Sync', 'UI', 'API', 'Notifications', 'Search'];
export const NEXT_ACTIONS = ['Fix now', 'Investigate', 'Merge', 'Close', 'Post-GA'];
export const CONFIDENCE_LEVELS = ['Low', 'Med', 'High'];

/**
 * @typedef {Object} AIRecommendation
 * @property {string} category
 * @property {string} component
 * @property {string} priority
 * @property {boolean} gaBlocker
 * @property {string} confidence - 'Low' | 'Med' | 'High'
 * @property {string} rationale
 * @property {string} suggestedNextAction
 * @property {string[]} [duplicateCandidates] - issue keys
 */

/**
 * @typedef {Object} MockBugIssue
 * @property {string} id
 * @property {string} key
 * @property {string} title
 * @property {string} created
 * @property {string} updated
 * @property {string} [description]
 * @property {string[]} [reproSteps]
 * @property {string} [expectedVsActual]
 * @property {'iOS'|'Android'|'Backend'|'Other'} platform
 * @property {string} component
 * @property {string} [appVersion]
 * @property {string[]} [labels]
 * @property {string} [severity]
 * @property {string} [customerImpact]
 * @property {string} [crashSnippet]
 * @property {{ author: string, body: string, created: string }[]} [comments]
 * @property {string[]} [relatedIssueIds]
 * @property {string} [clusterId]
 * @property {string} [clusterLabel]
 * @property {boolean} needsMoreInfo
 * @property {boolean} gaBlocker
 * @property {number} [rank] - mock triage score (higher = more urgent)
 * @property {AIRecommendation} aiRecommendation
 */

const now = new Date();
const day = (d) => new Date(now.getTime() - d * 24 * 60 * 60 * 1000).toISOString();

/** @type {MockBugIssue[]} */
export const mockBugIssues = [
  {
    id: '1',
    key: 'PROJ-101',
    title: 'App crashes on login when 2FA is enabled',
    created: day(2),
    updated: day(0),
    description: 'Users with 2FA enabled experience a crash immediately after entering the verification code.',
    reproSteps: ['Enable 2FA in account settings', 'Log out', 'Log in and enter 2FA code', 'App crashes'],
    expectedVsActual: 'Expected: successful login. Actual: crash to home screen.',
    platform: 'iOS',
    component: 'Auth',
    appVersion: '4.2.1',
    labels: ['crash', 'auth', 'ios'],
    severity: 'Critical',
    customerImpact: 'Blocks all 2FA users on iOS from logging in.',
    crashSnippet: 'EXC_BAD_ACCESS in AuthService.validate2FA at line 142',
    comments: [
      { author: 'QA', body: 'Reproduced on iOS 17.1 and 17.2', created: day(1) }
    ],
    relatedIssueIds: ['2'],
    clusterId: 'auth-2fa',
    clusterLabel: 'Auth 2FA flow',
    needsMoreInfo: false,
    gaBlocker: true,
    rank: 92,
    aiRecommendation: {
      category: 'Bug',
      component: 'Auth',
      priority: 'P0',
      gaBlocker: true,
      confidence: 'High',
      rationale: 'Based on crash logs and severity: affects all 2FA users on iOS. Critical path for GA.',
      suggestedNextAction: 'Fix now',
      duplicateCandidates: ['PROJ-102']
    }
  },
  {
    id: '2',
    key: 'PROJ-102',
    title: '2FA verification fails silently on Android',
    created: day(3),
    updated: day(1),
    description: 'After entering 2FA code on Android, request hangs and then fails without error message.',
    reproSteps: ['Enable 2FA', 'Log in on Android', 'Enter code', 'Spinner never completes'],
    platform: 'Android',
    component: 'Auth',
    appVersion: '4.2.0',
    labels: ['auth', 'android'],
    severity: 'High',
    customerImpact: 'Users cannot complete login on Android with 2FA.',
    clusterId: 'auth-2fa',
    clusterLabel: 'Auth 2FA flow',
    needsMoreInfo: true,
    gaBlocker: true,
    rank: 88,
    aiRecommendation: {
      category: 'Bug',
      component: 'Auth',
      priority: 'P0',
      gaBlocker: true,
      confidence: 'Med',
      rationale: 'Same auth flow as PROJ-101; likely related. Needs more info on network/timeout.',
      suggestedNextAction: 'Investigate',
      duplicateCandidates: ['PROJ-101']
    }
  },
  {
    id: '3',
    key: 'PROJ-103',
    title: 'Payment fails for subscription renewal',
    created: day(5),
    updated: day(2),
    description: 'Subscription renewal charge fails with "Payment method declined" for valid cards.',
    reproSteps: ['Have active subscription', 'Wait for renewal or trigger manually', 'Charge fails'],
    expectedVsActual: 'Expected: renewal succeeds. Actual: generic decline error.',
    platform: 'Backend',
    component: 'Payments',
    labels: ['payments', 'subscription'],
    severity: 'Critical',
    customerImpact: 'Revenue impact; subscribers lose access.',
    comments: [
      { author: 'Support', body: 'Seen for Stripe customers in EU', created: day(3) },
      { author: 'Eng', body: 'Checking Stripe webhook handling', created: day(2) }
    ],
    clusterId: 'pay-renewal',
    clusterLabel: 'Payment renewal',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 85,
    aiRecommendation: {
      category: 'Bug',
      component: 'Payments',
      priority: 'P0',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on customer impact and frequency. Not GA blocker per release criteria.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '4',
    key: 'PROJ-104',
    title: 'Onboarding screen layout broken on small phones',
    created: day(7),
    updated: day(4),
    description: 'Step 2 of onboarding overlaps buttons on devices with width < 375pt.',
    reproSteps: ['Fresh install', 'Start onboarding', 'Navigate to step 2', 'Observe layout'],
    platform: 'iOS',
    component: 'Onboarding',
    appVersion: '4.2.1',
    labels: ['ui', 'onboarding'],
    severity: 'Medium',
    customerImpact: 'Poor first impression; users may abandon.',
    clusterId: 'onboard-ui',
    clusterLabel: 'Onboarding UI',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 52,
    aiRecommendation: {
      category: 'Bug',
      component: 'Onboarding',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'UI-only; affected platform and component clear from description.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '5',
    key: 'PROJ-105',
    title: 'Sync stops after 1000 items',
    created: day(10),
    updated: day(6),
    description: 'Background sync stops processing after 1000 items with no error.',
    reproSteps: ['Account with >1000 items', 'Trigger full sync', 'Check progress'],
    platform: 'Backend',
    component: 'Sync',
    labels: ['sync', 'backend'],
    severity: 'High',
    customerImpact: 'Large accounts never get full sync.',
    needsMoreInfo: true,
    gaBlocker: false,
    rank: 78,
    aiRecommendation: {
      category: 'Bug',
      component: 'Sync',
      priority: 'P1',
      gaBlocker: false,
      confidence: 'Med',
      rationale: 'Based on affected platform and customer impact. Needs more info on repro.',
      suggestedNextAction: 'Investigate'
    }
  },
  {
    id: '6',
    key: 'PROJ-106',
    title: 'Push notifications not received on Android 14',
    created: day(1),
    updated: day(0),
    description: 'Users on Android 14 do not receive push notifications after app restart.',
    reproSteps: ['Android 14 device', 'Grant notification permission', 'Kill app', 'Send push'],
    platform: 'Android',
    component: 'Notifications',
    appVersion: '4.2.1',
    labels: ['notifications', 'android'],
    severity: 'High',
    customerImpact: 'Critical for engagement on Android.',
    crashSnippet: null,
    clusterId: 'notif-android',
    clusterLabel: 'Android notifications',
    needsMoreInfo: false,
    gaBlocker: true,
    rank: 90,
    aiRecommendation: {
      category: 'Bug',
      component: 'Notifications',
      priority: 'P0',
      gaBlocker: true,
      confidence: 'High',
      rationale: 'Android 14 is target platform; notification delivery is GA blocker per product.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '7',
    key: 'PROJ-107',
    title: 'Search returns no results for special characters',
    created: day(4),
    updated: day(2),
    description: 'Search query with & or " returns empty results.',
    reproSteps: ['Go to search', 'Enter "test & demo"', 'No results'],
    platform: 'Backend',
    component: 'Search',
    severity: 'Medium',
    customerImpact: 'Users with special chars in content cannot find items.',
    clusterId: 'search-query',
    clusterLabel: 'Search query parsing',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 55,
    aiRecommendation: {
      category: 'Bug',
      component: 'Search',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on component and description; likely escaping/encoding.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '8',
    key: 'PROJ-108',
    title: 'API 500 on bulk export',
    created: day(6),
    updated: day(3),
    description: 'POST /export with large payload returns 500 after ~30s.',
    reproSteps: ['Call export API with 5k items', 'Observe 500'],
    platform: 'Backend',
    component: 'API',
    severity: 'High',
    customerImpact: 'Integrations and internal tools blocked.',
    needsMoreInfo: true,
    gaBlocker: false,
    rank: 70,
    aiRecommendation: {
      category: 'Bug',
      component: 'API',
      priority: 'P1',
      gaBlocker: false,
      confidence: 'Med',
      rationale: 'Based on crash logs and frequency. Needs more info on payload size limits.',
      suggestedNextAction: 'Investigate'
    }
  },
  {
    id: '9',
    key: 'PROJ-109',
    title: 'Dark mode contrast fails accessibility',
    created: day(12),
    updated: day(8),
    description: 'Secondary text in dark mode does not meet WCAG contrast ratio.',
    reproSteps: ['Enable dark mode', 'Open Settings screen', 'Check secondary text'],
    platform: 'iOS',
    component: 'UI',
    labels: ['ui', 'a11y'],
    severity: 'Medium',
    customerImpact: 'Accessibility compliance.',
    clusterId: 'ui-theme',
    clusterLabel: 'Theme / UI',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 45,
    aiRecommendation: {
      category: 'Bug',
      component: 'UI',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on component and labels. Not GA blocker.',
      suggestedNextAction: 'Post-GA'
    }
  },
  {
    id: '10',
    key: 'PROJ-110',
    title: 'Duplicate events sent to analytics',
    created: day(8),
    updated: day(5),
    description: 'Same event fires 2–3 times per user action in some flows.',
    reproSteps: ['Enable analytics debug', 'Perform checkout', 'Observe duplicate events'],
    platform: 'Other',
    component: 'API',
    severity: 'Low',
    customerImpact: 'Inflated metrics; possible billing impact.',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 38,
    aiRecommendation: {
      category: 'Bug',
      component: 'API',
      priority: 'P3',
      gaBlocker: false,
      confidence: 'Low',
      rationale: 'Impact is analytics-only; suggested Post-GA.',
      suggestedNextAction: 'Post-GA'
    }
  },
  {
    id: '11',
    key: 'PROJ-111',
    title: 'Login screen flashes white on cold start',
    created: day(14),
    updated: day(10),
    description: 'Brief white flash before theme is applied on app launch.',
    reproSteps: ['Kill app', 'Launch app', 'Observe flash'],
    platform: 'Android',
    component: 'UI',
    severity: 'Low',
    customerImpact: 'Cosmetic.',
    clusterId: 'ui-theme',
    clusterLabel: 'Theme / UI',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 28,
    aiRecommendation: {
      category: 'Bug',
      component: 'UI',
      priority: 'P3',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'UI-only, low severity. Post-GA.',
      suggestedNextAction: 'Post-GA'
    }
  },
  {
    id: '12',
    key: 'PROJ-112',
    title: 'Webhook retries exhaust rate limit',
    created: day(3),
    updated: day(1),
    description: 'Failed webhook retries cause 429 and block other API traffic.',
    platform: 'Backend',
    component: 'API',
    severity: 'High',
    customerImpact: 'Partners see failures during our retry storms.',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 72,
    aiRecommendation: {
      category: 'Bug',
      component: 'API',
      priority: 'P1',
      gaBlocker: false,
      confidence: 'Med',
      rationale: 'Based on platform and customer impact.',
      suggestedNextAction: 'Investigate'
    }
  },
  {
    id: '13',
    key: 'PROJ-113',
    title: 'Password reset email not received',
    created: day(2),
    updated: day(0),
    description: 'Users report not receiving password reset email (Gmail).',
    reproSteps: ['Request password reset', 'Check Gmail', 'No email'],
    platform: 'Backend',
    component: 'Auth',
    severity: 'Critical',
    customerImpact: 'Users locked out of accounts.',
    comments: [{ author: 'Support', body: 'Only Gmail so far', created: day(1) }],
    needsMoreInfo: true,
    gaBlocker: true,
    rank: 86,
    aiRecommendation: {
      category: 'Bug',
      component: 'Auth',
      priority: 'P0',
      gaBlocker: true,
      confidence: 'High',
      rationale: 'Auth flow critical; affects account recovery. GA blocker.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '14',
    key: 'PROJ-114',
    title: 'In-app purchase restore fails on iOS',
    created: day(5),
    updated: day(3),
    description: 'Restore purchases button does nothing on first tap.',
    reproSteps: ['Reinstall app', 'Tap Restore purchases', 'Nothing happens'],
    platform: 'iOS',
    component: 'Payments',
    severity: 'High',
    customerImpact: 'Users who reinstall lose access to paid content.',
    clusterId: 'pay-renewal',
    clusterLabel: 'Payment renewal',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 75,
    aiRecommendation: {
      category: 'Bug',
      component: 'Payments',
      priority: 'P1',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on platform and component; revenue impact.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '15',
    key: 'PROJ-115',
    title: 'Offline queue never drains after reconnect',
    created: day(9),
    updated: day(6),
    description: 'After going offline and back online, queued actions are not sent.',
    platform: 'Android',
    component: 'Sync',
    severity: 'High',
    customerImpact: 'Data loss perception; stale state.',
    needsMoreInfo: true,
    gaBlocker: false,
    rank: 68,
    aiRecommendation: {
      category: 'Bug',
      component: 'Sync',
      priority: 'P1',
      gaBlocker: false,
      confidence: 'Med',
      rationale: 'Based on component; needs more info on repro.',
      suggestedNextAction: 'Investigate'
    }
  },
  {
    id: '16',
    key: 'PROJ-116',
    title: 'Notification tap opens wrong screen',
    created: day(4),
    updated: day(2),
    description: 'Deep link from notification opens Settings instead of the item.',
    reproSteps: ['Receive notification', 'Tap notification', 'Wrong screen opens'],
    platform: 'Android',
    component: 'Notifications',
    severity: 'Medium',
    clusterId: 'notif-android',
    clusterLabel: 'Android notifications',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 58,
    aiRecommendation: {
      category: 'Bug',
      component: 'Notifications',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on component and platform.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '17',
    key: 'PROJ-117',
    title: 'Search filters reset on sort change',
    created: day(11),
    updated: day(7),
    description: 'Changing sort order clears selected filters.',
    reproSteps: ['Apply filters', 'Change sort', 'Filters reset'],
    platform: 'Backend',
    component: 'Search',
    severity: 'Medium',
    clusterId: 'search-query',
    clusterLabel: 'Search query parsing',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 48,
    aiRecommendation: {
      category: 'Bug',
      component: 'Search',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on component.',
      suggestedNextAction: 'Post-GA'
    }
  },
  {
    id: '18',
    key: 'PROJ-118',
    title: 'OAuth redirect_uri mismatch in sandbox',
    created: day(6),
    updated: day(4),
    description: 'Sandbox OAuth config rejects valid redirect URIs.',
    platform: 'Backend',
    component: 'Auth',
    severity: 'Medium',
    customerImpact: 'Developers cannot test integrations.',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 62,
    aiRecommendation: {
      category: 'Bug',
      component: 'Auth',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Auth component; sandbox-only reduces urgency.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '19',
    key: 'PROJ-119',
    title: 'Onboarding skip not persisted',
    created: day(8),
    updated: day(5),
    description: 'Skipping onboarding still shows tips on next launch.',
    platform: 'iOS',
    component: 'Onboarding',
    clusterId: 'onboard-ui',
    clusterLabel: 'Onboarding UI',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 50,
    aiRecommendation: {
      category: 'Bug',
      component: 'Onboarding',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on component and description.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '20',
    key: 'PROJ-120',
    title: 'API returns 403 for valid scope',
    created: day(1),
    updated: day(0),
    description: 'Endpoint /v2/me returns 403 for token with user:read scope.',
    platform: 'Backend',
    component: 'API',
    severity: 'Critical',
    customerImpact: 'Third-party apps cannot fetch user profile.',
    needsMoreInfo: false,
    gaBlocker: true,
    rank: 84,
    aiRecommendation: {
      category: 'Bug',
      component: 'API',
      priority: 'P0',
      gaBlocker: true,
      confidence: 'High',
      rationale: 'Based on severity and customer impact. API contract broken.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '21',
    key: 'PROJ-121',
    title: 'Payments screen shows wrong currency',
    created: day(13),
    updated: day(9),
    description: 'After switching region, currency symbol updates but amounts stay in previous currency.',
    platform: 'iOS',
    component: 'Payments',
    severity: 'Medium',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 56,
    aiRecommendation: {
      category: 'Bug',
      component: 'Payments',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'Med',
      rationale: 'Based on component; could cause billing confusion.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '22',
    key: 'PROJ-122',
    title: 'Sync conflict resolution overwrites local changes',
    created: day(7),
    updated: day(4),
    description: 'When conflict occurs, server wins and local edits are lost without warning.',
    platform: 'Backend',
    component: 'Sync',
    severity: 'High',
    customerImpact: 'Data loss.',
    needsMoreInfo: true,
    gaBlocker: false,
    rank: 80,
    aiRecommendation: {
      category: 'Bug',
      component: 'Sync',
      priority: 'P1',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on severity and customer impact. Needs more info on frequency.',
      suggestedNextAction: 'Investigate'
    }
  },
  {
    id: '23',
    key: 'PROJ-123',
    title: 'Notification permission prompt never shown',
    created: day(3),
    updated: day(1),
    description: 'On first launch, iOS never shows the notification permission dialog.',
    platform: 'iOS',
    component: 'Notifications',
    severity: 'High',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 74,
    aiRecommendation: {
      category: 'Bug',
      component: 'Notifications',
      priority: 'P1',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on platform and component; affects opt-in rate.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '24',
    key: 'PROJ-124',
    title: 'Search autocomplete suggests deleted items',
    created: day(10),
    updated: day(6),
    description: 'Autocomplete returns items that were deleted minutes ago.',
    platform: 'Backend',
    component: 'Search',
    severity: 'Medium',
    clusterId: 'search-query',
    clusterLabel: 'Search query parsing',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 52,
    aiRecommendation: {
      category: 'Bug',
      component: 'Search',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'Med',
      rationale: 'Based on component; likely cache invalidation.',
      suggestedNextAction: 'Investigate'
    }
  },
  {
    id: '25',
    key: 'PROJ-125',
    title: 'Settings screen crash on rotate',
    created: day(15),
    updated: day(11),
    description: 'App crashes when rotating device on Settings > Account.',
    reproSteps: ['Open Settings', 'Account', 'Rotate device', 'Crash'],
    platform: 'Android',
    component: 'UI',
    severity: 'Medium',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 54,
    aiRecommendation: {
      category: 'Bug',
      component: 'UI',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on crash and platform.',
      suggestedNextAction: 'Fix now'
    }
  },
  {
    id: '26',
    key: 'PROJ-126',
    title: 'Duplicate of PROJ-101 (different reporter)',
    created: day(1),
    updated: day(0),
    description: 'Same as PROJ-101: crash on 2FA login.',
    platform: 'iOS',
    component: 'Auth',
    severity: 'Critical',
    clusterId: 'auth-2fa',
    clusterLabel: 'Auth 2FA flow',
    relatedIssueIds: ['1'],
    needsMoreInfo: false,
    gaBlocker: true,
    rank: 91,
    aiRecommendation: {
      category: 'Bug',
      component: 'Auth',
      priority: 'P0',
      gaBlocker: true,
      confidence: 'High',
      rationale: 'Duplicate of PROJ-101 based on description and cluster.',
      suggestedNextAction: 'Merge',
      duplicateCandidates: ['PROJ-101']
    }
  },
  {
    id: '27',
    key: 'PROJ-127',
    title: 'Logout does not clear session on API',
    created: day(4),
    updated: day(2),
    description: 'After logout, some API calls still succeed with old token for a short window.',
    platform: 'Backend',
    component: 'Auth',
    severity: 'High',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 76,
    aiRecommendation: {
      category: 'Bug',
      component: 'Auth',
      priority: 'P1',
      gaBlocker: false,
      confidence: 'Med',
      rationale: 'Based on component and security impact.',
      suggestedNextAction: 'Investigate'
    }
  },
  {
    id: '28',
    key: 'PROJ-128',
    title: 'In-app message dismissed reappears',
    created: day(12),
    updated: day(8),
    description: 'Dismissing the promo banner brings it back after app background/foreground.',
    platform: 'Other',
    component: 'UI',
    severity: 'Low',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 32,
    aiRecommendation: {
      category: 'Bug',
      component: 'UI',
      priority: 'P3',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Low severity; cosmetic.',
      suggestedNextAction: 'Post-GA'
    }
  },
  {
    id: '29',
    key: 'PROJ-129',
    title: 'Webhook signature verification fails with padding',
    created: day(5),
    updated: day(3),
    description: 'Some webhooks fail verification when payload has trailing newline.',
    platform: 'Backend',
    component: 'API',
    severity: 'Medium',
    needsMoreInfo: true,
    gaBlocker: false,
    rank: 60,
    aiRecommendation: {
      category: 'Bug',
      component: 'API',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'Low',
      rationale: 'Needs more info on which senders. API component.',
      suggestedNextAction: 'Investigate'
    }
  },
  {
    id: '30',
    key: 'PROJ-130',
    title: 'Onboarding video does not play on slow network',
    created: day(9),
    updated: day(5),
    description: 'Video stays loading indefinitely on 3G.',
    platform: 'iOS',
    component: 'Onboarding',
    severity: 'Medium',
    clusterId: 'onboard-ui',
    clusterLabel: 'Onboarding UI',
    needsMoreInfo: false,
    gaBlocker: false,
    rank: 46,
    aiRecommendation: {
      category: 'Bug',
      component: 'Onboarding',
      priority: 'P2',
      gaBlocker: false,
      confidence: 'High',
      rationale: 'Based on component and platform. First-run experience.',
      suggestedNextAction: 'Fix now'
    }
  }
];
