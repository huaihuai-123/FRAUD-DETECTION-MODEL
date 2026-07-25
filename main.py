# main.py
# -------
# Main entry point that runs the full project pipeline.
# Think of it like the boss that tells all the other files what to do.

import joblib

from src.data.load_data import load_data
from src.data.preprocess import preprocess_data
from src.explainability.shap_explainer import save_shap_summary_plot
from src.models.evaluate_model import evaluate_models
from src.models.train_model import train_models
from src.utils.config import BEST_MODEL_PATH, METRICS_PATH, RANDOM_STATE, REPORT_PATH
from src.utils.helpers import ensure_project_directories, save_text, set_seed
from src.visualization.eda import run_eda
from src.visualization.plots import save_feature_importance_plot


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(best_model_name: str, metrics_df) -> None:
    """Generate and save a Markdown summary report after training completes.

    Captures the best model name, the full model comparison table, and a
    summary of the key pipeline decisions made during training.

    Args:
        best_model_name: Name of the top-ranked model by ROC-AUC score.
        metrics_df:      DataFrame of all model metrics as returned by evaluate_models().
    """
    # Build the markdown report as a multi-line f-string for readability
    report = f"""# Fraud Detection AI Report

## Best Model
**{best_model_name}**

## Model Comparison
{metrics_df.to_markdown(index=False)}

## Notes
- The model was trained on processed and scaled transaction data.
- SMOTE was used to balance the fraud class.
- SHAP was used to explain predictions.
- Hugging Face was used to turn technical reasons into human-friendly language.
"""
    # Persist the report to disk so it can be reviewed without re-running
    save_text(report, REPORT_PATH)


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------

def run_pipeline() -> None:
    """Execute the full fraud detection pipeline from raw data to saved artefacts.

    Think of it like the boss that tells all the other files what to do.
    Runs every stage in order and persists all outputs to disk so the
    Streamlit app can load them without re-training.

    Pipeline stages:
        1) Initialise directories and seed the random-number generators.
        2) Load the raw transaction CSV from disk.
        3) Run EDA and save exploratory charts.
        4) Preprocess — feature engineering, train/test split, scaling.
        5) Train all candidate models on SMOTE-balanced data.
        6) Evaluate all models and rank by ROC-AUC.
        7) Persist the best model, feature importance plot, and SHAP plot.
        8) Write the final Markdown report.
    """

    # ---------------------------------------------------------------------------
    # Stage 1 — Initialise
    # ---------------------------------------------------------------------------

    # Create all required output directories before any file writes occur
    ensure_project_directories()

    # Seed all RNGs so every run produces identical results
    set_seed(RANDOM_STATE)

    # ---------------------------------------------------------------------------
    # Stage 2 — Load raw data
    # ---------------------------------------------------------------------------

    print("Loading raw data...")
    df = load_data()

    # ---------------------------------------------------------------------------
    # Stage 3 — Exploratory data analysis
    # ---------------------------------------------------------------------------

    print("Running EDA...")
    # Generates class balance, amount, time, and correlation charts
    run_eda(df)

    # ---------------------------------------------------------------------------
    # Stage 4 — Preprocessing
    # ---------------------------------------------------------------------------

    print("Preprocessing data...")
    # Returns scaled train/test splits, the fitted scaler, and ordered feature names
    X_train, X_test, y_train, y_test, scaler, feature_names = preprocess_data(df)

    # ---------------------------------------------------------------------------
    # Stage 5 — Model training
    # ---------------------------------------------------------------------------

    print("Training models...")
    # Trains all candidate models on SMOTE-resampled data and saves them to disk
    models, X_res, y_res = train_models(X_train, y_train)

    # ---------------------------------------------------------------------------
    # Stage 6 — Model evaluation
    # ---------------------------------------------------------------------------

    print("Evaluating models...")
    # Returns a DataFrame sorted by ROC-AUC descending — best model is at row 0
    metrics_df = evaluate_models(models, X_test, y_test)

    if metrics_df.empty:
        raise RuntimeError("No models were evaluated successfully — check training logs.")

    # ---------------------------------------------------------------------------
    # Stage 7 — Persist best model and explainability artefacts
    # ---------------------------------------------------------------------------

    # The top row is the best model after sorting by ROC-AUC in evaluate_models()
    best_row  = metrics_df.iloc[0]
    best_name = best_row["model"]
    best_model = models[best_name]

    print(f"Best model is: {best_name}")

    # Save the best model separately so the Streamlit app can load it directly
    joblib.dump(best_model, BEST_MODEL_PATH)

    # Save a feature importance bar chart — skipped silently for models without it
    save_feature_importance_plot(best_model, feature_names, best_name)

    # Use a random subset of the test set for the SHAP plot to keep it fast
    sample = X_test.sample(min(500, len(X_test)), random_state=RANDOM_STATE)
    save_shap_summary_plot(best_model, sample, "shap_summary.png")

    # ---------------------------------------------------------------------------
    # Stage 8 — Write final report
    # ---------------------------------------------------------------------------

    # Persist a human-readable Markdown summary of the run to reports/report.md
    write_report(best_name, metrics_df)

    print("Pipeline complete.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_pipeline()