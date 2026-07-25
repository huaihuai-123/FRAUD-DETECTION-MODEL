import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

from src.data.feature_engineering import create_features
from src.models.huggingface_model import generate_explanation
from src.utils.config import (
    BEST_MODEL_PATH,
    FEATURE_NAMES_PATH,
    LGBM_MODEL_PATH,
    RAW_DATA_PATH,
    SCALER_PATH,
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Fraud Detection AI Terminal",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------
# CUSTOM STYLING
# -----------------------------------
st.markdown("""
<style>
body { background-color: #0e1117; }
.block-container { padding-top: 1rem; }
h1, h2, h3 { color: #00D9FF; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown("# 🧠 Fraud Detection AI Terminal")
st.markdown("### Real-time AI Risk Analysis • Trading Style Dashboard")

# -----------------------------------
# LAZY-LOAD ARTEFACTS
# -----------------------------------

@st.cache_resource
def load_model():
    """Load the best available model (prefer pipeline-selected best)."""
    path = str(BEST_MODEL_PATH) if BEST_MODEL_PATH.exists() else str(LGBM_MODEL_PATH)
    return joblib.load(path), Path(path).stem


@st.cache_resource
def load_scaler():
    return joblib.load(SCALER_PATH)


@st.cache_resource
def load_feature_names():
    import json
    with FEATURE_NAMES_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


@st.cache_data
def load_data():
    return pd.read_csv(RAW_DATA_PATH)


model, model_name = load_model()
scaler = load_scaler()
feature_names = load_feature_names()
df = load_data()

# -----------------------------------
# GUARD: empty dataset
# -----------------------------------
if len(df) == 0:
    st.error("No data loaded. Place transactions.csv at data/raw/transactions.csv")
    st.stop()

# -----------------------------------
# TOP STATS BAR
# -----------------------------------
colA, colB, colC, colD = st.columns(4)
colA.metric("Total Transactions", f"{len(df):,}")
colB.metric("Fraud Cases", f"{df['Class'].sum():,}")
colC.metric("Features", df.shape[1])
colD.metric("Model", model_name.replace("_", " ").title())

st.divider()

# -----------------------------------
# MAIN DASHBOARD (3 COLUMNS)
# -----------------------------------
col1, col2, col3 = st.columns([2, 3, 2])

# -----------------------------------
# LEFT PANEL — DATA CONTROL
# -----------------------------------
with col1:
    st.markdown("## 📂 Data Control")
    txn_id = st.slider("Select Transaction", 0, len(df) - 1, 0)
    selected_txn = df.iloc[txn_id]
    st.markdown("### 📄 Transaction Data")
    st.dataframe(selected_txn.to_frame().T, use_container_width=True)
    run_btn = st.button("⚡ Run AI Analysis")

# -----------------------------------
# PREPROCESSING HELPER
# -----------------------------------
def preprocess_for_inference(raw_row: pd.Series) -> np.ndarray:
    """Apply the same feature-engineering + scaling as the training pipeline."""
    row_dict = raw_row.to_dict()
    if "Class" in row_dict:
        del row_dict["Class"]
    df = pd.DataFrame([row_dict])
    df = create_features(df)
    df = df.reindex(columns=feature_names, fill_value=0)
    return scaler.transform(df)


# -----------------------------------
# CENTER PANEL — FRAUD GAUGE
# -----------------------------------
with col2:
    st.markdown("## 📊 Risk Engine")

    if run_btn:
        input_data = preprocess_for_inference(selected_txn)
        prob = float(model.predict_proba(input_data)[0, 1])

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={"text": "Fraud Risk %"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00D9FF"},
                "steps": [
                    {"range": [0, 50], "color": "#00FF9C"},
                    {"range": [50, 80], "color": "#FFA500"},
                    {"range": [80, 100], "color": "#FF3B3B"},
                ],
            },
        ))
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# RIGHT PANEL — VERDICT
# -----------------------------------
with col3:
    st.markdown("## 🧾 Decision")

    if run_btn:
        pred = int(model.predict(input_data)[0])
        if pred == 1:
            st.error("🚨 FRAUD DETECTED")
        else:
            st.success("✅ SAFE TRANSACTION")
        st.metric("Confidence", f"{prob * 100:.2f}%")

# -----------------------------------
# AI EXPLANATION
# -----------------------------------
st.divider()

if run_btn:
    st.markdown("## 🤖 AI Financial Explanation")
    # Pass engineered features (not raw PCA values) to the explainer
    engineered = create_features(pd.DataFrame([selected_txn.to_dict()]).drop(columns=["Class"] if "Class" in selected_txn.index else []))
    explanation = generate_explanation(engineered.iloc[0], pred, prob)
    st.write(explanation)

# -----------------------------------
# DATASET INSIGHTS
# -----------------------------------
st.divider()
st.markdown("## 📊 Dataset Insights")

col4, col5 = st.columns(2)

with col4:
    fraud_counts = df["Class"].value_counts()
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Safe", "Fraud"], values=fraud_counts.values, hole=0.5,
    )])
    fig_pie.update_layout(title="Fraud Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

with col5:
    @st.cache_data
    def cached_corr():
        return df.corr()

    corr = cached_corr()
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.columns.tolist(),
        colorscale="RdBu",
    ))
    fig_heatmap.update_layout(title="Feature Correlation Heatmap")
    st.plotly_chart(fig_heatmap, use_container_width=True)

# -----------------------------------
# FOOTER
# -----------------------------------
st.divider()
st.markdown("Built with AI • Streamlit • LightGBM • Hugging Face")
