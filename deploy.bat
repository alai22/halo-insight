@echo off
setlocal enabledelayedexpansion

echo 🚀 Gladly Deployment Script
echo ==========================

REM Default values
set "ENVIRONMENT=%1"
if "%ENVIRONMENT%"=="" set "ENVIRONMENT=development"

set "REGION=%2"
if "%REGION%"=="" set "REGION=us-east-1"

set "PROJECT_NAME=%3"
if "%PROJECT_NAME%"=="" set "PROJECT_NAME=halo-insight"

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Docker is not running. Please start Docker and try again.
    exit /b 1
)

echo ✓ Docker is running

REM Build the Docker image
echo ✓ Building Docker image...
docker build -t %PROJECT_NAME%:%ENVIRONMENT% .

REM Check if environment variables are set
if "%ANTHROPIC_API_KEY%"=="" (
    echo ⚠ ANTHROPIC_API_KEY environment variable is not set
    echo ⚠ You'll need to set this in your cloud environment
)

if "%S3_BUCKET_NAME%"=="" if not "%ENVIRONMENT%"=="development" (
    echo ⚠ S3_BUCKET_NAME environment variable is not set
    echo ⚠ You'll need to set this for cloud deployment
)

if "%ENVIRONMENT%"=="development" (
    echo ✓ Deploying for development...
    echo ✓ Starting container on http://localhost:5000
    docker run --rm -it ^
        -p 5000:5000 ^
        -e FLASK_ENV=development ^
        -e FLASK_DEBUG=true ^
        -v "%cd%\config_cloud.py:/app/config_local.py:ro" ^
        --name gladly-dev ^
        %PROJECT_NAME%:%ENVIRONMENT%
) else if "%ENVIRONMENT%"=="production" (
    echo ✓ Deploying for production...
    echo ⚠ Make sure to set all required environment variables!
    echo ✓ Starting container as daemon...
    echo ✓ Removing existing container if present...
    docker rm -f gladly-prod >nul 2>&1
    docker run -d ^
        -p 80:5000 ^
        --restart unless-stopped ^
        -e ANTHROPIC_API_KEY="%ANTHROPIC_API_KEY%" ^
        -e S3_BUCKET_NAME="%S3_BUCKET_NAME%" ^
        -e AWS_DEFAULT_REGION="%AWS_DEFAULT_REGION%" ^
        -e AWS_REGION="%AWS_DEFAULT_REGION%" ^
        --name gladly-prod ^
        %PROJECT_NAME%:%ENVIRONMENT%
    
    echo ✓ Application deployed at http://localhost
    echo ✓ Check logs with: docker logs gladly-prod
) else if "%ENVIRONMENT%"=="ec2" (
    echo ✓ Preparing for EC2 deployment...
    echo ✓ Tagging image for AWS ECR (if using)...
    docker save %PROJECT_NAME%:%ENVIRONMENT% | gzip > %PROJECT_NAME%-%ENVIRONMENT%.tar.gz
    echo ✓ Image saved as %PROJECT_NAME%-%ENVIRONMENT%.tar.gz
    echo ✓ Transfer this file to your EC2 instance and run:
    echo   gunzip -c %PROJECT_NAME%-%ENVIRONMENT%.tar.gz ^| docker load
    echo   docker run -d -p 80:5000 --restart unless-stopped --name gladly-app ^
    echo     -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY ^
    echo     -e S3_BUCKET_NAME=$S3_BUCKET_NAME ^
    echo     -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID ^
    echo     -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY ^
    echo     %PROJECT_NAME%:%ENVIRONMENT%
) else (
    echo ✗ Unknown environment: %ENVIRONMENT%
    echo ✓ Usage: %0 [development^|production^|ec2] [region] [project-name]
    exit /b 1
)

echo ✓ Deployment completed!
