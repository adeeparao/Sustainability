# Sustainability Regulation Dashboard

**Author:** Deepa Rao | Sustainability Compliance Analyst

## Overview

Professional interactive dashboard tracking global sustainability regulations including EU CSRD/ESRS, IFRS S1/S2, UK SRS, Japan SSBJ, India BRSR, and SBTi standards.

## Features

- ✅ **Interactive Dashboard** - Click stat cards to filter and view regulations
- ✅ **Compliance Tracker** - Monitor your organization's progress with local storage
- ✅ **Comprehensive Metadata** - Deadlines, impact levels, affected sectors, significant changes
- ✅ **Auto-Updates** - Refreshes daily with latest regulatory information
- ✅ **Export Reports** - Download compliance status reports
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile

## Quick Start

### Local Development

```powershell
# Clone and setup
git clone https://github.com/YOUR_USERNAME/sustainability-dashboard.git
cd sustainability-dashboard

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Generate dashboard
python sustainability_agent_enhanced.py
python generate_interactive_dashboard.py

# Open dashboard
Start-Process sustainability_dashboard_interactive.html
```

### Deploy to Netlify

See [DEPLOY_TO_NETLIFY.md](./DEPLOY_TO_NETLIFY.md) for complete setup instructions.

**Quick Deploy:**

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy)

## Project Structure

```
sustainability-dashboard/
├── public/                              # Netlify publish directory
│   └── index.html                       # Generated dashboard
├── scripts/
│   ├── build_for_netlify.py            # Netlify build script
│   ├── deploy_to_netlify.ps1           # Local deployment
│   ├── run_sustainability_agent.ps1    # Daily runner
│   └── env.example.ps1                 # Environment template
├── .github/workflows/
│   └── daily-update.yml                # GitHub Actions workflow
├── sustainability_agent_enhanced.py     # Data collection & DB
├── generate_interactive_dashboard.py    # Dashboard generator
├── netlify.toml                        # Netlify config
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Technologies

- **Python 3.11+** - Data processing and dashboard generation
- **SQLite** - Regulation storage and tracking
- **JavaScript** - Interactive features and compliance tracker
- **HTML/CSS** - Professional responsive design
- **GitHub Actions** - Automated daily updates
- **Netlify** - Free hosting and deployment

## Tracked Regulations

| Source | Standard | Jurisdiction | Impact |
|--------|----------|--------------|--------|
| EU | CSRD/ESRS | European Union | High |
| IFRS | S1 & S2 | Global (30+ countries) | High |
| UK | UK SRS | United Kingdom | High |
| Japan | SSBJ Standards | Japan | High |
| India | BRSR/BRSR Core | India | High |
| SBTi | Net-Zero Standard | Global (voluntary) | High |

## Automated Updates

The dashboard automatically updates daily at 8 AM UTC via:

1. **GitHub Actions** - Fetches latest regulation data
2. **Python Scripts** - Regenerates dashboard with new information
3. **Git Push** - Commits changes to repository
4. **Netlify** - Auto-deploys updated dashboard

## Compliance Tracker

Built-in compliance tracker allows teams to:

- ✅ Mark regulations as Not Started / In Progress / Completed
- 👥 Assign team members and owners
- 📝 Add notes and action items
- 📊 View progress statistics
- 📄 Export compliance reports

All data stored locally in browser using localStorage API.

## Manual Updates

### Update Dashboard Locally

```powershell
# Generate latest data
python sustainability_agent_enhanced.py

# Build interactive dashboard
python generate_interactive_dashboard.py

# Deploy to Netlify
.\scripts\deploy_to_netlify.ps1
```

### Trigger Remote Update

```powershell
# Using GitHub Actions
gh workflow run daily-update.yml

# Or via GitHub web UI:
# Repository → Actions → Daily Dashboard Update → Run workflow
```

## Configuration

### Environment Variables (Optional)

For email notifications, create `scripts/env.ps1`:

```powershell
$env:SMTP_HOST = 'smtp.gmail.com'
$env:SMTP_PORT = '587'
$env:SMTP_USER = 'your-email@gmail.com'
$env:SMTP_PASSWORD = 'your-app-password'
$env:SMTP_FROM = $env:SMTP_USER
$env:SMTP_TO = 'recipient@example.com'
$env:DATA_DIR = 'C:\deepa\data'
```

### Netlify Build Settings

Configured in `netlify.toml`:
- **Build Command:** `python scripts/build_for_netlify.py`
- **Publish Directory:** `public`
- **Python Version:** 3.11

## Contributing

This is a personal project by Deepa Rao. For questions or suggestions:

- **Email:** your-email@example.com
- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/sustainability-dashboard/issues)

## License

© 2025 Deepa Rao. All rights reserved.

## Acknowledgments

Sustainability regulation data sourced from:
- European Commission
- IFRS Foundation
- UK Government
- Japan FSA
- India SEBI
- Science Based Targets initiative

---

**Dashboard Prepared by:** Deepa Rao | Sustainability Compliance Analyst  
**Last Updated:** Auto-generated daily via GitHub Actions  
**Live Dashboard:** [your-site.netlify.app](https://your-site.netlify.app)
