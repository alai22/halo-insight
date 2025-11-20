# Survicate API Test - Demonstrating 403 Error

These tests demonstrate that the API key is correctly formatted and being sent, but Survicate's API is returning 403 Forbidden errors.

## Prerequisites

1. Get your API key from your `.env` file or Survicate account
2. Replace `YOUR_API_KEY` in the examples below with your actual API key
3. Replace `YOUR_SURVEY_ID` with your survey ID (default: `e08c3365f14085e2`)

## Test 1: cURL Command (Terminal/Browser DevTools)

### Basic Authentication Test

```bash
# Test 1: List surveys endpoint
curl -X GET "https://api.survicate.com/v1/surveys" \
  -H "Authorization: Basic $(echo -n 'YOUR_API_KEY:' | base64)" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -v

# Test 2: Get responses for specific survey
curl -X GET "https://api.survicate.com/v1/surveys/YOUR_SURVEY_ID/responses?items_per_page=10" \
  -H "Authorization: Basic $(echo -n 'YOUR_API_KEY:' | base64)" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -v
```

### Windows PowerShell Version

```powershell
# Encode API key for Basic auth
$apiKey = "YOUR_API_KEY"
$credentials = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${apiKey}:"))

# Test 1: List surveys
Invoke-WebRequest -Uri "https://api.survicate.com/v1/surveys" `
  -Headers @{
    "Authorization" = "Basic $credentials"
    "Content-Type" = "application/json"
    "Accept" = "application/json"
  } `
  -Method GET

# Test 2: Get responses
Invoke-WebRequest -Uri "https://api.survicate.com/v1/surveys/YOUR_SURVEY_ID/responses?items_per_page=10" `
  -Headers @{
    "Authorization" = "Basic $credentials"
    "Content-Type" = "application/json"
    "Accept" = "application/json"
  } `
  -Method GET
```

## Test 2: Postman Collection

### Setup Instructions

1. **Create a new request** in Postman
2. **Set Method**: `GET`
3. **Set URL**: `https://api.survicate.com/v1/surveys`
4. **Go to Authorization tab**:
   - Type: `Basic Auth`
   - Username: `YOUR_API_KEY`
   - Password: (leave empty)
5. **Go to Headers tab** (add these manually):
   - `Content-Type`: `application/json`
   - `Accept`: `application/json`
6. **Click Send**

### Test Requests

#### Request 1: List All Surveys
```
Method: GET
URL: https://api.survicate.com/v1/surveys
Authorization: Basic Auth
  Username: YOUR_API_KEY
  Password: (empty)
Headers:
  Content-Type: application/json
  Accept: application/json
```

#### Request 2: Get Survey Responses
```
Method: GET
URL: https://api.survicate.com/v1/surveys/YOUR_SURVEY_ID/responses?items_per_page=10
Authorization: Basic Auth
  Username: YOUR_API_KEY
  Password: (empty)
Headers:
  Content-Type: application/json
  Accept: application/json
```

#### Request 3: Get Survey Responses with Attributes
```
Method: GET
URL: https://api.survicate.com/v1/surveys/YOUR_SURVEY_ID/responses?items_per_page=10&attributes[]=email&attributes[]=first_name
Authorization: Basic Auth
  Username: YOUR_API_KEY
  Password: (empty)
Headers:
  Content-Type: application/json
  Accept: application/json
```

## Test 3: Browser (JavaScript Console)

**Note**: Browsers don't easily support Basic Auth in fetch requests. Use Postman or cURL instead.

However, you can test the endpoint structure:

```javascript
// This will show the 403 error in browser console
fetch('https://api.survicate.com/v1/surveys', {
  method: 'GET',
  headers: {
    'Authorization': 'Basic ' + btoa('YOUR_API_KEY:'),
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})
.then(response => {
  console.log('Status:', response.status);
  console.log('Headers:', [...response.headers.entries()]);
  return response.text();
})
.then(text => {
  console.log('Response:', text);
})
.catch(error => {
  console.error('Error:', error);
});
```

## Expected Results

### ✅ Correct Authentication Format
- Authorization header: `Basic <base64_encoded_api_key:>`
- Content-Type: `application/json`
- Accept: `application/json`

### ❌ Current Error Response
- **Status Code**: `403 Forbidden`
- **Response Body**: HTML error page from AWS S3
- **Headers**: 
  - `Server: BunnyCDN-IL1-1348`
  - `x-amz-request-id: ...`
  - `x-amz-id-2: ...`

This indicates:
1. ✅ Authentication format is correct
2. ✅ Request reaches Survicate's infrastructure
3. ❌ Survicate's backend denies access (likely permissions/subscription issue)

## What to Share with Survicate Support

When contacting Survicate support, include:

1. **API Key** (first 10 characters): `YOUR_API_KEY[:10]...`
2. **Test Results**:
   - Status code: `403`
   - Response headers showing BunnyCDN and AWS S3 errors
   - Full error response body
3. **Request Details**:
   - Endpoint: `https://api.survicate.com/v1/surveys`
   - Method: `GET`
   - Authorization: `Basic Auth` with API key
4. **Subscription Plan**: Confirm your plan includes Data Export API access
5. **API Key Permissions**: Verify the key has Data Export API permissions enabled

## Quick Test Script

Save this as `test_survicate.sh`:

```bash
#!/bin/bash

# Configuration
API_KEY="${SURVICATE_API_KEY:-YOUR_API_KEY}"
SURVEY_ID="${SURVICATE_SURVEY_ID:-e08c3365f14085e2}"
BASE_URL="https://api.survicate.com/v1"

# Encode API key for Basic auth
AUTH_HEADER=$(echo -n "${API_KEY}:" | base64)

echo "Testing Survicate API..."
echo "API Key (first 10 chars): ${API_KEY:0:10}..."
echo "Survey ID: ${SURVEY_ID}"
echo ""

# Test 1: List surveys
echo "=== Test 1: List Surveys ==="
curl -X GET "${BASE_URL}/surveys" \
  -H "Authorization: Basic ${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s

echo ""
echo "=== Test 2: Get Survey Responses ==="
curl -X GET "${BASE_URL}/surveys/${SURVEY_ID}/responses?items_per_page=10" \
  -H "Authorization: Basic ${AUTH_HEADER}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s

echo ""
echo "=== Test Complete ==="
```

Make it executable and run:
```bash
chmod +x test_survicate.sh
export SURVICATE_API_KEY="your_actual_api_key"
./test_survicate.sh
```

