#!/bin/bash
# Test different authentication formats for Survicate API

API_KEY="YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL="https://data-api.survicate.com/v2/"

echo "=== Testing Different Authentication Formats ==="
echo ""
echo "API Key (first 12 chars): ${API_KEY:0:12}..."
echo "Base URL: $BASE_URL"
echo ""

# Test 1: Basic auth with apiKey: (current format)
echo "--- Test 1: Basic auth with 'apiKey:' format ---"
AUTH1="Basic $(echo -n "${API_KEY}:" | base64)"
echo "Auth Header: ${AUTH1:0:30}..."
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test1.json -X GET \
  -H "Authorization: $AUTH1" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ SUCCESS!"
    cat /tmp/test1.json | jq '.' 2>/dev/null || cat /tmp/test1.json
else
    echo "✗ Failed"
    cat /tmp/test1.json
fi
echo ""

# Test 2: Basic auth with just apiKey (no colon)
echo "--- Test 2: Basic auth with 'apiKey' format (no colon) ---"
AUTH2="Basic $(echo -n "${API_KEY}" | base64)"
echo "Auth Header: ${AUTH2:0:30}..."
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test2.json -X GET \
  -H "Authorization: $AUTH2" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ SUCCESS!"
    cat /tmp/test2.json | jq '.' 2>/dev/null || cat /tmp/test2.json
else
    echo "✗ Failed"
    cat /tmp/test2.json
fi
echo ""

# Test 3: Bearer token
echo "--- Test 3: Bearer token format ---"
AUTH3="Bearer ${API_KEY}"
echo "Auth Header: ${AUTH3:0:30}..."
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test3.json -X GET \
  -H "Authorization: $AUTH3" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ SUCCESS!"
    cat /tmp/test3.json | jq '.' 2>/dev/null || cat /tmp/test3.json
else
    echo "✗ Failed"
    cat /tmp/test3.json
fi
echo ""

# Test 4: X-API-Key header
echo "--- Test 4: X-API-Key header format ---"
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/test4.json -X GET \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys")
echo "HTTP Status: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ SUCCESS!"
    cat /tmp/test4.json | jq '.' 2>/dev/null || cat /tmp/test4.json
else
    echo "✗ Failed"
    cat /tmp/test4.json
fi
echo ""

# Test 5: Verify base64 encoding
echo "--- Debug: Verify base64 encoding ---"
echo "Original API Key length: ${#API_KEY}"
echo "API Key with colon: ${API_KEY}:"
ENCODED=$(echo -n "${API_KEY}:" | base64)
echo "Base64 encoded: $ENCODED"
DECODED=$(echo -n "$ENCODED" | base64 -d)
echo "Base64 decoded back: $DECODED"
if [ "$DECODED" = "${API_KEY}:" ]; then
    echo "✓ Base64 encoding is correct"
else
    echo "✗ Base64 encoding mismatch!"
fi
echo ""

echo "=== Testing Complete ==="

