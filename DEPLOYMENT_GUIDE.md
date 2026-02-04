# CI/CD Deployment Guide - Healthcare App

## 🚀 Free Deployment Options

Your GitHub Actions CI/CD pipeline is now configured to automatically test and build your Healthcare App. You can deploy it for **free** to any of these platforms:

---

## Option 1: **Render.com** (Recommended - Easiest)

### Setup (5 minutes):

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Select your GitHub repo: `saliva-hormone-ai-tracker`
4. Configure:
   - **Name**: `healthcare-app`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Free Plan**: ✓ (your app will sleep after 15 min inactivity)

5. **Enable Auto-Deploy**: GitHub → Settings → Webhooks
6. Get your Deploy Hook URL from Render settings
7. Add to GitHub Secrets:
   - Go to: **Your Repo → Settings → Secrets and variables → Actions**
   - Add: `RENDER_DEPLOY_HOOK` = your Deploy Hook URL

✅ **Every push to main** will automatically deploy!

---

## Option 2: **Railway.app** (Simple Alternative)

### Setup (3 minutes):

1. Go to [railway.app](https://railway.app) and sign up
2. Click **"Create New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-detects `Procfile` and deploys automatically
5. Free tier includes $5/month credit (enough for testing)

✅ **No secrets needed** - Railway handles everything!

---

## Option 3: **Google Cloud Run** (Best for Learning)

### Setup (10 minutes):

1. Install Google Cloud CLI:
   ```bash
   curl https://sdk.cloud.google.com | bash
   ```

2. Authenticate:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. Deploy:
   ```bash
   gcloud run deploy healthcare-app \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

**Free tier**: 2 million requests/month, 360,000 GB-seconds/month ✓

---

## Option 4: **Fly.io** (Most Powerful Free Option)

### Setup (10 minutes):

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`

2. Sign up: `flyctl auth signup`

3. Initialize:
   ```bash
   flyctl launch
   ```
   - App name: `healthcare-app`
   - Select region (closest to you)
   - Say "no" to PostgreSQL

4. Deploy:
   ```bash
   flyctl deploy
   ```

**Free tier**: 3 shared-cpu-1x 256MB VMs, 160GB bandwidth/month ✓

---

## 📊 Comparison Table

| Platform | Setup Time | Free Tier | Cold Start | Custom Domain |
|----------|-----------|-----------|-----------|----------------|
| **Render** | 5 min | ✓ (sleeps) | 30-50s | ✓ Free |
| **Railway** | 3 min | ✓ ($5/mo) | 10-20s | ✓ Paid |
| **Cloud Run** | 10 min | ✓ Generous | 5-10s | ✓ Free |
| **Fly.io** | 10 min | ✓ Best | 10-20s | ✓ Free |

---

## 🔧 GitHub Actions Configuration

### Your CI/CD Pipeline Does:

✅ **On every push to main:**
- Runs Python linting (flake8, black, isort)
- Tests your code (pytest)
- Security scanning (bandit, safety)
- Builds Docker image
- Creates deployment package
- Triggers Render/Railway deployment (if configured)

✅ **On every pull request:**
- Runs all tests before merge
- Code quality checks
- Security vulnerabilities scan

### View Pipeline Status:
- Go to: **Your Repo → Actions**
- See all workflow runs and logs

---

## 🔐 Setting Up GitHub Secrets (for Render deployment)

1. Go to: **Your Repo → Settings → Secrets and variables → Actions**
2. Click **"New repository secret"**
3. Add:
   - **Name**: `RENDER_DEPLOY_HOOK`
   - **Value**: Your Render Deploy Hook URL (from Render dashboard)

---

## 📝 Environment Variables

For production, add these to your hosting platform:

```
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
```

### In Render:
1. Go to service settings → Environment
2. Add variables there

### In Railway:
1. Go to Variables tab
2. Add them directly

### In Cloud Run:
```bash
gcloud run deploy --set-env-vars SECRET_KEY=value,FLASK_ENV=production
```

---

## ✅ Testing Your Deployment

After deployment, test the app:

```bash
curl https://your-app-name.onrender.com/
```

Should return HTML homepage. If you see a page, ✓ it works!

---

## 📊 Monitoring & Logs

### Render:
Dashboard → Logs tab → Real-time logs

### Railway:
Project → Deployments → View Logs

### Cloud Run:
```bash
gcloud run logs read healthcare-app --limit 50
```

### Fly.io:
```bash
flyctl logs
```

---

## 🐛 Troubleshooting

### App won't start:
1. Check logs for errors
2. Verify `Procfile` exists
3. Ensure all dependencies in `requirements.txt`
4. Check that `app.py` has `if __name__ == '__main__'` block

### Database errors:
- SQLite uses local file `database.db`
- On Render/Railway: use persistent storage or add PostgreSQL
- For free tier, local SQLite works fine

### Cold starts are slow:
- Normal on free tiers
- Python cold start: 5-50 seconds
- Use paid plans for <1s starts

---

## 🚀 Next Steps

1. **Choose a platform** (Render recommended for simplicity)
2. **Follow the setup steps** above
3. **Add GitHub Secrets** if using Render
4. **Push to main branch** and watch it deploy!
5. **Share your link**:
   - Render: `https://healthcare-app.onrender.com`
   - Railway: Check your Railways dashboard
   - Cloud Run: `gcloud run describe healthcare-app`
   - Fly.io: `flyctl open`

---

## 📚 Additional Resources

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Fly.io Docs](https://fly.io/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

**Need help?** Check GitHub Actions logs → Your Repo → Actions tab

---

*Last Updated: February 2026*
