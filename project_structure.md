fraud-detection-ai/
│
├── data/
│   ├── raw/
│   │   └── transactions.csv
│   │
│   ├── processed/
│   │   ├── X_train.csv
│   │   ├── X_test.csv
│   │   ├── y_train.csv
│   │   ├── y_test.csv
│   │   ├── scaler.pkl
│   │   └── feature_names.json
│   │
│   └── external/
│       └── huggingface_cache/
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   ├── data/
│   │   ├── load_data.py
│   │   ├── preprocess.py
│   │   └── feature_engineering.py
│   │
│   ├── models/
│   │   ├── train_model.py
│   │   ├── evaluate_model.py
│   │   ├── predict.py
│   │   └── huggingface_model.py
│   │
│   ├── visualization/
│   │   ├── eda.py
│   │   └── plots.py
│   │
│   ├── explainability/
│   │   └── shap_explainer.py
│   │
│   └── utils/
│       ├── config.py
│       └── helpers.py
│
├── app/
│   └── streamlit_app.py
│
├── models/
│   ├── random_forest.pkl
│   ├── xgboost_model.pkl
│   └── lightgbm_model.pkl
│
├── reports/
│   ├── figures/
│   └── report.md
│
├── requirements.txt
├── README.md
└── main.py