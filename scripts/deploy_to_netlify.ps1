$ErrorActionPreference = 'Stop'

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "Deploying Sustainability Dashboard to Netlify" -ForegroundColor Cyan
Write-Host "Author: Deepa Rao" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Navigate to project root
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $projectRoot

# Load environment if exists (for local runs)
$envScript = Join-Path $PSScriptRoot 'env.ps1'
if (Test-Path $envScript) {
    Write-Host "Loading environment variables..." -ForegroundColor Yellow
    . $envScript
}

# Get Python path
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Write-Host "Virtual environment not found. Using system Python..." -ForegroundColor Yellow
    $python = 'python'
}

# Build for Netlify
Write-Host "`n1. Building dashboard..." -ForegroundColor Green
& $python (Join-Path $PSScriptRoot 'build_for_netlify.py')
if ($LASTEXITCODE -ne 0) {
    throw "Build failed with exit code $LASTEXITCODE"
}

# Check if git is initialized
if (-not (Test-Path '.git')) {
    Write-Host "`n2. Initializing git repository..." -ForegroundColor Green
    git init
    git config user.name "Deepa Rao"
    git config user.email "sustainability-dashboard@example.com"
}

# Stage changes
Write-Host "`n3. Staging changes..." -ForegroundColor Green
git add public/
git add sustainability_updates_enhanced.db -ErrorAction SilentlyContinue
git add netlify.toml -ErrorAction SilentlyContinue
git add requirements.txt -ErrorAction SilentlyContinue
git add runtime.txt -ErrorAction SilentlyContinue

# Check if there are changes
$status = git status --porcelain
if ($status) {
    Write-Host "`n4. Committing changes..." -ForegroundColor Green
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Auto-update dashboard: $timestamp - Deepa Rao"
    
    # Push to GitHub (if remote configured)
    $remotes = git remote
    if ($remotes -contains 'origin') {
        Write-Host "`n5. Pushing to GitHub..." -ForegroundColor Green
        git push origin main
        Write-Host "`n✓ Successfully pushed to GitHub. Netlify will auto-deploy." -ForegroundColor Green
    } else {
        Write-Host "`n⚠ No 'origin' remote configured. Skipping push." -ForegroundColor Yellow
        Write-Host "   Set up GitHub remote with:" -ForegroundColor Yellow
        Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/sustainability-dashboard.git" -ForegroundColor Yellow
        Write-Host "   git push -u origin main" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n✓ No changes detected. Dashboard is up to date." -ForegroundColor Green
}

Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "`nDashboard by: Deepa Rao | Sustainability Compliance Analyst" -ForegroundColor White
