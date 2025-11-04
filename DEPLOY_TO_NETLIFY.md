# Sustainability Dashboard - Auto-Deploy to Netlify

**Author:** Deepa Rao

This guide explains how to automatically publish your sustainability dashboard to Netlify every day.

## Prerequisites

1. **Netlify Account** (free): [Sign up at netlify.com](https://www.netlify.com/)
2. **GitHub Account** (free): [Sign up at github.com](https://github.com/)
3. **Git installed** on your computer

## Setup Steps

### 1. Initialize Git Repository

```powershell
# Navigate to your project folder
cd C:\deepa

# Initialize git (if not already done)
git init

# Configure git (first time only)
git config user.name "Deepa Rao"
git config user.email "your-email@example.com"

# Add files
git add .

# Make first commit
git commit -m "Initial commit: Sustainability Dashboard by Deepa Rao"
```

### 2. Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `sustainability-dashboard`
3. Description: "Sustainability Regulation Dashboard by Deepa Rao"
4. Choose **Public** or **Private**
5. Click **Create repository**

### 3. Push to GitHub

```powershell
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/sustainability-dashboard.git

# Push code
git branch -M main
git push -u origin main
```

### 4. Connect to Netlify

#### Option A: Netlify UI (Easiest)

1. Log into [app.netlify.com](https://app.netlify.com)
2. Click **Add new site** → **Import an existing project**
3. Choose **GitHub** and authorize
4. Select your `sustainability-dashboard` repository
5. **Build settings:**
   - Build command: `python scripts/build_for_netlify.py`
   - Publish directory: `public`
6. Click **Deploy site**

#### Option B: Netlify CLI

```powershell
# Install Netlify CLI globally
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize site
cd C:\deepa
netlify init

# Follow prompts to connect to your GitHub repo
```

### 5. Set Up Daily Auto-Deployment

Two options:

#### Option A: GitHub Actions (Recommended)

Already set up! The workflow file `.github/workflows/daily-update.yml` will:
- Run every day at 8 AM UTC
- Generate fresh dashboard
- Commit and push to GitHub
- Netlify automatically deploys

**GitHub Secrets Required:**
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add secrets (if using SMTP):
   - `SMTP_HOST`: smtp.gmail.com
   - `SMTP_PORT`: 587
   - `SMTP_USER`: your email
   - `SMTP_PASSWORD`: your app password
   - `SMTP_FROM`: your email
   - `SMTP_TO`: adeeprao@gmail.com

#### Option B: Windows Task Scheduler (Local)

Use the existing scheduled task:
```powershell
# Run the deployment script manually to test
powershell -NoProfile -ExecutionPolicy Bypass -File C:\deepa\scripts\deploy_to_netlify.ps1

# The existing task runs at 08:00 daily and will now also deploy
```

### 6. Configure Netlify Site

After first deployment:

1. **Custom Domain** (optional):
   - Netlify dashboard → Domain settings
   - Add custom domain like `sustainability.yourdomain.com`

2. **Site Name**:
   - Settings → General → Change site name
   - Example: `sustainability-dashboard-deepa-rao`
   - Your URL: `sustainability-dashboard-deepa-rao.netlify.app`

3. **Build Hooks** (for manual triggers):
   - Settings → Build & deploy → Build hooks
   - Create hook: "Daily Update"
   - Save the webhook URL

## How It Works

```
Daily (8 AM) → Generate Dashboard → Commit to Git → Push to GitHub → Netlify Auto-Deploy
                      ↓
              sustainability_agent_enhanced.py
              generate_interactive_dashboard.py
                      ↓
              sustainability_dashboard_interactive.html
                      ↓
              Live at: your-site.netlify.app
```

## File Structure for Netlify

```
C:\deepa\
├── public/                          # Netlify publish directory
│   └── index.html                   # Auto-copied dashboard
├── .github/
│   └── workflows/
│       └── daily-update.yml         # GitHub Actions workflow
├── scripts/
│   ├── build_for_netlify.py         # Build script for Netlify
│   └── deploy_to_netlify.ps1        # Local deployment script
├── netlify.toml                     # Netlify configuration
├── .gitignore                       # Exclude sensitive files
└── README.md                        # This file
```

## Manual Deployment

To deploy manually anytime:

```powershell
# Option 1: Run build and git push
cd C:\deepa
C:/deepa/.venv/Scripts/python.exe scripts/build_for_netlify.py
git add .
git commit -m "Update dashboard: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push

# Option 2: Use Netlify CLI
netlify deploy --prod

# Option 3: Trigger build hook (if configured)
Invoke-WebRequest -Uri "YOUR_BUILD_HOOK_URL" -Method POST
```

## Viewing Your Dashboard

Once deployed, your dashboard is live at:
- **Netlify URL**: `https://your-site-name.netlify.app`
- **Custom Domain** (if configured): `https://sustainability.yourdomain.com`

Features automatically included:
- ✅ HTTPS enabled
- ✅ CDN for fast loading worldwide
- ✅ Automatic updates when you push to GitHub
- ✅ Free hosting for public sites
- ✅ Deploy previews for branches

## Troubleshooting

### Build fails on Netlify

Check build log in Netlify dashboard. Common issues:
- Python version (add `runtime.txt` with `3.11` or `3.12`)
- Missing dependencies (ensure `requirements.txt` is committed)

### Dashboard not updating

```powershell
# Check if git push worked
git status
git log

# Check Netlify dashboard for latest deploy
```

### Want to test before pushing

```powershell
# Build locally first
C:/deepa/.venv/Scripts/python.exe scripts/build_for_netlify.py

# Open the output
Start-Process public/index.html

# If good, commit and push
git add .
git commit -m "Update dashboard"
git push
```

## Cost

- **GitHub**: Free for public repos
- **Netlify**: Free tier includes:
  - 100 GB bandwidth/month
  - 300 build minutes/month
  - Automatic HTTPS
  - Your dashboard easily fits in free tier!

## Next Steps

1. Complete steps 1-4 above
2. Wait for first deployment (or trigger manually)
3. Visit your Netlify URL to see live dashboard
4. Share the URL with stakeholders
5. Dashboard auto-updates daily at 8 AM

## Support

Questions? Contact: Deepa Rao (your-email@example.com)

Dashboard prepared by: **Deepa Rao** | Sustainability Compliance Analyst
