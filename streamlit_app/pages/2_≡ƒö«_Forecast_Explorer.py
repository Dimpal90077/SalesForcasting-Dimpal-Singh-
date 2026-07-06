import plotly.graph_objects as go
import streamlit as st

from utils import load_data, train_and_forecast

st.set_page_config(page_title="Forecast Explorer", page_icon="🔮", layout="wide")
st.title("🔮 Forecast Explorer")
st.caption("Forecasts generated with the best-performing model from analysis: **XGBoost**")

df = load_data()

# --------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1.5, 1.5])

with col1:
    dimension = st.selectbox("Forecast by", ["Overall", "Category", "Region"])

with col2:
    if dimension == "Category":
        value = st.selectbox("Select Category", sorted(df["Category"].unique()))
    elif dimension == "Region":
        value = st.selectbox("Select Region", sorted(df["Region"].unique()))
    else:
        value = None
        st.selectbox("Select Category", ["(all data)"], disabled=True)

with col3:
    horizon = st.select_slider(
        "Forecast horizon (months ahead)", options=[1, 2, 3], value=3
    )

# --------------------------------------------------------------------
# Run forecast
# --------------------------------------------------------------------
result = train_and_forecast(df, dimension, value, horizon)

if result is None:
    st.error("Not enough historical data for this selection to build a reliable forecast.")
else:
    history = result["history"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history.index, y=history.values, mode="lines", name="Historical Sales",
        line=dict(color="royalblue"),
    ))
    fig.add_trace(go.Scatter(
        x=result["test_dates"], y=result["test_actual"], mode="markers", name="Actual (holdout)",
        marker=dict(color="green", size=9),
    ))
    fig.add_trace(go.Scatter(
        x=result["test_dates"], y=result["test_pred"], mode="markers+lines", name="Backtest Prediction",
        marker=dict(color="orange", size=9), line=dict(dash="dot", color="orange"),
    ))
    fig.add_trace(go.Scatter(
        x=result["future_dates"], y=result["future_pred"], mode="markers+lines",
        name=f"Forecast (next {horizon} month{'s' if horizon > 1 else ''})",
        marker=dict(color="red", size=10), line=dict(dash="dash", color="red"),
    ))

    label = "Overall" if dimension == "Overall" else f"{dimension}: {value}"
    fig.update_layout(
        title=f"Sales Forecast — {label}",
        xaxis_title="Date", yaxis_title="Sales ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Forecasted Values")
    forecast_table = {
        "Month": [d.strftime("%b %Y") for d in result["future_dates"]],
        "Forecasted Sales ($)": [f"{v:,.2f}" for v in result["future_pred"]],
    }
    st.table(forecast_table)

    st.subheader("Model Performance (Backtest on last 3 known months)")
    m1, m2 = st.columns(2)
    m1.metric("MAE", f"${result['mae']:,.2f}")
    m2.metric("RMSE", f"${result['rmse']:,.2f}")
    st.caption(
        "MAE/RMSE are computed by holding out the last 3 actual months as a test "
        "set — the same methodology used during model evaluation."
    )
