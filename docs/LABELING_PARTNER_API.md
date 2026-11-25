# Labeling partner API (Treat Therapeutics)

Treat Therapeutics recruits and manages labelers for Halo. Treat can see labeling progress
for **its own participants only**: Halo lists each participant's email, and every response
is built only from sessions sent from those emails. Treat cannot add participants itself.

## For Halo admins

Labeling data → **Partners** tab:

- **Participants**: the email each Treat participant labels from, one per line. Someone
  listed before they send anything shows with zero minutes.
- **Staff logins**: Treat staff emails. They request a login link on the normal login page
  and see only the Treat participants page. Removing an email ends their access on their
  next request.
- **API keys**: **Create key** shows the key once; send it to Treat securely. Halo stores
  only a hash. The trash icon revokes a key at once.
- **What Treat Therapeutics sees** previews the exact page Treat staff get.

The config is in S3 at `labeling-jobs/partners.json`. Partner orgs are defined in code
(`PARTNER_ORGS` in `backend/services/labeling_partner_service.py`).

## For Treat: using the API

Base URL: `https://<halo dashboard host>/api/partner/v1`

Send the key on every request, either way:

```
Authorization: Bearer hlp_treat_...
X-API-Key: hlp_treat_...
```

Every endpoint takes optional `start` and `end` (`YYYY-MM-DD`, inclusive) on the day the
session was recorded. Leave both out for all time. Minutes are rounded to 0.01.

Data refreshes through the day as Halo processes new uploads; `data_as_of` says when the
numbers were built.

### `GET /participants`

Every participant, with minutes per label against the target of 3 minutes per label.

```json
{
  "organization": "Treat Therapeutics",
  "start": null, "end": null, "data_as_of": "2026-11-25T15:04:00Z",
  "target_minutes_per_label": 3.0,
  "labels": [{"key": "Lying", "name": "Lying", "group": "posture"}, "..."],
  "participants": [{
    "email": "ana@example.com", "name": "Ana", "dogs": ["Rex"],
    "sessions": 12, "minutes": 41.5, "days_active": 5,
    "first_contribution": "2026-11-10", "last_contribution": "2026-11-24",
    "labels_done": 9, "labels_total": 17,
    "labels": {"Lying": {"minutes": 4.2, "remaining_minutes": 0.0, "done": true}, "...": {}},
    "other_labels": {"Sedentary": 0.8}
  }]
}
```

`labels` covers the 17 target labels (12 postures, 5 indoor/outdoor environments).
Spelling variants are combined (Potty1, Potty2 and PottyTwo count as Potty). Labels outside
the 17 are in `other_labels`.

### `GET /participants/{email}/daily`

Each day the participant sent sessions, with minutes per label.

```json
{"email": "ana@example.com",
 "days": [{"date": "2026-11-12", "minutes": 6.2, "sessions": 2,
           "labels": {"Lying": 1.5, "OutdoorOpenSky": 0.5}}]}
```

### `GET /participants/{email}/sessions`

Every session, newest first.

```json
{"email": "ana@example.com",
 "sessions": [{"session_id": "2026-11-12T11:00:00_0", "started_at": "2026-11-12T11:00:00",
               "date": "2026-11-12", "model": "indoor_outdoor", "dog": "Rex",
               "collar_sn": "24h...", "minutes": 0.5, "labels": {"OutdoorOpenSky": 0.5}}]}
```

`model` is `activity` (postures) or `indoor_outdoor` (environments).

### `GET /me`

Which organization the key belongs to and how many participants are listed.

### Errors

| Status | Meaning |
| --- | --- |
| 400 | `start`/`end` not `YYYY-MM-DD`, or start after end |
| 401 | Missing, wrong or revoked key |
| 404 | Email isn't one of your participants |
| 503 | Stats are loading after a restart; retry in a minute |

### Example

```bash
curl -H "Authorization: Bearer $HALO_KEY" \
  "https://<halo dashboard host>/api/partner/v1/participants?start=2026-11-01"
```
