# Zoom Chat Scopes Setup Guide

## Problem
The Zoom API endpoint `/im/chat/sessions` is requesting IM Chat scopes (`imchat:read`, `imchat:read:admin`), but these scopes are **no longer available** in Zoom Marketplace. Zoom has deprecated IM Chat API in favor of Team Chat API.

## Solution: Enable Team Chat Scopes

**IM Chat scopes don't exist anymore** - you need to use Team Chat scopes instead.

### Step-by-Step Instructions

1. **Go to Zoom Marketplace**
   - Navigate to: https://marketplace.zoom.us/
   - Sign in with your Zoom account

2. **Access Your Server-to-Server OAuth App**
   - Click on "Manage" → "Created Apps" (or go directly to your app)
   - Find your Server-to-Server OAuth app
   - Click on it to edit

3. **Navigate to Scopes Section**
   - In your app settings, find the "Scopes" or "Permissions" tab
   - This is where you enable API permissions

4. **Find Team Chat Scopes**
   - Look for the **"Team Chat"** category (NOT "IM Chat" - that doesn't exist)
   - Enable these scopes:
     - **chat_message:read:admin** - Read chat messages (Admin)
     - **team_chat:read:list_user_messages:admin** - List user messages (Admin)
     - **team_chat:read:user_message:admin** - Read user messages (Admin)
     - **team_chat:read:list_user_sessions:admin** - List user chat sessions (Admin)

5. **Enable the Required Scopes**
   - Check the boxes next to the Team Chat scopes listed above
   - Enable as many Team Chat read scopes as you see available

6. **Save and Activate**
   - Click "Save" or "Update"
   - If your app needs to be activated/reactivated, do so
   - Wait 2-3 minutes for changes to propagate

## Understanding the Situation

### IM Chat API Deprecation

- **IM Chat API** (`/im/chat/*` endpoints):
  - **DEPRECATED** - No longer supported by Zoom
  - Scopes (`imchat:read`, `imchat:read:admin`) are no longer available in Marketplace
  - The endpoints may still exist but require Team Chat scopes

- **Team Chat API** (`/chat/*` endpoints):
  - **Current/Active** - This is what Zoom now uses
  - Requires scopes: `team_chat:read:*`, `chat_message:read:admin`
  - May work with IM Chat endpoints if you have Team Chat scopes enabled

### What to Try

1. **First**: Enable Team Chat scopes (see instructions above) and try the download again
2. **If that doesn't work**: We may need to migrate the code to use Team Chat endpoints instead of IM Chat endpoints

## Verification

After enabling the scopes:

1. Wait 2-3 minutes for the changes to take effect
2. Try the download again from the frontend
3. Check the logs - you should no longer see the scope error

## Troubleshooting

If you still see scope errors after enabling:

1. **Verify the scopes are saved**: Go back to your app settings and confirm both `imchat:read` and `imchat:read:admin` are checked
2. **Check app status**: Make sure your app is "Active" or "Published"
3. **Wait longer**: Sometimes it takes 5-10 minutes for scope changes to propagate
4. **Re-authenticate**: The access token might be cached - wait for it to expire (usually 1 hour) or restart the application

## API Reference

- Zoom IM Chat API: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/IM-Chat
- Endpoint used: `GET /im/chat/sessions`
- Required scopes: `imchat:read`, `imchat:read:admin`

