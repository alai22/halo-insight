#!/bin/bash
# Bash script to test Survicate Data Export API
# Base URL: https://data-api.survicate.com/v2/

# ============================================
# STEP 1: Set your API credentials
# ============================================
API_KEY="YOUR_API_KEY_HERE"  # Replace with your actual API key
WORKSPACE_KEY="YOUR_WORKSPACE_KEY_HERE"  # Optional, replace if you have one
BASE_URL="https://data-api.survicate.com/v2/"

# ============================================
# STEP 2: Create Basic Auth header
# ============================================
# Basic auth format: base64(apiKey:)
CREDENTIALS="${API_KEY}:"
BASE64_CREDENTIALS=$(echo -n "$CREDENTIALS" | base64)
AUTH_HEADER="Basic ${BASE64_CREDENTIALS}"

echo ""
echo "=== Testing Survicate API ==="
echo "Base URL: $BASE_URL"
echo "API Key (first 12 chars): ${API_KEY:0:12}..."
echo "Auth Header: ${AUTH_HEADER:0:20}..."

# ============================================
# STEP 3: Test 1 - List Surveys
# ============================================
echo ""
echo "--- Test 1: List Surveys ---"
URL="${BASE_URL}surveys"
echo "GET $URL"

RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET \
    -H "Authorization: $AUTH_HEADER" \
    -H "Content-Type: application/json" \
    "$URL")

HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS/d')

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "✓ Success! Status: $HTTP_STATUS"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
else
    echo "✗ Failed! Status: $HTTP_STATUS"
    echo "Response:"
    echo "$BODY"
fi

# ============================================
# STEP 4: Test 2 - Get Survey Responses (if you have a survey ID)
# ============================================
echo ""
echo "--- Test 2: Get Survey Responses ---"
SURVEY_ID="YOUR_SURVEY_ID_HERE"  # Replace with your actual survey ID

if [ "$SURVEY_ID" != "YOUR_SURVEY_ID_HERE" ]; then
    URL="${BASE_URL}surveys/${SURVEY_ID}/responses?items_per_page=10"
    echo "GET $URL"
    
    RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
        -X GET \
        -H "Authorization: $AUTH_HEADER" \
        -H "Content-Type: application/json" \
        "$URL")
    
    HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
    BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS/d')
    
    if [ "$HTTP_STATUS" -eq 200 ]; then
        echo "✓ Success! Status: $HTTP_STATUS"
        echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    else
        echo "✗ Failed! Status: $HTTP_STATUS"
        echo "Response:"
        echo "$BODY"
    fi
else
    echo "Skipping - Set SURVEY_ID variable first"
fi

# ============================================
# STEP 5: Test 3 - Verbose curl (shows headers)
# ============================================
echo ""
echo "--- Test 3: Verbose Request (shows headers) ---"
URL="${BASE_URL}surveys"
echo "GET $URL"
echo ""

curl -v \
    -X GET \
    -H "Authorization: $AUTH_HEADER" \
    -H "Content-Type: application/json" \
    "$URL" 2>&1 | grep -E "(< |> |HTTP|{|\"|\[)"

echo ""
echo "=== Testing Complete ==="

