param(
    [switch]$InstallDeps
)
$ErrorActionPreference = 'Stop'

# Load environment variables (SMTP, DATA_DIR)
$envScript = Join-Path $PSScriptRoot 'env.ps1'
if (Test-Path $envScript) {
    . $envScript
} else {
    Write-Warning "env.ps1 not found in $PSScriptRoot. Using env.example.ps1 as a template."
    $example = Join-Path $PSScriptRoot 'env.example.ps1'
    if (Test-Path $example) { . $example }
}

# Ensure data directory exists
if (-not (Test-Path $env:DATA_DIR)) {
    New-Item -ItemType Directory -Force -Path $env:DATA_DIR | Out-Null
}

# Resolve python path
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$python = Join-Path $repoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Write-Warning "Virtualenv Python not found at $python. Falling back to system Python."
    $python = 'py'
}

# Optionally ensure dependencies are installed
if ($InstallDeps) {
    & $python -m pip install --disable-pip-version-check -r (Join-Path $repoRoot 'requirements.txt')
}

# Run the agent
$scriptPath = Join-Path $repoRoot 'sustainability_agent.py'
Write-Host "Running sustainability agent with DATA_DIR=$($env:DATA_DIR) ..."
& $python $scriptPath
if ($LASTEXITCODE -ne 0) {
    throw "Agent failed with exit code $LASTEXITCODE"
}

Write-Host 'Done.'
