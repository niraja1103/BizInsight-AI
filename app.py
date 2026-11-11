
import os
import time
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from google import genai

# =====================================
# 1. CONFIGURATION
# =====================================

load_dotenv()

st.set_page_config(
    page_title="BizInsight AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 BizInsight AI")
st.subheader("Your AI-powered Business Intelligence Analyst")

st.write(
    "Upload your business sales data and discover "
    "useful insights about your business."
)

# =====================================
# 2. GEMINI CONNECTION
# =====================================

api_key = os.getenv("GEMINI_API_KEY")
client = None

if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception:
        st.error("Could not initialize Gemini. Check your API setup.")

# =====================================
# 3. FILE UPLOAD
# =====================================

uploaded_file = st.file_uploader(
    "Upload your Excel or CSV file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is None:
    st.info("Please upload an Excel or CSV file to get started.")
    st.stop()

# =====================================
# 4. READ FILE
# =====================================

try:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.astype(str).str.strip()

except Exception as e:
    st.error(f"Unable to read your file: {e}")
    st.stop()

# =====================================
# 5. VALIDATE DATA
# =====================================

required_columns = ["Product", "Quantity", "Price", "Cost"]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )
    st.write("Required columns:", required_columns)
    st.stop()

if df.empty:
    st.error("Your file has no records.")
    st.stop()

for column in ["Quantity", "Price", "Cost"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=required_columns).copy()

df = df[
    (df["Quantity"] >= 0) &
    (df["Price"] >= 0) &
    (df["Cost"] >= 0)
].copy()

if df.empty:
    st.error("No valid sales records were found.")
    st.stop()

if "Category" not in df.columns:
    df["Category"] = "Uncategorized"

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# =====================================
# 6. BUSINESS CALCULATIONS
# =====================================

df["Revenue"] = df["Quantity"] * df["Price"]
df["Total Cost"] = df["Quantity"] * df["Cost"]
df["Profit"] = df["Revenue"] - df["Total Cost"]

total_revenue = df["Revenue"].sum()
total_cost = df["Total Cost"].sum()
total_profit = df["Profit"].sum()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue > 0 else 0
)

total_units = df["Quantity"].sum()

# =====================================
# 7. BUSINESS OVERVIEW
# =====================================

st.success("File uploaded successfully!")

