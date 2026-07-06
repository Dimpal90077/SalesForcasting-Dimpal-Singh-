"""
Shared data loading and modeling utilities for the Superstore Sales
Analytics Streamlit app. All heavy computation is cached so pages load fast.
"""

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

DATA_PATH = "train.csv"


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
    df = df.drop_duplicates()

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.month_name()
    df["Quarter"] = df["Order Date"].dt.quarter

    return df


# --------------------------------------------------------------------------
# Page 1 helpers
# --------------------------------------------------------------------------
@st.cache_data
def yearly_sales(df):
    return df.groupby("Year")["Sales"].sum().reset_index()


@st.cache_data
def monthly_sales_trend(df):
    monthly = (
        df.set_index("Order Date")["Sales"]
        .resample("ME")
        .sum()
        .reset_index()
    )
    return monthly


@st.cache_data
def region_category_sales(df, regions, categories):
    filtered = df[df["Region"].isin(regions) & df["Category"].isin(categories)]
    grouped = (
        filtered.groupby(["Region", "Category"])["Sales"]
        .sum()
        .reset_index()
    )
    return grouped


# --------------------------------------------------------------------------
# Page 2 helpers — XGBoost forecasting (best model per notebook Task 3)
# --------------------------------------------------------------------------
def _get_season(month):
    if month in [12, 1, 2]:
        return 0
    elif month in [3, 4, 5]:
        return 1
    elif month in [6, 7, 8]:
        return 2
    return 3


def _build_feature_frame(monthly_series):
    """monthly_series: a Series indexed by month-end date, values = Sales."""
    frame = monthly_series.to_frame(name="Sales")
    frame["Lag_1"] = frame["Sales"].shift(1)
    frame["Lag_2"] = frame["Sales"].shift(2)
    frame["Lag_3"] = frame["Sales"].shift(3)
    frame["Rolling_Mean_3"] = frame["Sales"].rolling(window=3).mean()
    frame["Month"] = frame.index.month
    frame["Quarter"] = frame.index.quarter
    frame["Season"] = frame["Month"].apply(_get_season)
    return frame


FEATURE_COLS = ["Lag_1", "Lag_2", "Lag_3", "Rolling_Mean_3", "Month", "Quarter", "Season"]


@st.cache_data
def get_filtered_monthly_series(df, dimension, value):
    """dimension: 'Overall' | 'Category' | 'Region'. value: e.g. 'Furniture'."""
    if dimension == "Overall":
        subset = df
    else:
        subset = df[df[dimension] == value]
    monthly = subset.groupby("Order Date")["Sales"].sum().resample("ME").sum()
    return monthly


@st.cache_data
def train_and_forecast(df, dimension, value, horizon):
    """
    Trains an XGBoost regressor on lag/seasonal features for the selected
    Category/Region/Overall series, backtests on the last 3 actual months
    (MAE/RMSE), then recursively forecasts `horizon` months beyond the
    last available date.
    """
    monthly = get_filtered_monthly_series(df, dimension, value)
    feat = _build_feature_frame(monthly).dropna()

    if len(feat) < 8:
        return None  # not enough history for this slice

    X = feat[FEATURE_COLS]
    y = feat["Sales"]

    # --- Backtest on last 3 months (same methodology as notebook) ---
    X_train, X_test = X[:-3], X[-3:]
    y_train, y_test = y[:-3], y[-3:]

    backtest_model = XGBRegressor(
        n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42
    )
    backtest_model.fit(X_train, y_train)
    test_pred = backtest_model.predict(X_test)

    mae = mean_absolute_error(y_test, test_pred)
    rmse = np.sqrt(mean_squared_error(y_test, test_pred))

    # --- Refit on ALL available data, then recursively forecast forward ---
    final_model = XGBRegressor(
        n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42
    )
    final_model.fit(X, y)

    history = monthly.copy()
    future_dates = []
    future_preds = []

    for _ in range(horizon):
        feat_full = _build_feature_frame(history).dropna()
        last_row = feat_full[FEATURE_COLS].iloc[[-1]]
        next_date = history.index[-1] + pd.offsets.MonthEnd(1)
        next_pred = final_model.predict(last_row)[0]

        future_dates.append(next_date)
        future_preds.append(next_pred)

        history.loc[next_date] = next_pred

    return {
        "history": monthly,
        "test_dates": y_test.index,
        "test_actual": y_test.values,
        "test_pred": test_pred,
        "future_dates": pd.DatetimeIndex(future_dates),
        "future_pred": np.array(future_preds),
        "mae": mae,
        "rmse": rmse,
    }


# --------------------------------------------------------------------------
# Page 3 helpers — Anomaly detection (Isolation Forest, Task 5)
# --------------------------------------------------------------------------
@st.cache_data
def detect_anomalies(df):
    daily_sales = df.groupby("Order Date")["Sales"].sum().reset_index()
    weekly_sales = (
        daily_sales.set_index("Order Date")
        .resample("W")["Sales"]
        .sum()
        .reset_index()
    )

    iso = IsolationForest(contamination=0.05, random_state=42)
    weekly_sales["Anomaly"] = iso.fit_predict(weekly_sales[["Sales"]])
    weekly_sales["Is_Anomaly"] = weekly_sales["Anomaly"] == -1

    return weekly_sales


# --------------------------------------------------------------------------
# Page 4 helpers — Product demand segmentation (KMeans, Task 6)
# --------------------------------------------------------------------------
CLUSTER_NAMES = {
    0: "High Volume, Stable Demand",
    1: "Growing Demand",
    2: "Low Volume, High Volatility",
    3: "Declining Demand",
}


@st.cache_data
def build_clusters(df):
    monthly = (
        df.groupby(["Sub-Category", pd.Grouper(key="Order Date", freq="ME")])["Sales"]
        .sum()
        .reset_index()
    )

    total_sales = monthly.groupby("Sub-Category")["Sales"].sum()

    monthly["Year"] = monthly["Order Date"].dt.year
    yearly_sales_pivot = monthly.groupby(["Sub-Category", "Year"])["Sales"].sum().unstack()
    growth_rate = (
        (yearly_sales_pivot.iloc[:, -1] - yearly_sales_pivot.iloc[:, 0])
        / yearly_sales_pivot.iloc[:, 0]
    ) * 100

    volatility = monthly.groupby("Sub-Category")["Sales"].std()
    avg_order = df.groupby("Sub-Category")["Sales"].mean()

    cluster_df = pd.DataFrame(
        {
            "Total_Sales": total_sales,
            "Growth_Rate": growth_rate,
            "Volatility": volatility,
            "Average_Order_Value": avg_order,
        }
    ).fillna(0)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(cluster_df)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    cluster_df["Cluster"] = kmeans.fit_predict(scaled)
    cluster_df["Cluster_Name"] = cluster_df["Cluster"].map(CLUSTER_NAMES)

    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(scaled)
    cluster_df["PC1"] = pca_features[:, 0]
    cluster_df["PC2"] = pca_features[:, 1]

    cluster_df = cluster_df.reset_index().rename(columns={"index": "Sub-Category"})
    return cluster_df
