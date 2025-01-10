import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Sales Performance Dashboard")

# Generate sample data
np.random.seed(42)
date_range = pd.date_range(
    start=datetime.now() - timedelta(days=365), end=datetime.now(), freq="D"
)
sales_data = pd.DataFrame(
    {
        "Date": date_range,
        "Sales": np.random.normal(1000, 200, len(date_range)),
        "Region": np.random.choice(["North", "South", "East", "West"], len(date_range)),
        "Product": np.random.choice(
            ["Electronics", "Clothing", "Food", "Books"], len(date_range)
        ),
    }
)

# Create three columns for KPIs
col1, col2, col3 = st.columns(3)

with col1:
    total_sales = sales_data["Sales"].sum()
    st.metric("Total Sales", f"${total_sales:,.2f}")

with col2:
    avg_daily_sales = sales_data["Sales"].mean()
    st.metric("Average Daily Sales", f"${avg_daily_sales:,.2f}")

with col3:
    recent_trend = (
        sales_data["Sales"].iloc[-7:].mean() - sales_data["Sales"].iloc[-14:-7].mean()
    )
    st.metric(
        "Weekly Trend",
        f"${recent_trend:,.2f}",
        delta=f"{recent_trend/avg_daily_sales*100:.1f}%",
    )

# Create two columns for charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Sales Trend Over Time")
    fig_trend = px.line(
        sales_data, x="Date", y="Sales", title="Daily Sales Performance"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("Sales by Region")
    fig_region = px.pie(
        sales_data, values="Sales", names="Region", title="Regional Sales Distribution"
    )
    st.plotly_chart(fig_region, use_container_width=True)

# Product Performance
st.subheader("Product Category Performance")
product_sales = sales_data.groupby("Product")["Sales"].sum().reset_index()
fig_product = px.bar(
    product_sales, x="Product", y="Sales", title="Sales by Product Category"
)
st.plotly_chart(fig_product, use_container_width=True)

# Add filters in sidebar
st.sidebar.title("Filters")
selected_region = st.sidebar.multiselect(
    "Select Region",
    options=sales_data["Region"].unique(),
    default=sales_data["Region"].unique(),
)

selected_product = st.sidebar.multiselect(
    "Select Product",
    options=sales_data["Product"].unique(),
    default=sales_data["Product"].unique(),
)

date_range = st.sidebar.date_input(
    "Select Date Range", [sales_data["Date"].min(), sales_data["Date"].max()]
)

st.sidebar.markdown("[Logout](/logout)")


# Footer
st.markdown("---")
st.markdown("*Dashboard created with Streamlit - Sample Data*")