st.header("📌 Business Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
c2.metric("Total Cost", f"₹{total_cost:,.2f}")
c3.metric("Gross Profit", f"₹{total_profit:,.2f}")
c4.metric("Profit Margin", f"{profit_margin:.2f}%")

c5, c6 = st.columns(2)

c5.metric("Total Records", len(df))
c6.metric("Units Sold", f"{total_units:,.0f}")

# =====================================
# 8. SALES DATA PREVIEW
# =====================================

st.header("📋 Sales Data Preview")
st.dataframe(df, use_container_width=True)

# =====================================
# 9. PRODUCT FILTER
# =====================================

st.header("🔎 Filter Your Products")

products = sorted(df["Product"].astype(str).unique())

selected_products = st.multiselect(
    "Select products",
    products,
    default=products
)

filtered_df = df[
    df["Product"].astype(str).isin(selected_products)
].copy()

if filtered_df.empty:
    st.warning("Please select at least one product.")
    st.stop()

# =====================================
# 10. PRODUCT PERFORMANCE
# =====================================

st.header("📊 Product Performance")

product_summary = (
    filtered_df.groupby("Product")
    .agg(
        Units_Sold=("Quantity", "sum"),
        Revenue=("Revenue", "sum"),
        Cost=("Total Cost", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

product_summary["Profit Margin (%)"] = (
    product_summary["Profit"] /
    product_summary["Revenue"].replace(0, float("nan")) * 100
).fillna(0)

st.dataframe(product_summary, use_container_width=True)

# =====================================
# 11. VISUAL ANALYTICS
# =====================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")

    fig1 = px.bar(
        product_summary,
        x="Product",
        y="Revenue",
        color="Product",
        title="Product Revenue"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Profit by Product")

    fig2 = px.bar(
        product_summary,
        x="Product",
        y="Profit",
        color="Product",
        title="Product Profit"
    )

    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales Quantity Distribution")

    fig3 = px.pie(
        product_summary,
        names="Product",
        values="Units_Sold"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Profit Margin by Product")

    fig4 = px.bar(
        product_summary,
        x="Product",
        y="Profit Margin (%)",
        color="Product"
    )

    st.plotly_chart(fig4, use_container_width=True)

# =====================================
# 12. BUSINESS RECOMMENDATIONS
# =====================================

st.header("💡 Business Recommendations")

best_selling = product_summary.loc[
    product_summary["Units_Sold"].idxmax()
]

most_profitable = product_summary.loc[
    product_summary["Profit"].idxmax()
]

least_profitable = product_summary.loc[
    product_summary["Profit"].idxmin()
]

st.write(
    f"1. Your business generated ₹{total_revenue:,.2f} in revenue."
)

st.write(
    f"2. Your gross profit is ₹{total_profit:,.2f}."
)

st.write(
    f"3. Your profit margin is {profit_margin:.2f}%."
)

st.write(
    f"4. {best_selling['Product']} has the highest sales quantity."
)

st.write(
    f"5. {most_profitable['Product']} generates the highest total profit."
)

st.write(
    f"6. Review the costs and pricing of "
    f"{least_profitable['Product']}."
)

# =====================================
# 13. AI BUSINESS ADVISOR
# =====================================

st.header("🤖 AI Business Advisor")

st.write(
    "Ask questions about your business "
    "and receive AI-generated recommendations."
)

if client is None:

    st.warning(
        "Gemini is not connected. Check your .env file "
        "and make sure GEMINI_API_KEY is configured."
    )

else:

    business_context = f"""
    You are BizInsight AI, a professional business analyst.

    Analyze this sales information:

    Total Revenue: ₹{total_revenue:,.2f}
    Total Cost: ₹{total_cost:,.2f}
    Gross Profit: ₹{total_profit:,.2f}
    Profit Margin: {profit_margin:.2f}%
    Units Sold: {total_units}

    Product Performance:
    {product_summary.to_string(index=False)}

    Instructions:
    - Explain business performance in simple language.
    - Give practical recommendations.
    - Identify products with low profitability.
    - Never invent missing business information.
    - Clearly mention when more data is required.
    """

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask something about your business..."
    )

    if question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing your business..."):

                answer = None
                last_error = None

                # Primary model and backup model
                models = [
                    "gemini-3.8-flash",
                    "gemini-3.5-flash-lite"
                ]

                for model in models:

                    for attempt in range(3):

                        try:

                            response = client.models.generate_content(
                                model=model,
                                contents=(
                                    business_context
                                    + "\n\nBusiness owner's question: "
                                    + question
                                )
                            )

                            answer = response.text

                            if answer:
                                break

                        except Exception as e:

                            last_error = e
                            error_text = str(e).upper()

                            if (
                                "503" in error_text
                                or "UNAVAILABLE" in error_text
                                or "429" in error_text
                                or "RESOURCE_EXHAUSTED" in error_text
                            ):

                                time.sleep(2 ** (attempt + 1))

                            else:
                                break

                    if answer:
                        break

                if answer:

                    st.markdown(answer)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })

                else:

                    st.error(
                        "Gemini is temporarily unavailable "
                        "or the request could not be completed."
                    )

                    st.caption(
                        "Please try again later. Check your API "
                        "quota and model availability if this continues."
                    )

                    if last_error:
                        st.caption(str(last_error))

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# =====================================
# 14. DOWNLOAD ANALYSIS
# =====================================

st.header("📥 Download Your Analysis")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Analysed Sales Data",
    data=csv_data,
    file_name="bizinsight_analysis.csv",
    mime="text/csv"
)

st.caption("BizInsight AI | Business Analytics Dashboard")
