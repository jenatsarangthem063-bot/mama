import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="Factory Optimization Dashboard",
    page_icon="🏭",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Nassau_Data.csv")

    if "Lead Time" not in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
        df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
        df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

    if "Profit Margin" not in df.columns:
        df["Profit Margin"] = (
            df["Gross Profit"] / df["Sales"]
        ) * 100

    return df

df = load_data()

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("🏭 Factory Reallocation & Shipping Optimization Recommendation System")

st.markdown(
"""
Analyze shipping performance, sales, gross profit,
lead time and factory optimization recommendations.
"""
)

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

division = st.sidebar.multiselect(
    "Division",
    sorted(df["Division"].unique()),
    default=sorted(df["Division"].unique())
)

ship_mode = st.sidebar.multiselect(
    "Ship Mode",
    sorted(df["Ship Mode"].unique()),
    default=sorted(df["Ship Mode"].unique())
)

country = st.sidebar.multiselect(
    "Country",
    sorted(df["Country/Region"].unique()),
    default=sorted(df["Country/Region"].unique())
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Division"].isin(division)) &
    (df["Ship Mode"].isin(ship_mode)) &
    (df["Country/Region"].isin(country))
]

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Orders",
    len(filtered_df)
)

col2.metric(
    "Total Sales",
    f"${filtered_df['Sales'].sum():,.2f}"
)

col3.metric(
    "Total Gross Profit",
    f"${filtered_df['Gross Profit'].sum():,.2f}"
)

col4.metric(
    "Average Lead Time",
    f"{filtered_df['Lead Time'].mean():.2f} Days"
)

col5, col6, col7 = st.columns(3)

col5.metric(
    "Average Profit Margin",
    f"{filtered_df['Profit Margin'].mean():.2f}%"
)

col6.metric(
    "Average Sales",
    f"${filtered_df['Sales'].mean():,.2f}"
)

col7.metric(
    "Average Units Sold",
    f"{filtered_df['Units'].mean():.2f}"
)

st.divider()
# -------------------------------------------------
# SALES BY REGION
# -------------------------------------------------
st.subheader("📈 Sales by Region")

sales_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    color="Region",
    title="Sales by Region"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------
# SALES BY DIVISION
# -------------------------------------------------
st.subheader("🍫 Sales by Division")

sales_division = (
    filtered_df.groupby("Division")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    sales_division,
    names="Division",
    values="Sales",
    title="Sales Distribution by Division"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# SHIP MODE ANALYSIS
# -------------------------------------------------
st.subheader("🚚 Orders by Ship Mode")

ship_mode_df = (
    filtered_df.groupby("Ship Mode")
    .size()
    .reset_index(name="Orders")
)

fig3 = px.bar(
    ship_mode_df,
    x="Ship Mode",
    y="Orders",
    color="Ship Mode",
    title="Orders by Ship Mode"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# LEAD TIME DISTRIBUTION
# -------------------------------------------------
st.subheader("⏳ Lead Time Distribution")

fig4 = px.histogram(
    filtered_df,
    x="Lead Time",
    nbins=20,
    title="Lead Time Distribution"
)

st.plotly_chart(fig4, use_container_width=True)
