# 📦 Quick GitHub Setup

## Create Repository and Push

### Option 1: Using GitHub Web Interface

1. **Create Repository on GitHub:**
   - Go to https://github.com/new
   - Repository name: `expense-tracker` (or your preferred name)
   - Description: "Full-stack expense tracking app"
   - Make it **Public**
   - **DO NOT** check "Initialize with README"
   - Click **"Create repository"**

2. **Push Your Code:**
   
   After creating the repo, GitHub will show you commands. Run these in your terminal:

   ```bash
   cd /Users/rhishibansode/Project/Fenmo_Project
   
   # Add remote (replace YOUR_USERNAME with your GitHub username)
   git remote add origin https://github.com/YOUR_USERNAME/expense-tracker.git
   
   # Push to GitHub
   git push -u origin main
   ```

### Option 2: Using GitHub CLI (if installed)

```bash
cd /Users/rhishibansode/Project/Fenmo_Project

# Create repo and push in one command
gh repo create expense-tracker --public --source=. --remote=origin --push
```

## Authentication

If you're asked for credentials:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your password)

### Create Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name it: "Expense Tracker Deployment"
4. Select scopes: `repo` (full control)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

## Verify Push

After pushing, check your GitHub repository:
- All files should be visible
- README.md should display properly
- Code should be on the `main` branch

## Next Steps

Once code is on GitHub:
1. ✅ Proceed to Vercel deployment (see DEPLOYMENT.md)
2. ✅ Then deploy to Streamlit Cloud

