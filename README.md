# 📈 Sales Forecasting & Business Analytics Dashboard

> **Predict Tomorrow's Sales with Data-Driven Insights 🚀**

An end-to-end **Sales Forecasting & Business Analytics Dashboard** built using **Python, Machine Learning, Time Series Forecasting, and Streamlit**.

This project analyzes historical Superstore sales data, forecasts future sales, detects anomalies, segments products based on demand, and provides an interactive dashboard to support business decision-making.

---

# 🌐 Live Demo

🚀 **Streamlit App:**  
👉(https://ex2huxpjq2jwu5rytxmmec.streamlit.app/)

💻 **GitHub Repository:**  
👉 https://github.com/Dimpal90077/SalesForcasting-Dimpal-Singh-

---

# 🎯 Problem Statement

Businesses generate thousands of sales transactions every day, but making strategic decisions from this data can be challenging.

Some common business questions include:

- 📈 Will sales increase or decrease in the coming months?
- 🛒 Which product category contributes the highest revenue?
- 🌍 Which region performs the best?
- 🚨 Are there unusual spikes or drops in sales?
- 📦 Which products should be stocked more?
- 💰 How can inventory planning be improved?

Without proper analysis and forecasting, businesses may:

- Overstock slow-moving products
- Run out of high-demand products
- Miss seasonal opportunities
- Increase operational costs
- Lose revenue due to poor planning

This project addresses these challenges using Data Analytics and Machine Learning techniques.

---

# 💡 Solution Approach

This project follows a complete end-to-end Data Analytics workflow.

## 📥 Step 1 — Data Collection

The Superstore Sales dataset is loaded using **Pandas**.

The dataset contains:

- Orders
- Products
- Customers
- Sales
- Profit
- Regions
- Categories
- Shipping Information

---

## 🧹 Step 2 — Data Cleaning

The dataset is prepared by:

- ✅ Removing duplicate records
- ✅ Handling missing values
- ✅ Converting date columns into datetime format
- ✅ Creating new features:
  - Year
  - Month
  - Quarter
  - Week
  - Day
  - Season

---

## 📊 Step 3 — Exploratory Data Analysis (EDA)

The data is analyzed to answer important business questions, such as:

- Which category generates the highest revenue?
- Which region performs the best?
- Which months record the highest sales?
- Is there any seasonal sales pattern?

Interactive charts help visualize these insights.

---

## ⏳ Step 4 — Time Series Analysis

Monthly sales are transformed into a time series to understand historical behavior.

Analysis includes:

- 📈 Monthly Sales Trend
- 📉 Time Series Decomposition
  - Trend
  - Seasonality
  - Residual
- 📊 Stationarity Testing using the ADF Test

These steps prepare the data for forecasting.

---

## 🤖 Step 5 — Sales Forecasting

Three forecasting models are developed and compared.

### 📉 SARIMA

A statistical forecasting model that captures:

- Trend
- Seasonality
- Historical patterns

### 🔮 Facebook Prophet

Automatically models:

- Long-term trends
- Yearly seasonality
- Holiday effects

### 🚀 XGBoost Regressor

A machine learning model trained using engineered features:

- Lag 1
- Lag 2
- Lag 3
- Rolling Mean
- Month
- Quarter
- Season

The models are evaluated using:

- MAE
- RMSE
- MAPE

The best-performing model is selected based on evaluation metrics rather than personal preference.

---

## 🚨 Step 6 — Anomaly Detection

Unusual sales spikes and drops are detected using:

- 🌲 Isolation Forest
- 📊 Z-Score Detection

Possible causes include:

- Festival sales
- Heavy discounts
- Supply shortages
- Unexpected customer demand

---

## 📦 Step 7 — Product Demand Segmentation

Products are grouped into demand-based clusters using **K-Means Clustering**.

Demand groups include:

- 📦 High Volume, Stable Demand
- 📈 Growing Demand
- ⚡ Low Volume, High Volatility
- 📉 Declining Demand

This helps improve inventory planning and stock management.

---

## 🌐 Step 8 — Interactive Dashboard

The complete analysis is deployed using **Streamlit**.

Users can:

- 📊 Explore sales trends
- 🔮 Generate forecasts
- 🚨 Detect anomalies
- 📦 Analyze product demand

through an easy-to-use web dashboard.

---

# 🛠️ Tech Stack

| Category | Tools |
|----------|--------|
| Programming | 🐍 Python |
| Data Analysis | 📊 Pandas, NumPy |
| Visualization | 📉 Matplotlib, Seaborn, Plotly |
| Statistical Forecasting | 📈 SARIMA (Statsmodels) |
| Business Forecasting | 🔮 Facebook Prophet |
| Machine Learning | 🚀 XGBoost |
| Clustering | 🎯 K-Means |
| Anomaly Detection | 🌲 Isolation Forest, Z-Score |
| Dashboard | 🌐 Streamlit |

---

# 📂 Project Structure

```text
streamlit_app/
│
├── app.py
├── utils.py
├── train.csv
├── requirements.txt
│
└── pages/
    ├── 📊 Sales Overview
    ├── 🔮 Forecast Explorer
    ├── 🚨 Anomaly Report
    └── 🧩 Product Segments
```

---

# 📊 Dashboard Features

## 📊 Sales Overview

- Total Sales by Year
- Monthly Sales Trend
- Interactive Region Filter
- Interactive Category Filter

---

## 🔮 Forecast Explorer

- Category-wise Forecast
- Region-wise Forecast
- Forecast Horizon (1–3 Months)
- Model Performance (MAE & RMSE)

---

## 🚨 Anomaly Report

- Weekly Sales Trend
- Isolation Forest Detection
- Z-Score Detection
- Anomaly Table

---

## 🧩 Product Demand Segmentation

- K-Means Cluster Visualization
- Product Cluster Table
- Demand Classification

---

# 🤖 Machine Learning Models Used

| Model | Purpose |
|--------|----------|
| 📉 SARIMA | Statistical Time Series Forecasting |
| 🔮 Prophet | Trend & Seasonality Forecasting |
| 🚀 XGBoost | Machine Learning Forecasting |
| 🌲 Isolation Forest | Sales Anomaly Detection |
| 🎯 K-Means | Product Demand Segmentation |

---

# 📌 Key Business Insights

- ✔ Identified top-performing product categories
- ✔ Forecasted future monthly sales
- ✔ Compared multiple forecasting models
- ✔ Detected seasonal sales patterns
- ✔ Identified unusual sales spikes and drops
- ✔ Segmented products based on demand
- ✔ Built an interactive analytics dashboard

---

# ▶️ Getting Started

## Clone the Repository

```bash
git clone https://github.com/Dimpal90077/SalesForcasting-Dimpal-Singh-.git
```

## Navigate to the Project

```bash
cd SalesForcasting-Dimpal-Singh-
```

## Install Dependencies

```bash
pip install -r streamlit_app/requirements.txt
```

## Run the Application

```bash
cd streamlit_app
streamlit run app.py
```

---

# 🚀 Future Improvements

- 🤖 LSTM-based Deep Learning Forecasting
- ☁️ Cloud Database Integration
- 📈 Real-Time Sales Prediction
- 📊 Advanced KPI Dashboard
- 📱 Mobile-Friendly Interface

---

# 👩‍💻 About Me

**Dimpal Kumari Singh**

🎓 B.Tech Student

📊 Aspiring Data Analyst

🤖 Machine Learning Enthusiast

💻 Passionate about Data Analytics, Business Intelligence, and AI.

📧 Email: your-email@example.com

🔗 LinkedIn: https://www.linkedin.com/in/your-linkedin/

🔗 GitHub: https://github.com/Dimpal90077

🌐 Streamlit App: https://your-streamlit-app.streamlit.app

---

# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.

Your support motivates me to build and share more Data Science, Machine Learning, and Business Analytics projects.
