import plotly.express as px
import streamlit as st

from utils import load_data, build_clusters

st.set_page_config(page_title="Product Demand Segments", page_icon="🧩", layout="wide")
st.title("🧩 Product Demand Segments")
st.caption("K-Means clustering (k=4) of sub-categories on Total Sales, Growth Rate, Volatility, and Average Order Value")

df = load_data()
clusters = build_clusters(df)

fig = px.scatter(
    clusters, x="PC1", y="PC2", color="Cluster_Name", text="Sub-Category",
    size="Total_Sales", size_max=40,
    labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2"},
    title="Product Demand Segmentation (PCA projection)",
)
fig.update_traces(textposition="top center")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sub-Categories by Demand Cluster")
table = clusters[
    ["Sub-Category", "Cluster_Name", "Total_Sales", "Growth_Rate", "Volatility", "Average_Order_Value"]
].sort_values(["Cluster_Name", "Total_Sales"], ascending=[True, False]).copy()

table["Total_Sales"] = table["Total_Sales"].map(lambda v: f"${v:,.0f}")
table["Growth_Rate"] = table["Growth_Rate"].map(lambda v: f"{v:,.1f}%")
table["Volatility"] = table["Volatility"].map(lambda v: f"${v:,.0f}")
table["Average_Order_Value"] = table["Average_Order_Value"].map(lambda v: f"${v:,.2f}")
table = table.rename(columns={"Cluster_Name": "Demand Cluster"})

st.dataframe(table, use_container_width=True, hide_index=True)

with st.expander("What do these clusters mean?"):
    st.markdown(
        """
        - **High Volume, Stable Demand** — top sellers with low volatility; keep well-stocked at all times.
        - **Growing Demand** — fastest sales growth; gradually increase inventory and monitor closely.
        - **Low Volume, High Volatility** — unpredictable, lower-selling items; stock conservatively, order on demand.
        - **Declining Demand** — shrinking sales; reduce inventory commitments and reassess assortment.
        """
    )
