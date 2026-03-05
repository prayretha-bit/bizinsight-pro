import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BizInsight Pro", layout="wide")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📊 BizInsight Pro")
page = st.sidebar.radio("Navigation",
                        ["Executive Dashboard",
                         "Sales Analytics",
                         "Segment Insights"])

# ---------------------------------------------------
# EXECUTIVE DASHBOARD
# ---------------------------------------------------
if page == "Executive Dashboard":

    st.title("Executive Dashboard")

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_quantity = df["Quantity"].sum()
    profit_margin = (total_profit / total_sales) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"${total_sales:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Total Quantity Sold", total_quantity)
    col4.metric("Profit Margin", f"{profit_margin:.2f}%")

    st.markdown("---")

    region_sales = df.groupby("Region")["Sales"].sum().reset_index()

    fig = px.bar(region_sales,
                 x="Region",
                 y="Sales",
                 title="Sales by Region")

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# SALES ANALYTICS
# ---------------------------------------------------
elif page == "Sales Analytics":

    st.title("Sales Analytics")

    category_filter = st.multiselect(
        "Select Category",
        df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[df["Category"].isin(category_filter)]

    col1, col2 = st.columns(2)

    category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig1 = px.bar(category_sales,
                  x="Category",
                  y="Sales",
                  title="Sales by Category")

    col1.plotly_chart(fig1, use_container_width=True)

    subcategory_profit = filtered_df.groupby("Sub-Category")["Profit"].sum().reset_index()
    fig2 = px.bar(subcategory_profit,
                  x="Sub-Category",
                  y="Profit",
                  title="Profit by Sub-Category")

    col2.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# SEGMENT INSIGHTS
# ---------------------------------------------------
elif page == "Segment Insights":

    st.title("Customer Segment Insights")

    segment_sales = df.groupby("Segment")["Sales"].sum().reset_index()

    fig = px.pie(segment_sales,
                 names="Segment",
                 values="Sales",
                 title="Sales Distribution by Segment")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top 10 Profitable States")

    top_states = df.groupby("State")["Profit"].sum() \
                   .sort_values(ascending=False) \
                   .head(10) \
                   .reset_index()

    st.dataframe(top_states)