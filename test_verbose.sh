#!/bin/bash
# Verbose test to see full response

API_KEY="YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL="https://data-api.survicate.com/v2/"

echo "=== Verbose Test ==="
echo "API Key length: ${#API_KEY}"
echo "Base URL: $BASE_URL"
echo ""

# Full verbose output
curl -v -X GET \
  -H "Authorization: Basic $(echo -n "${API_KEY}:" | base64)" \
  -H "Content-Type: application/json" \
  "${BASE_URL}surveys" 2>&1 | tee /tmp/verbose_output.txt

echo ""
echo "=== Extracted Info ==="
grep "< HTTP" /tmp/verbose_output.txt
grep -i "authorization" /tmp/verbose_output.txt | head -1
echo ""
echo "=== Response Body ==="
# Extract JSON response (everything after the last blank line before {)
sed -n '/^{/,$p' /tmp/verbose_output.txt

