---

## Abstract

Fraud detection in financial transactions is a high-stakes classification
problem characterised by extreme class imbalance, high cost of missed
detections, and strict regulatory requirements around explainability. This
project presents a complete, production-style machine learning pipeline built
on the ULB Credit Card Fraud dataset — 284,807 transactions of which only
492 (0.17%) are fraudulent.

The pipeline covers the full data science lifecycle. Raw transaction data is
enriched with four engineered features capturing time-of-day behaviour and
amount magnitude. The training set is rebalanced using SMOTE to prevent the
model from ignoring the minority fraud class. Four candidate models are trained
and evaluated — Logistic Regression, Random Forest, XGBoost, and LightGBM —
using ROC-AUC and Precision-Recall AUC as primary metrics, since standard
accuracy is misleading at this level of imbalance.

The best-performing model is selected automatically and explained using SHAP
(SHapley Additive exPlanations), which identifies the features most responsible
for each individual prediction. SHAP output is then passed to a DistilGPT-2
language model via Hugging Face, which converts technical feature contributions
into plain-English summaries accessible to non-technical stakeholders.

All results, trained models, evaluation charts, and SHAP plots are persisted
to disk and surfaced through an interactive Streamlit dashboard that supports
manual input, random sampling, and CSV upload for live fraud prediction.

| Property | Value |
|---|---|
| Dataset | ULB Credit Card Fraud — Kaggle |
| Total transactions | 284,807 |
| Fraud rate | 0.17% |
| Models compared | 4 |
| Primary metric | ROC-AUC |
| Explainability | SHAP + Hugging Face DistilGPT-2 |
| Interface | Streamlit dashboard |
| Pipeline entry point | `python main.py` |

---