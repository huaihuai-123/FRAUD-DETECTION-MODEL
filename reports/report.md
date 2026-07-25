# Fraud Detection AI Report

## Best Model
**lightgbm**

## Model Comparison
| model               |   accuracy |   precision |   recall |       f1 |   roc_auc |   pr_auc |
|:--------------------|-----------:|------------:|---------:|---------:|----------:|---------:|
| lightgbm            |   0.999245 |   0.743363  | 0.857143 | 0.796209 |  0.982711 | 0.876608 |
| xgboost             |   0.998666 |   0.574324  | 0.867347 | 0.691057 |  0.982216 | 0.855199 |
| random_forest       |   0.999491 |   0.879121  | 0.816327 | 0.846561 |  0.978362 | 0.873794 |
| logistic_regression |   0.972631 |   0.0548446 | 0.918367 | 0.103508 |  0.973586 | 0.729002 |

## Notes
- The model was trained on processed and scaled transaction data.
- SMOTE was used to balance the fraud class.
- SHAP was used to explain predictions.
- Hugging Face was used to turn technical reasons into human-friendly language.
