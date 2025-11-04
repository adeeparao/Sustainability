$ErrorActionPreference = 'Stop'

# Load environment variables
$envScript = Join-Path $PSScriptRoot 'env.ps1'
if (Test-Path $envScript) {
    . $envScript
} else {
    Write-Error "env.ps1 not found. Please create it from env.example.ps1 and set SMTP credentials."
    exit 1
}

# Resolve python path
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$python = Join-Path $repoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { $python = 'py' }

# Run the test sender
& $python (Join-Path $PSScriptRoot 'send_test_email.py')
if ($LASTEXITCODE -ne 0) {
    throw "Test email failed with exit code $LASTEXITCODE"
}

Write-Host 'Test email invoked. Check console output for send confirmation or error.'
