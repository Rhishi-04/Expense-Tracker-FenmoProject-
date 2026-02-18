# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend (Terminal 1)
```bash
uvicorn app:app --reload --port 8000
```

### Step 3: Start the Frontend (Terminal 2)
```bash
streamlit run streamlit_app.py
```

That's it! Your app will be running at:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📝 Testing the API

You can test the API directly using the interactive docs at `http://localhost:8000/docs` or using curl:

```bash
# Add an expense
curl -X POST "http://localhost:8000/expenses" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.50,
    "category": "Food",
    "description": "Lunch",
    "date": "2024-01-15"
  }'

# Get all expenses
curl http://localhost:8000/expenses

# Filter by category
curl "http://localhost:8000/expenses?category=Food"

# Sort by date (newest first)
curl "http://localhost:8000/expenses?sort=date_desc"

# Get summary
curl http://localhost:8000/expenses
```

## 🎯 Key Features

1. **Add Expenses**: Use the form at the top to add new expenses
2. **Filter by Category**: Use the dropdown to filter expenses
3. **Sort by Date**: Toggle the checkbox to sort newest first
4. **View Total**: See the total of currently visible expenses
5. **Category Summary**: Scroll down to see breakdown by category

## 🌐 Deployment Checklist

### For Streamlit Cloud:
1. ✅ Push code to GitHub
2. ✅ Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. ✅ Connect your repository
4. ✅ Add API URL in secrets (Settings → Secrets):
   ```toml
   API_URL = "https://your-api-url.vercel.app"
   ```
5. ✅ Deploy!

### For Vercel (FastAPI):
1. ✅ Install Vercel CLI: `npm i -g vercel`
2. ✅ Run `vercel` in project directory
3. ✅ Follow prompts
4. ✅ Update Streamlit secrets with the Vercel URL

## 💡 Tips

- The API is **idempotent** - if you accidentally submit the same expense twice, it won't create duplicates
- All amounts are handled with **Decimal precision** for accurate money calculations
- The app handles network errors gracefully - you'll see clear error messages if the API is unavailable
- Use the refresh button to reload expenses if needed

## 🐛 Troubleshooting

**Issue**: "Could not connect to the API"
- **Solution**: Make sure the backend is running on port 8000

**Issue**: "Request timed out"
- **Solution**: Check your network connection, the expense may have been created - try refreshing

**Issue**: Database errors
- **Solution**: Delete `expenses.db` and restart the backend to create a fresh database
