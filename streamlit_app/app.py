import streamlit as st
from utils import load_data

st.set_page_config(
    page_title="Superstore Sales Analytics",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Superstore Sales Analytics Dashboard")
st.caption("Sales overview, forecasting, anomaly detection, and product segmentation")

with st.spinner("Loading data..."):
    df = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
col2.metric("Orders", f"{df['Order ID'].nunique():,}")
col3.metric("Date Range", f"{df['Order Date'].min().date()} → {df['Order Date'].max().date()}")
col4.metric("Regions", df["Region"].nunique())

st.markdown("---")
st.markdown(
    """
    ### Use the sidebar to navigate:

    - **📊 Sales Overview** — yearly totals, monthly trend, and region/category breakdowns with filters
    - **🔮 Forecast Explorer** — XGBoost sales forecasts by Category or Region, with MAE/RMSE
    - **🚨 Anomaly Report** — Isolation Forest anomaly detection on weekly sales
    - **🧩 Product Segments** — K-Means clustering of sub-categories into demand groups
    """
)

st.dataframe(df.head(20), use_container_width=True)
