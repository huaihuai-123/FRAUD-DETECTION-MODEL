# config.py
# ---------
# Central configuration for the project.
# All paths and settings are defined here to avoid hardcoding them elsewhere.

from pathlib import Path


# ---------------------------------------------------------------------------
# Root directory
# ---------------------------------------------------------------------------

# Resolve the project root by stepping two levels up from this file
BASE_DIR = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Data directories
# ---------------------------------------------------------------------------

DATA_DIR           = BASE_DIR / "data"
RAW_DATA_DIR       = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR  = DATA_DIR / "external"

# Cache directory used by the Hugging Face hub
HF_CACHE_DIR = EXTERNAL_DATA_DIR / "huggingface_cache"


# ---------------------------------------------------------------------------
# Data files
# ---------------------------------------------------------------------------

# Raw transaction records — primary input to the pipeline
RAW_DATA_PATH = RAW_DATA_DIR / "transactions.csv"

# Serialised preprocessing artefacts consumed by inference scripts
SCALER_PATH         = PROCESSED_DATA_DIR / "scaler.pkl"
FEATURE_NAMES_PATH  = PROCESSED_DATA_DIR / "feature_names.json"

# Train / test splits saved during preprocessing
X_TRAIN_PATH = PROCESSED_DATA_DIR / "X_train.csv"
X_TEST_PATH  = PROCESSED_DATA_DIR / "X_test.csv"
Y_TRAIN_PATH = PROCESSED_DATA_DIR / "y_train.csv"
Y_TEST_PATH  = PROCESSED_DATA_DIR / "y_test.csv"


# ---------------------------------------------------------------------------
# Model directories and artefact paths
# ---------------------------------------------------------------------------

MODELS_DIR = BASE_DIR / "models"

# Serialised model artefacts produced during training
BEST_MODEL_PATH = MODELS_DIR / "fraud_model.pkl"
RF_MODEL_PATH   = MODELS_DIR / "random_forest.pkl"
XGB_MODEL_PATH  = MODELS_DIR / "xgboost_model.pkl"
LGBM_MODEL_PATH = MODELS_DIR / "lightgbm_model.pkl"


# ---------------------------------------------------------------------------
# Report directories and output paths
# ---------------------------------------------------------------------------

REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Final deliverables written after evaluation
REPORT_PATH  = REPORTS_DIR / "report.md"
METRICS_PATH = REPORTS_DIR / "metrics.csv"


# ---------------------------------------------------------------------------
# Miscellaneous directories
# ---------------------------------------------------------------------------

NOTEBOOKS_DIR = BASE_DIR / "notebooks"
APP_DIR       = BASE_DIR / "app"


# ---------------------------------------------------------------------------
# Modelling hyperparameters
# ---------------------------------------------------------------------------

# Ensures reproducible splits and model initialisation across all estimators
RANDOM_STATE = 42

# Fraction of data reserved for evaluation
TEST_SIZE = 0.2

# Minimum predicted probability required to classify a transaction as fraud
THRESHOLD = 0.5

# SMOTE sampling ratio: fraud class will be resampled to 20% of the majority
# class size. Increase to generate more synthetic minority samples.
SMOTE_RATIO = 0.2


# ---------------------------------------------------------------------------
# Hugging Face settings
# ---------------------------------------------------------------------------

# FLAN-T5 used to generate human-readable fraud explanations via text2text-generation
HF_MODEL_NAME = "google/flan-t5-base"


# ---------------------------------------------------------------------------
# Feature engineering thresholds
# ---------------------------------------------------------------------------

# Transactions above this value (USD) are flagged as high-value
LARGE_AMOUNT_THRESHOLD = 200.0


# ---------------------------------------------------------------------------
# Directory registry
# ---------------------------------------------------------------------------

# Passed to ensure_project_directories() in helpers.py to create all folders
ALL_DIRS = [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    HF_CACHE_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    NOTEBOOKS_DIR,
    APP_DIR,
]