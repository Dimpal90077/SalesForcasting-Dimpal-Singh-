import plotly.graph_objects as go
import streamlit as st

from utils import load_data, detect_anomalies

st.set_page_config(page_title="Anomaly Report", page_icon="🚨", layout="wide")
st.title("🚨 Anomaly Report")
st.caption("Weekly sales anomalies detected with Isolation Forest (contamination = 5%)")

df = load_data()
weekly = detect_anomalies(df)
anomalies = weekly[weekly["Is_Anomaly"]]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=weekly["Order Date"], y=weekly["Sales"], mode="lines", name="Weekly Sales",
    line=dict(color="royalblue"),
))
fig.add_trace(go.Scatter(
    x=anomalies["Order Date"], y=anomalies["Sales"], mode="markers", name="Anomaly",
    marker=dict(color="red", size=12, symbol="circle-open", line=dict(width=3)),
))
fig.update_layout(
    title="Weekly Sales with Detected Anomalies",
    xaxis_title="Date", yaxis_title="Sales ($)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig, use_container_width=True)

st.subheader(f"Detected Anomalies ({len(anomalies)} weeks)")
display_table = anomalies[["Order Date", "Sales"]].copy()
display_table["Order Date"] = display_table["Order Date"].dt.date
display_table["Sales"] = display_table["Sales"].map(lambda v: f"${v:,.2f}")
display_table = display_table.rename(columns={"Order Date": "Week Ending", "Sales": "Sales Value"})
st.dataframe(display_table, use_container_width=True, hide_index=True)
