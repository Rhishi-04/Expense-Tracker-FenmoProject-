# 🚀 Deployment Guide

This guide will help you deploy the Expense Tracker application to GitHub, Vercel (backend), and Streamlit Cloud (frontend).

## Step 1: Push to GitHub

### 1.1 Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository details:
   - **Name**: `expense-tracker` (or any name you prefer)
   - **Description**: "Full-stack expense tracking app with FastAPI and Streamlit"
   - **Visibility**: Public (required for free hosting)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

### 1.2 Push Your Code

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /Users/rhishibansode/Project/Fenmo_Project

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker.git

# Push to GitHub
git push -u origin main
```

**Note**: If you haven't configured git credentials, you may need to:
- Use a Personal Access Token instead of password
- Or use SSH: `git@github.com:YOUR_USERNAME/expense-tracker.git`

## Step 2: Deploy Backend to Vercel

### 2.1 Install Vercel CLI

```bash
npm install -g vercel
```

If you don't have Node.js/npm, install it first from [nodejs.org](https://nodejs.org/)

### 2.2 Deploy to Vercel

```bash
cd /Users/rhishibansode/Project/Fenmo_Project

# Login to Vercel (will open browser)
vercel login

# Deploy (follow prompts)
vercel

# When prompted:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name: expense-tracker-api (or any name)
# - Directory: ./
# - Override settings? No
```

### 2.3 Get Your Vercel URL

After deployment, Vercel will give you a URL like:
```
https://expense-tracker-api.vercel.app
```

**Save this URL** - you'll need it for Streamlit Cloud!

### 2.4 Verify Backend Deployment

Test your API:
```bash
curl https://YOUR_VERCEL_URL.vercel.app/health
```

You should see: `{"status":"healthy"}`

## Step 3: Deploy Frontend to Streamlit Cloud

### 3.1 Go to Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**

### 3.2 Configure Deployment

1. **Repository**: Select your `expense-tracker` repository
2. **Branch**: `main`
3. **Main file path**: `streamlit_app.py`
4. **App URL**: (auto-generated, e.g., `expense-tracker.streamlit.app`)

### 3.3 Set API URL Secret

1. Click **"Advanced settings"**
2. Go to **"Secrets"** tab
3. Add this secret:

```toml
API_URL = "https://YOUR_VERCEL_URL.vercel.app"
```

Replace `YOUR_VERCEL_URL` with your actual Vercel URL from Step 2.3

4. Click **"Save"**
5. Click **"Deploy!"**

### 3.4 Wait for Deployment

Streamlit Cloud will:
- Install dependencies from `requirements.txt`
- Start your app
- Show you the live URL

## Step 4: Verify Everything Works

### Test Backend (Vercel)
```bash
# Health check
curl https://YOUR_VERCEL_URL.vercel.app/health

# Create an expense
curl -X POST "https://YOUR_VERCEL_URL.vercel.app/expenses" \
  -H "Content-Type: application/json" \
  -d '{"amount": "100.50", "category": "Food", "description": "Test", "date": "2024-01-15"}'

# Get expenses
curl https://YOUR_VERCEL_URL.vercel.app/expenses
```

### Test Frontend (Streamlit Cloud)
1. Visit your Streamlit Cloud URL
2. Try adding an expense
3. Test filtering and sorting
4. Verify the total calculation

## Troubleshooting

### Backend Issues (Vercel)

**Problem**: API returns 404 or errors
- **Solution**: Check that `vercel.json` is in the root directory
- Verify the build logs in Vercel dashboard

**Problem**: Database errors
- **Solution**: Vercel uses serverless functions. SQLite works but data is ephemeral.
- For production, consider using a cloud database (PostgreSQL, MongoDB, etc.)

### Frontend Issues (Streamlit Cloud)

**Problem**: "Could not connect to API"
- **Solution**: 
  1. Check that `API_URL` secret is set correctly in Streamlit Cloud
  2. Verify your Vercel URL is correct
  3. Make sure CORS is enabled in your FastAPI app (it is!)

**Problem**: Dependencies not installing
- **Solution**: Check `requirements.txt` has all dependencies
- Check Streamlit Cloud build logs for errors

## Important Notes

1. **Database Persistence**: 
   - SQLite on Vercel is ephemeral (data resets on each deployment)
   - For production, use a cloud database service
   - For this assignment, SQLite is fine for demonstration

2. **API URL Updates**:
   - If you redeploy to Vercel and get a new URL, update the Streamlit secret

3. **Free Tier Limits**:
   - Vercel: 100GB bandwidth/month (usually enough)
   - Streamlit Cloud: Unlimited apps (great!)

## Next Steps

Once deployed:
1. ✅ Share your GitHub repository link
2. ✅ Share your Streamlit Cloud app URL
3. ✅ Share your Vercel API URL (optional, for API docs)

Your application is now live! 🎉

