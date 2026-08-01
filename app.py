import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Factory Optimization Dashboard",
    page_icon="🏭",
    layout="wide"
)


# LOAD DATA
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


# TITLE
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

# KPI CARDS
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

# SALES BY REGION

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


# SALES BY DIVISION
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

# SHIP MODE ANALYSIS
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

# LEAD TIME DISTRIBUTION
st.subheader("⏳ Lead Time Distribution")

fig4 = px.histogram(
    filtered_df,
    x="Lead Time",
    nbins=20,
    title="Lead Time Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

# PROFIT VS SALES
st.subheader("💰 Sales vs Gross Profit")

fig5 = px.scatter(
    filtered_df,
    x="Sales",
    y="Gross Profit",
    color="Division",
    size="Units",
    hover_name="Product Name",
    title="Sales vs Gross Profit"
)

st.plotly_chart(fig5, use_container_width=True)

# TOP 10 PRODUCTS

st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig6 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top 10 Products"
)

st.plotly_chart(fig6, use_container_width=True)

# FACTORY PERFORMANCE
if "Factory" in filtered_df.columns:

    st.subheader("🏭 Factory Performance")

    factory_df = (
        filtered_df.groupby("Factory")
        .agg({
            "Sales": "sum",
            "Gross Profit": "sum",
            "Lead Time": "mean"
        })
        .reset_index()
    )

    st.dataframe(factory_df)

# DATA TABLE
st.subheader("📄 Complete Dataset")

st.dataframe(filtered_df)

# DOWNLOAD BUTTON
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="Filtered_Data.csv",
    mime="text/csv"
)

# PROJECT INSIGHTS
st.subheader("📌 Key Insights")

st.markdown(f"""
- **Total Orders:** {len(filtered_df)}
- **Total Sales:** ${filtered_df['Sales'].sum():,.2f}
- **Total Gross Profit:** ${filtered_df['Gross Profit'].sum():,.2f}
- **Average Lead Time:** {filtered_df['Lead Time'].mean():.2f} days
- **Average Profit Margin:** {filtered_df['Profit Margin'].mean():.2f}%
- Use the sidebar filters to analyze different regions, divisions and shipping modes.
""")
# FACTORY RECOMMENDATION DASHBOARD
st.subheader("🏭 Factory Recommendation Dashboard")

factory_summary = (
    filtered_df.groupby("Factory")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Lead Time", "mean")
    )
    .reset_index()
)

st.dataframe(factory_summary)

# WHAT-IF SCENARIO ANALYSIS

st.subheader("🔄 What-If Scenario Analysis")

product = st.selectbox(
    "Select Product",
    sorted(filtered_df["Product Name"].unique())
)

scenario = filtered_df[
    filtered_df["Product Name"] == product
]

st.write("### Selected Product Details")
st.dataframe(scenario)

st.metric(
    "Average Lead Time",
    f"{scenario['Lead Time'].mean():.2f} Days"
)

st.metric(
    "Average Profit",
    f"${scenario['Gross Profit'].mean():,.2f}"
)

# RISK PANEL

st.subheader("⚠️ Risk & Impact Panel")

high_risk = filtered_df[
    filtered_df["Lead Time"] >
    filtered_df["Lead Time"].mean()
]

st.metric(
    "High Risk Orders",
    len(high_risk)
)

st.dataframe(high_risk.head(20))

# EXECUTIVE SUMMARY

st.subheader("📋 Executive Summary")

st.success("""
✔ Sales and profit trends are displayed.

✔ Shipping performance is monitored.

✔ Lead time analysis identifies slow deliveries.

✔ Factory performance helps identify optimization opportunities.

✔ Dashboard supports business decision making.
""")
# OPTIMIZATION RECOMMENDATIONS

st.subheader("🎯 Optimization Recommendations")

recommendations = filtered_df.groupby("Factory").agg(
    Average_Lead_Time=("Lead Time", "mean"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum")
).reset_index()

recommendations["Recommendation"] = recommendations["Average_Lead_Time"].apply(
    lambda x: "Optimize Route" if x > recommendations["Average_Lead_Time"].mean()
    else "Current Factory is Efficient"
)

st.dataframe(recommendations)

# DASHBOARD FOOTER

st.markdown("---")

st.caption(
    "Factory Reallocation & Shipping Optimization Recommendation System | "
    "Developed using Streamlit, Python, Pandas and Plotly"
)

# ABOUT THE PROJECT

st.markdown("---")

st.header("📖 About the Project")

st.write("""
This dashboard was developed as part of the Unified Mentor Internship Project.

The objective is to analyze shipping performance, sales, profitability,
and factory allocation for Nassau Candy Distributor.

Using interactive visualizations and recommendation logic, the dashboard
helps identify opportunities to reduce lead time, improve operational
efficiency, and support better factory allocation decisions.
""")

st.markdown("---")

st.success("✅ Dashboard Completed Successfully")
