"""
Seasonal Agriculture Performance Dashboard
Salendra Singh Yadav - Chitkara University, HP

Run with:  streamlit run dashboard.py
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Seasonal Agriculture Dashboard", layout="wide")

# ---------------------------------------------------------------
# Load & clean data (same cleaning logic as the notebook)
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("seasonal_agriculture_performance_dataset.csv")
    for col in ["Rainfall_mm", "Soil_Moisture_pct", "Yield_Tonnes_Ha"]:
        data[col] = data.groupby("Season")[col].transform(lambda x: x.fillna(x.median()))
    data["Season"] = data["Season"].str.strip()
    data["Crop"] = data["Crop"].str.strip()
    data["Irrigation_Method"] = data["Irrigation_Method"].str.strip()
    return data

df = load_data()
SEASON_ORDER = ["Kharif", "Rabi", "Zaid"]
SEASON_COLORS = {"Kharif": "#2C5F2D", "Rabi": "#97BC62", "Zaid": "#B85042"}

# ---------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------
st.sidebar.header("Filters")

season_filter = st.sidebar.multiselect(
    "Season", options=SEASON_ORDER, default=SEASON_ORDER
)

state_options = sorted(df["State"].unique())
state_filter = st.sidebar.multiselect(
    "State", options=state_options, default=[]
)

crop_options = sorted(df["Crop"].unique())
crop_filter = st.sidebar.multiselect(
    "Crop", options=crop_options, default=[]
)

irr_options = sorted(df["Irrigation_Method"].unique())
irr_filter = st.sidebar.multiselect(
    "Irrigation Method", options=irr_options, default=[]
)

filtered = df[df["Season"].isin(season_filter)] if season_filter else df.copy()
if state_filter:
    filtered = filtered[filtered["State"].isin(state_filter)]
if crop_filter:
    filtered = filtered[filtered["Crop"].isin(crop_filter)]
if irr_filter:
    filtered = filtered[filtered["Irrigation_Method"].isin(irr_filter)]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(filtered):,}** of {len(df):,} farm records")

# ---------------------------------------------------------------
# Header
# ---------------------------------------------------------------
st.title("🌾 Seasonal Agriculture Performance Dashboard")
st.caption("Explore how yield, profit and resource usage change across Kharif, Rabi and Zaid seasons.")

if filtered.empty:
    st.warning("No records match the selected filters. Try widening your selection.")
    st.stop()

# ---------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Farm Records", f"{len(filtered):,}")
col2.metric("Avg Yield (t/ha)", f"{filtered['Yield_Tonnes_Ha'].mean():.2f}")
col3.metric("Avg Profit (₹)", f"{filtered['Profit_INR'].mean():,.0f}")
col4.metric("Avg Disease/Pest Risk", f"{filtered['Disease_Pest_Risk_pct'].mean():.1f}%")

st.markdown("---")

# ---------------------------------------------------------------
# Row 1: Yield & Profit by season
# ---------------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

season_summary = (
    filtered.groupby("Season")[["Yield_Tonnes_Ha", "Profit_INR"]]
    .mean()
    .reindex([s for s in SEASON_ORDER if s in filtered["Season"].unique()])
    .reset_index()
)

with row1_col1:
    fig = px.bar(
        season_summary, x="Season", y="Yield_Tonnes_Ha", color="Season",
        color_discrete_map=SEASON_COLORS, text_auto=".2f",
        title="Average Yield by Season (t/ha)",
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with row1_col2:
    fig = px.bar(
        season_summary, x="Season", y="Profit_INR", color="Season",
        color_discrete_map=SEASON_COLORS, text_auto=".2s",
        title="Average Profit by Season (INR)",
    )
    fig.add_hline(y=0, line_color="black", line_width=1)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# Row 2: Irrigation profitability & Disease risk
# ---------------------------------------------------------------
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    irr_profit = (
        filtered.groupby(["Irrigation_Method", "Season"])["Profit_INR"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        irr_profit, x="Irrigation_Method", y="Profit_INR", color="Season",
        color_discrete_map=SEASON_COLORS, barmode="group",
        title="Average Profit by Irrigation Method",
    )
    fig.add_hline(y=0, line_color="black", line_width=1)
    st.plotly_chart(fig, use_container_width=True)

with row2_col2:
    disease = (
        filtered.groupby("Season")["Disease_Pest_Risk_pct"]
        .mean()
        .reindex([s for s in SEASON_ORDER if s in filtered["Season"].unique()])
        .reset_index()
    )
    fig = px.bar(
        disease, x="Season", y="Disease_Pest_Risk_pct", color="Season",
        color_discrete_map=SEASON_COLORS, text_auto=".1f",
        title="Average Disease/Pest Risk (%) by Season",
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# Row 3: Crop x Season heatmap & Yield vs Profit scatter
# ---------------------------------------------------------------
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    pivot = filtered.pivot_table(
        values="Yield_Tonnes_Ha", index="Crop", columns="Season", aggfunc="mean"
    )
    pivot = pivot[[s for s in SEASON_ORDER if s in pivot.columns]]
    fig = px.imshow(
        pivot, text_auto=".2f", color_continuous_scale="YlGn",
        title="Average Yield (t/ha) - Crop vs Season",
        aspect="auto",
    )
    st.plotly_chart(fig, use_container_width=True)

with row3_col2:
    sample = filtered.sample(min(1500, len(filtered)), random_state=42)
    fig = px.scatter(
        sample, x="Rainfall_mm", y="Yield_Tonnes_Ha", color="Season",
        color_discrete_map=SEASON_COLORS, opacity=0.6,
        title="Rainfall vs Yield",
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# Row 4: State-wise comparison
# ---------------------------------------------------------------
st.markdown("### State-wise Profit Comparison")
top_states = filtered["State"].value_counts().head(8).index
state_data = (
    filtered[filtered["State"].isin(top_states)]
    .groupby(["State", "Season"])["Profit_INR"]
    .mean()
    .reset_index()
)
fig = px.bar(
    state_data, x="State", y="Profit_INR", color="Season",
    color_discrete_map=SEASON_COLORS, barmode="group",
    title="Average Profit by State (Top 8 states by record count)",
)
fig.add_hline(y=0, line_color="black", line_width=1)
fig.update_xaxes(tickangle=-30)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# Raw data
# ---------------------------------------------------------------
with st.expander("View filtered raw data"):
    st.dataframe(filtered, use_container_width=True)
