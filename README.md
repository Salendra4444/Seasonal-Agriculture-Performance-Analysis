# Seasonal Agriculture Performance Analysis

**Salendra Singh Yadav** | Chitkara University, HP | AICTE STU ID: STU6a69a32dee0e41785307949

Data analytics project analyzing seasonal agriculture performance (Kharif, Rabi, Zaid) — covers yield, profit, irrigation efficiency and pest risk trends using Python, with an interactive Streamlit dashboard.

## Live Dashboard

🔗 **[View the live dashboard here](https://agri-performance-dashboard.streamlit.app/)**

## Files in this project

- `Seasonal_Agriculture_Performance_Analysis.ipynb` - the full analysis notebook (data cleaning, EDA, statistical tests, visualizations, insights and recommendations). Already run end-to-end, so all charts and outputs are visible without re-running anything.
- `dashboard.py` - the interactive Streamlit dashboard (deployed live above) for exploring the same dataset - filter by season/state/crop/irrigation and see the charts update live.
- `seasonal_agriculture_performance_dataset.csv` - the raw dataset used.
- `requirements.txt` - packages needed to run both files.

## How to run the notebook

```
pip install -r requirements.txt
jupyter notebook Seasonal_Agriculture_Performance_Analysis.ipynb
```

## How to run the dashboard locally (optional)

The dashboard is already live at the link above, but if you want to run it on your own machine:

```
pip install -r requirements.txt
streamlit run dashboard.py
```

This opens the dashboard in your browser (usually at `http://localhost:8501`). Use the sidebar to filter by season, state, crop or irrigation method - the KPIs and every chart update automatically.
