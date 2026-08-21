# Expense Roaster AI — Technical Design Document

## 1. Project Overview

Expense Roaster AI is an AI-powered personal expense analytics application developed using Streamlit, Python, Pandas, Plotly, and Google Gemini.

The application allows users to upload monthly expense data in CSV format, analyzes the data using Pandas, visualizes spending patterns through interactive charts, and uses Gemini AI to generate a personalized spending analysis and budget recovery plan.

---

## 2. Problem Statement

Many users track their expenses without clearly understanding where their money is being spent.

Traditional expense trackers generally provide numerical information but may not provide personalized explanations or actionable recommendations.

Expense Roaster AI addresses this problem by combining data analytics with generative AI.

The application analyzes expense patterns and converts the results into understandable recommendations and a practical budget recovery strategy.

---

## 3. Objectives

The main objectives are:

* Analyze monthly expense data.
* Calculate important financial KPIs.
* Visualize spending patterns.
* Identify high-spending categories.
* Provide AI-powered spending analysis.
* Generate a personalized budget recovery plan.
* Provide an interactive and user-friendly dashboard.
* Deploy the application as a cloud-based Streamlit application.

---

## 4. Technology Stack

### Python

Python is used as the primary programming language for application logic and data processing.

### Streamlit

Streamlit provides the web interface and interactive dashboard.

### Pandas

Pandas is used for:

* CSV processing
* Data cleaning
* Aggregation
* Expense calculations
* Category analysis

### Plotly

Plotly is used to create interactive:

* Bar charts
* Pie charts
* Line charts

### Google Gemini

Gemini provides generative AI capabilities for:

* Expense roasting
* Spending analysis
* Budget recommendations
* Recovery planning

### GitHub

GitHub is used for source-code management and project version control.

### Streamlit Community Cloud

Streamlit Community Cloud is used to host the deployed application.

---

## 5. System Architecture

```text
                    USER
                      |
                      v
              STREAMLIT INTERFACE
                      |
          +-----------+-----------+
          |                       |
          v                       v
      CSV UPLOAD           FINANCIAL INPUT
          |                 Income/Savings
          v                       |
     PANDAS PROCESSING            |
          |                       |
          +-----------+-----------+
                      |
                      v
              DATA ANALYSIS
                      |
          +-----------+-----------+
          |                       |
          v                       v
     KPI CALCULATIONS       CATEGORY ANALYSIS
          |                       |
          +-----------+-----------+
                      |
                      v
              PROMPT BUILDER
                      |
                      v
              GOOGLE GEMINI
                      |
          +-----------+-----------+
          |                       |
          v                       v
     AI EXPENSE ROAST       BUDGET PLAN
          |                       |
          +-----------+-----------+
                      |
                      v
              STREAMLIT OUTPUT
```

---

## 6. Data Flow

The application's data flow follows these stages:

### Stage 1 — Data Input

The user uploads a monthly expense CSV through Streamlit.

The application expects the following fields:

* Date
* Category
* Description
* Amount
* Payment_Method

### Stage 2 — Data Processing

The uploaded CSV is converted into a Pandas DataFrame.

The application converts:

* Date values into datetime format.
* Amount values into numeric format.

Invalid rows missing required analytical values are removed.

### Stage 3 — Data Analysis

Pandas is used to calculate:

* Total spending
* Average expense
* Highest expense
* Transaction count
* Category-wise spending
* Daily spending

### Stage 4 — Visualization

Processed data is displayed through interactive Plotly charts.

The dashboard includes:

* Spending by category
* Expense distribution
* Daily spending trend

### Stage 5 — AI Processing

Relevant expense information is dynamically inserted into a Gemini prompt.

The prompt contains actual information from the user's expense dataset.

Gemini analyzes the information and generates personalized recommendations.

### Stage 6 — Output

The AI results are displayed through the Streamlit interface.

The application provides:

* Expense roast
* Spending problems
* Reduction recommendations
* Budget recovery plan
* Savings recommendations
* Weekly spending strategy

---

## 7. Gemini API Integration

The application uses Google's Gemini API through the `google-genai` Python SDK.

The Gemini client is initialized using a securely stored API key.

The API key is accessed through Streamlit Secrets rather than being hard-coded in the application.

The application dynamically constructs prompts based on the user's expense data.

This allows Gemini to respond to the actual financial information rather than producing generic responses.

---

## 8. Prompt Engineering Strategy

The application uses role-based prompting.

Gemini is instructed to act as a specialized personal finance analyst and coach.

The prompt contains:

* Total spending
* Highest spending category
* Category-wise expenses
* Expense records
* Monthly income
* Desired savings

The AI is instructed to:

1. Analyze actual expense data.
2. Identify major spending problems.
3. Provide practical recommendations.
4. Create a realistic recovery plan.
5. Avoid generic financial advice.
6. Adapt recommendations for a college student.

This dynamic context makes the AI output specific to the user's data.

---

## 9. Session State Management

Streamlit's `st.session_state` is used to preserve important application data across interactions.

The application maintains:

* Uploaded expense DataFrame
* AI expense roast
* AI budget recovery plan

This prevents important results from being lost during Streamlit reruns.

---

## 10. Form-Based API Calls

The budget planning interface uses `st.form`.

The user enters:

* Monthly income
* Desired savings

The Gemini API call is triggered only after the user submits the form.

This prevents unnecessary API calls during input changes.

---

## 11. Security

The Gemini API key is stored using Streamlit Secrets.

The local secrets file is excluded from Git using `.gitignore`.

The API key is therefore not stored inside the public source code.

Sensitive credentials should never be committed to the GitHub repository.

---

## 12. Error Handling

The application performs validation before processing uploaded expense data.

It checks whether the required CSV columns are available.

The application also handles invalid date and amount values during data processing.

If the required information is missing, the user receives an appropriate Streamlit error message.

---

## 13. Deployment Architecture

```text
GitHub Repository
       |
       v
Streamlit Community Cloud
       |
       +---- requirements.txt
       |
       +---- app.py
       |
       +---- Streamlit Secrets
       |
       v
Live Web Application
```

The application is deployed using Streamlit Community Cloud.

The Gemini API key is configured separately through deployment secrets.

---

## 14. Project Modules

### Dashboard Module

Responsible for:

* CSV upload
* Data validation
* KPI calculation
* Data visualization
* Expense table

### AI Analysis Module

Responsible for:

* Expense summarization
* Dynamic prompt construction
* Gemini API interaction
* Spending roast

### Budget Module

Responsible for:

* Income input
* Savings goal input
* Budget calculations
* Gemini budget recovery plan

### State Management Module

Responsible for maintaining:

* Expense data
* AI results
* User session information

---

## 15. Future Enhancements

Potential future improvements include:

* Automatic detection of different CSV column names.
* Receipt image analysis using Gemini Vision.
* Monthly expense forecasting.
* Expense anomaly detection.
* Downloadable PDF budget reports.
* Voice-based expense entry.
* Personalized financial dashboards.
* User authentication.
* Historical expense tracking.

---

## 16. Conclusion

Expense Roaster AI demonstrates the integration of data analytics, interactive visualization, and generative artificial intelligence within a Streamlit application.

The project transforms raw expense records into visual insights and personalized AI-generated recommendations.

The architecture separates data processing, visualization, AI analysis, and budget planning into logical modules, making the application easier to maintain and extend.
