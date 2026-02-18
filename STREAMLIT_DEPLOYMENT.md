# 🚀 Streamlit Cloud Deployment Guide

## Prerequisites

✅ Your code is on GitHub: https://github.com/Rhishi-04/Expense-Tracker-FenmoProject-
✅ Your backend is deployed on Vercel: `https://expense-tracker-api-lemon-nu.vercel.app`

## Step-by-Step Deployment

### Step 1: Go to Streamlit Cloud

1. Visit **https://share.streamlit.io**
2. Sign in with your **GitHub account** (same account as your repository)

### Step 2: Create New App

1. Click the **"New app"** button (top right)
2. You'll see a form to configure your app

### Step 3: Configure Your App

Fill in the following details:

**Repository**: 
- Select: `Rhishi-04/Expense-Tracker-FenmoProject-`
- If you don't see it, click "Add repository" and authorize Streamlit Cloud

**Branch**: 
- Select: `main`

**Main file path**: 
- Enter: `streamlit_app.py`

**App URL** (optional):
- Leave default or customize: `expense-tracker` (will create: `expense-tracker.streamlit.app`)

### Step 4: Configure API URL Secret

**IMPORTANT**: This connects your frontend to the backend!

1. Click **"Advanced settings"** (at the bottom)
2. Go to the **"Secrets"** tab
3. Add the following secret:

```toml
API_URL = "https://expense-tracker-api-lemon-nu.vercel.app"
```

**How to add:**
- Click "New secret"
- Key: `API_URL`
- Value: `https://expense-tracker-api-lemon-nu.vercel.app`
- Click "Add"

### Step 5: Deploy!

1. Click the **"Deploy!"** button
2. Wait for the deployment to complete (usually 1-2 minutes)
3. You'll see your live app URL!

## ✅ After Deployment

### Test Your App

1. Visit your Streamlit Cloud URL (e.g., `https://expense-tracker.streamlit.app`)
2. Try adding an expense
3. Test filtering by category
4. Test sorting by date
5. Verify the total calculation

### Verify Backend Connection

If you see "Could not connect to API":
- Check that the `API_URL` secret is set correctly
- Verify your Vercel backend is accessible
- Check Streamlit Cloud logs (click "Manage app" → "Logs")

## 🔧 Troubleshooting

### Issue: "Could not connect to the API"

**Solution:**
1. Verify API URL in secrets matches your Vercel URL exactly
2. Test your Vercel API directly:
   ```bash
   curl https://expense-tracker-api-lemon-nu.vercel.app/health
   ```
3. Check CORS settings (should be enabled in `app.py`)

### Issue: "Module not found" errors

**Solution:**
1. Check `requirements.txt` has all dependencies
2. Check Streamlit Cloud build logs for specific errors
3. Ensure all imports are in requirements.txt

### Issue: App won't start

**Solution:**
1. Check Streamlit Cloud logs for error messages
2. Verify `streamlit_app.py` is in the root directory
3. Ensure Python version compatibility

## 📋 Quick Checklist

- [ ] Signed in to Streamlit Cloud with GitHub
- [ ] Selected correct repository: `Rhishi-04/Expense-Tracker-FenmoProject-`
- [ ] Branch: `main`
- [ ] Main file: `streamlit_app.py`
- [ ] Added `API_URL` secret with Vercel URL
- [ ] Clicked "Deploy!"
- [ ] Tested the live app

## 🔗 Your Deployment URLs

- **GitHub**: https://github.com/Rhishi-04/Expense-Tracker-FenmoProject-
- **Backend API**: https://expense-tracker-api-lemon-nu.vercel.app
- **Frontend**: (Your Streamlit Cloud URL after deployment)

## 📝 Notes

- Streamlit Cloud automatically redeploys when you push to the `main` branch
- Changes to secrets require manual redeployment
- Free tier includes unlimited apps!

---

**Need Help?** Check Streamlit Cloud documentation: https://docs.streamlit.io/streamlit-community-cloud

