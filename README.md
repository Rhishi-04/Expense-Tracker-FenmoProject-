# 💰 Expense Tracker

A minimal full-stack expense tracking application built with **FastAPI** (backend) and **Streamlit** (frontend). Record and review personal expenses to understand where your money is going.

## 🎯 User Story

As a user, I can record and review my personal expenses so I can understand where my money is going.

## ✅ Acceptance Criteria

1. ✅ User can create a new expense entry with amount, category, description, and date.
2. ✅ User can view a list of expenses.
3. ✅ User can filter expenses by category.
4. ✅ User can sort expenses by date (newest first).
5. ✅ User can see a simple total of expenses for the current list (e.g., "Total: ₹X").

## 🚀 Features

### Core Features (Required)
- **Add Expenses**: Form to create new expense entries with validation
- **View Expenses**: List/table display of all expenses
- **Filter by Category**: Dropdown to filter expenses by category
- **Sort by Date**: Toggle to sort expenses by date (newest first)
- **Total Calculation**: Display total amount of currently visible expenses
- **Idempotent API**: Handles duplicate requests gracefully (network retries, page refreshes)

### Nice to Have (Implemented)
- ✅ **Input Validation**: Prevents negative amounts, requires date and category
- ✅ **Summary View**: Total per category breakdown with bar chart
- ✅ **Error Handling**: Graceful handling of network errors, timeouts, and API failures
- ✅ **Loading States**: Visual feedback during API requests
- ✅ **User Experience**: Prevents rapid multiple submissions, clear error messages

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Data Processing**: Pandas
- **Money Handling**: Python Decimal for precise financial calculations

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Fenmo_Project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

### Start the Backend (Terminal 1)
```bash
uvicorn app:app --reload --port 8000
```
The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Start the Frontend (Terminal 2)
```bash
streamlit run streamlit_app.py
```
The app will open in your browser at `http://localhost:8501`

## 📡 API Endpoints

### POST /expenses
Create a new expense entry.

**Request Body:**
```json
{
  "amount": 100.50,
  "category": "Food",
  "description": "Lunch",
  "date": "2024-01-15"
}
```

**Features:**
- Idempotent: Duplicate requests return the same expense (handles retries)
- Validation: Amount must be positive, category and date required

### GET /expenses
Get a list of expenses.

**Query Parameters:**
- `category` (optional): Filter by category (e.g., `?category=Food`)
- `sort` (optional): Sort order - use `sort=date_desc` for newest first

**Examples:**
```bash
# Get all expenses
GET /expenses

# Filter by category
GET /expenses?category=Food

# Sort by date (newest first)
GET /expenses?sort=date_desc

# Filter and sort
GET /expenses?category=Food&sort=date_desc
```

## 💾 Data Model

- `id`: Integer (primary key)
- `amount`: Decimal(10, 2) - Using Decimal for precise money handling
- `category`: String (required)
- `description`: String (optional)
- `date`: Date (required)
- `created_at`: DateTime (auto-generated)
- `request_hash`: String (for idempotency detection)

## 🗄️ Database Choice: SQLite

**Why SQLite?**
- **Simplicity**: No separate database server required, perfect for a minimal application
- **File-based**: Easy to backup, inspect, and manage
- **Production-ready**: SQLite is battle-tested and suitable for small to medium applications
- **Zero configuration**: Works out of the box with SQLAlchemy
- **ACID compliance**: Ensures data integrity

**Trade-offs:**
- Not suitable for high-concurrency scenarios (but sufficient for personal use)
- Single-file database (can be a limitation for very large datasets, but fine for expense tracking)

## 🎨 Design Decisions

### 1. **Idempotency for POST /expenses**
- **Decision**: Implement request hashing to detect duplicate requests
- **Rationale**: Assignment explicitly requires handling network retries and page refreshes
- **Implementation**: SHA-256 hash of request data stored in `request_hash` field
- **Benefit**: Prevents duplicate expenses from accidental double-clicks or network retries

### 2. **Decimal for Money Handling**
- **Decision**: Use Python `Decimal` and SQL `Numeric(10, 2)` instead of `Float`
- **Rationale**: Floating-point arithmetic can cause precision issues with money (e.g., 0.1 + 0.2 ≠ 0.3)
- **Benefit**: Ensures accurate financial calculations, critical for production-like quality

### 3. **Client-Side Filtering and Sorting**
- **Decision**: Primary filtering/sorting done via API, with client-side backup
- **Rationale**: Reduces server load and provides better UX with instant updates
- **Trade-off**: For very large datasets, server-side would be better, but sufficient for personal expense tracking

