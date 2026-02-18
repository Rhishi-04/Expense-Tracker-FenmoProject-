# 🔧 Vercel 500 Error Fix

## Issue
The backend was returning 500 errors because SQLite database files can't be written to the default location in Vercel's serverless environment.

## Solution Applied
Updated `app.py` to use `/tmp` directory for the database file in serverless environments:

```python
# Use /tmp for serverless environments (Vercel), otherwise use local file
import os
if os.path.exists("/tmp"):
    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/expenses.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"
```

## Important Notes

⚠️ **Database Persistence**: 
- Vercel serverless functions are stateless
- The database in `/tmp` will be reset between deployments
- Data is ephemeral (this is fine for the assignment demonstration)
- For production, consider using a cloud database (PostgreSQL, MongoDB, etc.)

## Testing

After Vercel redeploys (automatic from GitHub push), test:

```bash
curl https://expense-tracker-api-lemon-nu.vercel.app/health
```

Should return: `{"status":"healthy"}`

## If Still Getting Errors

1. Check Vercel Dashboard → Your Project → Deployments → Latest → Logs
2. Verify the deployment completed successfully
3. Check that all dependencies are in `requirements.txt`
4. Ensure Python version is compatible

## Alternative: Use In-Memory Database (for testing)

If SQLite continues to have issues, we can switch to an in-memory database for demonstration:

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
```

Note: This will lose all data on each function invocation, but works reliably on Vercel.

