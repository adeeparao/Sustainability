param(
    [string]$Time = '08:00',
    [string]$TaskName = 'SustainabilityAgentDaily'
)
$ErrorActionPreference = 'Stop'

$runner = (Resolve-Path (Join-Path $PSScriptRoot 'run_sustainability_agent.ps1')).Path

# Ensure data dir exists ahead of the first run
$envScript = Join-Path $PSScriptRoot 'env.ps1'
if (Test-Path $envScript) { . $envScript }
if (-not $env:DATA_DIR) { $env:DATA_DIR = 'C:\deepa\data' }
if (-not (Test-Path $env:DATA_DIR)) { New-Item -ItemType Directory -Force -Path $env:DATA_DIR | Out-Null }

# Build the command line for schtasks. Use full path to PowerShell.
$ps = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$tr = "$ps -NoProfile -ExecutionPolicy Bypass -File `"$runner`""

# Create or update the task
schtasks /Create /F /SC DAILY /TN $TaskName /ST $Time /RL LIMITED /TR $tr | Out-Null

Write-Host "Scheduled task '$TaskName' registered to run daily at $Time."