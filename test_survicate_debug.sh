#!/bin/bash
# Debug script for Survicate API - shows full response details

API_KEY="YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL="https://data-api.survicate.com/v2/"
AUTH_HEADER="Basic $(echo -n "${API_KEY}:" | base64)"

echo "=== Testing Survicate API with Full Debug Info ==="
echo ""
echo "API Key (first 12 chars): ${API_KEY:0:12}..."
echo "Base URL: $BASE_URL"
echo "Auth Header (first 30 chars): ${AUTH_HEADER:0:30}..."
echo ""

# Test with verbose output
echo "--- Making request with verbose output ---"
echo ""

curl -v -X GET \
  -H "Authorization: $AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys" 2>&1 | tee /tmp/survicate_response.txt

echo ""
echo ""
echo "--- Parsed Response ---"
HTTP_CODE=$(grep "< HTTP" /tmp/survicate_response.txt | tail -1 | awk '{print $3}')
echo "HTTP Status Code: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ Success! Status 200 OK"
    echo ""
    echo "Response body:"
    # Extract just the JSON body (everything after the last blank line before JSON)
    sed -n '/^{/,$p' /tmp/survicate_response.txt | jq '.' 2>/dev/null || sed -n '/^{/,$p' /tmp/survicate_response.txt
    
    # Check if response is empty
    RESPONSE_BODY=$(sed -n '/^{/,$p' /tmp/survicate_response.txt)
    if [ "$RESPONSE_BODY" = "{}" ] || [ -z "$RESPONSE_BODY" ]; then
        echo ""
        echo "⚠ WARNING: Empty response {} - This could mean:"
        echo "  1. Authentication succeeded but you have no surveys"
        echo "  2. API key doesn't have access to any surveys"
        echo "  3. Workspace has no surveys configured"
    fi
elif [ "$HTTP_CODE" = "403" ]; then
    echo "✗ Forbidden (403) - Authentication or permissions issue"
    echo ""
    echo "Full response:"
    cat /tmp/survicate_response.txt
elif [ "$HTTP_CODE" = "401" ]; then
    echo "✗ Unauthorized (401) - Invalid API key"
elif [ -n "$HTTP_CODE" ]; then
    echo "✗ Error! HTTP Status: $HTTP_CODE"
    echo ""
    echo "Full response:"
    cat /tmp/survicate_response.txt
else
    echo "⚠ Could not determine HTTP status"
    echo ""
    echo "Full response:"
    cat /tmp/survicate_response.txt
fi

echo ""
echo "=== Test Complete ==="