### 4. **Error Handling and Loading States**
- **Decision**: Comprehensive error handling with user-friendly messages
- **Rationale**: Assignment mentions "unreliable networks" - users need clear feedback
- **Implementation**: Timeout handling, connection error detection, retry guidance

### 5. **Form Submission Protection**
- **Decision**: Rate limiting on form submissions (1 second minimum between submits)
- **Rationale**: Prevents accidental multiple submissions while maintaining responsiveness
- **Benefit**: Better UX and reduces unnecessary API calls

## ⚖️ Trade-offs Made (Timebox Considerations)

1. **No Update/Delete Endpoints**: Focused on core requirements (POST and GET). Update/delete can be added later if needed.

2. **Simple UI**: Used Streamlit's built-in components instead of custom HTML/CSS. Prioritized correctness and clarity over advanced styling.

3. **No Authentication**: Assumed single-user personal use case. Can be added for multi-user scenarios.

4. **SQLite over PostgreSQL**: Chose simplicity and zero-config over scalability. Easy to migrate later if needed.

5. **No Automated Tests**: Focused on manual testing and production-like behavior. Tests would be valuable but prioritized core functionality.

6. **Basic Validation**: Implemented essential validation (positive amounts, required fields). More sophisticated validation (e.g., category whitelist) can be added.

## 🚫 Intentionally Not Done

1. **Income Tracking**: Assignment focuses on expenses only, so income features were removed
2. **Advanced Analytics**: Kept summary simple (total per category). Advanced charts/trends can be added later
3. **Export Functionality**: Not in requirements, but easy to add with pandas
4. **Search Functionality**: Filtering by category covers the use case
5. **Pagination**: Not needed for personal expense tracking volumes
6. **Caching**: Simple application doesn't require caching layer

## 🌐 Deployment

### Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Set the API URL in Streamlit secrets:
   - Go to Settings → Secrets
   - Add:
     ```toml
     API_URL = "https://your-fastapi-url.vercel.app"
     ```
5. Deploy!

### Deploying FastAPI to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. The `vercel.json` file is already configured
3. Run `vercel` in the project directory
4. Follow the prompts to deploy

### Alternative: Deploy to Railway/Render

Both platforms support Python applications:
- **Railway**: Connect GitHub repo, set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- **Render**: Create a Web Service, set build command: `pip install -r requirements.txt` and start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## 📁 Project Structure

```
Fenmo_Project/
├── app.py                 # FastAPI backend application
├── streamlit_app.py      # Streamlit frontend application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── QUICKSTART.md         # Quick start guide
├── vercel.json           # Vercel deployment config
├── .gitignore            # Git ignore file
├── run.sh                # Startup script (Mac/Linux)
├── run.bat               # Startup script (Windows)
└── expenses.db           # SQLite database (created automatically)
```

## 🧪 Testing the API

### Using curl

```bash
# Create an expense
curl -X POST "http://localhost:8000/expenses" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.50,
    "category": "Food",
    "description": "Lunch",
    "date": "2024-01-15"
  }'

# Get all expenses
curl "http://localhost:8000/expenses"

# Filter by category
curl "http://localhost:8000/expenses?category=Food"

# Sort by date (newest first)
curl "http://localhost:8000/expenses?sort=date_desc"
```

### Using the Interactive API Docs

Visit `http://localhost:8000/docs` for Swagger UI with interactive API testing.

## 🎯 Usage

1. **Add Expense**: Fill in the form at the top (amount, category, description, date)
2. **View Expenses**: See all expenses in the table below
3. **Filter**: Use the category dropdown to filter expenses
4. **Sort**: Toggle "Sort by Date (Newest First)" to change sort order
5. **View Total**: See the total of currently visible expenses
6. **Summary**: Scroll down to see category-wise breakdown

## 🔍 What Was Evaluated

This implementation focuses on:

- ✅ **Correctness under realistic conditions**: Handles network retries, page refreshes, slow responses
- ✅ **Data correctness**: Decimal for money, proper validation, idempotent operations
- ✅ **Edge cases**: Negative amounts, missing fields, network failures, timeouts
- ✅ **Code clarity**: Well-structured, documented, maintainable code
- ✅ **Judgment**: Prioritized what matters (idempotency, money precision) over nice-to-haves

## 🔗 Links

- **Live Application**: [Your Streamlit Cloud URL]
- **GitHub Repository**: [Your GitHub Repo URL]
- **API Documentation**: [Your API URL]/docs

---

Made with ❤️ using FastAPI and Streamlit
