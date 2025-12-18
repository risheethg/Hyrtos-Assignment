# Quick Setup Script for Singapore Transport Query Agent
# This script helps set up the project with Gemini API

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Singapore Transport Query Agent" -ForegroundColor Cyan
Write-Host "Setup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "  $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "  Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "  Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "  Dependencies installed" -ForegroundColor Green
Write-Host ""

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "  .env file created from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Edit .env file and add your API keys:" -ForegroundColor Red
    Write-Host "  - LTA_API_KEY (from https://datamall.lta.gov.sg)" -ForegroundColor Red
    Write-Host "  - GEMINI_API_KEY (from https://makersuite.google.com/app/apikey)" -ForegroundColor Red
    Write-Host ""
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
    Write-Host ""
}

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env and add your API keys" -ForegroundColor White
Write-Host "2. Run: jupyter notebook transport_agent_demo.ipynb" -ForegroundColor White
Write-Host "   OR" -ForegroundColor White
Write-Host "   Run: python main.py" -ForegroundColor White
Write-Host ""
