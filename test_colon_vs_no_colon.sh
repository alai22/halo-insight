#!/bin/bash
# Test with and without colon in Basic auth

API_KEY="YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL="https://data-api.survicate.com/v2/"

echo "=== Testing With vs Without Colon ==="
echo ""

# Test 1: WITH colon (current implementation)
echo "--- Test 1: WITH colon (apiKey:) ---"
AUTH_WITH_COLON="Basic $(echo -n "${API_KEY}:" | base64)"
echo "Auth: ${AUTH_WITH_COLON:0:40}..."
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/with_colon.json -X GET \
  -H "Authorization: $AUTH_WITH_COLON" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ SUCCESS!"
    cat /tmp/with_colon.json | jq '.' 2>/dev/null || cat /tmp/with_colon.json
else
    echo "✗ Failed"
    echo "Response: $(cat /tmp/with_colon.json)"
fi
echo ""

# Test 2: WITHOUT colon (just apiKey)
echo "--- Test 2: WITHOUT colon (apiKey) ---"
AUTH_NO_COLON="Basic $(echo -n "${API_KEY}" | base64)"
echo "Auth: ${AUTH_NO_COLON:0:40}..."
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/no_colon.json -X GET \
  -H "Authorization: $AUTH_NO_COLON" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ SUCCESS!"
    cat /tmp/no_colon.json | jq '.' 2>/dev/null || cat /tmp/no_colon.json
else
    echo "✗ Failed"
    echo "Response: $(cat /tmp/no_colon.json)"
fi
echo ""

echo "=== Summary ==="
echo "With colon (apiKey:): $(cat /tmp/with_colon.json)"
echo "Without colon (apiKey): $(cat /tmp/no_colon.json)"

