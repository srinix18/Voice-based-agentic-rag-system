# Financial RAG Agent - Setup Script
# Run this script to set up the project quickly

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "Financial RAG Agent - Quick Setup" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/6] Checking Python version..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] $pythonVersion" -ForegroundColor Green
}
else {
    Write-Host "  [ERROR] Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Virtual environment handling
Write-Host "`n[2/6] Virtual environment detection..." -ForegroundColor Cyan
# Prefer parent directory .venv (matches VS Code configuration), then local options
$venvCandidates = @('..\\.venv', '.venv', 'venv', 'ENV', 'env')
$venvPath = $null

foreach ($candidate in $venvCandidates) {
    if (Test-Path $candidate) {
        $venvPath = (Resolve-Path $candidate).Path
        break
    }
}

if ($venvPath) {
    Write-Host "  [OK] Found existing virtual environment: $venvPath" -ForegroundColor Green
}
else {
    Write-Host "  [WARN] No virtual environment found (checked: .venv, venv, ENV, env)" -ForegroundColor Yellow
    $createVenv = Read-Host "Would you like to create a new virtual environment now? (y/n)"
    if ($createVenv -eq 'y' -or $createVenv -eq 'Y') {
        # Create a venv named .venv by default on Windows
        python -m venv .venv
        if ($LASTEXITCODE -eq 0) {
            $venvPath = '.venv'
            Write-Host "  [OK] Virtual environment '.venv' created" -ForegroundColor Green
        }
        else {
            Write-Host "  [ERROR] Failed to create virtual environment" -ForegroundColor Red
        }
    }
    else {
        Write-Host "  [INFO] Skipping virtual environment creation. You can still install dependencies into your existing environment manually." -ForegroundColor Yellow
    }
}

# Activate virtual environment if found
if ($venvPath) {
    Write-Host "`n[3/6] Activating virtual environment ($venvPath)..." -ForegroundColor Cyan
    $activateScript = Join-Path -Path $venvPath -ChildPath 'Scripts\Activate.ps1'
    if (Test-Path $activateScript) {
        & $activateScript
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Virtual environment activated" -ForegroundColor Green
        }
        else {
            Write-Host "  [WARN] Activation script ran but returned a non-zero exit code" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "  [ERROR] Activation script not found at $activateScript. If this is a valid venv, activate it manually." -ForegroundColor Red
    }
}
else {
    Write-Host "`n[3/6] Skipping activation (no virtual environment)." -ForegroundColor Yellow
}

# Install dependencies
Write-Host "`n[4/6] Installing dependencies..." -ForegroundColor Cyan
Write-Host "  (This may take a few minutes...)" -ForegroundColor Gray
pip install --upgrade pip -q
pip install -r requirements.txt -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "  [ERROR] Error installing dependencies" -ForegroundColor Red
    exit 1
}

# Set up environment file
Write-Host "`n[5/6] Setting up environment file..." -ForegroundColor Cyan
if (Test-Path ".env") {
    Write-Host "  [WARN] .env file already exists" -ForegroundColor Yellow
}
else {
    Copy-Item ".env.example" ".env"
    Write-Host "  [OK] .env file created from template" -ForegroundColor Green
    Write-Host "  [WARN] Please edit .env and add your GOOGLE_API_KEY" -ForegroundColor Yellow
}

# Check PDF directory
Write-Host "`n[6/6] Checking PDF directory..." -ForegroundColor Cyan
$pdfDir = "data\ncfe_books"
$pdfCount = (Get-ChildItem -Path $pdfDir -Filter "*.pdf" -ErrorAction SilentlyContinue).Count
if ($pdfCount -gt 0) {
    Write-Host "  [OK] Found $pdfCount PDF file(s)" -ForegroundColor Green
}
else {
    Write-Host "  [WARN] No PDF files found in $pdfDir" -ForegroundColor Yellow
    Write-Host "     Please add PDF files from NCFE e-Library" -ForegroundColor Gray
}

# Summary
Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Edit .env file and add your Google API key" -ForegroundColor White
Write-Host "     Get key from: https://makersuite.google.com/app/apikey" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Add PDF files to: $pdfDir" -ForegroundColor White
Write-Host ""
Write-Host "  3. Run the demo to test setup:" -ForegroundColor White
Write-Host "     python demo.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  4. Start the agent:" -ForegroundColor White
Write-Host "     python main_agent.py    (CLI mode)" -ForegroundColor Cyan
Write-Host "     adk serve main_agent.py (Voice UI mode)" -ForegroundColor Cyan
Write-Host ""

# Offer to open .env file
$response = Read-Host "Would you like to edit the .env file now? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    notepad .env
}

Write-Host ""
Write-Host "Happy coding!" -ForegroundColor Magenta
