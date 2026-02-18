from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.sql import func
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import date as date_type, datetime
from decimal import Decimal
import hashlib
import json

# Database setup
# Use /tmp for serverless environments (Vercel), otherwise use local file
import os
try:
    # Try /tmp first (for serverless like Vercel)
    if os.path.exists("/tmp"):
        db_path = "/tmp/expenses.db"
    else:
        db_path = "./expenses.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
except Exception:
    # Fallback to in-memory database if file system access fails
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)  # Using Numeric for precise money handling
    category = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)  # type: ignore
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # For idempotency: store hash of request to detect duplicates
    request_hash = Column(String, unique=True, index=True)

# Create tables (with error handling)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # Log error but continue (tables might already exist)
    print(f"Database initialization note: {e}")

# Pydantic models
class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=0, description="Expense amount must be positive")
    category: str = Field(min_length=1, description="Category is required")
    description: Optional[str] = None
    date: date_type = Field(..., description="Date is required")
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v
    
    model_config = ConfigDict(
        json_encoders={
            Decimal: str
        }
    )

class ExpenseResponse(BaseModel):
    id: int
    amount: Decimal
    category: str
    description: Optional[str]
    date: date_type
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            Decimal: str,
            datetime: lambda v: v.isoformat()
        }
    )

# FastAPI app
app = FastAPI(
    title="Expense Tracker API",
    description="A minimal expense tracking API for personal finance management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to generate request hash for idempotency
def generate_request_hash(expense_data: dict) -> str:
    """Generate a hash from expense data to detect duplicate requests"""
    # Create a deterministic hash from the expense data
    data_str = json.dumps({
        "amount": str(expense_data["amount"]),
        "category": expense_data["category"],
        "description": expense_data.get("description", ""),
        "date": expense_data["date"].isoformat() if isinstance(expense_data["date"], date_type) else expense_data["date"]
    }, sort_keys=True)
    return hashlib.sha256(data_str.encode()).hexdigest()

# API Routes
@app.get("/")
def read_root():
    return {
        "message": "Expense Tracker API",
        "version": "1.0.0",
        "endpoints": {
            "POST /expenses": "Create a new expense",
            "GET /expenses": "Get list of expenses (supports ?category=X&sort=date_desc)"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """
    Create a new expense entry.
    
    This endpoint is idempotent - if the same request is made multiple times
    (e.g., due to network retries or page refreshes), it will return the
    existing expense instead of creating duplicates.
    """
    # Convert to dict for hashing
    expense_dict = expense.model_dump()
    expense_dict["date"] = expense.date
    
    # Generate hash for idempotency check
    request_hash = generate_request_hash(expense_dict)
    
    # Check if this exact request was already made
    existing_expense = db.query(Expense).filter(Expense.request_hash == request_hash).first()
    if existing_expense:
        # Return existing expense (idempotent behavior)
        return existing_expense
    
    # Create new expense
    db_expense = Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date,
        request_hash=request_hash
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(
    category: Optional[str] = Query(None, description="Filter expenses by category"),
    sort: Optional[str] = Query(None, description="Sort order: 'date_desc' for newest first"),
    db: Session = Depends(get_db)
):
    """
    Get a list of expenses.
    
    Query parameters:
    - category: Filter by category (optional)
    - sort: Set to 'date_desc' to sort by date, newest first (optional)
    """
    query = db.query(Expense)
    
    # Apply category filter if provided
    if category:
        query = query.filter(Expense.category == category)
    
    # Apply sorting if requested
    if sort == "date_desc":
        query = query.order_by(Expense.date.desc(), Expense.created_at.desc())
    else:
        # Default: newest first by created_at
        query = query.order_by(Expense.created_at.desc())
    
    expenses = query.all()
    return expenses

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
