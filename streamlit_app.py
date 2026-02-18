import streamlit as st
import requests
import pandas as pd
from datetime import date
from decimal import Decimal
import time

# Configuration
try:
    API_URL = st.secrets.get("API_URL", "http://localhost:8000")
except:
    API_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Initialize session state for form submission tracking
if "submitting" not in st.session_state:
    st.session_state.submitting = False
if "last_submit_time" not in st.session_state:
    st.session_state.last_submit_time = 0

# Helper functions
def fetch_expenses(category_filter=None, sort_date_desc=False):
    """Fetch expenses from API with optional filtering and sorting"""
    try:
        params = {}
        if category_filter:
            params["category"] = category_filter
        if sort_date_desc:
            params["sort"] = "date_desc"
        
        response = requests.get(f"{API_URL}/expenses", params=params, timeout=5)
        if response.status_code == 200:
            return response.json(), None
        else:
            return [], f"API returned status {response.status_code}"
    except requests.exceptions.Timeout:
        return [], "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return [], "Could not connect to the API. Make sure the backend is running."
    except Exception as e:
        return [], f"Error fetching expenses: {str(e)}"

def add_expense(expense_data):
    """Add a new expense with error handling"""
    try:
        response = requests.post(
            f"{API_URL}/expenses",
            json=expense_data,
            timeout=10  # Longer timeout for POST requests
        )
        if response.status_code == 201:
            return True, response.json(), None
        else:
            return False, None, f"API returned status {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return False, None, "Request timed out. The expense may have been created. Please refresh to check."
    except requests.exceptions.ConnectionError:
        return False, None, "Could not connect to the API. Please check your connection and try again."
    except Exception as e:
        return False, None, f"Error adding expense: {str(e)}"

# Main app
st.title("💰 Expense Tracker")
st.markdown("Record and review your personal expenses")

# Form to add new expense
with st.form("add_expense_form", clear_on_submit=True):
    st.subheader("➕ Add New Expense")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            step=0.01,
            format="%.2f",
            help="Enter the expense amount"
        )
        category = st.text_input(
            "Category *",
            placeholder="e.g., Food, Transport, Entertainment",
            help="Required: Enter a category for this expense"
        )
    
    with col2:
        expense_date = st.date_input(
            "Date *",
            value=date.today(),
            help="Required: Select the date of the expense"
        )
        description = st.text_area(
            "Description",
            placeholder="Optional description",
            help="Optional: Add any additional details"
        )
    
    submit_button = st.form_submit_button(
        "Add Expense",
        type="primary",
        use_container_width=True
    )
    
    # Handle form submission
    if submit_button:
        # Prevent multiple rapid submissions
        current_time = time.time()
        if current_time - st.session_state.last_submit_time < 1:
            st.warning("Please wait a moment before submitting again.")
        else:
            st.session_state.last_submit_time = current_time
            
            # Validation
            if amount <= 0:
                st.error("❌ Amount must be greater than 0")
            elif not category or not category.strip():
                st.error("❌ Category is required")
            elif not expense_date:
                st.error("❌ Date is required")
            else:
                # Show loading state
                with st.spinner("Adding expense..."):
                    expense_data = {
                        "amount": str(Decimal(str(amount))),  # Convert to string for Decimal
                        "category": category.strip(),
                        "description": description.strip() if description else None,
                        "date": expense_date.isoformat()
                    }
                    
                    success, result, error = add_expense(expense_data)
                    
                    if success:
                        st.success("✅ Expense added successfully!")
                        # Small delay to show success message
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to add expense: {error}")

# Filters and controls
st.markdown("---")
st.subheader("📋 Expense List")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    # Category filter
    all_expenses, _ = fetch_expenses()
    if all_expenses:
        categories = sorted(set(exp.get("category", "") for exp in all_expenses if exp.get("category")))
        category_filter = st.selectbox(
            "Filter by Category",
            options=["All"] + categories,
            help="Filter expenses by category"
        )
    else:
        category_filter = "All"

with col2:
    # Sort option
    sort_date_desc = st.checkbox(
        "Sort by Date (Newest First)",
        value=True,
        help="Sort expenses by date, newest first"
    )

with col3:
    # Refresh button
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# Fetch expenses with filters
expenses, fetch_error = fetch_expenses(
    category_filter=None if category_filter == "All" else category_filter,
    sort_date_desc=sort_date_desc
)

# Display expenses
if fetch_error:
    st.error(f"⚠️ {fetch_error}")
    st.info("💡 Make sure the backend API is running on http://localhost:8000")

if expenses:
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['amount'] = df['amount'].apply(lambda x: Decimal(str(x)))
    df['created_at'] = pd.to_datetime(df['created_at'])
    
    # Apply client-side sorting if needed (as backup)
    if sort_date_desc:
        df = df.sort_values('date', ascending=False)
    
    # Display total
    total_amount = df['amount'].sum()
    st.metric("Total Expenses (₹)", f"₹{total_amount:,.2f}", help="Total of currently visible expenses")
    
    # Display expenses table
    if len(df) > 0:
        # Format for display
        display_df = df.copy()
        display_df['date'] = display_df['date'].astype(str)
        display_df['amount'] = display_df['amount'].apply(lambda x: f"₹{float(x):,.2f}")
        display_df['description'] = display_df['description'].fillna("-")
        
        # Select columns to display
        display_columns = ['date', 'category', 'amount', 'description']
        st.dataframe(
            display_df[display_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "date": "Date",
                "category": "Category",
                "amount": "Amount",
                "description": "Description"
            }
        )
        
        st.caption(f"Showing {len(df)} expense(s)")
    else:
        st.info("No expenses match the current filters.")
else:
    if not fetch_error:
        st.info("📝 No expenses yet. Add your first expense using the form above!")

# Summary view (Nice to have)
if expenses and len(expenses) > 0:
    st.markdown("---")
    st.subheader("📊 Summary by Category")
    
    df_summary = pd.DataFrame(expenses)
    df_summary['amount'] = df_summary['amount'].apply(lambda x: Decimal(str(x)))
    
    category_totals = df_summary.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Total per Category:**")
        for category, total in category_totals.items():
            st.write(f"- **{category}**: ₹{float(total):,.2f}")
    
    with col2:
        if len(category_totals) > 0:
            st.bar_chart(category_totals.astype(float))

# Footer
st.markdown("---")
st.caption("Built with FastAPI and Streamlit | Handles network retries and page refreshes gracefully")
