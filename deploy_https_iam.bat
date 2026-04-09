@echo off
REM HTTPS Deployment Script for Gladly Conversation Analyzer (IP-based with existing IAM role)
REM This script deploys HTTPS using your existing IAM role GladlyS3FA

setlocal enabledelayedexpansion

echo 🚀 HTTPS Deployment Script for Gladly Conversation Analyzer
echo ============================================================
echo Using existing IAM role: GladlyS3FA
echo Deployment type: IP-based (no custom domain)
echo.

REM Default values
set ENVIRONMENT=gladly-prod
set AWS_REGION=us-east-1

REM Check prerequisites
echo ℹ Checking prerequisites...

REM Check if AWS CLI is installed
aws --version >nul 2>&1
if errorlevel 1 (
    echo ✗ AWS CLI is not installed. Please install it first.
    exit /b 1
)
echo ✓ AWS CLI is installed

REM Check if Terraform is installed
terraform --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Terraform is not installed. Please install it first.
    exit /b 1
)
echo ✓ Terraform is installed

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ✗ Docker is not running. Please start Docker and try again.
    exit /b 1
)
echo ✓ Docker is running

REM Check AWS credentials
aws sts get-caller-identity >nul 2>&1
if errorlevel 1 (
    echo ✗ AWS credentials not configured. Please run 'aws configure' first.
    exit /b 1
)
echo ✓ AWS credentials configured

REM Check if IAM role exists
echo ℹ Checking IAM role GladlyS3FA...
aws iam get-role --role-name GladlyS3FA >nul 2>&1
if errorlevel 1 (
    echo ✗ IAM role 'GladlyS3FA' not found. Please create this role first.
    exit /b 1
)
echo ✓ IAM role GladlyS3FA found

REM Check required environment variables
echo ℹ Checking environment variables...

if "%ANTHROPIC_API_KEY%"=="" (
    echo ✗ Required environment variable ANTHROPIC_API_KEY is not set
    exit /b 1
)
echo ✓ ANTHROPIC_API_KEY is set

if "%GLADLY_API_KEY%"=="" (
    echo ✗ Required environment variable GLADLY_API_KEY is not set
    exit /b 1
)
echo ✓ GLADLY_API_KEY is set

if "%GLADLY_AGENT_EMAIL%"=="" (
    echo ✗ Required environment variable GLADLY_AGENT_EMAIL is not set
    exit /b 1
)
echo ✓ GLADLY_AGENT_EMAIL is set

if "%S3_BUCKET_NAME%"=="" (
    echo ✗ Required environment variable S3_BUCKET_NAME is not set
    exit /b 1
)
echo ✓ S3_BUCKET_NAME is set

echo ℹ Using IAM role for S3 access (no AWS credentials needed in environment)

REM Create terraform.tfvars file
echo ℹ Creating Terraform configuration...

echo environment = "%ENVIRONMENT%" > terraform\terraform.tfvars
echo aws_region = "%AWS_REGION%" >> terraform\terraform.tfvars

echo ✓ Terraform configuration created

REM Deploy infrastructure
echo ℹ Deploying infrastructure with Terraform...

cd terraform

REM Initialize Terraform
echo ✓ Initializing Terraform...
terraform init

REM Plan deployment
echo ✓ Planning deployment...
terraform plan

REM Ask for confirmation
echo.
echo ⚠ This will deploy/update your AWS infrastructure with HTTPS support.
echo ⚠ It will use your existing IAM role 'GladlyS3FA' for S3 access.
echo ⚠ Continue? (y/N)
set /p response=
if /i not "%response%"=="y" (
    echo ℹ Deployment cancelled by user
    exit /b 0
)

REM Apply changes
echo ✓ Applying Terraform changes...
terraform apply -auto-approve

REM Get outputs
echo ✓ Getting deployment outputs...
for /f "tokens=*" %%i in ('terraform output -raw application_url') do set APP_URL=%%i
for /f "tokens=*" %%i in ('terraform output -raw application_url_http') do set APP_URL_HTTP=%%i

echo ✓ Infrastructure deployed successfully!

REM Go back to project root
cd ..

REM Deploy application
echo ℹ Deploying application...

REM Build and deploy the application
echo ✓ Building Docker image...
docker build -t halo-insight:%ENVIRONMENT% .

REM Remove existing container if present (running or stopped)
echo ✓ Removing existing container if present...
docker rm -f gladly-prod >nul 2>&1

echo ✓ Deploying application container...
docker run -d ^
    -p 80:5000 ^
    --restart unless-stopped ^
    -e ANTHROPIC_API_KEY="%ANTHROPIC_API_KEY%" ^
    -e GLADLY_API_KEY="%GLADLY_API_KEY%" ^
    -e GLADLY_AGENT_EMAIL="%GLADLY_AGENT_EMAIL%" ^
    -e S3_BUCKET_NAME="%S3_BUCKET_NAME%" ^
    -e AWS_DEFAULT_REGION="%AWS_REGION%" ^
    -e AWS_REGION="%AWS_REGION%" ^
    --name gladly-prod ^
    halo-insight:%ENVIRONMENT%

REM Wait for application to start
echo ✓ Waiting for application to start...
timeout /t 30 /nobreak >nul

REM Display results
echo.
echo 🎉 Deployment Complete!
echo =======================
echo.
echo ✓ Your application is now available at:
echo   HTTPS: %APP_URL%
echo   HTTP:  %APP_URL_HTTP% (redirects to HTTPS)
echo.

echo ℹ Key changes made:
echo   ✓ HTTPS enabled with SSL certificate
echo   ✓ HTTP traffic redirected to HTTPS
echo   ✓ Using existing IAM role 'GladlyS3FA' for S3 access
echo   ✓ No more public S3 bucket access needed
echo.

echo ℹ Useful commands:
echo   Check application logs: docker logs gladly-prod
echo   Check load balancer: aws elbv2 describe-load-balancers --region %AWS_REGION%
echo   Test HTTPS: curl -I %APP_URL%
echo   Test S3 access: docker exec gladly-prod aws s3 ls s3://%S3_BUCKET_NAME%
echo.

echo ✓ HTTPS deployment with IAM role completed successfully!
