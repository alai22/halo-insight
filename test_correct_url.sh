#!/bin/bash
# Test with the CORRECT base URL: https://data-api.survicate.com/v2/

API_KEY="YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL="https://data-api.survicate.com/v2/"  # CORRECT URL

echo "=== Testing with CORRECT Base URL ==="
echo "Base URL: $BASE_URL"
echo ""

# Test 1: WITH colon
echo "--- Test 1: WITH colon (apiKey:) ---"
AUTH_WITH_COLON="Basic $(echo -n "${API_KEY}:" | base64)"
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test1.json -X GET \
  -H "Authorization: $AUTH_WITH_COLON" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ SUCCESS!"
    cat /tmp/test1.json | jq '.' 2>/dev/null || cat /tmp/test1.json
else
    echo "✗ Failed"
    echo "Response: $(cat /tmp/test1.json)"
fi
echo ""

# Test 2: WITHOUT colon
echo "--- Test 2: WITHOUT colon (apiKey) ---"
AUTH_NO_COLON="Basic $(echo -n "${API_KEY}" | base64)"
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test2.json -X GET \
  -H "Authorization: $AUTH_NO_COLON" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ SUCCESS!"
    cat /tmp/test2.json | jq '.' 2>/dev/null || cat /tmp/test2.json
else
    echo "✗ Failed"
    echo "Response: $(cat /tmp/test2.json)"
fi
echo ""

# Test 3: Verbose output to see full response
echo "--- Test 3: Verbose output (WITH colon) ---"
curl -v -X GET \
  -H "Authorization: Basic $(echo -n "${API_KEY}:" | base64)" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys" 2>&1 | head -30

