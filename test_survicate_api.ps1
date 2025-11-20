# PowerShell script to test Survicate Data Export API
# Base URL: https://data-api.survicate.com/v2/

# ============================================
# STEP 1: Set your API credentials
# ============================================
$apiKey = "YOUR_API_KEY_HERE"  # Replace with your actual API key
$workspaceKey = "YOUR_WORKSPACE_KEY_HERE"  # Optional, replace if you have one
$baseUrl = "https://data-api.survicate.com/v2/"

# ============================================
# STEP 2: Create Basic Auth header
# ============================================
# Basic auth format: base64(apiKey:)
$credentials = "$apiKey" + ":"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($credentials)
$base64Credentials = [Convert]::ToBase64String($bytes)
$authHeader = "Basic $base64Credentials"

Write-Host "`n=== Testing Survicate API ===" -ForegroundColor Cyan
Write-Host "Base URL: $baseUrl" -ForegroundColor Gray
Write-Host "API Key (first 12 chars): $($apiKey.Substring(0, [Math]::Min(12, $apiKey.Length)))..." -ForegroundColor Gray
Write-Host "Auth Header: $($authHeader.Substring(0, 20))..." -ForegroundColor Gray

# ============================================
# STEP 3: Test 1 - List Surveys
# ============================================
Write-Host "`n--- Test 1: List Surveys ---" -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = $authHeader
        "Content-Type" = "application/json"
    }
    
    $url = "${baseUrl}surveys"
    Write-Host "GET $url" -ForegroundColor Gray
    
    $response = Invoke-RestMethod -Uri $url -Method Get -Headers $headers -ErrorAction Stop
    
    Write-Host "✓ Success! Found $($response.Count) surveys" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3 | Write-Host
} catch {
    Write-Host "✗ Failed!" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body: $responseBody" -ForegroundColor Red
    }
}

# ============================================
# STEP 4: Test 2 - Get Survey Responses (if you have a survey ID)
# ============================================
Write-Host "`n--- Test 2: Get Survey Responses ---" -ForegroundColor Yellow
$surveyId = "YOUR_SURVEY_ID_HERE"  # Replace with your actual survey ID

if ($surveyId -ne "YOUR_SURVEY_ID_HERE") {
    try {
        $headers = @{
            "Authorization" = $authHeader
            "Content-Type" = "application/json"
        }
        
        # Get first page of responses
        $url = "${baseUrl}surveys/$surveyId/responses?items_per_page=10"
        Write-Host "GET $url" -ForegroundColor Gray
        
        $response = Invoke-RestMethod -Uri $url -Method Get -Headers $headers -ErrorAction Stop
        
        Write-Host "✓ Success! Found responses" -ForegroundColor Green
        Write-Host "Total items: $($response.items.Count)" -ForegroundColor Gray
        Write-Host "Has next page: $($response.pagination_data.next_url -ne $null)" -ForegroundColor Gray
        $response | ConvertTo-Json -Depth 2 | Write-Host
    } catch {
        Write-Host "✗ Failed!" -ForegroundColor Red
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "Response Body: $responseBody" -ForegroundColor Red
        }
    }
} else {
    Write-Host "Skipping - Set surveyId variable first" -ForegroundColor Gray
}

# ============================================
# STEP 5: Test 3 - Raw HTTP Request (alternative method)
# ============================================
Write-Host "`n--- Test 3: Raw HTTP Request (Alternative) ---" -ForegroundColor Yellow
try {
    $url = "${baseUrl}surveys"
    $request = [System.Net.WebRequest]::Create($url)
    $request.Method = "GET"
    $request.Headers.Add("Authorization", $authHeader)
    $request.ContentType = "application/json"
    
    Write-Host "GET $url" -ForegroundColor Gray
    
    $response = $request.GetResponse()
    $stream = $response.GetResponseStream()
    $reader = New-Object System.IO.StreamReader($stream)
    $responseBody = $reader.ReadToEnd()
    
    Write-Host "✓ Success!" -ForegroundColor Green
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Gray
    Write-Host "Response:" -ForegroundColor Gray
    $responseBody | ConvertFrom-Json | ConvertTo-Json -Depth 3 | Write-Host
    
    $reader.Close()
    $stream.Close()
    $response.Close()
} catch {
    Write-Host "✗ Failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "Status Code: $statusCode" -ForegroundColor Red
        
        $errorStream = $_.Exception.Response.GetResponseStream()
        $errorReader = New-Object System.IO.StreamReader($errorStream)
        $errorBody = $errorReader.ReadToEnd()
        Write-Host "Response Body: $errorBody" -ForegroundColor Red
        $errorReader.Close()
        $errorStream.Close()
    }
}

Write-Host "`n=== Testing Complete ===" -ForegroundColor Cyan

