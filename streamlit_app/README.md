# Superstore Sales Analytics Dashboard

A 4-page Streamlit app built from the sales analysis notebook:

1. **Sales Overview** — yearly totals, monthly trend, region/category filters
2. **Forecast Explorer** — XGBoost forecasts by Category/Region with MAE & RMSE
3. **Anomaly Report** — Isolation Forest anomaly detection on weekly sales
4. **Product Segments** — K-Means clustering of sub-categories into demand groups

## Files

```
streamlit_app/
├── app.py                          # Home page
├── utils.py                        # Shared data loading & model logic
├── train.csv                       # Dataset
├── requirements.txt                # Dependencies for Streamlit Cloud
└── pages/
    ├── 1_📊_Sales_Overview.py
    ├── 2_🔮_Forecast_Explorer.py
    ├── 3_🚨_Anomaly_Report.py
    └── 4_🧩_Product_Segments.py
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud (free)

1. **Create a GitHub repo**
   - Go to https://github.com/new, create a new repository (e.g. `superstore-dashboard`), public or private.
   - Upload every file/folder above into the repo root, **keeping the `pages/` folder structure and file names exactly as-is** (Streamlit uses the filenames for sidebar navigation and ordering).
   - Easiest way: on your computer, `git init`, `git add .`, `git commit -m "Streamlit dashboard"`, then `git remote add origin <your-repo-url>` and `git push -u origin main`. Or just drag-and-drop the files via GitHub's web "Add file → Upload files" button.

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io and sign in with your GitHub account.
   - Click **"New app"**.
   - Select your repository, branch (`main`), and set the **Main file path** to `app.py`.
   - Click **Deploy**.
   - Streamlit Cloud will install everything in `requirements.txt` automatically and launch the app. First deploy takes ~2–3 minutes.

3. **Get your live link**
   - Once deployed, your app is live at a URL like `https://<your-app-name>.streamlit.app` — this is the link to submit.

### Notes
- `train.csv` is bundled in the repo so the app is self-contained — no external database or API needed.
- If you update the code later, just push to GitHub — Streamlit Cloud auto-redeploys.
- If the app goes to sleep from inactivity (free tier), the next visitor just needs to click "Yes, wake it up".
