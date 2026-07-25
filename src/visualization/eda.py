# eda.py
# ------
# Generates the first exploration charts for the raw dataset.
# EDA means Exploratory Data Analysis — we create simple charts
# so we can understand the data before building any models.

import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.config import FIGURES_DIR


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _ensure_figures_dir() -> None:
    # Create the figures output directory if it does not already exist
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# EDA pipeline
# ---------------------------------------------------------------------------

def run_eda(df) -> None:
    """Generate and save exploratory charts for the raw transaction dataset.

    EDA means Exploratory Data Analysis — we create simple charts so we can
    understand the data better before building any models. Each chart is saved
    as a high-resolution PNG to the reports/figures directory.

    Charts produced:
        1) Class balance      — fraud vs legitimate transaction counts.
        2) Amount distribution — histogram of raw transaction amounts.
        3) Time distribution   — histogram of transaction timestamps in seconds.
        4) Correlation heatmap — pairwise feature correlations across all columns.

    Args:
        df: Raw transaction DataFrame as returned by load_data().
    """
    _ensure_figures_dir()

    # ---------------------------------------------------------------------------
    # Chart 1 — Class balance
    # ---------------------------------------------------------------------------

    # Shows how many fraud vs legitimate transactions exist in the dataset
    # A large imbalance here is why we use SMOTE and specialised metrics
    plt.figure(figsize=(6, 4))
    sns.countplot(x="Class", data=df)
    plt.title("Fraud vs Non-Fraud Count")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "class_balance.png", dpi=200)
    plt.close()

    # ---------------------------------------------------------------------------
    # Chart 2 — Amount distribution
    # ---------------------------------------------------------------------------

    # Reveals skew in transaction values — most are small, a few are very large
    # KDE overlay helps visualise the underlying distribution shape
    plt.figure(figsize=(8, 4))
    sns.histplot(df["Amount"], bins=50, kde=True)
    plt.title("Transaction Amount Distribution")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "amount_distribution.png", dpi=200)
    plt.close()

    # ---------------------------------------------------------------------------
    # Chart 3 — Time distribution
    # ---------------------------------------------------------------------------

    # Shows when transactions occur — useful for spotting overnight activity spikes
    # KDE is disabled here as time is measured in raw seconds, not a smooth variable
    plt.figure(figsize=(8, 4))
    sns.histplot(df["Time"], bins=50, kde=False)
    plt.title("Transaction Time Distribution")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "time_distribution.png", dpi=200)
    plt.close()

    # ---------------------------------------------------------------------------
    # Chart 4 — Correlation heatmap
    # ---------------------------------------------------------------------------

    # Highlights which features move together — helps spot redundant columns
    # center=0 ensures the diverging colormap is anchored at zero correlation
    plt.figure(figsize=(14, 10))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "correlation_heatmap.png", dpi=200)
    plt.close()

    print("EDA charts saved to reports/figures/")