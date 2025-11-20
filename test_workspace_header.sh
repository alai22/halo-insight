#!/bin/bash
# Test with workspace key in header or query parameter

API_KEY="YOUR_API_KEY_HERE"
WORKSPACE_KEY="YOUR_WORKSPACE_KEY_HERE"
BASE_URL="https://data-api.survicate.com/v2/"

echo "=== Testing Workspace Key in Different Locations ==="
echo ""

# Test 1: Workspace key in X-Workspace-Key header
if [ -n "$WORKSPACE_KEY" ] && [ "$WORKSPACE_KEY" != "YOUR_WORKSPACE_KEY_HERE" ]; then
    echo "--- Test 1: Workspace key in X-Workspace-Key header ---"
    HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test1.json -X GET \
      -H "Authorization: Basic $(echo -n "${API_KEY}:" | base64)" \
      -H "X-Workspace-Key: ${WORKSPACE_KEY}" \
      -H "Content-Type: application/json" \
      "${BASE_URL}surveys")
    echo "HTTP Status: $HTTP_CODE"
    [ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test1.json)"
    echo ""
fi

# Test 2: Workspace key in X-Workspace-ID header
if [ -n "$WORKSPACE_KEY" ] && [ "$WORKSPACE_KEY" != "YOUR_WORKSPACE_KEY_HERE" ]; then
    echo "--- Test 2: Workspace key in X-Workspace-ID header ---"
    HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test2.json -X GET \
      -H "Authorization: Basic $(echo -n "${API_KEY}:" | base64)" \
      -H "X-Workspace-ID: ${WORKSPACE_KEY}" \
      -H "Content-Type: application/json" \
      "${BASE_URL}surveys")
    echo "HTTP Status: $HTTP_CODE"
    [ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test2.json)"
    echo ""
fi

# Test 3: Workspace key as query parameter
if [ -n "$WORKSPACE_KEY" ] && [ "$WORKSPACE_KEY" != "YOUR_WORKSPACE_KEY_HERE" ]; then
    echo "--- Test 3: Workspace key as query parameter ---"
    HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test3.json -X GET \
      -H "Authorization: Basic $(echo -n "${API_KEY}:" | base64)" \
      -H "Content-Type: application/json" \
      "${BASE_URL}surveys?workspace_key=${WORKSPACE_KEY}")
    echo "HTTP Status: $HTTP_CODE"
    [ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test3.json)"
    echo ""
fi

# Test 4: Both API key and workspace key in Basic auth (apiKey:workspaceKey)
if [ -n "$WORKSPACE_KEY" ] && [ "$WORKSPACE_KEY" != "YOUR_WORKSPACE_KEY_HERE" ]; then
    echo "--- Test 4: Both in Basic auth (apiKey:workspaceKey) ---"
    HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test4.json -X GET \
      -H "Authorization: Basic $(echo -n "${API_KEY}:${WORKSPACE_KEY}" | base64)" \
      -H "Content-Type: application/json" \
      "${BASE_URL}surveys")
    echo "HTTP Status: $HTTP_CODE"
    [ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test4.json)"
    echo ""
fi

echo "=== If all tests failed ==="
echo "The API key authentication format appears correct, but the key is being rejected."
echo "This suggests:"
echo "1. API key is invalid or expired"
echo "2. API key doesn't have Data Export API permissions"
echo "3. Account doesn't have Data Export API access"
echo ""
echo "Contact Survicate support with:"
echo "- Endpoint: ${BASE_URL}surveys"
echo "- Error: 401 Unauthorized"
echo "- Request format: Basic auth with API key"

