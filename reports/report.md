# Fraud Detection AI Report

## Best Model
**xgboost**

## Model Comparison
| model               |   accuracy |   precision |   recall |       f1 |   roc_auc |   pr_auc |
|:--------------------|-----------:|------------:|---------:|---------:|----------:|---------:|
| xgboost             |   0.998578 |   0.554839  | 0.877551 | 0.679842 |  0.982734 | 0.861248 |
| lightgbm            |   0.999245 |   0.743363  | 0.857143 | 0.796209 |  0.982711 | 0.876608 |
| random_forest       |   0.999491 |   0.879121  | 0.816327 | 0.846561 |  0.978353 | 0.87406  |
| logistic_regression |   0.972631 |   0.0548446 | 0.918367 | 0.103508 |  0.973586 | 0.729002 |

## Notes
- The model was trained on processed and scaled transaction data.
- SMOTE was used to balance the fraud class.
- SHAP was used to explain predictions.
- Hugging Face was used to turn technical reasons into human-friendly language.
