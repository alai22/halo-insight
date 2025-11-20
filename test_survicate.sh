#!/bin/bash

# Survicate API Test Script
# Demonstrates 403 Forbidden error despite correct API key format

# Configuration - Set these environment variables or edit directly
API_KEY="${SURVICATE_API_KEY:-YOUR_API_KEY}"
SURVEY_ID="${SURVICATE_SURVEY_ID:-e08c3365f14085e2}"
BASE_URL="https://api.survicate.com/v1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Survicate API Test - 403 Error Demo"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  API Key (first 10 chars): ${API_KEY:0:10}..."
echo "  Survey ID: ${SURVEY_ID}"
echo "  Base URL: ${BASE_URL}"
echo ""

# Check if API key is set
if [ "$API_KEY" == "YOUR_API_KEY" ] || [ -z "$API_KEY" ]; then
    echo -e "${RED}ERROR: SURVICATE_API_KEY not set!${NC}"
    echo "Set it with: export SURVICATE_API_KEY='your_api_key'"
    exit 1
fi

# Encode API key for Basic auth
AUTH_HEADER=$(echo -n "${API_KEY}:" | base64)

echo "=========================================="
echo "Test 1: List All Surveys"
echo "=========================================="
echo "Endpoint: GET ${BASE_URL}/surveys"
echo "Authorization: Basic ${AUTH_HEADER:0:20}..."
echo ""

RESPONSE=$(curl -X GET "${BASE_URL}/surveys" \
  -H "Authorization: Basic ${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -w "\n%{http_code}" \
  -s)

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo -e "HTTP Status Code: ${YELLOW}${HTTP_CODE}${NC}"
echo ""
echo "Response Body (first 500 chars):"
echo "$BODY" | head -c 500
echo ""
echo ""

if [ "$HTTP_CODE" == "403" ]; then
    echo -e "${RED}❌ 403 Forbidden - API access denied${NC}"
    echo "This indicates:"
    echo "  ✓ Authentication format is correct"
    echo "  ✓ Request reaches Survicate infrastructure"
    echo "  ✗ API key lacks permissions or subscription doesn't include API access"
elif [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✅ Success - API is working!${NC}"
else
    echo -e "${YELLOW}⚠️  Unexpected status code: ${HTTP_CODE}${NC}"
fi

echo ""
echo "=========================================="
echo "Test 2: Get Survey Responses"
echo "=========================================="
echo "Endpoint: GET ${BASE_URL}/surveys/${SURVEY_ID}/responses?items_per_page=10"
echo "Authorization: Basic ${AUTH_HEADER:0:20}..."
echo ""

RESPONSE2=$(curl -X GET "${BASE_URL}/surveys/${SURVEY_ID}/responses?items_per_page=10" \
  -H "Authorization: Basic ${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -w "\n%{http_code}" \
  -s)

HTTP_CODE2=$(echo "$RESPONSE2" | tail -n1)
BODY2=$(echo "$RESPONSE2" | sed '$d')

echo -e "HTTP Status Code: ${YELLOW}${HTTP_CODE2}${NC}"
echo ""
echo "Response Body (first 500 chars):"
echo "$BODY2" | head -c 500
echo ""
echo ""

if [ "$HTTP_CODE2" == "403" ]; then
    echo -e "${RED}❌ 403 Forbidden - API access denied${NC}"
elif [ "$HTTP_CODE2" == "200" ]; then
    echo -e "${GREEN}✅ Success - API is working!${NC}"
else
    echo -e "${YELLOW}⚠️  Unexpected status code: ${HTTP_CODE2}${NC}"
fi

echo ""
echo "=========================================="
echo "Test Complete"
echo "=========================================="
echo ""
echo "What to share with Survicate Support:"
echo "  1. API Key (first 10 chars): ${API_KEY:0:10}..."
echo "  2. HTTP Status Codes: ${HTTP_CODE}, ${HTTP_CODE2}"
echo "  3. Response headers showing BunnyCDN and AWS S3 errors"
echo "  4. Full error response body"
echo "  5. Confirmation that subscription plan includes Data Export API access"

