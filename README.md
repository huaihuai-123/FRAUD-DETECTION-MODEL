我把一些东西修改了更方便cc使用
<img width="1774" height="887" alt="46a03974-6c15-41a9-85f0-c2d73092ea7c" src="https://github.com/user-attachments/assets/1c0be275-6b28-45fe-9ab1-a47bfc9b8123" />
<br>

# 💳 Fraud Detection AI — End-to-End ML System with SHAP + Hugging Face Explainability

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Gradient%20Boosting-00ADD8?style=for-the-badge)
![SHAP](https://img.shields.io/badge/SHAP-Explainability-purple?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00C853?style=for-the-badge)

**A production-style, end-to-end machine learning pipeline for detecting fraudulent credit card transactions — featuring a 4-model benchmark, SMOTE class balancing, SHAP per-prediction explainability, FLAN-T5 plain-English summaries, and an interactive Streamlit dashboard.**

[🔗 View Repository](https://github.com/ibtesaamaslam/Fraud-Detection-Model) · [🐛 Report Bug](https://github.com/ibtesaamaslam/Fraud-Detection-Model/issues) · [✨ Request Feature](https://github.com/ibtesaamaslam/Fraud-Detection-Model/issues)

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [8-Stage Pipeline](#-8-stage-pipeline)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [Feature Engineering](#-feature-engineering)
- [Models Trained](#-models-trained)
- [Evaluation Metrics](#-evaluation-metrics)
- [SHAP Explainability](#-shap-explainability)
- [Hugging Face Plain-English Explanations](#-hugging-face-plain-english-explanations)
- [Streamlit Dashboard](#-streamlit-dashboard)
- [Generated Outputs](#-generated-outputs)
- [Configuration](#-configuration)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Running the Dashboard](#-running-the-dashboard)
- [Requirements](#-requirements)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 📌 Project Overview

Credit card fraud costs the global financial system billions of dollars annually. Fraudulent transactions are rare — typically less than 0.2% of all activity — which makes detection extremely difficult using standard machine learning approaches. A naive model that simply predicts "legitimate" for every transaction would achieve over 99% accuracy while catching zero fraud cases.

This project builds a **complete, production-style AI pipeline** that:

- Ingests raw transaction data from the Kaggle Credit Card Fraud dataset
- Engineers meaningful features from raw inputs
- Handles the severe class imbalance using **SMOTE** (Synthetic Minority Oversampling Technique)
- Trains and benchmarks **four machine learning models** side by side
- Evaluates them using metrics designed for imbalanced classification
- Explains every prediction using **SHAP** (SHapley Additive exPlanations)
- Converts technical SHAP output into plain English using a **Hugging Face FLAN-T5** language model
- Presents everything through an interactive **Streamlit dashboard** with three input modes
- Auto-generates a full Markdown training report after every run

---

## ✨ Key Features

| Feature | Description |
|---|---|
| Multi-model training | Logistic Regression · Random Forest · XGBoost · LightGBM |
| Class imbalance handling | SMOTE resampling before training (configurable ratio) |
| Rigorous evaluation | ROC-AUC · PR-AUC · Precision · Recall · F1 |
| SHAP explainability | Per-prediction feature contribution breakdown |
| Human-readable explanations | FLAN-T5 narrates the SHAP output in plain English |
| Interactive UI | Streamlit dashboard — Manual · Random · CSV input modes |
| Reproducible pipeline | Seeded RNGs · saved scaler · saved feature name order |
| Centralized config | All paths and hyperparameters in one `config.py` |
| Automated reporting | Markdown report + metrics CSV generated after every run |

---

## 🔄 8-Stage Pipeline

Run the entire pipeline with a single command: `python main.py`

```
Raw CSV
│
▼
Stage 1 — Load Data
  Reads data/raw/transactions.csv · validates shape · logs fraud rate
│
▼
Stage 2 — EDA
  Class balance chart · amount histogram · time histogram · correlation heatmap
  → All charts saved to reports/figures/
│
▼
Stage 3 — Preprocessing
  Feature engineering (Amount_Log, Hour, Is_Night, Is_Large_Amount)
  → train/test split (80/20, stratified) → StandardScaler
  → saves scaler.pkl + feature_names.json to data/processed/
│
▼
Stage 4 — SMOTE Resampling
  Resamples fraud class to SMOTE_RATIO (default 0.2) of majority
  → prevents dominant legitimate class from biasing all models
│
▼
Stage 5 — Model Training
  Trains all 4 models on SMOTE-resampled training data
  → saves each model to models/
│
▼
Stage 6 — Evaluation
  Scores all models: ROC-AUC · PR-AUC · Precision · Recall · F1
  → ranks by ROC-AUC · saves best model to models/fraud_model.pkl
  → saves confusion matrix, ROC, PR, feature importance charts per model
│
▼
Stage 7 — Explainability
  SHAP values computed for best model
  → beeswarm summary plot saved → FLAN-T5 plain-English narration
│
▼
Stage 8 — Report
  Writes reports/report.md with full results table
  Writes reports/metrics.csv for downstream analysis
```

---

## 📂 Project Structure

```
fraud-detection-ai/
│
├── app/
│   └── streamlit_app.py            # Interactive Streamlit dashboard
│
├── data/
│   ├── raw/
│   │   └── transactions.csv        # ← Place Kaggle dataset here
│   ├── processed/
│   │   ├── X_train.csv             # Scaled training features
│   │   ├── X_test.csv              # Scaled test features
│   │   ├── y_train.csv             # Training labels
│   │   ├── y_test.csv              # Test labels
│   │   ├── scaler.pkl              # Fitted StandardScaler
│   │   └── feature_names.json      # Ordered feature column names
│   └── external/
│       └── huggingface_cache/      # Cached HF model weights
│
├── models/
│   ├── fraud_model.pkl             # Best model (selected by ROC-AUC)
│   ├── random_forest.pkl
│   ├── xgboost_model.pkl
│   └── lightgbm_model.pkl
│
├── notebooks/                      # Jupyter notebooks for exploration
│
├── reports/
│   ├── figures/                    # All generated charts
│   ├── report.md                   # Auto-generated training report
│   └── metrics.csv                 # Model comparison table
│
├── src/
│   ├── data/
│   │   ├── load_data.py            # Loads raw CSV from disk
│   │   ├── preprocess.py           # Cleaning, splitting, and scaling
│   │   └── feature_engineering.py  # Derives smart features from raw columns
│   │
│   ├── models/
│   │   ├── train_model.py          # Trains all candidate models
│   │   ├── evaluate_model.py       # Scores and ranks all models
│   │   ├── predict.py              # Single-transaction prediction pipeline
│   │   └── huggingface_model.py    # Hugging Face plain-English explanation
│   │
│   ├── explainability/
│   │   └── shap_explainer.py       # SHAP values and summary plots
│   │
│   ├── visualization/
│   │   ├── eda.py                  # Exploratory data analysis charts
│   │   └── plots.py                # Confusion matrix, ROC, PR, importance
│   │
│   └── utils/
│       ├── config.py               # All paths and hyperparameters
│       └── helpers.py              # Shared utility functions
│
├── main.py                         # Pipeline entry point
├── requirements.txt                # Python dependencies
├── project_structure.md            # Extended structure documentation
├── workflow.md                     # Pipeline workflow documentation
└── README.md
```

---

## 📦 Dataset

This project uses the **Credit Card Fraud Detection** dataset published by the Machine Learning Group at Université Libre de Bruxelles (ULB).

**Download:** [https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

**After downloading, rename and place at:** `data/raw/transactions.csv`

| Property | Value |
|---|---|
| Total Transactions | 284,807 |
| Fraudulent Transactions | 492 (0.17%) |
| Legitimate Transactions | 284,315 (99.83%) |
| Raw Features | 30 (Time · V1–V28 PCA · Amount) |
| Target Column | Class (0 = legitimate · 1 = fraud) |

> **Note:** The V1–V28 columns are PCA-transformed by the dataset authors to protect cardholder privacy. Original feature names are not available.

---

## 🔧 Feature Engineering

Four smart features are derived from the raw dataset in `src/data/feature_engineering.py`:

| Feature | Source | Description |
|---|---|---|
| `Amount_Log` | Amount | Log-transformed transaction amount — handles the wide right-skewed distribution |
| `Hour` | Time | Hour of day extracted from the Unix-style Time column (0–23) |
| `Is_Night` | Hour | Binary flag: 1 if transaction happened between 10 PM and 6 AM |
| `Is_Large_Amount` | Amount | Binary flag: 1 if Amount > $200 (configurable via `LARGE_AMOUNT_THRESHOLD`) |

---

## 🤖 Models Trained

All models are trained on SMOTE-resampled data where the fraud class is resampled to 20% of the majority class size (`SMOTE_RATIO = 0.2`).

| Model | Key Settings | Class Imbalance Strategy |
|---|---|---|
| Logistic Regression | `max_iter=2000` | `class_weight=balanced` |
| Random Forest | `n_estimators=200` | `class_weight=balanced_subsample` |
| XGBoost | `n_estimators=200` · `learning_rate=0.05` · `max_depth=5` | SMOTE pre-training |
| LightGBM | `n_estimators=200` · `learning_rate=0.05` | SMOTE pre-training |

---

## 📊 Evaluation Metrics

Standard accuracy is deliberately excluded from model selection — a model predicting "legitimate" for every transaction would achieve 99.83% accuracy while catching zero fraud.

| Metric | Purpose | Used For |
|---|---|---|
| **ROC-AUC** | Ranking quality across all thresholds | ✅ Primary model selection |
| **PR-AUC** | Best metric for severely imbalanced datasets | ✅ Model selection |
| **Precision** | Of all flagged transactions, how many were actual fraud | ✅ Business impact |
| **Recall** | Of all actual fraud cases, how many were caught | ✅ Business impact |
| **F1 Score** | Harmonic mean of precision and recall | ✅ Balanced comparison |
| Accuracy | Reference only | ❌ Not used for selection |

---

## 🔍 SHAP Explainability

Fraud detection systems must be explainable — regulators and end users need to understand why a specific transaction was flagged.

SHAP assigns each feature a contribution score for every individual prediction:
- **Positive score** → pushes the model toward predicting fraud
- **Negative score** → pushes the model toward predicting legitimate

**Example SHAP output:**

```
V14           (-2.341) → pushes toward safe     🟢
Amount_Log    (+1.823) → pushes toward fraud     🔴
Hour          (+0.912) → pushes toward fraud     🔴
V17           (-0.748) → pushes toward safe      🟢
V4            (+0.631) → pushes toward fraud     🔴
```

**Generated SHAP outputs:**
- Per-prediction top feature contributions (shown in the Streamlit dashboard)
- Global beeswarm summary plot saved to `reports/figures/shap_summary.png`

---

## 🤖 Hugging Face Plain-English Explanations

The SHAP feature summary is passed as a structured prompt to **FLAN-T5**, which generates a short, beginner-friendly explanation of the model's decision.

**Example output:**
```
"This transaction looks suspicious because the amount is unusually large for
this time of day, and several anonymised signals are elevated. The model
estimated a fraud risk of 0.91."
```

If the Hugging Face model is unavailable (no internet or download fails), a clean, readable static fallback explanation is returned automatically.

---

## 📊 Streamlit Dashboard

Once `main.py` has completed at least once, launch the interactive dashboard:

```bash
streamlit run app/streamlit_app.py
```

**Three input modes:**

| Mode | Description | Best For |
|---|---|---|
| Manual | Type raw transaction values into the form directly | Testing specific or hypothetical transactions |
| Random Sample | Picks a random row from the test dataset | Quick demo on real data |
| Upload CSV | Upload a single-row CSV file | Integration testing |

**Every prediction shows:**
- Fraud probability score (0.00 – 1.00)
- Risk level: Low / Medium / High
- Pass ✅ or Fail 🚨 banner
- FLAN-T5 plain-English explanation
- Top SHAP feature contributions ranked by absolute impact

---

## 📁 Generated Outputs

After running `main.py`, the following are created automatically:

| File | Description |
|---|---|
| `data/processed/X_train.csv` | Scaled training feature matrix |
| `data/processed/X_test.csv` | Scaled test feature matrix |
| `data/processed/scaler.pkl` | Fitted StandardScaler for inference |
| `data/processed/feature_names.json` | Ordered feature column list |
| `models/fraud_model.pkl` | Best model selected by ROC-AUC |
| `models/random_forest.pkl` | Saved Random Forest |
| `models/xgboost_model.pkl` | Saved XGBoost |
| `models/lightgbm_model.pkl` | Saved LightGBM |
| `reports/figures/class_balance.png` | Fraud vs legitimate count chart |
| `reports/figures/correlation_heatmap.png` | Feature correlation heatmap |
| `reports/figures/*_confusion_matrix.png` | Confusion matrix per model |
| `reports/figures/*_roc_curve.png` | ROC curve per model |
| `reports/figures/*_pr_curve.png` | Precision-Recall curve per model |
| `reports/figures/*_feature_importance.png` | Feature importance per model |
| `reports/figures/shap_summary.png` | SHAP beeswarm plot for best model |
| `reports/report.md` | Full Markdown training summary |
| `reports/metrics.csv` | Model comparison table (CSV) |

---

## ⚙️ Configuration

All paths and hyperparameters are centralised in `src/utils/config.py`. Nothing is hardcoded elsewhere.

| Setting | Default | Description |
|---|---|---|
| `RANDOM_STATE` | `42` | Seeds all RNGs — ensures full reproducibility |
| `TEST_SIZE` | `0.2` | Fraction of data reserved for evaluation |
| `THRESHOLD` | `0.5` | Minimum probability to classify as fraud |
| `SMOTE_RATIO` | `0.2` | Fraud class target ratio after resampling |
| `LARGE_AMOUNT_THRESHOLD` | `200.0` | USD threshold for `Is_Large_Amount` flag |
| `HF_MODEL_NAME` | `google/flan-t5-base` | Hugging Face model for explanation generation |

---

## 🚀 Installation

**1. Clone the repository:**
```bash
git clone https://github.com/ibtesaamaslam/Fraud-Detection-Model.git
cd Fraud-Detection-Model
```

**2. Create a virtual environment (recommended):**
```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Place the dataset:**

Download `creditcard.csv` from Kaggle, rename it to `transactions.csv`, and place at:
```
data/raw/transactions.csv
```

---

## ▶️ Running the Project

Run the full 8-stage pipeline:

```bash
python main.py
```

This executes all stages in order and produces:
- Processed data in `data/processed/`
- Trained models in `models/`
- EDA and evaluation charts in `reports/figures/`
- Final report at `reports/report.md`

---

## 📊 Running the Dashboard

After `main.py` completes:

```bash
streamlit run app/streamlit_app.py
```

→ Opens at [http://localhost:8501](http://localhost:8501)

---

## 📋 Requirements

```
pandas
numpy
scikit-learn
imbalanced-learn
xgboost
lightgbm
shap
transformers
joblib
matplotlib
seaborn
streamlit
tabulate
```

```bash
pip install -r requirements.txt
```

---

## 🗺️ Roadmap

- [ ] FastAPI endpoint — expose `/predict` for banking system integration
- [ ] LIME explainability — add alongside SHAP for comparison
- [ ] Threshold optimisation — auto-tune decision threshold by maximising F1
- [ ] Deep learning baseline — neural network benchmark vs tree models
- [ ] Drift detection — flag when retraining is needed
- [ ] Docker containerisation — Dockerfile for reproducible deployment
- [ ] MLflow experiment tracking — log all runs and metrics
- [ ] Hugging Face Spaces deployment — public demo

---

## 📜 License

```
MIT License — Copyright (c) 2024 Ibtesaam Aslam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies, subject to the copyright notice appearing in all copies.
Provided "as is" — without warranty of any kind.
```

---

<div align="center">

Built with ❤️ by **[Ibtesaam Aslam](https://github.com/ibtesaamaslam)**

⭐ If this project helped you learn fraud detection or ML pipelines, please give it a star!

*Explainable AI for financial fraud detection.*

</div>
