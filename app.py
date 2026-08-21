import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

st.set_page_config(
    page_title="Expense Roaster AI",
    page_icon="💰",
    layout="wide"
)

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame()

st.title("💰 Expense Roaster AI")
st.caption("AI-Powered Personal Expense Analytics")

st.sidebar.title("Dashboard")

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "AI Analysis", "Budget Plan"]
)

if page == "Dashboard":

    st.header("📊 Expense Dashboard")

    uploaded_file = st.file_uploader(
        "Upload your expense CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        required_columns = [
            "Date",
            "Category",
            "Description",
            "Amount",
            "Payment_Method"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            st.error(
                f"Missing columns: {', '.join(missing_columns)}"
            )
            st.stop()

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["Date", "Amount"]
        )

        st.session_state.expenses = df

        total_spending = df["Amount"].sum()
        average_expense = df["Amount"].mean()
        highest_expense = df["Amount"].max()
        transaction_count = len(df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "💰 Total Spending",
                f"₹{total_spending:,.2f}"
            )

        with col2:
            st.metric(
                "📊 Average Expense",
                f"₹{average_expense:,.2f}"
            )

        with col3:
            st.metric(
                "🔥 Highest Expense",
                f"₹{highest_expense:,.2f}"
            )

        with col4:
            st.metric(
                "🧾 Transactions",
                transaction_count
            )

        st.divider()

        st.subheader("📈 Spending Analysis")

        col1, col2 = st.columns(2)

        category_data = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
            .sort_values(
                "Amount",
                ascending=False
            )
        )

        with col1:

            fig = px.bar(
                category_data,
                x="Category",
                y="Amount",
                title="Spending by Category",
                labels={
                    "Amount": "Amount (₹)",
                    "Category": "Category"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            fig = px.pie(
                category_data,
                names="Category",
                values="Amount",
                title="Expense Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        daily_data = (
            df.groupby("Date")["Amount"]
            .sum()
            .reset_index()
        )

        st.subheader("📅 Daily Spending")

        fig = px.line(
            daily_data,
            x="Date",
            y="Amount",
            markers=True,
            title="Daily Expense Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("📋 Expense Records")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Upload a CSV file to start analyzing your expenses."
        )

elif page == "AI Analysis":

    st.header("🤖 AI Expense Analysis")

    if st.session_state.expenses.empty:

        st.warning(
            "Please upload an expense CSV first."
        )

    else:

        df = st.session_state.expenses

        total_spending = df["Amount"].sum()

        category_data = (
            df.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        top_category = category_data.index[0]
        top_category_amount = category_data.iloc[0]

        expense_summary = df[
            ["Date", "Category", "Description", "Amount"]
        ].to_string(index=False)

        prompt = f"""
You are Expense Roaster AI, an expert personal finance analyst.

Analyze the user's expense data.

Total spending: ₹{total_spending:,.2f}

Highest spending category:
{top_category}

Amount spent in highest category:
₹{top_category_amount:,.2f}

Expense records:
{expense_summary}

Your response must contain:

1. A brutally honest but humorous roast of the user's spending.
2. The three biggest spending problems.
3. Specific ways to reduce unnecessary spending.
4. A realistic budget recovery plan.
5. Three actionable goals for next month.

Use the actual data provided.
Do not give generic advice.
Keep the recommendations practical for a student.
"""

        if st.button("🔥 Roast My Spending"):

            with st.spinner("Gemini is analyzing your spending..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.subheader("🔥 Your Expense Roast")

            st.write(response.text)

elif page == "Budget Plan":

    st.header("💡 AI Budget Recovery Plan")

    if st.session_state.expenses.empty:

        st.warning(
            "Please upload an expense CSV first."
        )

    else:

        df = st.session_state.expenses

        total_spending = df["Amount"].sum()

        category_data = (
            df.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        top_category = category_data.index[0]
        top_category_amount = category_data.iloc[0]

        st.subheader("📊 Your Spending Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Spending",
                f"₹{total_spending:,.2f}"
            )

        with col2:
            st.metric(
                "Highest Category",
                top_category
            )

        with col3:
            st.metric(
                "Highest Category Spending",
                f"₹{top_category_amount:,.2f}"
            )

        st.divider()

        st.subheader("💰 Generate Your Recovery Plan")

        with st.form("budget_form"):

            monthly_income = st.number_input(
                "Monthly Income (₹)",
                min_value=0.0,
                value=30000.0,
                step=1000.0
            )

            savings_goal = st.number_input(
                "Desired Monthly Savings (₹)",
                min_value=0.0,
                value=5000.0,
                step=500.0
            )

            submitted = st.form_submit_button(
                "🚀 Generate Budget Plan"
            )

        if submitted:

            remaining_money = monthly_income - total_spending

            expense_summary = (
                category_data
                .to_string()
            )

            prompt = f"""
You are Expense Roaster AI, a strict but helpful
personal finance coach for a college student.

Analyze the following financial information.

Monthly income:
₹{monthly_income:,.2f}

Current monthly spending:
₹{total_spending:,.2f}

Desired monthly savings:
₹{savings_goal:,.2f}

Money remaining after current spending:
₹{remaining_money:,.2f}

Spending by category:
{expense_summary}

Create a strict but realistic budget recovery plan.

Your response must include:

1. Financial health assessment.
2. Biggest spending problem.
3. Categories that should be reduced.
4. Suggested spending limits for major categories.
5. How much the user should save.
6. A weekly spending strategy.
7. Three specific actions to take immediately.
8. A short motivational conclusion.

Use the actual numbers provided.
Do not give generic financial advice.
Keep the plan realistic for a college student.
"""

            with st.spinner(
                "Gemini is creating your recovery plan..."
            ):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.success(
                "Your personalized budget recovery plan is ready!"
            )

            with st.expander(
                "💡 View Your AI Budget Recovery Plan",
                expanded=True
            ):

                st.write(response.text)            