# plots.py
# --------
# Saves all diagnostic plots to the reports/figures directory.
# Plots help us see patterns instead of reading raw numbers.

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import PrecisionRecallDisplay, RocCurveDisplay

from src.utils.config import FIGURES_DIR


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _ensure_figures_dir() -> None:
    # Create the figures output directory if it does not already exist
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Confusion matrix
# ---------------------------------------------------------------------------

def save_confusion_matrix_plot(cm, model_name: str) -> None:
    """Save a confusion matrix as a colour-coded heatmap.

    Plots help us see patterns instead of reading raw numbers.
    The heatmap shows true positives, false positives, true negatives,
    and false negatives at a glance.

    Args:
        cm:         Confusion matrix array as returned by sklearn.metrics.confusion_matrix.
        model_name: Model identifier used in the plot title and output filename.
    """
    _ensure_figures_dir()

    plt.figure(figsize=(5, 4))

    # Annotate each cell with its raw count and use a blue gradient for intensity
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()

    # Save at 200 DPI for crisp report-quality output
    plt.savefig(FIGURES_DIR / f"{model_name}_confusion_matrix.png", dpi=200)

    # Close the figure to free memory — important in long-running pipelines
    plt.close()


# ---------------------------------------------------------------------------
# ROC curve
# ---------------------------------------------------------------------------

def save_roc_curve(y_true, y_score, model_name: str) -> None:
    """Save a ROC curve plot for a trained model.

    The ROC curve shows the trade-off between true positive rate and false
    positive rate across all possible classification thresholds.

    Args:
        y_true:     True binary labels (0 = legitimate, 1 = fraud).
        y_score:    Predicted fraud probabilities from the model.
        model_name: Model identifier used in the plot title and output filename.
    """
    _ensure_figures_dir()

    plt.figure(figsize=(6, 5))

    # from_predictions handles the threshold sweep and AUC calculation internally
    RocCurveDisplay.from_predictions(y_true, y_score)

    plt.title(f"ROC Curve - {model_name}")
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / f"{model_name}_roc_curve.png", dpi=200)
    plt.close()


# ---------------------------------------------------------------------------
# Precision-Recall curve
# ---------------------------------------------------------------------------

def save_pr_curve(y_true, y_score, model_name: str) -> None:
    """Save a Precision-Recall curve plot for a trained model.

    More informative than ROC for imbalanced datasets like fraud detection —
    it focuses on the minority (fraud) class performance directly.

    Args:
        y_true:     True binary labels (0 = legitimate, 1 = fraud).
        y_score:    Predicted fraud probabilities from the model.
        model_name: Model identifier used in the plot title and output filename.
    """
    _ensure_figures_dir()

    plt.figure(figsize=(6, 5))

    # from_predictions sweeps thresholds and computes precision/recall at each point
    PrecisionRecallDisplay.from_predictions(y_true, y_score)

    plt.title(f"Precision-Recall Curve - {model_name}")
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / f"{model_name}_pr_curve.png", dpi=200)
    plt.close()


# ---------------------------------------------------------------------------
# Feature importance
# ---------------------------------------------------------------------------

def save_feature_importance_plot(model, feature_names, model_name: str) -> None:
    """Save a horizontal bar chart of the top 15 most important features.

    Only applicable to tree-based models that expose a feature_importances_
    attribute (e.g. RandomForest, XGBoost, LightGBM). Silently skips models
    that do not support feature importance.

    Args:
        model:         A fitted estimator — skipped if feature_importances_ is absent.
        feature_names: Ordered list of feature column names matching the model input.
        model_name:    Model identifier used in the plot title and output filename.
    """
    # Skip silently for models that do not expose feature importances (e.g. LogReg)
    if not hasattr(model, "feature_importances_"):
        return

    _ensure_figures_dir()

    importance = model.feature_importances_

    # Select the top 15 features sorted by descending importance
    indices = np.argsort(importance)[::-1][:15]

    plt.figure(figsize=(8, 6))

    # Reverse order so the most important feature appears at the top of the chart
    plt.barh(
        [feature_names[i] for i in indices][::-1],
        importance[indices][::-1],
    )

    plt.title(f"Top Feature Importance - {model_name}")
    plt.xlabel("Importance")
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / f"{model_name}_feature_importance.png", dpi=200)
    plt.close()