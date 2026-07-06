import plotly.express as px
import streamlit as st

from utils import load_data, yearly_sales, monthly_sales_trend, region_category_sales

st.set_page_config(page_title="Sales Overview", page_icon="📊", layout="wide")
st.title("📊 Sales Overview Dashboard")

df = load_data()

# --------------------------------------------------------------------
# Total sales by year
# --------------------------------------------------------------------
st.subheader("Total Sales by Year")
ys = yearly_sales(df)
fig_year = px.bar(
    ys, x="Year", y="Sales", text_auto=".2s",
    labels={"Sales": "Total Sales ($)"},
    color="Sales", color_continuous_scale="Blues",
)
fig_year.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig_year, use_container_width=True)

# --------------------------------------------------------------------
# Monthly sales trend
# --------------------------------------------------------------------
st.subheader("Monthly Sales Trend")
mst = monthly_sales_trend(df)
fig_trend = px.line(
    mst, x="Order Date", y="Sales", markers=True,
    labels={"Sales": "Total Sales ($)", "Order Date": "Month"},
)
st.plotly_chart(fig_trend, use_container_width=True)

# --------------------------------------------------------------------
# Sales by region & category (with interactive filters)
# --------------------------------------------------------------------
st.subheader("Sales by Region and Category")

col1, col2 = st.columns(2)
with col1:
    regions = st.multiselect(
        "Filter by Region", options=sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique()),
    )
with col2:
    categories = st.multiselect(
        "Filter by Category", options=sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique()),
    )

if not regions or not categories:
    st.warning("Select at least one Region and one Category to see results.")
else:
    rcs = region_category_sales(df, regions, categories)
    fig_rc = px.bar(
        rcs, x="Region", y="Sales", color="Category",
        barmode="group", text_auto=".2s",
        labels={"Sales": "Total Sales ($)"},
    )
    st.plotly_chart(fig_rc, use_container_width=True)

    with st.expander("View underlying data"):
        st.dataframe(rcs, use_container_width=True)
