import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def display_dashboard():
    # Generate mock sales data
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    n_products = 5
    products = ["Product A", "Product B", "Product C", "Product D", "Product E"]

    data = {
        "Date": np.repeat(dates, n_products),
        "Product": np.tile(products, len(dates)),
        "Sales": np.random.normal(1000, 200, len(dates) * n_products).round(2),
        "Units": np.random.randint(50, 200, len(dates) * n_products),
    }

    df = pd.DataFrame(data)

    # Add some seasonality to sales
    df["Sales"] = df["Sales"] * (
        1 + 0.3 * np.sin(2 * np.pi * (df["Date"].dt.month - 1) / 12)
    )

    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        total_sales = df["Sales"].sum()
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        total_units = df["Units"].sum()
        st.metric("Total Units Sold", f"{total_units:,}")
    with col3:
        avg_order = total_sales / total_units
        st.metric("Average Order Value", f"${avg_order:.2f}")

    # Time series plot
    st.subheader("Sales Trend Over Time")
    daily_sales = df.groupby(["Date", "Product"])["Sales"].sum().reset_index()
    fig_trend = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        color="Product",
        title="Daily Sales by Product",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # Product performance
    st.subheader("Product Performance")
    col1, col2 = st.columns(2)

    with col1:
        product_sales = df.groupby("Product")["Sales"].sum().reset_index()
        fig_pie = px.pie(
            product_sales,
            values="Sales",
            names="Product",
            title="Sales Distribution by Product",
        )
        st.plotly_chart(fig_pie)

    with col2:
        monthly_sales = (
            df.groupby([df["Date"].dt.strftime("%B"), "Product"])["Sales"]
            .sum()
            .reset_index()
        )
        monthly_sales.columns = ["Month", "Product", "Sales"]
        fig_bar = px.bar(
            monthly_sales,
            x="Month",
            y="Sales",
            color="Product",
            title="Monthly Sales by Product",
        )
        st.plotly_chart(fig_bar)

    # Interactive data table
    st.subheader("Detailed Sales Data")
    date_range = st.date_input(
        "Select Date Range",
        value=(df["Date"].min(), df["Date"].max()),
        min_value=df["Date"].min(),
        max_value=df["Date"].max(),
    )

    filtered_df = df[
        (df["Date"] >= pd.Timestamp(date_range[0]))
        & (df["Date"] <= pd.Timestamp(date_range[1]))
    ]
    st.dataframe(
        filtered_df.groupby("Product")
        .agg({"Sales": ["sum", "mean"], "Units": ["sum", "mean"]})
        .round(2)
    )


st.title("Sales Dashboard")
is_authenticated = st.context.headers.get("X-Auth")

if is_authenticated:
    st.subheader("Welcome!")
    display_dashboard()
else:
    st.subheader("Welcome, Guest")
    st.write("Please sign in to view the sales data.")
