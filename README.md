# Seasonal Agriculture Performance Analysis

**Salendra Singh Yadav** | Chitkara University, HP | AICTE STU ID: STU6a69a32dee0e41785307949

## Files in this project

- `Seasonal_Agriculture_Performance_Analysis.ipynb` - the full analysis notebook (data cleaning, EDA, statistical tests, visualizations, insights and recommendations). Already run end-to-end, so all charts and outputs are visible without re-running anything.
- `dashboard.py` - an interactive Streamlit dashboard for exploring the same dataset (filter by season/state/crop/irrigation and see the charts update live).
- `seasonal_agriculture_performance_dataset.csv` - the raw dataset used.
- `requirements.txt` - packages needed to run both files.

## How to run the notebook

```
pip install -r requirements.txt
jupyter notebook Seasonal_Agriculture_Performance_Analysis.ipynb
```

## How to run the dashboard

```
pip install -r requirements.txt
streamlit run dashboard.py
```

This opens the dashboard in your browser (usually at http://localhost:8501). Use the sidebar to filter by season, state, crop or irrigation method - the KPIs and every chart update automatically.

