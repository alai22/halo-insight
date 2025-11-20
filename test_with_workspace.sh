#!/bin/bash
# Test different authentication formats including workspace key

API_KEY="YOUR_API_KEY_HERE"
WORKSPACE_KEY="YOUR_WORKSPACE_KEY_HERE"  # If you have one
BASE_URL="https://data-api.survicate.com/v2/"

echo "=== Testing Different Authentication Formats ==="
echo ""

# Test 1: API key only (current)
echo "--- Test 1: API key only (apiKey:) ---"
AUTH1="Basic $(echo -n "${API_KEY}:" | base64)"
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test1.json -X GET \
  -H "Authorization: $AUTH1" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test1.json)"
echo ""

# Test 2: API key:Workspace key
if [ -n "$WORKSPACE_KEY" ] && [ "$WORKSPACE_KEY" != "YOUR_WORKSPACE_KEY_HERE" ]; then
    echo "--- Test 2: API key:Workspace key (apiKey:workspaceKey) ---"
    AUTH2="Basic $(echo -n "${API_KEY}:${WORKSPACE_KEY}" | base64)"
    HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test2.json -X GET \
      -H "Authorization: $AUTH2" \
      -H "Content-Type: application/json" \
      "${BASE_URL}surveys")
    echo "HTTP Status: $HTTP_CODE"
    [ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test2.json)"
    echo ""
fi

# Test 3: Workspace key:API key (reversed)
if [ -n "$WORKSPACE_KEY" ] && [ "$WORKSPACE_KEY" != "YOUR_WORKSPACE_KEY_HERE" ]; then
    echo "--- Test 3: Workspace key:API key (workspaceKey:apiKey) ---"
    AUTH3="Basic $(echo -n "${WORKSPACE_KEY}:${API_KEY}" | base64)"
    HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test3.json -X GET \
      -H "Authorization: $AUTH3" \
      -H "Content-Type: application/json" \
      "${BASE_URL}surveys")
    echo "HTTP Status: $HTTP_CODE"
    [ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test3.json)"
    echo ""
fi

# Test 4: X-API-Key header
echo "--- Test 4: X-API-Key header ---"
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test4.json -X GET \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test4.json)"
echo ""

# Test 5: X-Workspace-Key header (if workspace key exists)
if [ -n "$WORKSPACE_KEY" ] && [ "$WORKSPACE_KEY" != "YOUR_WORKSPACE_KEY_HERE" ]; then
    echo "--- Test 5: X-Workspace-Key header ---"
    HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test5.json -X GET \
      -H "X-Workspace-Key: ${WORKSPACE_KEY}" \
      -H "Content-Type: application/json" \
      "${BASE_URL}surveys")
    echo "HTTP Status: $HTTP_CODE"
    [ "$HTTP_CODE" = "200" ] && echo "✓ SUCCESS!" || echo "✗ Failed: $(cat /tmp/test5.json)"
    echo ""
fi

echo "=== Summary ==="
echo "If all tests failed with 401, the issue is likely:"
echo "1. API key is invalid or expired"
echo "2. API key doesn't have Data Export API permissions"
echo "3. Account/workspace doesn't have Data Export API access enabled"
echo "4. Need to contact Survicate support to verify API key status"

