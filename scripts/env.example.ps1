# Copy this file to env.ps1 and fill in your details.
# Gmail requires an App Password for SMTP when 2-Step Verification is enabled.
# Create one at https://myaccount.google.com/apppasswords and paste it below.

$env:SMTP_HOST = 'smtp.gmail.com'
$env:SMTP_PORT = '587'
$env:SMTP_USER = 'your_gmail_username@gmail.com'
$env:SMTP_PASSWORD = '<APP_PASSWORD_16_CHARS>'
$env:SMTP_FROM = $env:SMTP_USER
$env:SMTP_TO = 'adeeprao@gmail.com'

# Optional: where to store data (DB and dashboard)
if (-not $env:DATA_DIR) { $env:DATA_DIR = 'C:\deepa\data' }
