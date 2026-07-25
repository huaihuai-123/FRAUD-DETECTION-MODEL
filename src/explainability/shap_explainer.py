# shap_explainer.py
# -----------------
# Explains why the model made a decision using SHAP values.
# Supports both tree-based models (TreeExplainer) and non-tree models
# (KernelExplainer fallback).  Handles SHAP API shape changes across versions.

import matplotlib.pyplot as plt
import pandas as pd
import shap

from src.utils.config import FIGURES_DIR


# ---------------------------------------------------------------------------
# SHAP explainer factory (handles tree and non-tree models)
# ---------------------------------------------------------------------------

def _build_explainer(model, sample_df: pd.DataFrame):
    """Return a SHAP explainer appropriate for the model type.

    Uses TreeExplainer for tree-based models (fast, exact) and falls back
    to KernelExplainer for linear / other models (slower but universal).
    """
    try:
        return shap.TreeExplainer(model)
    except (TypeError, AttributeError, ValueError):
        # Model is not tree-based — fall back to KernelExplainer with a
        # small background to keep computation tractable
        background = shap.kmeans(sample_df, min(10, len(sample_df)))
        return shap.KernelExplainer(model.predict_proba, background)


# ---------------------------------------------------------------------------
# SHAP values normalisation (handles SHAP >= 0.42 shape changes)
# ---------------------------------------------------------------------------

def _extract_fraud_shap(explainer, sample_df, shap_values):
    """Normalise SHAP output into a 2-D (n_samples, n_features) array for the fraud class.

    SHAP < 0.42 returned a list of 2D arrays (one per class).
    SHAP >= 0.42 returns a single 3D array (n_samples, n_features, n_classes).
    This helper abstracts both formats away.
    """
    if isinstance(shap_values, list):
        # Old API: list of (n_samples, n_features) arrays
        if len(shap_values) > 1:
            return shap_values[1]   # fraud class (index 1 for binary)
        return shap_values[0]       # single-output model
    # New API: single (n_samples, n_features, n_classes) array
    if shap_values.ndim == 3 and shap_values.shape[2] > 1:
        return shap_values[:, :, 1]
    # Single-output model with new API — (n_samples, n_features)
    return shap_values


# ---------------------------------------------------------------------------
# SHAP text summary
# ---------------------------------------------------------------------------

def get_shap_summary(model, sample_df: pd.DataFrame, top_n: int = 5):
    """Return a short text summary of the most important SHAP features.

    Example output:
        "Hour (+0.900) pushes toward fraud, Amount_Log (+0.700) pushes toward fraud,
         Is_Night (-0.500) pushes toward safe"

    Args:
        model:     A fitted estimator with a predict_proba method.
        sample_df: A single-row or small DataFrame of scaled input features.
        top_n:     Number of top features to include. Defaults to 5.

    Returns:
        A tuple of (summary_str, shap_values, explainer), or
        (fallback_str, None, None) on failure.
    """
    try:
        explainer = _build_explainer(model, sample_df)
        shap_values = explainer.shap_values(sample_df)

        # Normalise into 2-D for the fraud class
        fraud_shap = _extract_fraud_shap(explainer, sample_df, shap_values)
        # Take the first row (single-sample case)
        values = fraud_shap[0]

        # Pair feature names with contributions, sort by absolute impact
        pairs = sorted(
            zip(sample_df.columns, values),
            key=lambda x: abs(x[1]),
            reverse=True,
        )[:top_n]

        parts = []
        for feature, value in pairs:
            direction = "pushes toward fraud" if value > 0 else "pushes toward safe"
            parts.append(f"{feature} ({value:+.3f}) {direction}")

        return ", ".join(parts), shap_values, explainer

    except Exception as e:
        print(f"SHAP failed: {e}")
        return "No SHAP explanation available.", None, None


# ---------------------------------------------------------------------------
# SHAP summary plot
# ---------------------------------------------------------------------------

def save_shap_summary_plot(model, sample_df: pd.DataFrame, output_name: str = "shap_summary.png"):
    """Save a SHAP beeswarm summary plot to the reports/figures directory.

    Args:
        model:       A fitted estimator with a predict_proba method.
        sample_df:   DataFrame of scaled input features to explain.
        output_name: Filename for the saved plot.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    try:
        explainer = _build_explainer(model, sample_df)
        shap_values = explainer.shap_values(sample_df)

        plt.figure()

        # Normalise for the summary_plot call
        if isinstance(shap_values, list):
            if len(shap_values) > 1:
                shap.summary_plot(shap_values[1], sample_df, show=False)
            else:
                shap.summary_plot(shap_values[0], sample_df, show=False)
        else:
            shap.summary_plot(shap_values, sample_df, show=False)

        plt.tight_layout()
        plt.savefig(FIGURES_DIR / output_name, dpi=200, bbox_inches="tight")
        plt.close()

    except Exception as e:
        print(f"Could not save SHAP plot: {e}")
        # Close any leaked figure to avoid memory accumulation
        plt.close("all")
